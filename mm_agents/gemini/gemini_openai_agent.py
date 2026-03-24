import base64
import copy
import os
import time
from PIL import Image
import io
import json
from typing import Literal, Optional, Union, Any, Dict, Tuple, List

# 替换为 OpenAI SDK
from openai import OpenAI
import termcolor
from rich.console import Console
from rich.table import Table
import pydantic
from datetime import datetime
import logging

logger = logging.getLogger("desktopenv.agent")
console = Console()

PREDEFINED_COMPUTER_USE_FUNCTIONS = [
    "open_web_browser",
    "click_at",
    "hover_at",
    "type_text_at",
    "scroll_document",
    "scroll_at",
    "wait_5_seconds",
    "search",
    "key_combination",
    "drag_and_drop",
]

SYSTEM_PROMPT = f"""
* You are utilising an Ubuntu virtual machine using x86_64 architecture with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open browser, please just click on the Chrome icon.  Note, Chrome is what is installed on your system.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell. For example "(DISPLAY=:1 xterm &)". GUI apps run with bash tool will appear within your desktop environment, but they may take some time to appear. Take a screenshot to confirm it did.
* When using your bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file and use str_replace_editor or `grep -n -B <lines before> -A <lines after> <query> <filename>` to confirm output.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.  Either that, or make sure you scroll down to see everything before deciding something isn't available.
* DO NOT ask users for clarification during task execution. DO NOT stop to request more information from users. Always take action using available tools.
* The current date is {datetime.today().strftime('%A, %B %d, %Y')}.
* Home directory of this Ubuntu system is '/home/user'.
* You can only use the following predefiend computer use functions: {", ".join(PREDEFINED_COMPUTER_USE_FUNCTIONS)}
* DO NOT use other functions! 
* Use ONE function each time.
"""

# 修改: 评估系统提示词，要求输出 JSON 格式的思考和分数
EVALUATION_SYSTEM_PROMPT = """
* You are an expert evaluator for an autonomous computer agent.
* Your job is to review the conversation history, the actions taken by the agent, and the final screenshot of the screen.
* You must determine if the user's initial instruction has been successfully completed based on the visual evidence in the final screenshot.
* Be strict. If the screenshot does not show clear evidence that the task is finished (e.g., the specific webpage is not open, the file is not created, the text is not typed), consider it a failure.
* You must output your result in valid JSON format with exactly two keys:
  - "thought": A brief explanation of your reasoning.
  - "score": The integer 1 if the task is successfully completed, or 0 if failed/incomplete.
* Example Output: {"thought": "The browser is open and shows the correct website.", "score": 1}
* Do not output any other text outside the JSON object.
"""

# OpenAI 需要明确的 Tool Schema 定义
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "open_web_browser",
            "description": "Opens the web browser.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "click_at",
            "description": "Clicks at a specific coordinate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "The x coordinate (0-1000)."},
                    "y": {"type": "integer", "description": "The y coordinate (0-1000)."}
                },
                "required": ["x", "y"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hover_at",
            "description": "Moves the mouse to a specific coordinate without clicking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "The x coordinate (0-1000)."},
                    "y": {"type": "integer", "description": "The y coordinate (0-1000)."}
                },
                "required": ["x", "y"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "type_text_at",
            "description": "Types text at a specific location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "The x coordinate (0-1000)."},
                    "y": {"type": "integer", "description": "The y coordinate (0-1000)."},
                    "text": {"type": "string", "description": "The text to type."},
                    "press_enter": {"type": "boolean", "description": "Whether to press enter after typing."},
                    "clear_before_typing": {"type": "boolean", "description": "Whether to clear the field before typing."}
                },
                "required": ["x", "y", "text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scroll_document",
            "description": "Scrolls the entire document/page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {"type": "string", "enum": ["up", "down", "left", "right"]}
                },
                "required": ["direction"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scroll_at",
            "description": "Scrolls at a specific location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "direction": {"type": "string", "enum": ["up", "down", "left", "right"]},
                    "magnitude": {"type": "integer"}
                },
                "required": ["x", "y", "direction"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wait_5_seconds",
            "description": "Waits for 5 seconds.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Performs a Google search (Browser action).",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "navigate",
            "description": "Navigates to a specific URL (Browser action).",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "key_combination",
            "description": "Presses a combination of keys.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keys": {"type": "string", "description": "Keys separated by +, e.g. ctrl+c"}
                },
                "required": ["keys"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "drag_and_drop",
            "description": "Drags items from one location to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "destination_x": {"type": "integer"},
                    "destination_y": {"type": "integer"}
                },
                "required": ["x", "y", "destination_x", "destination_y"]
            }
        }
    }
]

