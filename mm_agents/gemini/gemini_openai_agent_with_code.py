import base64
import copy
import os
from pathlib import Path
import time
from PIL import Image
import io
import json
from typing import Optional, Any, Dict, Tuple, List

from openai import OpenAI
from datetime import datetime
import logging

from mm_agents.utils.call_api_log import log_openai_api_call
from mm_agents.anthropic.utils import SYSTEM_PROMPT_ORM, SYSTEM_PROMPT_WITH_CODE as SYSTEM_PROMPT
from .utils import BROWSER_TO_DESKTOP_SCROLL_RATIO, build_qwen_sft_sample_for_gemini

logger = logging.getLogger("desktopenv.agent")
PREDEFINED_COMPUTER_USE_FUNCTIONS = [
    "click_at",
    "hover_at",
    "type_text_at",
    "scroll_document",
    "scroll_at",
    "wait_5_seconds",
    "key_combination",
    "drag_and_drop",
    "code",
]

# OpenAI 需要明确的 Tool Schema 定义
TOOLS_SCHEMA = [
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
    },
    {
        "type": "function",
        "function": {
            "name": "code",
            "description": "Generate higher-level automation code (Python or Bash).",
            "parameters": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "enum": ["python", "bash"],
                    },
                    "execute_code": {
                        "type": "string",
                        "description": "Complete code to execute as a script.",
                    },
                    "thought": {
                        "type": "string",
                        "description": "Explain reasoning BEFORE writing this code.",
                    },
                },
                "required": ["language", "execute_code", "thought"],
            },
        },
    },
]

