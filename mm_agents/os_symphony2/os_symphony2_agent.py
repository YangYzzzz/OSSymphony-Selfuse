from ast import Pass
import base64
import json
import logging
import time
import copy
from io import BytesIO
from typing import Dict, List, Tuple, Any, Optional

import backoff
import openai
from openai import OpenAI
from PIL import Image
from requests.exceptions import SSLError
from mm_agents.utils.qwen_vl_utils import smart_resize
from mm_agents.uitars15_v2 import IMAGE_FACTOR
from mm_agents.base import ComputerUseBaseAgent


logger = logging.getLogger("desktopenv.agent")

MAX_RETRY_TIMES = 5

def encode_image(image_content):
    return base64.b64encode(image_content).decode("utf-8")

def process_image(image_bytes):
    """
    Process an image for Qwen VL models.
    """
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


class OSSymphony2Agent(ComputerUseBaseAgent):

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
        keep_first_image: bool = True
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

        self.responses = []

        # 为了执行code设置的变量
        self.last_code_result = None
        self.code_results_history = []

        # 统一维护对话历史（system + user + assistant）
        self.messages = []

    def predict(self, instruction: str, obs: Dict) -> Tuple[List[Dict], List[str]]:
        """
        Predict the next action(s) based on the current observation.
        Returns:
            response_list (List[Dict]): Structured metadata for logging.
            action_list (List[str]): Executable PyAutoGUI code.
        """
        screenshot_bytes = obs["screenshot"]

        image = Image.open(BytesIO(screenshot_bytes))
        width, height = image.size

        processed_image = process_image(screenshot_bytes)
        processed_img = Image.open(
            BytesIO(base64.b64decode(processed_image))
        )
        processed_width, processed_height = processed_img.size

        # ================== Old Prompts ==================
        old_description_prompt_lines = [
            "Use a mouse and keyboard to interact with a computer, and take screenshots.",
            "* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.",
            "* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.",
            (
                f"* The screen's resolution is {processed_width}x{processed_height}."
                if self.coordinate_type == "absolute"
                else "* The screen's resolution is 1000x1000."
            ),
            "* Whenever you intend to move the cursor to click on an element like an icon, you should consult a screenshot to determine the coordinates of the element before moving the cursor.",
            "* If you tried clicking on a program or link but it failed to load even after waiting, try adjusting your cursor position so that the tip of the cursor visually falls on the element that you want to click.",
            "* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.",
        ]
        # ================== Prompts ==================
        description_prompt_lines = [
            "You are a hybrid OS agent that can both operate the GUI (mouse and keyboard) and directly execute system-level code.",
            "* Prefer using `execute_code` (Python or Bash) to handle structured data, batch operations, and any repetitive or file-based tasks.",
            "* Use GUI actions mainly for navigation and visual interactions: opening applications, navigating menus, or interacting with purely visual UI elements.",
            (
                f"* The screen's resolution is {processed_width}x{processed_height}."
                if self.coordinate_type == "absolute"
                else "* The screen's resolution is represented on a 1000x1000 relative coordinate grid."
            ),
            "* Whenever you intend to move the cursor to click on an element like an icon or button, consult the latest screenshot (or code execution result if present) to determine the target coordinates before moving the cursor.",
            "* After running `execute_code`, you may rely on the provided code execution result text to plan the next step, and only request a new screenshot when necessary for visual verification.",
        ]
        description_prompt = "\n".join(description_prompt_lines)

        action_description_prompt = """
* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.
* `type`: Type a string of text on the keyboard.
* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.
* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.
* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.
* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.
* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.
* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.
* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).
* `scroll`: Performs a scroll of the mouse scroll wheel.
* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).
* `wait`: Wait specified seconds for the change to happen.
* `terminate`: Terminate the current task and report its completion status.
* `code`: Execute raw Python or Bash scripts to perform tasks directly in the operating system. Use this for batch processing, file manipulation, or tasks where GUI clicking is inefficient or repetitive.
"""

        tools_def = {
            "type": "function",
            "function": {
                "name_for_human": "custom_computer_use",
                "name": "custom_computer_use",
                "description": description_prompt,
                "parameters": {
                    "properties": {
                        "action": {
                            "description": action_description_prompt,
                            "enum": [
                                "key", "type", "mouse_move", "left_click", "left_click_drag",
                                "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll",
                                "wait", "terminate", "code"
                            ],
                            "type": "string"
                        },
                        "keys": {"description": "Required only by `action=key`.", "type": "array"},
                        "text": {"description": "Required only by `action=type`.", "type": "string"},
                        "coordinate": {"description": "The x,y coordinates for mouse actions.", "type": "array"},
                        "pixels": {"description": "The amount of scrolling.", "type": "number"},
                        "time": {"description": "The seconds to wait.", "type": "number"},
                        "status": {
                            "description": "The status of the task.", 
                            "type": "string", 
                            "enum": ["success", "failure"]
                        },
                        "execute_code": {
                            "description": "The raw code string to execute. Required only when `action=code`.",
                            "type": "string"
                        },
                        "language": {
                            "description": "The programming language of the code. Required only when `action=code`.",
                            "type": "string",
                            "enum": ["python", "bash"]
                        }
                    },
                    "required": ["action"],
                    "type": "object"
                },
                "args_format": "Format the arguments as a JSON object."
            }
        }

        # 有优化空间
        system_prompt = """# Role & Goal
You are a powerful OS Agent capable of both GUI interaction and direct System-Level programming.
Your goal is to complete tasks with MAXIMUM efficiency and MINIMUM steps.

# Tools
You may call the following functions:
<tools>
""" + json.dumps(tools_def) + """
</tools>

For each function call, return a JSON object within <tool_call></tool_call> tags.

# Response Format
You must output in the following EXACT order and structural format. Every component must be on a NEW LINE:

1) Action: [A single short imperative sentence]
2) <tool_call>
{"name": "...", "arguments": {"action": "execute_code", "language": "python", "code": "..."}}
</tool_call>

# Critical Execution Rules
- **Code-First for Data**: When handling structured data (Excel/Calc, CSV, JSON, Files), STRICTLY AVOID clicking cells one by one. Use `execute_code` to manipulate data using python
libraries (e.g., `pandas`, `openpyxl`).
- **Batch Processing**: If a task involves repetitive steps (e.g., renaming 10 files, extracting emails from 50 rows), write a Python script or Bash command to do it in one shot.
- **GUI-Only for Navigation**: Use GUI actions (click/type) ONLY for visual-only tasks, like opening an app, navigating menus, or browsing the web where no API/CLI is available.
- **Verification**: After `execute_code`, you may use the next screenshot to verify the result if needed.

# Examples of `execute_code` Usage:
- **Task**: "Sum column B in sheet.xlsx"
    **Action**: Use pandas to calculate the sum and save it.
    **Tool_Call**: {"action": "execute_code", "language": "python", "code": "import pandas as pd; df = pd.read_excel('sheet.xlsx'); print(df.iloc[:, 1].sum())"}

- **Task**: "Find all logs containing 'Error' and move to a folder"
    **Action**: Execute a bash command to filter and move files.
    **Tool_Call**: {"action": "execute_code", "language": "bash", "code": "grep -l 'Error' *.log | xargs -I {} mv {} ./errors/"}
"""

        instruction_prompt = f"""
Please generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {instruction}
"""

        # ================== 构造 self.messages ==================

        # 第一次调用 predict 时，初始化 system + 第一条 user
        if not self.messages:
            self.messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": system_prompt},
                    ],
                }
            ]

        # 如果上一轮有模型回复，先补上一条 assistant 消息
        if self.responses:
            last_response = self.responses[-1]
            self.messages.append(
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": last_response},
                    ],
                }
            )

        # 当前轮 user 消息
        curr_user_content = []
        if self.last_code_result:
            # 有代码执行结果则优先喂代码结果，不再附截图
            curr_user_content.append(
                {
                    "type": "text",
                    "text": f"Code Execution Result:\n```\n{self.last_code_result}\n```\nPlease continue based on this result.",
                }
            )
            self.last_code_result = None
        else:
            # 没有代码结果则附当前截图
            curr_img_url = f"data:image/png;base64,{processed_image}"
            curr_user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": curr_img_url},
                }
            )

        # 第一轮附带原始 instruction
        if not self.responses:
            curr_user_content.append({"type": "text", "text": instruction_prompt})

        self.messages.append(
            {
                "role": "user",
                "content": curr_user_content,
            }
        )

        # ========= 在 messages 上做截图裁剪 =========
        self._cleanup_old_screenshots()

        # debug
        # self.debug_print_messages(self.messages)

        response = self.call_llm(
            {
                "model": self.model,
                "messages": self.messages,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "temperature": self.temperature,
            },
            self.model,
        )

        logger.info(f"Qwen3VL Output: {response}")

        # Update History
        self.responses.append(response)

        meta_data, pyautogui_code = self.parse_response(
            response,
            width,
            height,
            processed_width,
            processed_height,
        )

        logger.info(f"Pyautogui code: {pyautogui_code}")
        return meta_data, pyautogui_code
    
    def _cleanup_old_screenshots(self):
        """
        在 self.messages 上清理超出配额的截图。

        规则：
        - 从后往前遍历 user 消息，统计其中含有 image_url 的“轮次”。
        - 只保留最近 history_n 轮带图的 user 消息。
        - 如果 keep_first_image=True，则如果第一个 user 消息带图，强制保留第一轮的截图，
        不占 history_n 的名额。
        """
        # 收集所有带截图的 user 消息索引（按出现顺序）
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

        # 需要保留的索引集合
        keep_indices = set()

        # 1. keep_first_image: 如果启用且第一条 user 有图，则强制保留那一条
        if self.keep_first_image:
            # 找到 messages 中第一条 user 消息并检查是否有图
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

        # 2. 在剩余带图 user 中，从后往前保留最近 history_n 个
        remaining = self.history_n
        for idx in reversed(user_indices_with_img):
            if idx in keep_indices:
                # 已经被 keep_first_image 占用，不占 history_n 名额
                continue
            if remaining <= 0:
                break
            keep_indices.add(idx)
            remaining -= 1

        # 3. 对不在 keep_indices 里的带图 user，清理其 image_url
        for idx in user_indices_with_img:
            if idx in keep_indices:
                continue
            msg = self.messages[idx]
            content = msg.get("content", [])
            new_content = [
                part for part in content
                if not (isinstance(part, dict) and part.get("type") == "image_url")
            ]
            if not new_content:
                msg["content"] = [
                    {
                        "type": "text",
                        "text": "[Old Screenshot Removed]",
                    }
                ]
            else:
                msg["content"] = new_content

    def parse_response(
        self,
        response: str,
        original_width: int = None,
        original_height: int = None,
        processed_width: int = None,
        processed_height: int = None,
    ) -> Tuple[List[Dict], List[str]]:
        """Parse LLM response and convert it to metadata and pyautogui code."""
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

        # ---- extract Action: line ----
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

        # ---- extract all tool_call JSON blocks ----
        # support both wrapped in <tool_call>...</tool_call> and bare JSON lines
        tool_json_blocks: List[str] = []

        for m in re.finditer(r"<tool_call>([\s\S]*?)</tool_call>", response):
            block = m.group(1).strip()
            if block:
                tool_json_blocks.append(block)

        # de-duplicate while preserving order
        seen = set()
        unique_blocks = []
        for b in tool_json_blocks:
            if b not in seen:
                seen.add(b)
                unique_blocks.append(b)

        def process_tool_call(json_str: str) -> None:
            try:
                tool_call = json.loads(json_str)
                args = tool_call["arguments"]
                action = args["action"]

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
                    coord: List[int] = []
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
                    coord: List[int] = []
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
                    coord: List[int] = []
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
                                if key.startswith("keys=["):
                                    key = key[6:]
                                if key.endswith("]"):
                                    key = key[:-1]
                                if key.startswith("['") or key.startswith('["'):
                                    key = key[2:] if len(key) > 2 else key
                                if key.endswith("']") or key.endswith('"]'):
                                    key = key[:-2] if len(key) > 2 else key
                                key = key.strip()
                                cleaned_keys.append(key)
                            else:
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
                    coord: List[int] = []
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
                    coord: List[int] = []
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
                    code_content = args.get("code", "")
                    language = args.get("language", "python")
                    code_str = f"EXEC_CODE|{language}|{code_content}"
                    pyautogui_code.append(code_str)
                    meta_data.append(make_meta(code_str))

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse tool call: {e}")

        for block in unique_blocks:
            process_tool_call(block)

        return meta_data, pyautogui_code
    
    def evaluate(self, task_instruction: str, obs: Dict) -> Dict[str, Any]:
        """
        Self-judge function.
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

        if "kubebrain" in  self.base_url:
            logger.info(f"H Cluster Local VLLM: {self.base_url}")
            client = OpenAI(base_url=self.base_url, api_key=self.api_key, default_headers=custom_headers)
        else:
            logger.info(f"H Service VLLM / Boyue: {self.base_url}")
            client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        
        for _ in range(MAX_RETRY_TIMES):
            # logger.info("Generating content with Qwen model: %s", model)
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"Error calling Qwen model: {e}")
                time.sleep(5)
                continue
        return ""
    
    def reset(self, _logger=None):
        global logger
        logger = (
            _logger if _logger is not None
            else logging.getLogger("desktopenv.qwen3vl_agent")
        )

        self.responses = []
        self.messages = []

    def debug_print_messages(self, messages: list):
        """
        优雅地打印 messages 列表，自动截断 Base64 图片以方便检查装填逻辑。
        """
        print("\n" + "="*50 + " MESSAGES LOGIC DEBUG " + "="*50)
        
        if not messages:
            print(" [!] Messages list is empty.")
            print("="*122 + "\n")
            return

        for i, msg in enumerate(messages):
            role = msg.get("role", "UNKNOWN").upper()
            # 用不同符号区分角色，视觉上更直观
            prefix = "👤" if role == "USER" else "🤖" if role == "ASSISTANT" else "⚙️"
            
            print(f"\n{prefix} [{i}] ROLE: {role}")
            print("-" * 80)
            
            content = msg.get("content", [])
            
            # 兼容 content 是纯字符串的情况
            if isinstance(content, str):
                print(f"  (Text) : {content}")
                continue
                
            # 遍历 content 列表里的多模态元素
            for j, item in enumerate(content):
                item_type = item.get("type", "unknown")
                
                if item_type == "text":
                    text_content = item.get('text', '')
                    # 如果文本是代码执行结果，稍微突出显示
                    if "Code Execution Result:" in text_content:
                        print(f"  📝 (Text-CodeResult) : {text_content}")
                    else:
                        # 超过 200 字符的普通长文本稍微截断一下，保持排版整洁
                        if len(text_content) > 2000:
                            text_content = text_content[:2000] + " ... [TEXT TRUNCATED]"
                        print(f"  💬 (Text)  : {text_content}")
                        
                elif item_type == "image_url":
                    # 拦截并替换图片 URL
                    print(f"  🖼️ (Image) : <BASE64_IMAGE_DATA_TRUNCATED>")
                    
                else:
                    print(f"  ❓ ({item_type}) : {item}")
                    
        print("\n" + "="*122 + "\n")