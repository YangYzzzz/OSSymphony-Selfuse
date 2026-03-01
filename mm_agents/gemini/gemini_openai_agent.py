import base64
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

# 没找到gemini的system prompt，可能是不需要，先用claude的顶一下
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

# OpenAI 需要明确的 Tool Schema 定义，以此模拟 Gemini 的 ComputerUse
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "open_web_browser",
            "description": "Opens the web browser.",
            "parameters": {
                "type": "object", 
                "properties": {
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your step-by-step reasoning for why you are opening the browser BEFORE taking the action."}
                }, 
                "required": ["thought"]
            }
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your step-by-step reasoning for why you are clicking here BEFORE taking the action."},
                    "x": {"type": "integer", "description": "The x coordinate (0-1000)."},
                    "y": {"type": "integer", "description": "The y coordinate (0-1000)."}
                },
                "required": ["thought", "x", "y"]
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for hovering here BEFORE taking the action."},
                    "x": {"type": "integer", "description": "The x coordinate (0-1000)."},
                    "y": {"type": "integer", "description": "The y coordinate (0-1000)."}
                },
                "required": ["thought", "x", "y"]
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for typing this text here BEFORE taking the action."},
                    "x": {"type": "integer", "description": "The x coordinate (0-1000)."},
                    "y": {"type": "integer", "description": "The y coordinate (0-1000)."},
                    "text": {"type": "string", "description": "The text to type."},
                    "press_enter": {"type": "boolean", "description": "Whether to press enter after typing."},
                    "clear_before_typing": {"type": "boolean", "description": "Whether to clear the field before typing."}
                },
                "required": ["thought", "x", "y", "text"]
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for scrolling the document BEFORE taking the action."},
                    "direction": {"type": "string", "enum": ["up", "down", "left", "right"]}
                },
                "required": ["thought", "direction"]
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for scrolling at this location BEFORE taking the action."},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "direction": {"type": "string", "enum": ["up", "down", "left", "right"]},
                    "magnitude": {"type": "integer"}
                },
                "required": ["thought", "x", "y", "direction"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wait_5_seconds",
            "description": "Waits for 5 seconds.",
            "parameters": {
                "type": "object", 
                "properties": {
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for why you need to wait BEFORE taking the action."}
                }, 
                "required": ["thought"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Performs a Google search (Browser action).",
            "parameters": {
                "type": "object", 
                "properties": {
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for performing this search BEFORE taking the action."}
                }, 
                "required": ["thought"]
            }
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for navigating to this URL BEFORE taking the action."},
                    "url": {"type": "string"}
                },
                "required": ["thought", "url"]
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for using this key combination BEFORE taking the action."},
                    "keys": {"type": "string", "description": "Keys separated by +, e.g. ctrl+c"}
                },
                "required": ["thought", "keys"]
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
                    "thought": {"type": "string", "description": "IMPORTANT: Explain your reasoning for dragging and dropping BEFORE taking the action."},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "destination_x": {"type": "integer"},
                    "destination_y": {"type": "integer"}
                },
                "required": ["thought", "x", "y", "destination_x", "destination_y"]
            }
        }
    }
]

