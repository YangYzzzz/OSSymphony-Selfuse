import base64
import os
import time
from PIL import Image
import io
from typing import Literal, Optional, Union, Any, Dict, Tuple, List

from google import genai
from google.genai import types
import termcolor
from google.genai.types import (
    Part,
    GenerateContentConfig,
    Content,
    Blob,
    Candidate,
    FunctionResponse,
    FinishReason,
    FunctionResponseBlob,
    FunctionResponsePart
)
from rich.console import Console
from rich.table import Table
import pydantic
from datetime import datetime



class EnvState(pydantic.BaseModel):
    # The screenshot in PNG format.
    screenshot: bytes
    # 官方代码里是url，我们这里换为action
    action: str


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

#Exclude browser functions
EXCLUDED_PREDEFINED_FUNCTIONS = [
    "go_forward",
    "go_back",
    "navigate",
]

MAX_RECENT_TURN_WITH_SCREENSHOTS = 1


# 没找到gemini的system prompt，可能是不需要，先用claude的顶一下
# 在实际测试中发现，模型所返回的function不完全遵从官网给出的action space！并且excluded_predefined_functions也没有用，只能通过system_prompt约束。
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
* ALWAYS analyze the screenshot first! Your action should be stricly based on the current screenshot. Describe what you see on the reasoning process in detail:
    * List the title of the active window.
    * List 3 visible text labels or icons you can see.
    * If the current screen does not match what you need for the task, explicitly state 'I am not on the correct page' and use navigation tools to get there."
