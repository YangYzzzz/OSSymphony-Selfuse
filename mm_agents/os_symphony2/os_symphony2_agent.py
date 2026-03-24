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
        self.add_thought_prefix = add_thought_prefix
        self.coordinate_type = coordinate_type

        assert action_space in ["pyautogui"], "Invalid action space"
        assert observation_type in ["screenshot"], "Invalid observation type"

        self.thoughts = []
        self.actions = []
        self.critic_actions = []
        self.observations = []
        self.responses = []
        self.screenshots = []
        self.keep_first_image = keep_first_image

        # 为了执行code设置的变量
        self.last_code_result = None
        self.code_results_history = []

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
        # logger.info(f"Original screen resolution: {width}x{height}")

        processed_image = process_image(screenshot_bytes)
        processed_img = Image.open(
            BytesIO(base64.b64decode(processed_image))
        )
        processed_width, processed_height = processed_img.size
        # logger.info(f"Processed image resolution: {processed_width}x{processed_height}")

        self.screenshots.append(processed_image)

        description_prompt_lines = [
            "Use a mouse and keyboard to interact with a computer, and take screenshots.",
            "* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.",
            "* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.",
            (
                f"* The screen's resolution is {processed_width}x{processed_height}."
                if self.coordinate_type == "absolute"
                else "* The screen's resolution is 1000x1000."
            ),
            "* Whenever you intend to move the cursor to click on an element like an icon, you should consult a screenshot to determine the coordinates of the element before moving the cursor.",
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
* `scroll`: Performs a scroll of the mouse scroll wheel.
* `execute_code`: Execute raw Python or Bash scripts to perform tasks directly in the operating system. Use this for batch processing, file manipulation, or tasks where GUI clicking is inefficient or repetitive.
* `wait`: Wait specified seconds for the change to happen.
* `terminate`: Terminate the current task and report its completion status.
# """

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
                                "right_click", "middle_click", "double_click", "scroll", 
                                "execute_code", "wait", "terminate"
                            ], 
                            "type": "string"
                        },
                        "keys": {"description": "Required only by `action=key`.", "type": "array"}, 
                        "text": {"description": "Required only by `action=type`.", "type": "string"}, 
                        "coordinate": {"description": "The x,y coordinates for mouse actions.", "type": "array"}, 
                        "pixels": {"description": "The amount of scrolling.", "type": "number"}, 
                        "time": {"description": "The seconds to wait.", "type": "number"}, 
                        # 新增！
                        "code": {
                            "description": "The raw code string to execute. Required only when `action=execute_code`.", 
                            "type": "string"
                        },
                        "language": {
                            "description": "The programming language of the code. Required only when `action=execute_code`.", 
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


#         system_prompt = """# Tools

# You may call one or more functions to assist with the user query.

# You are provided with function signatures within <tools></tools> XML tags:
# <tools>
# """ + json.dumps(tools_def) + """
# </tools>

# For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
# <tool_call>
# {"name": <function-name>, "arguments": <args-json-object>}
# </tool_call>

# # Response format

# Response format for every step:
# 1) Action: a short imperative describing what to do in the UI.
# 2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

# Rules:
# - Output exactly in the order: Action, <tool_call>.
# - Be brief: one sentence for Action.
# - Do not output anything else outside those parts.
# - If finishing, use action=terminate in the tool call."""

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
- **Code-First for Data**: When handling structured data (Excel/Calc, CSV, JSON, Files), STRICTLY AVOID clicking cells one by one. Use `execute_code` to manipulate data using python libraries (e.g., `pandas`, `openpyxl`).
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
        
        messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt},
                ],
            }
        ]

        self.code_results_history.append(self.last_code_result)
        # ================= History Construction =================
        # 保留全部回答 和 最近 history_n 张图片
        N = len(self.responses) 
        keep_image_indices = set()
        
        # 1. 计算需要保留图片的索引
        if self.history_n >= N + 1:
            keep_image_indices = set(range(N + 1))
        else:
            keep_image_indices.add(N) # 始终保留当前最新步
            
            if self.keep_first_image and self.history_n > 1:
                keep_image_indices.add(0)
                remaining_slots = self.history_n - 2
                for i in range(N - remaining_slots, N):
                    if i > 0:
                        keep_image_indices.add(i)
            else:
                remaining_slots = self.history_n - 1
                for i in range(N - remaining_slots, N):
                    if i >= 0:
                        keep_image_indices.add(i)

        # 2. 构建历史轮次 messages
        for i in range(N):
            user_content = []

            # 提取历史第 i 步对应的代码执行结果
            step_code_result = self.code_results_history[i]
            if step_code_result is not None:
                # 命中策略：如果这一步有代码结果，则【不喂截图】，喂入代码执行结果的文本
                user_content.append({
                    "type": "text",
                    "text": f"Code Execution Result:\n```\n{step_code_result}\n```\nPlease continue based on this result."
                })
            elif i in keep_image_indices:
                img_url = f"data:image/png;base64,{self.screenshots[i]}"
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": img_url},
                })
            
            if i == 0:
                user_content.append({"type": "text", "text": instruction_prompt})
                
            # 只有当 user_content 有内容时（有图或有首轮 prompt），才压入 user 消息
            if user_content:
                messages.append({
                    "role": "user",
                    "content": user_content,
                })

            # Assistant 的历史回复无条件全部压入（这会导致早期轮次出现连续的 assistant 消息）
            messages.append({
                "role": "assistant",
                "content": [
                    {"type": "text", "text": f"{self.responses[i]}"},
                ],
            })

        # 3. 追加当前步 (Current Step)
        curr_user_content = []
        # 当前步的结果就是刚刚 append 进去的 self.last_code_result
        curr_code_result = self.last_code_result
        
        if curr_code_result is not None:
            # 当前步跳过截图，直接给代码结果
            curr_user_content.append({
                "type": "text",
                "text": f"Code Execution Result:\n```\n{curr_code_result}\n```\nPlease continue based on this result."
            })
        elif N in keep_image_indices:
            # 当前步正常走截图逻辑
            curr_img_url = f"data:image/png;base64,{processed_image}" 
            curr_user_content.append({
                "type": "image_url",
                "image_url": {"url": curr_img_url},
            })
            
        if N == 0:
            curr_user_content.append({"type": "text", "text": instruction_prompt})

        # 当前步通常一定会有图或者 prompt，压入最后一条 user 消息触发模型生成
        if curr_user_content:
            messages.append({
                "role": "user",
                "content": curr_user_content,
            })

        # 重置为 None，防止对下一次 predict 产生污染
        self.last_code_result = None
        # ========================================================

        # 用于debug
        self.debug_print_messages(messages)

        response = self.call_llm(
            {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "temperature": self.temperature,
            },
            self.model,
        )

        logger.info(f"Qwen3VL Output: {response}")

        # Update History
        self.responses.append(response)
        
        low_level_instruction, pyautogui_code = self.parse_response(
            response,
            width,
            height,
            processed_width,
            processed_height,
        )

        logger.info(f"Low level instruction: {low_level_instruction}")
        logger.info(f"Pyautogui code: {pyautogui_code}")

        self.actions.append(low_level_instruction)

        return response, pyautogui_code

    def parse_response(
        self,
        response: str,
        original_width: int = None,
        original_height: int = None,
        processed_width: int = None,
        processed_height: int = None,
    ) -> Tuple[str, List[str]]:
        """
        Parse LLM response and convert it to low level action and pyautogui code.
        """
        low_level_instruction = ""
        pyautogui_code: List[str] = []

        if response is None or not response.strip():
            return low_level_instruction, pyautogui_code

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
                args = tool_call["arguments"]
                action = args["action"]

                if action == "left_click":
                    if "coordinate" in args:
                        x, y = args["coordinate"]
                        adj_x, adj_y = adjust_coordinates(x, y)
                        pyautogui_code.append(f"pyautogui.click({adj_x}, {adj_y})")
                    else:
                        pyautogui_code.append("pyautogui.click()")

                elif action == "right_click":
                    if "coordinate" in args:
                        x, y = args["coordinate"]
                        adj_x, adj_y = adjust_coordinates(x, y)
                        pyautogui_code.append(
                            f"pyautogui.rightClick({adj_x}, {adj_y})"
                        )
                    else:
                        pyautogui_code.append("pyautogui.rightClick()")

                elif action == "middle_click":
                    if "coordinate" in args:
                        x, y = args["coordinate"]
                        adj_x, adj_y = adjust_coordinates(x, y)
                        pyautogui_code.append(
                            f"pyautogui.middleClick({adj_x}, {adj_y})"
                        )
                    else:
                        pyautogui_code.append("pyautogui.middleClick()")

                elif action == "double_click":
                    if "coordinate" in args:
                        x, y = args["coordinate"]
                        adj_x, adj_y = adjust_coordinates(x, y)
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
                        pyautogui_code.append(
                            f"pyautogui.moveTo({adj_x}, {adj_y})"
                        )
                    else:
                        pyautogui_code.append("pyautogui.moveTo(0, 0)")

                elif action == "left_click_drag":
                    if "coordinate" in args:
                        x, y = args["coordinate"]
                        adj_x, adj_y = adjust_coordinates(x, y)
                        duration = args.get("duration", 0.5)
                        pyautogui_code.append(
                            f"pyautogui.dragTo({adj_x}, {adj_y}, duration={duration})"
                        )
                    else:
                        pyautogui_code.append("pyautogui.dragTo(0, 0)")
                # 新增 execute_code 的解析逻辑
                elif action == "execute_code":
                    code_content = args.get("code", "")
                    language = args.get("language", "python")
                    # 使用特殊的分隔符封装，以便下游执行引擎 (Environment) 拦截
                    # 确保 code_content 里的换行符等被安全转义或传递
                    # encoded_code = base64.b64encode(code_content.encode('utf-8')).decode('utf-8')
                    # pyautogui_code.append(f"EXEC_CODE|{language}|{encoded_code}")code_content
                    pyautogui_code.append(f"EXEC_CODE|{language}|{code_content}")
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

        return low_level_instruction, pyautogui_code
    
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

        self.thoughts = []
        self.actions = []
        self.critic_actions = []
        self.observations = []
        self.responses = []
        self.screenshots = []

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