class GeminiOpenAIAgent: # 重命名类以反映底层变更，但功能不变
    def __init__(
        self,
        platform: str = "Ubuntu",
        verbose: bool = True,
        model: str = "gemini-3-flash-preview", # 默认模型更改为适合 OpenAI 的模型
        max_tokens: int = 4096,
        api_key: str = "",
        base_url: str = "",
        action_space: str = "pyautogui",
        screen_size: tuple[int, int] = (1920, 1080),
        temperature: float = 0.1,
        top_p: float = 0.95, # OpenAI 通常不设为0，给个低值
        max_image_history_length: int = 8,
    ):
        self.platform = platform
        self.verbose = verbose
        self.action_space = action_space
        self.model_name = model
        self.messages: list = [] # 存储 OpenAI 格式的消息字典
        self.screen_size = screen_size
        
        # 初始化 OpenAI Client
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url if base_url else None
        )
        
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.max_image_history_length = max_image_history_length

        # 保存 system prompt 到消息历史
        self.messages.append({"role": "system", "content": SYSTEM_PROMPT})
        
        # 存储待处理的 tool calls (OpenAI 格式对象)
        self.pending_tool_calls = []

    def reset(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.pending_tool_calls = []
        logger.info("OpenAIAgent reset.")

    def _encode_image_to_base64(self, image_bytes: bytes, mime_type: str = "image/png") -> str:
        """Helper to encode bytes to base64 data url for OpenAI."""
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:{mime_type};base64,{base64_image}"

    def get_model_response(
        self, max_retries=5, base_delay_s=1
    ):
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
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
                logger.info(f'LLM Output: {response}')
                return response
            except Exception as e:
                print(e)
                if attempt < max_retries - 1:
                    delay = base_delay_s * (2**attempt)
                    message = (
                        f"Generating content failed on attempt {attempt + 1}. "
                        f"Retrying in {delay} seconds...\n"
                    )
                    termcolor.cprint(message, color="yellow")
                    time.sleep(delay)
                else:
                    termcolor.cprint(
                        f"Generating content failed after {max_retries} attempts.\n",
                        color="red",
                    )
                    raise

    def denormalize_x(self, x: int) -> int:
        return int(x / 1000 * self.screen_size[0])

    def denormalize_y(self, y: int) -> int:
        return int(y / 1000 * self.screen_size[1])

    def handle_action(self, action_name: str, action_args: dict) -> Tuple[Dict, List]:
        """Handles the action and returns the environment state."""
        env_state = {}
        coordinates = []        
        
        if action_name == "open_web_browser":
            env_state['action'] = "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0)"
        
        elif action_name == "click_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            env_state['action'] = f"pyautogui.click(x={x}, y={y})"
            coordinates += [x, y]

        elif action_name == "hover_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            env_state['action'] = f"pyautogui.moveTo(x={x}, y={y})"
            coordinates += [x, y]

        elif action_name == "type_text_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            coordinates += [x, y]

            text = action_args["text"]
            press_enter = action_args.get("press_enter", False)
            clear_before_typing = action_args.get("clear_before_typing", True)
            env_state['action'] = f"pyautogui.click(x={x}, y={y}); "
            if clear_before_typing:
                env_state['action'] += "time.sleep(0.1); pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace'); "

            env_state['action'] += f"pyautogui.write('{text}'); "

            if press_enter:
                env_state['action'] += "pyautogui.press('enter')"
        
        elif action_name == "scroll_document":
            direction = action_args["direction"]
            amount = -self.screen_size[1] if direction == "down" else self.screen_size[1]
            if direction in ["left", "right"]:
                env_state['action'] = f"pyautogui.hscroll({amount})"
            else:
                env_state['action'] = f"pyautogui.scroll({amount})"

        elif action_name == "scroll_at":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            coordinates += [x, y]

            magnitude = action_args.get("magnitude", 800)
            direction = action_args["direction"]
            env_state['action'] = f"pyautogui.moveTo({x}, {y}); "

            if direction in ("up", "down"):
                magnitude = self.denormalize_y(magnitude)
                scroll_amount = magnitude if direction == "up" else -magnitude
                env_state['action'] = f"pyautogui.scroll({scroll_amount})"
            elif direction in ("left", "right"):
                magnitude = self.denormalize_x(magnitude)
                scroll_amount = magnitude if direction == "left" else -magnitude
                env_state['action'] = f"pyautogui.hscroll({scroll_amount})"
            else:
                raise ValueError("Unknown direction: ", direction)
            
        elif action_name == "wait_5_seconds":
            env_state['action'] = "time.sleep(5)"
        
        elif action_name == "search":
            env_state['action'] = "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0); "
            env_state['action'] += "pyautogui.hotkey('ctrl', 'l'); pyautogui.write('www.google.com'); pyautogui.press('enter')"
        
        elif action_name == "navigate":
            url = action_args["url"]
            env_state['action'] = "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0); "
            env_state['action'] += f"pyautogui.hotkey('ctrl', 'l'); pyautogui.write('{url}'); pyautogui.press('enter')"
        
        elif action_name == "key_combination":
            keys = action_args["keys"].split("+")
            py_keys = [k.replace('control', 'ctrl') for k in keys]
            keys_str = ", ".join([f"'{k}'" for k in py_keys])
            env_state['action'] = f"pyautogui.hotkey({keys_str})"

        elif action_name == "drag_and_drop":
            x = self.denormalize_x(action_args["x"])
            y = self.denormalize_y(action_args["y"])
            destination_x = self.denormalize_x(action_args["destination_x"])
            destination_y = self.denormalize_y(action_args["destination_y"])
            env_state['action'] = f"pyautogui.moveTo({x}, {y}); pyautogui.dragTo({destination_x}, {destination_y}, duration=0.5)"
            coordinates += [x, y, destination_x, destination_y]
        else:
            raise ValueError(f"Unsupported function: {action_name}")

        return env_state, coordinates

    def predict(self, task_instruction: str, obs: Dict = {}) -> Tuple[Dict, List[str]]:
        
        # 处理截图 (Resize Logic unchanged)
        base64_screenshot = None
        if obs and "screenshot" in obs:
            screenshot_bytes = obs["screenshot"]
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes)) 
            new_width, new_height = 1920, 1080
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format='PNG')
            resized_obs_bytes = output_buffer.getvalue()
            # 转为 OpenAI 可用的 base64 字符串
            base64_screenshot = self._encode_image_to_base64(resized_obs_bytes)

        # 处理上一轮的 Tool Calls 结果
        # 逻辑映射：Gemini 将 FunctionResponse + 图片放在同一轮。
        # OpenAI 的做法：先添加 role: tool 消息（ID对应），然后紧跟一条 role: user 消息放入新图片。
        if self.pending_tool_calls:
            # Step A: 确认 Tool Execution (Screenshot updated)
            for tool_call in self.pending_tool_calls:
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": "Screenshot updated."
                })
            
            # Step B: 将新截图作为 User Message 传入，让模型看到动作结果
            # 这模拟了 Gemini 中 FunctionResponse 包含 inline_data 的行为
            if base64_screenshot:
                self.messages.append({
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": base64_screenshot}}
                    ]
                })
            
            self.pending_tool_calls = []
            self._cleanup_old_screenshots()

        # 处理初始状态 (First Turn)
        # 如果除了 system prompt 还没有其他消息 (user/assistant)
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
            return {}, []

        choice = response.choices[0]
        message = choice.message

        # 将模型回复添加到历史
        self.messages.append(message.model_dump(exclude_none=True))

        # 应该是没有东西的
        reasoning = getattr(message, "reasoning_content", None)
            
        tool_calls = message.tool_calls

        # 如果没有内容也没有工具调用，可能是异常
        if not reasoning and not tool_calls:
            if choice.finish_reason == "length":
                 print("Error: Max tokens reached.")
            return {}, []

        if not tool_calls:
            print(f"Agent Loop Complete: {reasoning}")
            return {"reasoning": "DONW"}, ["DONE"]

        function_call_strs = []
        action_strs = []
        coordinates = []
        
        # 4. 解析工具调用 -> pyautogui
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # 从参数里把 thought 提取出来，当作 reasoning 显示
            extracted_thought = function_args.pop("thought", "[No Thought Provided]")
            if not reasoning: 
                reasoning = extracted_thought
            else:
                reasoning += f"\n{extracted_thought}"
            logger.info(f'Response Reasoning: {reasoning}')
            
            # Print logic
            function_call_str = f"Name: {function_name}"
            if function_args:
                function_call_str += f"\nArgs:"
                for key, value in function_args.items():
                    function_call_str += f"\n  {key}: {value}"
            function_call_strs.append(function_call_str)

            # Handle Action
            try:
                fc_result, fc_coords = self.handle_action(function_name, function_args)
                if fc_result and 'action' in fc_result:
                    action_strs.append(fc_result['action'])
                coordinates.extend(fc_coords)
            except ValueError as e:
                print(f"Error handling action: {e}")
        
        # 可视化
        table = Table(expand=True)
        table.add_column("OpenAI Computer Use Reasoning", header_style="magenta", ratio=1)
        table.add_column("Function Call(s)", header_style="cyan", ratio=1)
        table.add_row(reasoning if reasoning else "[No Text]", "\n".join(function_call_strs))
        if self.verbose:
            console.print(table)
            print()

        # 挂起当前 Tool Calls，等待下一轮提供截图反馈
        self.pending_tool_calls = tool_calls
        
        final_response = {
            "reasoning": reasoning,
            "coordinates": coordinates
        }
        return final_response, action_strs

    def _cleanup_old_screenshots(self):
        """
        清理旧截图以节省 Token。
        逻辑：保留最近 max_image_history_length 轮包含图片的 User 消息。
        """
        turns_with_screenshots = 0
        # 从后往前遍历
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
                    # 如果超过了保留数量，移除该图片部分
                    if turns_with_screenshots > self.max_image_history_length:
                        # 过滤掉 image_url 类型的 part
                        new_content = [
                            p for p in msg["content"] 
                            if not (isinstance(p, dict) and p.get("type") == "image_url")
                        ]
                        # 如果过滤后只剩空列表或纯文本，更新消息
                        # (为了保持对话连贯性，通常保留文本提示 "Screenshot updated" 或指令)
                        if not new_content:
                            # 如果原本只有图片，替换为占位符
                            msg["content"] = "[Old Screenshot Removed]" 
                        else:
                            msg["content"] = new_content
                        
                        # print(f"Cleaned up screenshot from message index {i}")