class GeminiOpenAIAgentWithCode:
    def __init__(
        self,
        platform: str = "Ubuntu",
        verbose: bool = True,
        model: str = "gemini-3-flash-preview",
        max_tokens: int = 4096,
        api_key: str = "",
        base_url: str = "",
        screen_size: tuple[int, int] = (1920, 1080),
        temperature: float = 0.1,
        top_p: float = 0.95,
        max_image_history_length: int = 8,
        collect_qwen_sft: bool = False,
        collect_qwen_sft_image_dir: str = "qwen3vl_sft_dataset/image",
    ):
        self.platform = platform
        self.verbose = verbose
        self.model = model
        self.messages: list = []
        self.screen_size = screen_size

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url if base_url else None,
        )

        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.max_image_history_length = max_image_history_length

        self.messages.append({"role": "system", "content": SYSTEM_PROMPT})
        self.pending_tool_calls = []
        self.last_code_result: Optional[str] = None

        # Qwen3VL SFT
        self.collect_qwen_sft = collect_qwen_sft
        self.qwen_sft_image_hash_map: dict[str, str] = {}
        self.collect_qwen_sft_image_dir = Path(collect_qwen_sft_image_dir)

    def reset(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.pending_tool_calls = []
        self.last_code_result = None
        logger.info("GeminiOpenAIAgentWithCode reset.")

    def _encode_image_to_base64(self, image_bytes: bytes, mime_type: str = "image/png") -> str:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{base64_image}"

    def _denormalize_x(self, x: int) -> int:
        return int(x / 1000 * self.screen_size[0])

    def _denormalize_y(self, y: int) -> int:
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
            magnitude = magnitude // BROWSER_TO_DESKTOP_SCROLL_RATIO # Browser -> Desktop
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

    def get_model_response(self, max_retries=5, base_delay_s=1):
        for attempt in range(max_retries):
            start = time.time()
            response = None
            error_msg = None
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    max_tokens=self.max_tokens,
                    tools=TOOLS_SCHEMA, # TODO: Check
                    tool_choice="auto",
                    extra_body={
                        "thinking_config": {
                            "include_thoughts": True
                        },
                        # "chat_template_kwargs": {"enable_thinking": True} # 这个flag对gemini不管用
                    },
                )
                duration_ms = (time.time() - start) * 1000.0
                try:
                    log_openai_api_call(
                        model_name=self.model,
                        request_messages=self.messages,
                        response=response,
                        duration_ms=duration_ms,
                        success=True,
                        error=None,
                    )
                except Exception as log_e:
                    logger.warning(f"logging openai/gemini api call failed: {log_e}")
                return response
            except Exception as e:
                duration_ms = (time.time() - start) * 1000.0
                error_msg = str(e)
                try:
                    log_openai_api_call(
                        model_name=self.model,
                        request_messages=self.messages,
                        response=response,
                        duration_ms=duration_ms,
                        success=False,
                        error=error_msg,
                    )
                except Exception as log_e:
                    logger.warning(f"logging openai/gemini api call failed: {log_e}")
                if attempt < max_retries - 1:
                    delay = base_delay_s * (2 ** attempt)
                    time.sleep(delay)
                else:
                    raise
    
    def denormalize_x(self, x: int) -> int:
        return int(x / 1000 * self.screen_size[0])

    def denormalize_y(self, y: int) -> int:
        return int(y / 1000 * self.screen_size[1])
    
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
                            p
                            for p in msg["content"]
                            if not (isinstance(p, dict) and p.get("type") == "image_url")
                        ]
                        if not new_content:
                            msg["content"] = "[Old Screenshot Removed]"
                        else:
                            msg["content"] = new_content

    def predict(self, task_instruction: str, obs: Dict = None) -> Tuple[List[Dict], List[str]]:
        obs = obs or {}

        # screenshot -> image_url
        base64_screenshot = None
        if obs.get("screenshot"):
            screenshot_bytes = obs["screenshot"]
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes))
            new_width, new_height = 1920, 1080
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format="PNG")
            resized_obs_bytes = output_buffer.getvalue()
            base64_screenshot = self._encode_image_to_base64(resized_obs_bytes)

        # feed tool result for previous tool_calls
        if self.pending_tool_calls:
            for tool_call in self.pending_tool_calls:
                name = tool_call.function.name
                if name == "code" and self.last_code_result is not None:
                    result_text = self.last_code_result
                    self.last_code_result = None
                else:
                    result_text = "Success"
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_text
                    }
                )

            if base64_screenshot:
                self.messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": base64_screenshot},
                            }
                        ],
                    }
                )

            self.pending_tool_calls = []
            self._cleanup_old_screenshots()

        # initial user turn
        if len(self.messages) == 1:
            content_parts = [{"type": "text", "text": f"User Instruction: {task_instruction}"}]
            if base64_screenshot:
                content_parts.append(
                    {"type": "image_url", "image_url": {"url": base64_screenshot}}
                )
            self.messages.append({"role": "user", "content": content_parts})

        try:
            response = self.get_model_response()
        except Exception as e:
            logger.error(f"Failed to get model response: {e}")
            return [], []

        choice = response.choices[0]
        message = choice.message
        message_dict = message.model_dump(exclude_none=True)
        # logger.info(f'Gemini Message Dict: {message_dict}')
        self.messages.append(message_dict)

        reasoning = message_dict.get("reasoning_content", "") + message_dict.get("content", "")

        tool_calls = message.tool_calls or []
        response_meta_list: List[Dict[str, Any]] = []
        action_strs: List[str] = []
        screenshot_flag = False

        all_action_display_str = ""
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # 从参数中提取 thought，拼接到 reasoning 里用于 SFT
            extracted_thought = function_args.pop("thought", "[No Thought Provided]")
            if not reasoning:
                reasoning = extracted_thought
            else:
                # reasoning 为单纯的叠加，对于蒸馏不利
                reasoning += f"\n{extracted_thought}"
            logger.info(f'Response Reasoning: {reasoning}')

            # --- 1. 计算绝对坐标 (用于 metadata 和 visualization) ---
            coordinate = None
            if "\"x\"" in function_args:
                function_args["x"] = function_args["\"x\""]
                del function_args["\"x\""]
            if "\"y\"" in function_args:
                function_args["y"] = function_args["\"y\""]
                del function_args["\"y\""]

            if "x" in function_args and "y" in function_args:
                abs_x = self.denormalize_x(function_args["x"])
                abs_y = self.denormalize_y(function_args["y"])
                coordinate = [abs_x, abs_y]

                if "destination_x" in function_args and "destination_y" in function_args:
                    dest_x = self.denormalize_x(function_args["destination_x"])
                    dest_y = self.denormalize_y(function_args["destination_y"])
                    coordinate = [coordinate, [dest_x, dest_y]]  # 起点, 终点

            # --- 2. 生成 Action String (用于 metadata 展示) ---
            action_display_str = f"{json.dumps({'name': function_name, 'arguments': function_args}, ensure_ascii=False)}"
            all_action_display_str += action_display_str+"\n"
            # --- 3. 生成 Meta Action (详细结构) ---
            meta_action = {
                "type": function_name,
                "arguments": function_args
            }

            # --- 4. 生成 PyAutoGUI Action (用于执行) ---
            try:
                if function_name == "code":
                    # code 工具：不转成 pyautogui，直接把代码原样返回
                    lang = (function_args.get("language") or "python").lower()
                    code_str = function_args.get("execute_code") or ""
                    # 区分 python / bash，方便外层执行
                    if lang == "bash":
                        action_str = f"BASH|{code_str}"
                    else:
                        action_str = f"PYTHON|{code_str}"
                else:
                    action_str = self.handle_action(function_name, function_args)

                action_strs.append(action_str)
            except ValueError as e:
                logger.error(f"Error handling action {function_name}: {e}")
                continue  # 跳过错误的 action

            # --- 5. 组装 Metadata ---
            # 每一个tool_call的raw_response_text,thought,action均不同
            raw_response_text = f"{reasoning}\n{all_action_display_str}"

            metadata = {
                "raw_response": raw_response_text,
                "thought": reasoning,
                "action": action_display_str,
                "coordinate": coordinate,
                "meta_action": meta_action
            }

            response_meta_list.append(metadata)

        self.pending_tool_calls = tool_calls


        if not tool_calls:
            if "[INFEASIBLE]" in reasoning:
                response_meta_list = [
                    {
                        "raw_response": reasoning,
                        "thought": reasoning,
                        "action": "FAIL",
                        "coordinate": None,
                        "meta_action": {"type": "fail"},
                    }
                ]
                action_strs = ["FAIL"]
            else:
                response_meta_list = [
                    {
                        "raw_response": reasoning,
                        "thought": reasoning,
                        "action": "DONE",
                        "coordinate": None,
                        "meta_action": {"type": "done"},
                    }
                ]
                action_strs = ["DONE"]

        # 对于 Gemini, 重写最后一条 messages 的content内容
        self.messages[-1]["content"] = reasoning

        # Qwen3VL SFT collection (no screenshot action in this step)
        if self.collect_qwen_sft and not screenshot_flag and response_meta_list:
            try:
                sample, self.qwen_sft_image_hash_map = build_qwen_sft_sample_for_gemini(
                    messages=self.messages, # 都是 0~1000 归一化
                    image_hash_map=self.qwen_sft_image_hash_map,
                    image_root_dir=self.collect_qwen_sft_image_dir,
                )
                response_meta_list[0]["agent_sft"] = sample
            except Exception as e:
                logger.error(f"build_qwen_sft_sample_for_gemini error: {e}")

        return response_meta_list, action_strs

    def evaluate(self, task_instruction: str, obs: Dict) -> Dict[str, Any]:
        eval_messages = copy.deepcopy(self.messages)

        if eval_messages and eval_messages[0].get("role") == "system":
            eval_messages[0]["content"] = SYSTEM_PROMPT_ORM
        else:
            eval_messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT_ORM})

        if self.pending_tool_calls:
            for tool_call in self.pending_tool_calls:
                eval_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": "Action executed. See final screenshot below.",
                    }
                )

        base64_screenshot = None
        if obs and obs.get("screenshot"):
            screenshot_bytes = obs["screenshot"]
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes))
            new_width, new_height = 1920, 1080
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format="PNG")
            resized_obs_bytes = output_buffer.getvalue()
            base64_screenshot = self._encode_image_to_base64(resized_obs_bytes)

        content_parts = []
        if base64_screenshot:
            content_parts.append({"type": "image_url", "image_url": {"url": base64_screenshot}})
        eval_query = (
            f"The original user instruction was: '{task_instruction}'.\n"
            "Based on the conversation history and this final screenshot, provide your evaluation in JSON format."
        )
        content_parts.append({"type": "text", "text": eval_query})

        eval_messages.append({"role": "user", "content": content_parts})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=eval_messages,
                temperature=0.1,
                max_tokens=1024,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content.strip()
            logger.info(f"Evaluation Result Raw Output: {content}")

            result = json.loads(content)
            if "score" not in result:
                result["score"] = 0
            if "thought" not in result:
                result["thought"] = "No thought provided."
            return result
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return {"thought": f"Evaluation failed due to error: {str(e)}", "score": 0}