class GeminiOpenAIAgent:
    def __init__(
        self,
        platform: str = "Ubuntu",
        verbose: bool = True,
        model: str = "gemini-3-flash-preview",
        max_tokens: int = 4096,
        api_key: str = "",
        base_url: str = "",
        action_space: str = "pyautogui",
        screen_size: tuple[int, int] = (1920, 1080),
        temperature: float = 0.1,
        top_p: float = 0.95,
        max_image_history_length: int = 8,
    ):
        self.platform = platform
        self.verbose = verbose
        self.action_space = action_space
        self.model = model
        self.messages: list = []
        self.screen_size = screen_size
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url if base_url else None
        )
        
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.max_image_history_length = max_image_history_length

        self.messages.append({"role": "system", "content": SYSTEM_PROMPT})
        self.pending_tool_calls = []

    def reset(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.pending_tool_calls = []
        logger.info("OpenAIAgent reset.")

    def _encode_image_to_base64(self, image_bytes: bytes, mime_type: str = "image/png") -> str:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:{mime_type};base64,{base64_image}"

    def get_model_response(self, max_retries=5, base_delay_s=1):
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    max_tokens=self.max_tokens,
                    tools=TOOLS_SCHEMA,
                    extra_body={
                        "thinking_config": {
                            "include_thoughts": True
                        }
                    }
                )
                return response
            except Exception as e:
                print(e)
                if attempt < max_retries - 1:
                    delay = base_delay_s * (2**attempt)
                    time.sleep(delay)
                else:
                    raise

    def denormalize_x(self, x: int) -> int:
        return int(x / 1000 * self.screen_size[0])

    def denormalize_y(self, y: int) -> int:
        return int(y / 1000 * self.screen_size[1])

    def handle_action(self, action_name: str, action_args: dict) -> str:
        """
        Handles the action and returns the PyAutoGUI command string.
        Note: Coordinates calculation is moved to predict to ensure consistency in metadata.
        """
        if action_name == "open_web_browser":
            return "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0)"
        
        elif action_name == "click_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            return f"pyautogui.click(x={x}, y={y})"

        elif action_name == "hover_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            return f"pyautogui.moveTo(x={x}, y={y})"

        elif action_name == "type_text_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            text = action_args["text"]
            press_enter = action_args.get("press_enter", False)
            clear_before_typing = action_args.get("clear_before_typing", True)
            
            action_str = f"pyautogui.click(x={x}, y={y}); "
            if clear_before_typing:
                action_str += "time.sleep(0.1); pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace'); "
            action_str += f"pyautogui.write('{text}'); "
            if press_enter:
                action_str += "pyautogui.press('enter')"
            return action_str
        
        elif action_name == "scroll_document":
            direction = action_args["direction"]
            amount = -self.screen_size[1] if direction == "down" else self.screen_size[1]
            if direction in ["left", "right"]:
                return f"pyautogui.hscroll({amount})"
            else:
                return f"pyautogui.scroll({amount})"

        elif action_name == "scroll_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            magnitude = action_args.get("magnitude", 800)
            direction = action_args["direction"]
            
            action_str = f"pyautogui.moveTo({x}, {y}); "
            if direction in ("up", "down"):
                magnitude = self.denormalize_y(magnitude)
                scroll_amount = magnitude if direction == "up" else -magnitude
                action_str += f"pyautogui.scroll({scroll_amount})"
            elif direction in ("left", "right"):
                magnitude = self.denormalize_x(magnitude)
                scroll_amount = magnitude if direction == "left" else -magnitude
                action_str += f"pyautogui.hscroll({scroll_amount})"
            return action_str
            
        elif action_name == "wait_5_seconds":
            return "time.sleep(5)"
        
        elif action_name == "search":
            return "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0); pyautogui.hotkey('ctrl', 'l'); pyautogui.write('www.google.com'); pyautogui.press('enter')"
        
        elif action_name == "navigate":
            url = action_args["url"]
            return f"pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0); pyautogui.hotkey('ctrl', 'l'); pyautogui.write('{url}'); pyautogui.press('enter')"
        
        elif action_name == "key_combination":
            keys = action_args["keys"].split("+")
            py_keys = [k.replace('control', 'ctrl') for k in keys]
            keys_str = ", ".join([f"'{k}'" for k in py_keys])
            return f"pyautogui.hotkey({keys_str})"

        elif action_name == "drag_and_drop":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            destination_x = self.denormalize_x(action_args["destination_x"])
            destination_y = self.denormalize_y(action_args["destination_y"])
            return f"pyautogui.moveTo({x}, {y}); pyautogui.dragTo({destination_x}, {destination_y}, duration=0.5)"
        
        else:
            raise ValueError(f"Unsupported function: {action_name}")

    def predict(self, task_instruction: str, obs: Dict = {}) -> Tuple[List[Dict], List[str]]:
        """
        Returns:
            response_list: A list of dictionaries containing metadata (thought, action string, coords, etc.)
            action_list: A list of executable PyAutoGUI command strings.
        """
        
        # 处理截图
        base64_screenshot = None
        if obs and "screenshot" in obs:
            screenshot_bytes = obs["screenshot"]
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes)) 
            new_width, new_height = 1920, 1080
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format='PNG')
            resized_obs_bytes = output_buffer.getvalue()
            base64_screenshot = self._encode_image_to_base64(resized_obs_bytes)

        # 处理上一轮的 Tool Calls 结果
        if self.pending_tool_calls:
            for tool_call in self.pending_tool_calls:
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": "Screenshot updated."
                })
            
            if base64_screenshot:
                self.messages.append({
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": base64_screenshot}}
                    ]
                })
            
            self.pending_tool_calls = []
            self._cleanup_old_screenshots()

        # 处理初始状态
        if len(self.messages) == 1: 
            content_parts = [{"type": "text", "text": f"User Instruction: {task_instruction}"}]
            if base64_screenshot:
                content_parts.append({"type": "image_url", "image_url": {"url": base64_screenshot}})
            
            self.messages.append({
                "role": "user",
                "content": content_parts
            })

        try:
            response = self.get_model_response()
        except Exception as e:
            logger.error(f"Failed to get model response: {e}")
            return [], []

        choice = response.choices[0]
        logger.info(f'Choice[0] dump: {choice}.')
        
        message = choice.message
        message_dict = message.model_dump(exclude_none=True)
        # 将模型回复添加到历史
        self.messages.append(message_dict)

        reasoning = message_dict['reasoning_content'] if 'reasoning_content' in message_dict.keys() else "No thinking."
        logger.info(f'Reasoning content: {reasoning}')

        tool_calls = message.tool_calls
        if not tool_calls:
            # 如果没有工具调用，通常意味着结束
            return [
                {
                    "raw_response": reasoning,
                    "thought": reasoning,
                    "action": "done",
                    "coordinate": None,
                    "coordinate2": None,
                    "meta_action": {"type": "done"}
                }
            ], ["DONE"]

        response_metadata_list = []
        action_strs = []
        
        # 解析工具调用
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # --- 1. 计算绝对坐标 (用于 metadata 和 visualization) ---
            # 这里的坐标必须是绝对坐标 (PyAutoGUI 空间)
            coordinate = None

            if "x" in function_args and "y" in function_args:
                abs_x = self.denormalize_x(function_args["x"])
                abs_y = self.denormalize_y(function_args["y"])
                coordinate = [abs_x, abs_y]
                
                if "destination_x" in function_args and "destination_y" in function_args:
                    dest_x = self.denormalize_x(function_args["destination_x"])
                    dest_y = self.denormalize_y(function_args["destination_y"])
                    coordinate = [coordinate, [dest_x, dest_y]] # 起点, 终点
            
            # --- 2. 生成 Action String (用于 metadata 显示) ---
            action_display_str = f"{json.dumps({'name': function_name, 'arguments': function_args}, ensure_ascii=False)}"

            # --- 3. 生成 Meta Action (详细结构) ---
            meta_action = {
                "type": function_name,
                "arguments": function_args
            }

            # --- 4. 生成 PyAutoGUI Action (用于执行) ---
            try:
                py_action_str = self.handle_action(function_name, function_args)
                action_strs.append(py_action_str)
            except ValueError as e:
                logger.error(f"Error handling action {function_name}: {e}")
                continue # 跳过错误的 action

            # --- 5. 组装 Metadata ---
            # raw_response 包含 thought 和 action 的组合
            raw_response_text = f"{reasoning}\n{action_display_str}"
            
            metadata = {
                "raw_response": raw_response_text,
                "thought": reasoning,
                "action": action_display_str,
                "coordinate": coordinate,
                "meta_action": meta_action
            }

            response_metadata_list.append(metadata)

        # 挂起当前 Tool Calls
        self.pending_tool_calls = tool_calls
        
        return response_metadata_list, action_strs

    def _cleanup_old_screenshots(self):
        turns_with_screenshots = 0
        for i in range(len(self.messages) - 1, -1, -1):
            msg = self.messages[i]
            if msg.get("role") == "user" and isinstance(msg.get("content"), list):
                has_image = False
                for part in msg["content"]:
                    if isinstance(part, dict) and part.get("type") == "image_url":
                        has_image = True
                        break
                
                if has_image:
                    turns_with_screenshots += 1
                    if turns_with_screenshots > self.max_image_history_length:
                        new_content = [
                            p for p in msg["content"] 
                            if not (isinstance(p, dict) and p.get("type") == "image_url")
                        ]
                        if not new_content:
                            msg["content"] = "[Old Screenshot Removed]" 
                        else:
                            msg["content"] = new_content
                            
    def evaluate(self, task_instruction: str, obs: Dict) -> Dict[str, Any]:
        """
        Self-judge function.
        Returns a dictionary with 'thought' and 'score'.
        """
        eval_messages = copy.deepcopy(self.messages)
        
        # 替换 System Prompt
        if eval_messages and eval_messages[0].get("role") == "system":
            eval_messages[0]["content"] = EVALUATION_SYSTEM_PROMPT
        else:
            eval_messages.insert(0, {"role": "system", "content": EVALUATION_SYSTEM_PROMPT})

        # 闭合 Pending Tool Calls
        if self.pending_tool_calls:
            for tool_call in self.pending_tool_calls:
                eval_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": "Action executed. See final screenshot below."
                })

        # 处理截图
        base64_screenshot = None
        if obs and "screenshot" in obs:
            screenshot_bytes = obs["screenshot"]
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes)) 
            new_width, new_height = 1920, 1080
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format='PNG')
            resized_obs_bytes = output_buffer.getvalue()
            base64_screenshot = self._encode_image_to_base64(resized_obs_bytes)

        # 构建 Evaluation Query
        content_parts = []
        if base64_screenshot:
            content_parts.append({"type": "image_url", "image_url": {"url": base64_screenshot}})
        
        eval_query = f"The original user instruction was: '{task_instruction}'.\nBased on the conversation history and this final screenshot, provide your evaluation in JSON format."
        content_parts.append({"type": "text", "text": eval_query})

        eval_messages.append({
            "role": "user",
            "content": content_parts
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=eval_messages,
                temperature=0.1, 
                max_tokens=3268,
                response_format={"type": "json_object"} # 强制 JSON 输出
            )
            
            content = response.choices[0].message.content.strip()
            logger.info(f"Evaluation Result Raw Output: {content}")
            
            result = json.loads(content)
            
            # 确保包含必要的键
            if "score" not in result:
                result["score"] = 0
            if "thought" not in result:
                result["thought"] = "No thought provided."
                
            return result
                
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return {"thought": f"Evaluation failed due to error: {str(e)}", "score": 0}