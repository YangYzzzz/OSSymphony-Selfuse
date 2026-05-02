from ast import Pass
import base64
import json
import logging
import time
import copy
from io import BytesIO
from typing import Dict, List, Tuple, Any, Optional
import httpx
import backoff
import openai
from openai import OpenAI
from PIL import Image
from requests.exceptions import SSLError
from mm_agents.utils.qwen_vl_utils import smart_resize
from mm_agents.uitars15_v2 import IMAGE_FACTOR
from mm_agents.base import ComputerUseBaseAgent
from mm_agents.utils.qwen_vl_utils import (
    smart_resize,
)
import json
import textwrap


SYSTEM_PROMPT = """
# Role & Goal
You are a powerful OS Agent capable of both GUI interaction and direct system-level programming and are utilising an Ubuntu virtual machine using x86_64 architecture with internet access.
Your goal is to complete tasks with MAXIMUM efficiency and MINIMUM steps.

# Environment & Screen
- The user's home directory is "/home/user".
- The user's password is "password".
- The screen's resolution is represented on a 1000x1000 relative coordinate grid.

# Additional Rules & Action Guidelines

### 1. Action Selection Strategy
**Prioritize `code` actions for:**
- **Data Processing:** Parsing or manipulating structured data (e.g., CSV, Excel, JSON).
- **Batch Operations:** Bulk file management (rename, copy, move, delete).
- **Text Manipulation:** Complex search/replace across files or within large documents.

**Reserve GUI actions for:**
- **System Navigation:** Launching, focusing, or switching between applications.
- **Visual Interactions:** Precise clicking, dragging, or interacting with UI elements based on visual layout.
- **Non-Programmable Tasks:** Navigating browsers or desktop applications where no CLI/API is readily available.

### 2. Execution & Verification Workflow
- **Evaluate Output:** Immediately after executing a `code` action, analyze the textual output (stdout/stderr) to assess success before taking the next step.
- **Visual Verification:** Because code executes in the background, you MUST use GUI actions to open and inspect the modified files or final results to ensure the outcome is visible.
- **GUI Fallback:** If code-based approaches fail or encounter persistent errors, gracefully pivot to using GUI actions to complete the task.

### 3. Environment & Dependencies
- **Pre-installed Packages:** You have direct access to `ffmpeg`, `ffmpeg-python`, `av`, `python-pptx`, `python-docx`, `openpyxl`, `pillow`, `opencv-python`, `pydub`, `PyMuPDF`, `pdfplumber`.
- **Dynamic Installation:** You are authorized to install any missing dependencies as needed to accomplish the task.
"""

