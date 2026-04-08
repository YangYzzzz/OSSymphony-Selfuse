import base64
import json
import logging
import time
from io import BytesIO
from typing import Dict, List, Tuple, Any, Optional

import backoff
import openai
from openai import OpenAI
from PIL import Image
from requests.exceptions import SSLError

from mm_agents.utils.qwen_vl_utils import (
    smart_resize,
    QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
    QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN,
)
from mm_agents.uitars15_v2 import IMAGE_FACTOR
from mm_agents.base import ComputerUseBaseAgent


logger = logging.getLogger("desktopenv.agent")

MAX_RETRY_TIMES = 5


def encode_image(image_content):
    return base64.b64encode(image_content).decode("utf-8")


def process_image(image_bytes):
    """Process an image for Qwen VL models."""
    image = Image.open(BytesIO(image_bytes))
    width, height = image.size

    resized_height, resized_width = smart_resize(
        height=height,
        width=width,
        factor=32,
        max_pixels=16 * 16 * 4 * 1280,
    )

    image = image.resize((resized_width, resized_height))

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    processed_bytes = buffer.getvalue()

    return base64.b64encode(processed_bytes).decode("utf-8")


class OSSymphony2AgentWithToolCall(ComputerUseBaseAgent):

    def __init__(
        self,
        platform: str = "ubuntu",
        model: str = "qwen3-vl",
        base_url: str = "",
        api_key: str = "",
        max_tokens: int = 1500,
        top_p: float = 0.9,
        temperature: float = 0.0,
        action_space: str = "pyautogui",
        observation_type: str = "screenshot",
        history_n: int = 8,
        add_thought_prefix: bool = False,
        coordinate_type: str = "relative",
        keep_first_image: bool = True,
    ):
        self.platform = platform
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature
        self.action_space = action_space
        self.observation_type = observation_type
        self.history_n = history_n
        self.keep_first_image = keep_first_image
        self.add_thought_prefix = add_thought_prefix
        self.coordinate_type = coordinate_type

        assert action_space in ["pyautogui"], "Invalid action space"
        assert observation_type in ["screenshot"], "Invalid observation type"


        # 为了执行 code 设置的变量
        self.last_code_result: Optional[str] = None
        self.code_results_history: List[str] = []

        # 统一维护对话历史（system + user + assistant + tool）
        # 直接沿用 OpenAI/vLLM 的 messages 协议结构
        self.messages: List[Dict[str, Any]] = []

        # 记录上一轮产生的 tool_calls，供下一轮填充 tool 结果
        self.pending_tool_calls: List[Any] = []

    def _build_system_prompt(self, processed_width: int, processed_height: int) -> str:
        """在训练版 system prompt 的基础上做推理增强。"""
        screen_desc = (
            f"The current screenshot resolution after preprocessing is {processed_width}x{processed_height} pixels."
            if self.coordinate_type == "absolute"
            else "The current screenshot is mapped onto a 1000x1000 relative coordinate grid (0-999 on both axes)."
        )

        extra_rules = """
# Additional Inference-time Rules
- Always prefer `code` action for:
  - structured data processing (CSV/Excel/JSON/logs)
  - batch file operations (rename/copy/move/delete many files)
  - text search/replace across files or within large documents
- Use GUI actions for:
  - launching and switching applications
  - navigation in browsers / GUIs when no CLI/API is available
  - precise clicking/dragging based on visual layout
- Before clicking, explicitly locate the target region in the screenshot and then choose coordinates.
- After executing `code`, reason about the textual result first; only ask for another screenshot when visual confirmation is strictly required.

# Output Contract
You MUST call the `custom_computer_use` tool for every step instead of describing actions in free text.
- Each step must contain exactly one tool call.
- Do NOT mix multiple high-level actions into one tool invocation; keep them atomic and sequential.
"""
        return QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN + "\n" + screen_desc + "\n" + extra_rules

    def predict(self, instruction: str, obs: Dict) -> Tuple[List[Dict], List[str]]:
        """Predict the next action(s) based on the current observation.

        Returns:
            response_list (List[Dict]): Structured metadata for logging.
            action_list (List[str]): Executable PyAutoGUI code.
        """
        screenshot_bytes = obs["screenshot"]

        image = Image.open(BytesIO(screenshot_bytes))
        width, height = image.size

        processed_image = process_image(screenshot_bytes)
        processed_img = Image.open(BytesIO(base64.b64decode(processed_image)))
        processed_width, processed_height = processed_img.size

        system_prompt = self._build_system_prompt(processed_width, processed_height)

        # 第一次调用 predict 时，初始化 system
        if not self.messages:
            self.messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": system_prompt},
                    ],
                }
            ]

        # feed tool result for previous tool_calls
        if self.pending_tool_calls:
            for tool_call in self.pending_tool_calls:
                name = tool_call["function"]["name"]
                if name == "code" and self.last_code_result is not None:
                    result_text = f"Code Execution Result:\n```\n{self.last_code_result}\n```"
                    self.last_code_result = None
                else:
                    result_text = "Success"
                self.messages.append(
                    {
                        "role": "tool",
                        # "tool_call_id": tool_call.get("id", "tool_call_0"), 应该不是很重要
                        "content": result_text,
                    }
                )
            # 已经把上一轮的 tool 结果补完，本轮重新收集
            self.pending_tool_calls = []

        # 当前轮 user 消息
        curr_user_content = []

        # 第一轮附带原始 instruction
        if not self.messages:
            instruction_prompt = (
                "Please generate the next move according to the UI screenshot, instruction and previous actions.\n\n"
                f"Instruction: {instruction}"
            )
            curr_user_content.append({"type": "text", "text": instruction_prompt})

        curr_user_content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{processed_image}"},
            }
        )

        self.messages.append(
            {
                "role": "user",
                "content": curr_user_content,
            }
        )
        self._cleanup_old_screenshots()

        # 让 call_llm 返回原始 message 对象（包含 message.tool_calls 和结构化 content）
        response_message = self.call_llm(
            {
                "model": self.model,
                "messages": self.messages,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "temperature": self.temperature,
            },
            self.model,
        )

        logger.info(f"Qwen3VL Output: {response_message}")

        # 将本轮 assistant message（含 tool_calls）写回历史
        self.messages.append(response_message)

        # 记录本轮产生的 tool_calls，供下一轮填充 tool 结果
        tool_calls = getattr(response_message, "tool_calls", None) or response_message.get("tool_calls") or []
        self.pending_tool_calls = list(tool_calls)

        # 把工具调用转成我们现有的 meta_data / pyautogui_code
        # 这里仍沿用老的 parse_response 逻辑，只是从 message.content 中提取字符串
        content = getattr(response_message, "content", None)
        if isinstance(content, list):
            # 兼容 messages 协议：content 是多个块
            text_parts = [
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            ]
            response_str = "\n".join(text_parts)
        else:
            response_str = str(content or "")

        meta_data, pyautogui_code = self.parse_response(
            response_str,
            width,
            height,
            processed_width,
            processed_height,
        )

        logger.info(f"Pyautogui code: {pyautogui_code}")
        return meta_data, pyautogui_code

    def _cleanup_old_screenshots(self):
        """在 self.messages 上清理超出配额的截图。"""
        user_indices_with_img = []
        for idx, msg in enumerate(self.messages):
            if msg.get("role") != "user":
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            has_image = any(
                isinstance(part, dict) and part.get("type") == "image_url"
                for part in content
            )
            if has_image:
                user_indices_with_img.append(idx)

        if not user_indices_with_img:
            return

        keep_indices = set()

        # 保留第一条带图 user（如需要）
        if self.keep_first_image:
            first_user_idx = None
            for idx, msg in enumerate(self.messages):
                if msg.get("role") == "user":
                    first_user_idx = idx
                    break
            if first_user_idx is not None:
                content = self.messages[first_user_idx].get("content")
                if isinstance(content, list):
                    has_image = any(
                        isinstance(part, dict) and part.get("type") == "image_url"
                        for part in content
                    )
                    if has_image:
                        keep_indices.add(first_user_idx)

        # 从后往前保留最近 history_n 条带图 user
        remaining = self.history_n
        for idx in reversed(user_indices_with_img):
            if idx in keep_indices:
                continue
            if remaining <= 0:
                break
            keep_indices.add(idx)
            remaining -= 1

        # 清理不在 keep_indices 里的截图
        for idx in user_indices_with_img:
            if idx in keep_indices:
                continue
            msg = self.messages[idx]
            content = msg.get("content", [])
            new_content = [
                part
                for part in content
                if not (isinstance(part, dict) and part.get("type") == "image_url")
            ]
            if not new_content:
                # 不会有这种情况出现
                msg["content"] = [
                    {
                        "type": "text",
                        "text": "[Old Screenshot Removed]",
                    }
                ]
            else:
                msg["content"] = new_content

    def _parse_tool_calls_from_response(self, response: str) -> List[Dict[str, Any]]:
        """从模型输出中抽取 tool_call JSON，并解析为 dict 列表。

        兼容两种格式：
        - 明确包裹在 <tool_call>...</tool_call> 标签中
        - 直接输出的 JSON 行（降级兜底，可按需扩展）
        """
        import re

        if not response or not response.strip():
            return []

        tool_calls: List[Dict[str, Any]] = []

        # 1. 优先解析 <tool_call> 块
        for m in re.finditer(r"<tool_call>([\s\S]*?)</tool_call>", response):
            block = m.group(1).strip()
            if not block:
                continue
            try:
                tool_calls.append(json.loads(block))
            except json.JSONDecodeError:
                logger.error("Failed to decode tool_call block as JSON: %s", block)

        # 2. 如果没解析到任何 tool_call，尝试整段作为单个 JSON（兼容直接返回 JSON 的情况）
        if not tool_calls:
            try:
                obj = json.loads(response)
                if isinstance(obj, dict) and "arguments" in obj:
                    tool_calls.append(obj)
            except json.JSONDecodeError:
                pass

        return tool_calls

    def parse_response(
        self,
        response: str,
        original_width: int = None,
        original_height: int = None,
        processed_width: int = None,
        processed_height: int = None,
    ) -> Tuple[List[Dict], List[str]]:
        """Parse LLM response and convert it to metadata and pyautogui code via tool_schema."""
        import re

        pyautogui_code: List[str] = []
        meta_data: List[Dict] = []

        if response is None or not response.strip():
            return meta_data, pyautogui_code

        # ---- extract thought (before </think>) ----
        thought = ""
        think_match = re.search(r"<think>([\s\S]*?)</think>", response)
        if think_match:
            thought = think_match.group(1).strip()
        think_match_2 = re.search(r"([\s\S]*?)</think>", response)
        if not thought and think_match_2:
            thought = think_match_2.group(1).strip()

        # ---- extract Action: line（可选，保留兼容性） ----
        action_text = ""
        action_match = re.search(r"^\s*Action:\s*(.+)$", response, flags=re.MULTILINE | re.IGNORECASE)
        if action_match:
            action_text = action_match.group(1).strip()

        def adjust_coordinates(x: float, y: float) -> Tuple[int, int]:
            if not (original_width and original_height):
                return int(x), int(y)
            if self.coordinate_type == "absolute":
                if processed_width and processed_height:
                    x_scale = original_width / processed_width
                    y_scale = original_height / processed_height
                    return int(x * x_scale), int(y * y_scale)
                return int(x), int(y)
            x_scale = original_width / 999
            y_scale = original_height / 999
            return int(x * x_scale), int(y * y_scale)

        def make_meta(code: str, coordinate: Optional[List[int]] = None) -> Dict:
            return {
                "raw_response": response,
                "thought": thought,
                "action": action_text,
                "code": code,
                "coordinate": coordinate or [],
            }

        tool_calls = self._parse_tool_calls_from_response(response)

        for tool_call in tool_calls:
            try:
                args = tool_call["arguments"]
                action = args["action"]
            except (KeyError, TypeError) as e:
                logger.error("Invalid tool_call structure: %s", e)
                continue

            # 映射到具体 PyAutoGUI / 控制命令
            if action == "left_click":
                coord: List[int] = []
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    code_str = f"pyautogui.click({adj_x}, {adj_y})"
                else:
                    code_str = "pyautogui.click()"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str, coord))

            elif action == "right_click":
                coord = []
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    code_str = f"pyautogui.rightClick({adj_x}, {adj_y})"
                else:
                    code_str = "pyautogui.rightClick()"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str, coord))

            elif action == "middle_click":
                coord = []
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    code_str = f"pyautogui.middleClick({adj_x}, {adj_y})"
                else:
                    code_str = "pyautogui.middleClick()"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str, coord))

            elif action == "double_click":
                coord = []
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    code_str = f"pyautogui.doubleClick({adj_x}, {adj_y})"
                else:
                    code_str = "pyautogui.doubleClick()"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str, coord))

            elif action == "type":
                text = args.get("text", "")
                lines = text.split("\n")
                for idx, line in enumerate(lines):
                    if line:
                        code_str = f"pyautogui.typewrite({repr(line)}, interval=0.03)"
                        pyautogui_code.append(code_str)
                        meta_data.append(make_meta(code_str))
                    if idx < len(lines) - 1:
                        code_str = "pyautogui.press('enter')"
                        pyautogui_code.append(code_str)
                        meta_data.append(make_meta(code_str))

            elif action == "key":
                keys = args.get("keys", [])
                if isinstance(keys, list):
                    cleaned_keys = []
                    for key in keys:
                        if isinstance(key, str):
                            # 简单清洗
                            key = key.strip()
                        cleaned_keys.append(key)
                    keys = cleaned_keys

                keys_str = ", ".join([f"'{key}'" for key in keys])
                if len(keys) > 1:
                    code_str = f"pyautogui.hotkey({keys_str})"
                else:
                    code_str = f"pyautogui.press({keys_str})"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str))

            elif action == "scroll":
                pixels = args.get("pixels", 0)
                code_str = f"pyautogui.scroll({pixels})"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str))

            elif action == "wait":
                code_str = "WAIT"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str))

            elif action == "terminate":
                code_str = "DONE"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str))

            elif action == "mouse_move":
                coord = []
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    code_str = f"pyautogui.moveTo({adj_x}, {adj_y})"
                else:
                    code_str = "pyautogui.moveTo(0, 0)"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str, coord))

            elif action == "left_click_drag":
                coord = []
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    duration = args.get("duration", 0.5)
                    code_str = f"pyautogui.dragTo({adj_x}, {adj_y}, duration={duration})"
                else:
                    code_str = "pyautogui.dragTo(0, 0)"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str, coord))

            elif action == "code":
                code_content = args.get("execute_code") or args.get("code", "")
                language = args.get("language", "python")
                code_str = f"EXEC_CODE|{language}|{code_content}"
                pyautogui_code.append(code_str)
                meta_data.append(make_meta(code_str))

        return meta_data, pyautogui_code

    def evaluate(self, task_instruction: str, obs: Dict) -> Dict[str, Any]:
        """Self-judge function.

        Returns a dictionary with 'thought' and 'score'.
        """
        pass

    @backoff.on_exception(
        backoff.constant,
        (
            SSLError,
            openai.RateLimitError,
            openai.BadRequestError,
            openai.InternalServerError,
        ),
        interval=30,
        max_tries=5,
    )
    def call_llm(self, payload, model):
        messages = payload["messages"]
        custom_headers = {
            "Authorization": "Basic NWFkMzQxMDBlZTA1NWE0YmFlNjYzNzBhNWU2ODNiYWM6NjA3ZGU4MjQ5NjU3YTNiM2JkMDM2ZGM5NmQ0YzBiMmY="
        }

        if "kubebrain" in self.base_url:
            logger.info(f"H Cluster Local VLLM: {self.base_url}")
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                default_headers=custom_headers,
            )
        else:
            logger.info(f"H Service VLLM / Boyue: {self.base_url}")
            client = OpenAI(base_url=self.base_url, api_key=self.api_key)

        for _ in range(MAX_RETRY_TIMES):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    tools=[json.loads(QWEN3VL_COMPUTER_USE_TOOL_SCHEMA)],
                    tool_choice={"type": "function", "function": {"name": "custom_computer_use"}},
                )
                # 这里直接返回原始内容和 tool_calls（如果上层需要的话可以扩展返回结构）
                message = response.choices[0].message
                # 将完整 message.content 作为文本（便于调试），同时包含 tool_calls
                content_str = message.content if isinstance(message.content, str) else str(message.content)
                if message.tool_calls:
                    tool_calls_repr = json.dumps(
                        [tc.model_dump() for tc in message.tool_calls],
                        ensure_ascii=False,
                    )
                    return content_str + "\n<TOOL_CALLS>" + tool_calls_repr
                return content_str
            except Exception as e:
                logger.error(f"Error calling Qwen model: {e}")
                time.sleep(5)
                continue
        return ""

    def reset(self, _logger=None):
        global logger
        logger = _logger if _logger is not None else logging.getLogger("desktopenv.qwen3vl_agent")
        self.last_code_result = None
        self.messages = []
        self.pending_tool_calls = []

    def debug_print_messages(self, messages: list):
        """优雅地打印 messages 列表，自动截断 Base64 图片以方便检查装填逻辑。"""
        print("\n" + "=" * 50 + " MESSAGES LOGIC DEBUG " + "=" * 50)

        if not messages:
            print(" [!] Messages list is empty.")
            print("=" * 122 + "\n")
            return

        for i, msg in enumerate(messages):
            role = msg.get("role", "UNKNOWN").upper()
            prefix = "👤" if role == "USER" else "🤖" if role == "ASSISTANT" else "⚙️"

            print(f"\n{prefix} [{i}] ROLE: {role}")
            print("-" * 80)

            content = msg.get("content", [])

            if isinstance(content, str):
                print(f"  (Text) : {content}")
                continue

            for j, item in enumerate(content):
                item_type = item.get("type", "unknown")

                if item_type == "text":
                    text_content = item.get("text", "")
                    if "Code Execution Result:" in text_content:
                        print(f"  📝 (Text-CodeResult) : {text_content}")
                    else:
                        if len(text_content) > 2000:
                            text_content = text_content[:2000] + " ... [TEXT TRUNCATED]"
                        print(f"  💬 (Text)  : {text_content}")

                elif item_type == "image_url":
                    print(f"  🖼️ (Image) : <BASE64_IMAGE_DATA_TRUNCATED>")

                else:
                    print(f"  ❓ ({item_type}) : {item}")

        print("\n" + "=" * 122 + "\n")