"""


import logging
logger = logging.getLogger("desktopenv.agent")

console = Console()

class GeminiAgent:
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
        top_p: float = 0,
    ):
        self.platform = platform
        self.verbose = True
        self.action_space = action_space
        self.model_name = model
        self.messages: list = []
        self.screen_size = screen_size
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                base_url=base_url, # 填写你的中转地址
                api_version="v1beta"                 # 可选，指定API版本
            )
        )
        self.contents: list[Content] = []
        self.generate_content_config = GenerateContentConfig(
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_tokens,
            tools=[
                types.Tool(
                    computer_use=types.ComputerUse(
                        environment=types.Environment.ENVIRONMENT_UNSPECIFIED,
                        excluded_predefined_functions=EXCLUDED_PREDEFINED_FUNCTIONS,
                    ),
                ),
                # types.Tool(function_declarations=custom_functions),
            ],
            thinking_config=types.ThinkingConfig(
                include_thoughts=True
            ),
            system_instruction=SYSTEM_PROMPT
        )
        self.pending_function_calls = []
    
    def reset(self):
        self.contents = []
        self.pending_function_calls = []
        logger.info("GeminiAgent reset.")

    def get_model_response(
        self, max_retries=5, base_delay_s=1
    ) -> types.GenerateContentResponse:
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=self.contents,
                    config=self.generate_content_config,
                )
                return response  # Return response on success
            except Exception as e:
                print(e)
                if attempt < max_retries - 1:
                    delay = base_delay_s * (2**attempt)
                    message = (
                        f"Generating content failed on attempt {attempt + 1}. "
                        f"Retrying in {delay} seconds...\n"
                    )
                    termcolor.cprint(
                        message,
                        color="yellow",
                    )
                    time.sleep(delay)
                else:
                    termcolor.cprint(
                        f"Generating content failed after {max_retries} attempts.\n",
                        color="red",
                    )
                    raise

    def get_text(self, candidate: Candidate) -> Optional[str]:
        """Extracts the text from the candidate."""
        if not candidate.content or not candidate.content.parts:
            return None
        text = []
        for part in candidate.content.parts:
            if part.text:
                text.append(part.text)
        return " ".join(text) or None
    
    def extract_function_calls(self, candidate: Candidate) -> list[types.FunctionCall]:
        """Extracts the function call from the candidate."""
        if not candidate.content or not candidate.content.parts:
            return []
        ret = []
        for part in candidate.content.parts:
            if part.function_call:
                ret.append(part.function_call)
        return ret

    def denormalize_x(self, x: int) -> int:
        return int(x / 1000 * self.screen_size[0])

    def denormalize_y(self, y: int) -> int:
        return int(y / 1000 * self.screen_size[1])

    def handle_action(self, action: types.FunctionCall) -> dict:
        """Handles the action and returns the environment state."""
        env_state = {}
        coordinates = []        # coordinates只是为了可视化模型的坐标操作
        if action.name == "open_web_browser":
            env_state['action'] = "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0)"
        
        elif action.name == "click_at":
            x = self.denormalize_x(action.args["x"])
            y = self.denormalize_y(action.args["y"])
            env_state['action'] = f"pyautogui.click(x={x}, y={y})"
            coordinates += [x, y]

        elif action.name == "hover_at":
            x = self.denormalize_x(action.args["x"])
            y = self.denormalize_y(action.args["y"])
            env_state['action'] = f"pyautogui.moveTo(x={x}, y={y})"
            coordinates += [x, y]

        elif action.name == "type_text_at":
            x = self.denormalize_x(action.args["x"])
            y = self.denormalize_y(action.args["y"])
            coordinates += [x, y]

            text = action.args["text"]
            press_enter = action.args.get("press_enter", False)
            clear_before_typing = action.args.get("clear_before_typing", True)
            env_state['action'] = f"pyautogui.click(x={x}, y={y}); "
            if clear_before_typing:
                env_state['action'] += "time.sleep(0.1); pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace'); "

            env_state['action'] += f"pyautogui.write('{text}'); "

            if press_enter:
                env_state['action'] += "pyautogui.press('enter')"
        
        elif action.name == "scroll_document":
            # 滑动整个页面
            direction = action.args["direction"]
            amount = -self.screen_size[1] if direction == "down" else self.screen_size[1]
            if direction in ["left", "right"]:
                env_state['action'] = f"pyautogui.hscroll({amount})"
            else:
                env_state['action'] = f"pyautogui.scroll({amount})"

        elif action.name == "scroll_at":
            # 滑动指定量级，magnitude也需要归一化
            x = self.denormalize_x(action.args["x"])
            y = self.denormalize_y(action.args["y"])
            coordinates += [x, y]

            magnitude = action.args.get("magnitude", 800)
            direction = action.args["direction"]
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
            
        elif action.name == "wait_5_seconds":
            env_state['action'] = "time.sleep(5)"
        
        # elif action.name == "go_back":
        #     # 浏览器专属动作, exclude
        #     pass
        # elif action.name == "go_forward":
        #     # 浏览器专属动作, exclude
        #     pass
        
        elif action.name == "search":
            # 同样也是浏览器专属动作，在computer use里和open_web_browser没啥区别，这里设计成打开浏览器之后切换到谷歌界面。
            env_state['action'] = "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0); "
            env_state['action'] += "pyautogui.hotkey('ctrl', 'l'); pyautogui.write('www.google.com'); pyautogui.press('enter')"
        elif action.name == "navigate":
            # 同样也是浏览器专属动作, 这里设计成打开浏览器之后切换到指定界面。
            url = action.args["url"]
            env_state['action'] = "pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write('chrome'); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0); "
            env_state['action'] += f"pyautogui.hotkey('ctrl', 'l'); pyautogui.write('{url}'); pyautogui.press('enter')"
        elif action.name == "key_combination":
            # 类似ctrl + c这样的动作
            keys = action.args["keys"].split("+")
            # 兼容处理：将 control 替换为 ctrl
            py_keys = [k.replace('control', 'ctrl') for k in keys]
            
            # 格式化列表为字符串参数
            keys_str = ", ".join([f"'{k}'" for k in py_keys])
            env_state['action'] = f"pyautogui.hotkey({keys_str})"

        elif action.name == "drag_and_drop":
            x = self.denormalize_x(action.args["x"])
            y = self.denormalize_y(action.args["y"])
            destination_x = self.denormalize_x(action.args["destination_x"])
            destination_y = self.denormalize_y(action.args["destination_y"])
            env_state['action'] = f"pyautogui.moveTo({x}, {y}); pyautogui.dragTo({destination_x}, {destination_y}, duration=0.5)"
            coordinates += [x, y, destination_x, destination_y]
        # Handle the custom function declarations here.
        # elif action.name == multiply_numbers.__name__:
        #     return multiply_numbers(x=action.args["x"], y=action.args["y"])
        else:
            raise ValueError(f"Unsupported function: {action}")

        return env_state, coordinates

    def predict(self, task_instruction: str, obs: Dict = {}) -> Tuple[str, List[str]]:

        # resize screenshot if resize_factor is set
        current_screenshot_blob = None
        if obs and "screenshot" in obs:
            # Convert bytes to PIL Image
            screenshot_bytes = obs["screenshot"]
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes)) 
            # Calculate new size based on resize factor
            new_width, new_height = 1920, 1080
            # Resize the image
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Convert back to bytes
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format='PNG')
            resized_obs = output_buffer.getvalue()
            # 试过了，图像就应该用bytes传入
            current_screenshot_blob = FunctionResponseBlob(
                mime_type="image/png", 
                data=resized_obs
            )

        # **添加上一轮工具调用的结果与当前截图**：如果有挂起的工具调用，说明上一轮模型执行了动作，而现在的 obs 就是那个动作的结果
        if hasattr(self, "pending_function_calls") and self.pending_function_calls:
            function_responses = []
            # 理论上应该只有一个function call
            for i, function_call in enumerate(self.pending_function_calls):
                # 获取对应的执行结果描述（如果有缓存的话，没有就给个默认值）
                # 注意：Gemini 要求 FunctionResponse 必须包含 name
                # 使用当前的 obs (最新的截图) 作为上一轮动作的视觉反馈
                parts = []
                if current_screenshot_blob:
                    parts.append(FunctionResponsePart(inline_data=current_screenshot_blob))
                
                function_responses.append(
                    FunctionResponse(
                        name=function_call.name,
                        # 这里 response 字典里的内容是给模型看的文本反馈
                        response={"output": "Screenshot updated."}, 
                        parts=parts
                    )
                )

            self.contents.append(
                Content(
                    role="user",
                    parts=[Part(function_response=fr) for fr in function_responses],
                )
            )
            # print(self.contents)
            # 清空挂起状态
            self.pending_function_calls = []
            self._cleanup_old_screenshots()

        
        if len(self.contents) == 0: 
            init_screenshot = resized_obs
            self.contents.append(
                Content(
                    role="user",
                    parts=[
                        Part(text=f"User Instruction: {task_instruction}"),
                        Part(
                            inline_data=Blob(
                                mime_type="image/png",
                                data=init_screenshot,
                            )
                        )
                    ],
                )
            )

        print("!!!!!!!!!!! Latest Content !!!!!!!!!!!")
        print(self.contents)
        try:
            response = self.get_model_response()
        except Exception as e:
            return "", []
        
        if not response.candidates:
            print("Response has no candidates!")
            print(response)
            raise ValueError("Empty response")
        
        # 解析response
        # Extract the text and function call from the response.
        candidate = response.candidates[0]
        # Append the model turn to conversation history.
        if candidate.content:
            self.contents.append(candidate.content)

        reasoning = self.get_text(candidate)
        function_calls = self.extract_function_calls(candidate)

        # Retry the request in case of malformed FCs.
        if (
            not function_calls
            and not reasoning
            and candidate.finish_reason == FinishReason.MALFORMED_FUNCTION_CALL
        ):
            return "", []

        if not function_calls:
            print(f"Agent Loop Complete: {reasoning}")
            return "DONE", ["DONE"]

        function_call_strs = []
        for function_call in function_calls:
            # Print the function call and any reasoning.
            function_call_str = f"Name: {function_call.name}"
            if function_call.args:
                function_call_str += f"\nArgs:"
                for key, value in function_call.args.items():
                    function_call_str += f"\n  {key}: {value}"
            function_call_strs.append(function_call_str)
        
        # 可视化展示gemini的推理过程
        table = Table(expand=True)
        table.add_column(
            "Gemini Computer Use Reasoning", header_style="magenta", ratio=1
        )
        table.add_column("Function Call(s)", header_style="cyan", ratio=1)
        table.add_row(reasoning, "\n".join(function_call_strs))
        if self.verbose:
            console.print(table)
            print()

        # 解析工具 --> pyautogui代码
        action_strs = []
        coordinates = []
        for function_call in function_calls:
            # gemini的返回会包含安全检查，我们不需要这步
            # if function_call.args and (
            #     safety := function_call.args.get("safety_decision")
            # ):
            #     decision = self._get_safety_confirmation(safety)
            #     if decision == "TERMINATE":
            #         print("Terminating agent loop")
            #         return "COMPLETE"
            #     # Explicitly mark the safety check as acknowledged.
            #     extra_fr_fields["safety_acknowledgement"] = "true"
            

            fc_result, coordinates = self.handle_action(function_call)

            if fc_result and 'action' in fc_result:
                action_strs.append(fc_result['action'])
            else:
                raise ValueError(f'Unsupported function result format: {fc_result}')
        
        self.pending_function_calls = function_calls
        
        final_response = {
            "reasoning": reasoning,
            "coordinates": coordinates
        }
        return final_response, action_strs

    def _cleanup_old_screenshots(self):
        """把原有的清理逻辑封装成辅助函数，代码更整洁"""
        # 清理上下文，保留最近 K 轮图片
        # only keep screenshots in the few most recent turns, remove the screenshot images from the old turns.
        turn_with_screenshots_found = 0
        for content in reversed(self.contents):
            if content.role == "user" and content.parts:
                has_screenshot = False
                for part in content.parts:
                    if (
                        part.function_response
                        and part.function_response.parts
                        and part.function_response.name
                        in PREDEFINED_COMPUTER_USE_FUNCTIONS # 确保这个列表包含你所有的工具名
                    ):
                        has_screenshot = True
                        break

                if has_screenshot:
                    turn_with_screenshots_found += 1
                    if turn_with_screenshots_found > MAX_RECENT_TURN_WITH_SCREENSHOTS:
                        for part in content.parts:
                            if (
                                part.function_response
                                and part.function_response.parts
                                and part.function_response.name in PREDEFINED_COMPUTER_USE_FUNCTIONS
                            ):
                                print(part.function_response.name)
                                part.function_response.parts = None

    