TOOL_DEFINE_PROMPT = {
    "type": "function", 
    "function": {
        "name_for_human": "custom_computer_use", 
        "name": "custom_computer_use", 
        "description": (                                            
                "Control a desktop GUI and execute system-level code."
                "Use it to move the mouse, click, type, scroll, wait, terminate tasks,"
                "and run raw Python or Bash code on the operating system."
            ),
        "parameters": {
            "properties": {
                "action": {
                    "description": 
                        textwrap.dedent("""
                            The type of operation to perform: 
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
                            * `code`: Execute raw Python or Bash scripts to perform tasks directly in the operating system.
                        """),
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

OUTPUT_FORMAT_PROMPT = """
# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
""" + json.dumps(TOOL_DEFINE_PROMPT) + """
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one sentence for Action.
- Do not output anything else outside those parts.
- If finishing, use action=terminate in the tool call.
"""

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
        keep_first_image: bool = True,
        use_thinking: bool = False,
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

        # 记录上一轮产生的 tool_calls，供下一轮填充 tool 结果
        self.pending_tool_calls: List[Any] = []

        # 统一维护对话历史（system + user + assistant）
        self.messages = []

        self.system_prompt = SYSTEM_PROMPT + '\n' + OUTPUT_FORMAT_PROMPT
        self.use_thinking = use_thinking


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

        # feed tool result for previous tool_calls
        result_text = ""
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
                        "tool_call_id": tool_call.get("id", "tool_call_0"),
                        "content": result_text,
                    }
                )
            # 已经把上一轮的 tool 结果补完，本轮重新收集
            self.pending_tool_calls = []

        # 当前轮 user 消息
        curr_user_content = []

        # 第一次调用 predict 时，初始化 system 附带原始 instruction
        if not self.messages:
            self.messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": self.system_prompt},
                    ],
                }
            ]
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

        low_level_instuction, pyautogui_code, coordinates = self.parse_response(
            response,
            width,
            height,
            processed_width,
            processed_height,
        )

        logger.info(f"Pyautogui code: {pyautogui_code}")
        return [{"raw_response": response, "coordinates": coordinates, 'reflection': result_text}], pyautogui_code
    
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
    ) -> Tuple[str, List[str], List[int]]:
        """
        Parse LLM response and convert it to low level action and pyautogui code.
        Returns: (low_level_instruction, pyautogui_code, coordinates)
        """
        low_level_instruction = ""
        pyautogui_code: List[str] = []
        coordinates: List[int] = []

        if response is None or not response.strip():
            return low_level_instruction, pyautogui_code, coordinates

        def adjust_coordinates(x: float, y: float) -> Tuple[int, int]:
            if not (original_width and original_height):
                return int(x), int(y)
            if self.coordinate_type == "absolute":
                # scale from processed pixels to original
                if processed_width and processed_height:
                    x_scale = original_width / processed_width
                    y_scale = original_height / processed_height
                    return int(x * x_scale), int(y * y_scale)
                return int(x), int(y)
            # relative: scale from 0..999 grid
            x_scale = original_width / 999
            y_scale = original_height / 999
            return int(x * x_scale), int(y * y_scale)

        def process_tool_call(json_str: str) -> None:
            try:
                tool_call = json.loads(json_str)
                if tool_call.get("name") == "computer_use":
                    args = tool_call["arguments"]
                    action = args["action"]

                    if action == "left_click":
                        if "coordinate" in args:
                            x, y = args["coordinate"]
                            adj_x, adj_y = adjust_coordinates(x, y)
                            coordinates.extend([adj_x, adj_y])
                            pyautogui_code.append(f"pyautogui.click({adj_x}, {adj_y})")
                        else:
                            pyautogui_code.append("pyautogui.click()")

                    elif action == "right_click":
                        if "coordinate" in args:
                            x, y = args["coordinate"]
                            adj_x, adj_y = adjust_coordinates(x, y)
                            coordinates.extend([adj_x, adj_y])
                            pyautogui_code.append(
                                f"pyautogui.rightClick({adj_x}, {adj_y})"
                            )
                        else:
                            pyautogui_code.append("pyautogui.rightClick()")

                    elif action == "middle_click":
                        if "coordinate" in args:
                            x, y = args["coordinate"]
                            adj_x, adj_y = adjust_coordinates(x, y)
                            coordinates.extend([adj_x, adj_y])
                            pyautogui_code.append(
                                f"pyautogui.middleClick({adj_x}, {adj_y})"
                            )
                        else:
                            pyautogui_code.append("pyautogui.middleClick()")

                    elif action == "double_click":
                        if "coordinate" in args:
                            x, y = args["coordinate"]
                            adj_x, adj_y = adjust_coordinates(x, y)
                            coordinates.extend([adj_x, adj_y])
                            pyautogui_code.append(
                                f"pyautogui.doubleClick({adj_x}, {adj_y})"
                            )
                        else:
                            pyautogui_code.append("pyautogui.doubleClick()")

                    elif action == "type":
                        text = args.get("text", "")
                        lines = text.split("\n")
                        for idx, line in enumerate(lines):
                            if line:
                                pyautogui_code.append(f"pyautogui.typewrite({repr(line)}, interval=0.03)")
                            if idx < len(lines) - 1:
                                pyautogui_code.append("pyautogui.press('enter')")

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
                            pyautogui_code.append(f"pyautogui.hotkey({keys_str})")
                        else:
                            pyautogui_code.append(f"pyautogui.press({keys_str})")

                    elif action == "scroll":
                        pixels = args.get("pixels", 0)
                        pyautogui_code.append(f"pyautogui.scroll({pixels})")

                    elif action == "wait":
                        pyautogui_code.append("WAIT")

                    elif action == "terminate":
                        pyautogui_code.append("DONE")

                    elif action == "mouse_move":
                        if "coordinate" in args:
                            x, y = args["coordinate"]
                            adj_x, adj_y = adjust_coordinates(x, y)
                            coordinates.extend([adj_x, adj_y])
                            pyautogui_code.append(
                                f"pyautogui.moveTo({adj_x}, {adj_y})"
                            )
                        else:
                            pyautogui_code.append("pyautogui.moveTo(0, 0)")

                    elif action == "left_click_drag":
                        if "coordinate" in args:
                            x, y = args["coordinate"]
                            adj_x, adj_y = adjust_coordinates(x, y)
                            coordinates.extend([adj_x, adj_y])
                            duration = args.get("duration", 0.5)
                            pyautogui_code.append(
                                f"pyautogui.dragTo({adj_x}, {adj_y}, duration={duration})"
                            )
                        else:
                            pyautogui_code.append("pyautogui.dragTo(0, 0)")

                    elif action == "code":
                        code_content = args.get("execute_code", "")
                        language = args.get("language", "python")
                        code_str = f"{language.upper()}|{code_content}"
                        pyautogui_code.append(code_str)

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse tool call: {e}")

        lines = response.split("\n")
        inside_tool_call = False
        current_tool_call: List[str] = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.lower().startswith(("action:")):
                if not low_level_instruction:
                    low_level_instruction = line.split("Action:")[-1].strip()
                continue

            if line.startswith("<tool_call>"):
                inside_tool_call = True
                continue
            elif line.startswith("</tool_call>"):
                if current_tool_call:
                    process_tool_call("\n".join(current_tool_call))
                    current_tool_call = []
                inside_tool_call = False
                continue

            if inside_tool_call:
                current_tool_call.append(line)
                continue

            if line.startswith("{") and line.endswith("}"):
                try:
                    json_obj = json.loads(line)
                    if "name" in json_obj and "arguments" in json_obj:
                        process_tool_call(line)
                except json.JSONDecodeError:
                    pass

        if current_tool_call:
            process_tool_call("\n".join(current_tool_call))

        if not low_level_instruction and len(pyautogui_code) > 0:
            action_type = pyautogui_code[0].split(".", 1)[1].split("(", 1)[0]
            low_level_instruction = f"Performing {action_type} action"

        return low_level_instruction, pyautogui_code, coordinates
    

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

        custom_timeout = httpx.Timeout(600.0, read=600.0, connect=60.0)
        if "kubebrain" in  self.base_url:
            logger.info(f"H Cluster Local VLLM: {self.base_url}")
            client = OpenAI(base_url=self.base_url, api_key=self.api_key, default_headers=custom_headers, timeout=custom_timeout)
        else:
            logger.info(f"H Service VLLM / Boyue: {self.base_url}")
            client = OpenAI(base_url=self.base_url, api_key=self.api_key, timeout=custom_timeout)
        
        for _ in range(MAX_RETRY_TIMES):
            # logger.info("Generating content with Qwen model: %s", model)
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    tools=json.loads(QWEN3VL_COMPUTER_USE_TOOL_SCHEMA),
                    tool_choice="auto", # required 的话只会输出 tool_call, auto 可以自由一点
                    extra_body={
                        "chat_template_kwargs": {"enable_thinking": self.use_thinking}
                    }
                )
                return response.choices[0].message.content
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

    def evaluate(self, task_instruction: str, obs: Dict) -> Dict[str, Any]:
        """Self-judge function.

        Returns a dictionary with 'thought' and 'score'.
        """
        pass

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