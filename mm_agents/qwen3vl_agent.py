import base64
import json
import logging
import time
import os
import re
from io import BytesIO
from typing import Dict, List, Tuple, Any, Optional

import backoff
import openai
from openai import OpenAI
from PIL import Image
from requests.exceptions import SSLError
# 假设这些工具函数在你的环境中可用，保持引用
from mm_agents.utils.qwen_vl_utils import smart_resize
from mm_agents.os_symphony.agents.critic_agent import CriticAgent
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


class Qwen3VLAgent(ComputerUseBaseAgent):

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
        critic_agent: CriticAgent|None = None, 
        critic_times = 1,
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

        self.critic_agent = critic_agent
        self.critic_times = critic_times if critic_agent else 1

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

        current_step = len(self.actions)
        history_start_idx = max(0, current_step - self.history_n)

        previous_actions = []
        for i in range(history_start_idx):
            if i < len(self.actions):
                previous_actions.append(f"Step {i+1}: {self.actions[i]}")
        # previous_actions_str = (
        #     "\n".join(previous_actions) if previous_actions else "None"
        # )

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
* `wait`: Wait specified seconds for the change to happen.
* `terminate`: Terminate the current task and report its completion status.
        """

        tools_def = {
            "type": "function", 
            "function": {
                "name_for_human": "computer_use", 
                "name": "computer_use", 
                "description": description_prompt,
                "parameters": {
                    "properties": {
                        "action": {
                            "description": action_description_prompt,
                            "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", 
                                     "right_click", "middle_click", "double_click", "scroll", "wait", "terminate"], 
                            "type": "string"
                        },
                        "keys": {"description": "Required only by `action=key`.", "type": "array"}, 
                        "text": {"description": "Required only by `action=type`.", "type": "string"}, 
                        "coordinate": {"description": "The x,y coordinates for mouse actions.", "type": "array"}, 
                        "pixels": {"description": "The amount of scrolling.", "type": "number"}, 
                        "time": {"description": "The seconds to wait.", "type": "number"}, 
                    }, 
                    "required": ["action"], 
                    "type": "object"
                }, 
                "args_format": "Format the arguments as a JSON object."
            }
        }

        system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
""" + json.dumps(tools_def) + """
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
- If finishing, use action=terminate in the tool call."""

        instruction_prompt = f"""
Please generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {instruction}
"""
        
        """ FIX: Modified by Yang
        Previous actions:
        {previous_actions_str}
        """
        messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt},
                ],
            }
        ]

        # History Construction
        history_len = min(self.history_n, len(self.responses))
        if history_len > 0:
            history_responses = self.responses[-history_len:]
            history_screenshots = self.screenshots[- history_len - 1:-1]

            for idx in range(history_len):
                if idx < len(history_screenshots):
                    screenshot_b64 = history_screenshots[idx]
                    img_url = f"data:image/png;base64,{screenshot_b64}"
                    content = [{"type": "image_url", "image_url": {"url": img_url}}]
                    if idx == 0:
                        content.append({"type": "text", "text": instruction_prompt})
                    messages.append({"role": "user", "content": content})

                messages.append(
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": f"{history_responses[idx]}"}],
                    }
                )

            curr_img_url = f"data:image/png;base64,{processed_image}"
            messages.append(
                {
                    "role": "user",
                    "content": [{"type": "image_url", "image_url": {"url": curr_img_url}}],
                }
            )
        else:
            curr_img_url = f"data:image/png;base64,{processed_image}"
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": curr_img_url}},
                        {"type": "text", "text": instruction_prompt},
                    ],
                }
            )

        # Critic Loop
        response_list = []
        pyautogui_code = []
        
        for _ in range(self.critic_times):
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

            # 调用新的解析函数
            response_list, pyautogui_code = self.parse_response(
                response,
                width,
                height,
                processed_width,
                processed_height,
            )

            if self.critic_agent is None:
                break
            
            # Critic Logic (Simplified for compatibility)
            # 提取用于 Critic 的 action string
            # action_str_list = [item["action"] for item in response_list if "action" in item]
            # cur_action_str = action_str_list[0] if action_str_list else "None"
            
            # history_action_str = ""
            # for action_idx, action in enumerate(self.critic_actions, start=1):
            #     history_action_str += f"Step: {action_idx}: {action}\n"

            # critic_result = self.critic_agent.critic(
            #     task=instruction, 
            #     screenshot=processed_image, 
            #     action=cur_action_str, 
            #     history=history_action_str
            # )
            
            # if critic_result:
            #     break
            # else:
            #     continue

        # Update History
        self.responses.append(response)
        
        # 记录简短的 action 描述用于 history prompt
        short_instruction = response_list[0]["thought"] if response_list else "Action"
        self.actions.append(short_instruction)
        
        # 记录用于 critic 的 action string
        action_str_list = [item["action"] for item in response_list if "action" in item]
        self.critic_actions.extend(action_str_list)

        return response_list, pyautogui_code

    def parse_response(
        self,
        response: str,
        original_width: int,
        original_height: int,
        processed_width: int,
        processed_height: int,
    ) -> Tuple[List[Dict], List[str]]:
        """
        Parse LLM response into structured metadata and executable code.
        """
        response_list = []
        pyautogui_code = []

        if not response or not response.strip():
            return [], []

        def adjust_coordinates(x: float, y: float) -> Tuple[int, int]:
            """Returns (pyautogui_x, pyautogui_y)"""
            if not (original_width and original_height):
                return int(x), int(y)
            
            if self.coordinate_type == "absolute":
                if processed_width and processed_height:
                    x_scale = original_width / processed_width
                    y_scale = original_height / processed_height
                    return int(x * x_scale), int(y * y_scale)
                return int(x), int(y)
            
            # relative (0-1000)
            return int(x * original_width / 999), int(y * original_height / 999)

        # 1. Extract Thought (Text outside tool calls)
        # 简单处理：取 <tool_call> 之前的所有文本作为 thought
        thought_match = re.split(r'<tool_call>', response)
        thought = thought_match[0].strip()
        
        # 2. Extract Tool Calls
        tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
        tool_calls = re.findall(tool_call_pattern, response, re.DOTALL)

        if not tool_calls:
            # No tool call found, treat as message/thought only
            response_list.append({
                "thought": thought,
                "action": "wait", # Default to wait if no action
                "action_type": "wait",
                "coordinate": None,
                "coordinate2": None,
                "raw_response": response,
                "meta_action": None
            })
            pyautogui_code.append("pyautogui.sleep(1)") 
            return response_list, pyautogui_code

        for tool_call_str in tool_calls:
            try:
                tool_data = json.loads(tool_call_str)
                if tool_data.get("name") == "computer_use":
                    args = tool_data["arguments"]
                    action_type = args["action"]
                    
                    # Base structure for step_data
                    step_data = {
                        "thought": thought,
                        "action": tool_call_str,
                        "coordinate": None,
                        "coordinate2": None,
                        "raw_response": response,
                        "meta_action": tool_data # Store full args as meta
                    }

                    # --- Action Parsing & Code Generation ---
                    
                    # Coordinates Handling
                    coord = args.get("coordinate")
                    if coord:
                        adj_x, adj_y = adjust_coordinates(coord[0], coord[1])
                        step_data["coordinate"] = [adj_x, adj_y]

                    # Logic Mapping
                    if action_type in ["left_click", "right_click", "middle_click", "double_click"]:
                        py_method = {
                            "left_click": "click",
                            "right_click": "rightClick",
                            "middle_click": "middleClick",
                            "double_click": "doubleClick"
                        }[action_type]
                        
                        if coord:
                            pyautogui_code.append(f"pyautogui.{py_method}({adj_x}, {adj_y})")
                        else:
                            pyautogui_code.append(f"pyautogui.{py_method}()")

                    elif action_type == "mouse_move":
                        if coord:
                            pyautogui_code.append(f"pyautogui.moveTo({adj_x}, {adj_y})")
                        else:
                            pyautogui_code.append("pyautogui.moveTo(0, 0)")

                    elif action_type == "left_click_drag":
                        if coord:
                            duration = args.get("duration", 0.5)
                            pyautogui_code.append(f"pyautogui.dragTo({adj_x}, {adj_y}, duration={duration})")
                            # Note: drag usually implies a start point, but Qwen3VL tool def often just gives end point
                        else:
                            pyautogui_code.append("pyautogui.dragTo(0, 0)")

                    elif action_type == "type":
                        text = args.get("text", "")
                        # 创建一个临时列表来存放这一步的所有指令
                        type_code = ""

                        # 1. 判断 clear 参数：全选(Ctrl+A) 并 删除(Backspace)
                        if args.get("clear", 0) == 1:
                            type_code += "pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace');"

                        # 2. 输入文本
                        # 使用 repr(text) 可以自动处理文本中的引号转义问题，防止代码出错
                        type_code += f"pyautogui.write({repr(text)});"

                        # 3. 判断 enter 参数：按回车
                        if args.get("enter", 0) == 1:
                            type_code += "pyautogui.press('enter');"

                        pyautogui_code.append(type_code)

                    elif action_type == "key":
                        keys = args.get("keys", [])
                        # Clean keys logic (kept from original)
                        if isinstance(keys, list):
                            cleaned_keys = []
                            for key in keys:
                                if isinstance(key, str):
                                    key = key.replace("keys=[", "").replace("]", "").replace("'", "").replace('"', "").strip()
                                    cleaned_keys.append(key)
                                else:
                                    cleaned_keys.append(key)
                            keys = cleaned_keys
                        
                        keys_str = ", ".join([f"'{k}'" for k in keys])
                        if len(keys) > 1:
                            pyautogui_code.append(f"pyautogui.hotkey({keys_str})")
                        else:
                            pyautogui_code.append(f"pyautogui.press({keys_str})")

                    elif action_type == "scroll":
                        pixels = args.get("pixels", 0)
                        pyautogui_code.append(f"pyautogui.scroll({pixels})")

                    elif action_type == "wait":
                        pyautogui_code.append("pyautogui.sleep(1)")

                    elif action_type == "terminate":
                        pyautogui_code.append("DONE")
                        
                    response_list.append(step_data)

            except json.JSONDecodeError:
                logger.error(f"Failed to parse tool call JSON: {tool_call_str}")
                continue

        return response_list, pyautogui_code

    def evaluate(self, task_instruction: str, obs: Dict) -> Dict[str, Any]:
        """
        Self-judge function.
        Returns a dictionary with 'thought' and 'score'.
        """
        # 1. 定义评估专用的 System Prompt
        try:
            EVALUATION_SYSTEM_PROMPT = """
            You are an impartial judge evaluating the performance of a computer agent.
            Your task is to determine if the agent successfully completed the user's instruction based on the conversation history and the final screenshot.
            
            The user instruction was: "{instruction}"
            
            Analyze the sequence of actions taken by the agent and the final state of the screen.
            
            Output your evaluation strictly in the following JSON format:
            ```json
            {{
                "thought": "Detailed reasoning about why the task is considered success or failure...",
                "score": 1.0
            }}
            ```
            
            Set "score" to 1.0 if the task is successfully completed, and 0.0 if it failed.
            """
            
            # 2. 构建评估用的 Messages (类似于 predict 中的构建逻辑，但替换 System Prompt)
            messages: list[dict[str, Any]] = [
                {
                    "role": "system",
                    "content": EVALUATION_SYSTEM_PROMPT.format(instruction=task_instruction),
                }
            ]

            # 3. 回填历史信息 (Context)
            # Qwen3VL 需要上下文来判断之前的操作是否生效
            history_len = min(self.history_n, len(self.responses))
            if history_len > 0:
                history_responses = self.responses[-history_len:]
                history_screenshots = self.screenshots[-history_len - 1:-1]

                for idx in range(history_len):
                    if idx < len(history_screenshots):
                        screenshot_b64 = history_screenshots[idx]
                        img_url = f"data:image/png;base64,{screenshot_b64}"
                        
                        content = [{"type": "image_url", "image_url": {"url": img_url}}]
                        
                        # 第一帧通常包含初始指令，但在 Evaluate 中我们主要关注 Action 的执行流
                        if idx == 0:
                            content.append({"type": "text", "text": f"User Instruction: {task_instruction}"})
                        
                        messages.append({"role": "user", "content": content})

                    # 添加 Agent 的历史回复 (Action)
                    messages.append(
                        {
                            "role": "assistant",
                            "content": [{"type": "text", "text": f"{history_responses[idx]}"}],
                        }
                    )

            # 4. 处理当前(最终)截图
            base64_screenshot = None
            if obs and "screenshot" in obs:
                # 使用类内部统一的 process_image 逻辑，保持分辨率与 predict 一致
                base64_screenshot = process_image(obs["screenshot"])

            # 5. 构建最终的 Evaluation Query
            content_parts = []
            if base64_screenshot:
                content_parts.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_screenshot}"}})
            
            eval_query = f"Based on the conversation history above and this final screenshot, did the agent successfully complete the instruction: '{task_instruction}'? Please provide the JSON evaluation."
            content_parts.append({"type": "text", "text": eval_query})

            messages.append({
                "role": "user",
                "content": content_parts
            })
        except Exception as e:
            logger.info(f"What error: {e}")
            
        try:
            logger.info("Starting evaluation...")
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
            
            logger.info(f"Evaluation Result Raw Output: {response}")
            
            # 7. 解析 JSON
            # 即使使用了 json_object，模型有时仍会包裹在 ```json ... ``` 中
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].strip()

            result = json.loads(response)
            if "thought" not in result:
                result["thought"] = response # 如果解析不到 thought，将原始内容作为 thought
            if "score" not in result:
                result["score"] = 0
            return result
                
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            # 发生错误时返回默认失败结果
            return {
                "thought": f"Evaluation failed due to error: {str(e)}. Raw content: {response}",
                "score": 0.0
            }

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