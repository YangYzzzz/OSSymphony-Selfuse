import base64
import json
import logging
import textwrap
import time
from io import BytesIO
from typing import Dict, List, Tuple, Any, Optional
import httpx
import backoff
import openai
from openai import OpenAI
from PIL import Image
from requests.exceptions import SSLError

from mm_agents.utils.qwen_vl_utils import (
    QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_INFERENCE,
    QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_INFERENCE_WITHOUT_CODE,
    smart_resize,
    QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
    QWEN3VL_COMPUTER_USE_TOOL_SCHEMA_WITHOUT_CODE,
    QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN,
)
from mm_agents.base import ComputerUseBaseAgent
from mm_agents.anthropic.utils import SYSTEM_PROMPT_ORM


logger = logging.getLogger("desktopenv.agent")

MAX_RETRY_TIMES = 5
EMPTY_TOOL_CALL_RETRY_TIMES = 3


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
        max_trajectory_length: int = 8,
        add_thought_prefix: bool = False,
        coordinate_type: str = "relative",
        keep_first_image: bool = True,
        use_thinking: bool = False,
        enable_code_tool: bool = True
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
        self.max_trajectory_length = max_trajectory_length
        self.keep_first_image = keep_first_image
        self.add_thought_prefix = add_thought_prefix
        self.coordinate_type = coordinate_type
        self.use_thinking = use_thinking
        assert action_space in ["pyautogui"], "Invalid action space"
        assert observation_type in ["screenshot"], "Invalid observation type"


        # 为了执行 code 设置的变量
        self.last_code_result: Optional[str] = None
        self.code_results_history: List[str] = []

        # 统一维护对话历史（system + user + assistant + tool）
        # 直接沿用 OpenAI/vLLM 的 messages 协议结构
        self.system_prompt = QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_INFERENCE if enable_code_tool else QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_INFERENCE_WITHOUT_CODE
        self.messages: List[Dict[str, Any]] = []

        # 记录上一轮产生的 tool_calls，供下一轮填充 tool 结果
        self.pending_tool_calls: List[Any] = []

        self.enable_code_tool = enable_code_tool

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

        # feed tool result for previous tool_calls
        result_text = ""
        if self.pending_tool_calls:
            for tool_call in self.pending_tool_calls:
                try:
                    arguments = json.loads(tool_call["function"]["arguments"]) # vllm
                    name = arguments["action"]
                except json.JSONDecodeError as e:
                    print(f"解析 JSON 失败: {e}")
                    name = ""
                if name == "code" and self.last_code_result is not None:
                    result_text = f"Code Execution Result:\n```\n{self.last_code_result}\n```"
                    self.last_code_result = None
                elif name == "":
                    result_text = "Fail to parse tool! The output on previous step is NOT a valid JSON object"
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
        self._cleanup_old_screenshots()

        # 让 call_llm 返回原始 message 对象（包含 message.tool_calls 和结构化 content）
        # 如果解析不出来工具就重试
        response_message = self._call_llm_with_tool_call_retry(
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
        self.messages.append(response_message)

        # 记录本轮产生的 tool_calls，供下一轮填充 tool 结果
        tool_calls = response_message.get("tool_calls") or []
        self.pending_tool_calls = list(tool_calls)

        # 把工具调用转成我们现有的 meta_data / pyautogui_code
        # 这里不再依赖字符串匹配，response_str 只作为 thought 文本
        content = response_message.get("content", "") # 解析除 <tool_call></tool_call> block
        reasoning_content = response_message.get("reasoning_content", "") # 解析 <think></think> block
        response_str = (("<think>" + reasoning_content + "</think>") if reasoning_content else "") + content

        meta_data, pyautogui_code = self.parse_response(
            response_message,
            response_str,
            width,
            height,
            processed_width,
            processed_height,
        )

        if not pyautogui_code:
            # print('解析失败!!!!!!!')
            # print("tool_calls:", tool_calls)
            # print("原始内容:", response_message)
            print("tool call 为空!!!")
            fail_action = {
                "name": "done",
                "command": "DONE",
                "action_type": "DONE",
            }
            meta_data = [{
                "raw_response": f"No tool call\n {response_message}",
                "thought": "Completed",
                "action": "DONE",
                "meta_action": fail_action,
                "coordinate": None,
            }]
            pyautogui_code = ["DONE"]

        logger.info(f"Pyautogui code: {pyautogui_code}")
        # self.debug_print_messages()

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
        remaining = self.max_trajectory_length
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

    def parse_response(
        self,
        response_message: Dict[str, Any],
        thought: str,
        original_width: int = None,
        original_height: int = None,
        processed_width: int = None,
        processed_height: int = None,
    ) -> Tuple[List[Dict], List[str]]:
        """Parse LLM response (dict with tool_calls) and convert it to metadata and pyautogui code.

        - thought: 来自 message.content 提取的自然语言思考文本
        - response_message: 完整的 message dict，包含 tool_calls
        """

        pyautogui_code: List[str] = []
        meta_data: List[Dict] = []

        tool_calls = response_message.get("tool_calls") or []
        if not tool_calls:
            return meta_data, pyautogui_code

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

        def make_raw_response() -> str:
            """把 thought + tool_calls 转成原来的 raw_response 兼容格式.

            形如：
            <think>...</think>
            <tool>{...}</tool>
            <tool>{...}</tool>
            """

            parts: List[str] = []
            if thought:
                parts.append(f"{thought}")

            import json as _json

            for tc in tool_calls:
                # tc 可能是 pydantic 转成的 dict
                parts.append(f"<tool_call>{_json.dumps(tc, ensure_ascii=False)}</tool_call>")

            return "\n".join(parts)

        raw_response = make_raw_response()

        def make_meta(action_dict: Dict[str, Any], coordinate: Optional[List[Any]] = None) -> Dict:
            return {
                "raw_response": raw_response,
                "thought": thought,
                "action": action_dict.get("command", ""),
                "meta_action": action_dict,
                "coordinate": coordinate,
            }

        for tool_call in tool_calls:
            try:
                args = tool_call.get("function", {}).get("arguments", "")
                args = json.loads(args)
            except Exception as e:
                logger.error("Invalid tool_call structure: %s", e)
                continue
            
            action = args.get("action")
            if not action:
                continue

            # 每个 tool_call 只生成一条长的 pyautogui 代码，保证与 meta_data 一一对应
            step_code: str = ""
            coord: Optional[List[Any]] = None

            if action == "left_click":
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.click({adj_x}, {adj_y})"
                else:
                    step_code = "pyautogui.click(0, 0)"

            elif action == "right_click":
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.rightClick({adj_x}, {adj_y})"
                else:
                    step_code = "pyautogui.rightClick(0, 0)"

            elif action == "middle_click":
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.middleClick({adj_x}, {adj_y})"
                else:
                    step_code = "pyautogui.middleClick(0, 0)"

            elif action == "double_click":
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.doubleClick({adj_x}, {adj_y})"
                else:
                    step_code = "pyautogui.doubleClick(0, 0)"
            
            elif action == "triple_click":
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.click({adj_x}, {adj_y}, clicks=3)"
                else:
                    step_code = "pyautogui.click(0, 0, clicks=3)"

            elif action == "type":
                text = args.get("text", "")
                step_code = f"pyautogui.write({repr(text)})"

            elif action == "key":
                keys = args.get("keys", [])
                if isinstance(keys, list):
                    cleaned_keys = []
                    for key in keys:
                        if isinstance(key, str):
                            key = key.strip()
                        cleaned_keys.append(key)
                    keys = cleaned_keys

                keys_str = ", ".join([f"'{key}'" for key in keys])
                if len(keys) > 1:
                    step_code = f"pyautogui.hotkey({keys_str})"
                elif len(keys) == 1:
                    step_code = f"pyautogui.press({keys_str})"

            elif action == "scroll":
                # Modify: Fix Coordinate
                pixels = args.get("pixels", 5) # 默认 5
                step_code = ""
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code += f"pyautogui.moveTo({adj_x}, {adj_y});"
                step_code += f"pyautogui.scroll({pixels})"

            elif action == "hscroll":
                pixels = args.get("pixels", 5) # 默认 5
                step_code = ""
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code += f"pyautogui.moveTo({adj_x}, {adj_y});"
                step_code = f"pyautogui.hscroll({pixels})"

            elif action == "wait":
                time = args.get("time", 5)
                step_code = f"time.sleep({time})"

            elif action == "terminate":
                status = args.get("status", "success") # success / failure
                step_code = "DONE" if status == "success" else "FAIL"

            elif action == "mouse_move":
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.moveTo({adj_x}, {adj_y})"
                else:
                    step_code = "pyautogui.moveTo(0, 0)"

            elif action == "left_click_drag":
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.dragTo({adj_x}, {adj_y}, duration=0.5)"
                else:
                    step_code = "pyautogui.dragTo(0, 0)"

            elif action == "code":
                code_content = args.get("execute_code", "")
                language = args.get("language", "python")
                step_code = f"{language.upper()}|{code_content}"

            # 汇总本次 tool_call 的全部指令为一条长代码，使用 '; ' 连接
            if not step_code:
                continue

            meta_action = {
                "name": action,
                "input": args,
                "id": tool_call.get("id", ""),
                "action_type": tool_call.get("type", "tool_call"),
                "command": step_code,
                "coordinate": coord
            }

            pyautogui_code.append(step_code)
            meta_data.append(make_meta(meta_action, coord))

        return meta_data, pyautogui_code

    def evaluate(self, task_instruction: str, obs: Dict, **kwargs) -> Dict[str, Any]:
        """Self-judge function.

        Returns a dictionary with 'thought' and 'score'.
        """
        try:
            eval_prompt = SYSTEM_PROMPT_ORM
            hint = kwargs.get("hint", "")
            if hint:
                eval_prompt += f"\n\n[Hint]: The following are review guidelines. Please focus on checking these points: {hint}"

            eval_messages = self.messages

            if eval_messages and eval_messages[0].get("role") == "system":
                eval_messages[0]["content"] = [
                    {"type": "text", "text": eval_prompt}
                ]
            else:
                eval_messages.insert(0, {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": eval_prompt}
                    ],
                })

            if self.pending_tool_calls:
                for i, tool_call in enumerate(self.pending_tool_calls):
                    result_text = "Success"
                    try:
                        arguments = json.loads(tool_call["function"]["arguments"])
                        action = arguments.get("action")
                    except Exception:
                        action = None

                    if action == "code" and self.last_code_result is not None:
                        result_text = f"Code Execution Result:\n```\n{self.last_code_result}\n```"
                    elif i == len(self.pending_tool_calls) - 1:
                        result_text = "Action executed. See the final screenshot below."

                    eval_messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.get("id", "tool_call_0"),
                            "content": result_text,
                        }
                    )

            content_parts = []
            if obs and obs.get("screenshot"):
                processed_image = process_image(obs["screenshot"])
                content_parts.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{processed_image}"},
                    }
                )

            eval_query = (
                f"Based on the conversation history above and this final screenshot, did the agent successfully complete the instruction: '{task_instruction}'? Please provide the JSON evaluation."
            )
            content_parts.append({"type": "text", "text": eval_query})

            eval_messages.append({
                "role": "user",
                "content": content_parts,
            })

            logger.info(f"Starting evaluation for: {task_instruction}")

            response_message = self.call_llm_for_evaluate(
                {
                    "model": self.model,
                    "messages": eval_messages,
                    "max_tokens": self.max_tokens,
                    "top_p": self.top_p,
                    "temperature": self.temperature,
                },
                self.model,
            )

            reasoning_content = response_message.get("reasoning_content", "")
            content = response_message.get("content", "")
            raw_response_str = (("<think>" + reasoning_content + "</think>\n") if reasoning_content else "") + content
            raw_response_str = raw_response_str.strip()
            logger.info(f"Evaluation Raw Output: {raw_response_str}")

            if "```json" in raw_response_str:
                json_str = raw_response_str.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in raw_response_str:
                json_str = raw_response_str.split("```", 1)[1].split("```", 1)[0].strip()
            else:
                json_str = raw_response_str.strip()

            result = json.loads(json_str)

            if "thought" not in result:
                result["thought"] = raw_response_str
            if "score" not in result:
                result["score"] = 0.0

            return result
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return {
                "thought": f"Evaluation failed due to error: {str(e)}",
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
    def call_llm_for_evaluate(self, payload, model) -> dict:
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
                    max_tokens=payload.get("max_tokens", self.max_tokens),
                    temperature=payload.get("temperature", self.temperature),
                    top_p=payload.get("top_p", self.top_p),
                    extra_body={
                        "chat_template_kwargs": {"enable_thinking": self.use_thinking}
                    }
                )

                message_dict = response.choices[0].message.model_dump(exclude_none=True)
                return message_dict
            except Exception as e:
                logger.error(f"Error calling Qwen model for evaluate: {e}")
                time.sleep(5)
                continue
        return {}

    def _call_llm_with_tool_call_retry(self, payload: Dict[str, Any], model: str) -> Dict[str, Any]:                                             
        response_message = {}                 
                                                                                                                                                
        for attempt in range(EMPTY_TOOL_CALL_RETRY_TIMES):                                                                                       
            response_message = self.call_llm(payload, model)                                                                                     
            tool_calls = response_message.get("tool_calls") or []                                                                                
                                                                                                                                                
            if tool_calls:                                                                                                                       
                if attempt > 0:                                                                                                                  
                    logger.info(       
                        f"Received non-empty tool_calls after retry {attempt + 1}/{EMPTY_TOOL_CALL_RETRY_TIMES}"                                 
                    )                  
                return response_message                                                                                                          
                                        
            logger.warning(                                                                                                                      
                f"LLM response missing tool_calls on attempt {attempt + 1}/{EMPTY_TOOL_CALL_RETRY_TIMES}: {response_message}"
            )                                                                                                                                    
                                            
            if attempt < EMPTY_TOOL_CALL_RETRY_TIMES - 1:
                time.sleep(1)                                                                                                                    
                                        
        return response_message                     

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
    def call_llm(self, payload, model) -> dict:
        messages = payload["messages"]
        custom_headers = {
            "Authorization": "Basic NWFkMzQxMDBlZTA1NWE0YmFlNjYzNzBhNWU2ODNiYWM6NjA3ZGU4MjQ5NjU3YTNiM2JkMDM2ZGM5NmQ0YzBiMmY="
        }
        custom_timeout = httpx.Timeout(600.0, read=600.0, connect=60.0)

        if "kubebrain" in self.base_url:
            logger.info(f"H Cluster Local VLLM: {self.base_url}")
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                default_headers=custom_headers,
                timeout=custom_timeout,
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
                    tools=json.loads(QWEN3VL_COMPUTER_USE_TOOL_SCHEMA) if self.enable_code_tool else json.loads(QWEN3VL_COMPUTER_USE_TOOL_SCHEMA_WITHOUT_CODE),
                    tool_choice="auto", # required 的话只会输出 tool_call, auto 可以自由一点
                    extra_body={
                        "chat_template_kwargs": {"enable_thinking": self.use_thinking}
                    }
                )

                message_dict = response.choices[0].message.model_dump(exclude_none=True)
                return message_dict
            except Exception as e:
                logger.error(f"Error calling Qwen model: {e}")
                time.sleep(5)
                continue
        return {}

    def reset(self, _logger=None):
        global logger
        logger = _logger if _logger is not None else logging.getLogger("desktopenv.qwen3vl_agent")
        self.last_code_result = None
        self.messages = []
        self.pending_tool_calls = []

    def debug_print_messages(self):
        """优雅地打印 messages 列表，自动截断 Base64 图片以方便检查装填逻辑。"""
        print("\n" + "=" * 50 + " MESSAGES LOGIC DEBUG " + "=" * 50)

        if not self.messages:
            print(" [!] Messages list is empty.")
            print("=" * 122 + "\n")
            return

        for i, msg in enumerate(self.messages):
            role = msg.get("role", "UNKNOWN").upper()
            prefix = "👤" if role == "USER" else "🤖" if role == "ASSISTANT" else "⚙️" if role == "SYSTEM" else "🛠️" if role == "TOOL" else "❓" 

            print(f"\n{prefix} [{i}] ROLE: {role}")
            print("-" * 80)

            reasoning_content = msg.get("reasoning_content", "")
            content = msg.get("content", "")
            tool_calls = msg.get("tool_calls", [])

            if reasoning_content:
                print(f"  (Think) : {reasoning_content}")

            if isinstance(content, str):
                print(f"  (Text) : {content}")

            for _, tool_call in enumerate(tool_calls):
                print(f"  (Tool Call): {tool_call}")
            
            if isinstance(content, list):
                for _, item in enumerate(content):
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
