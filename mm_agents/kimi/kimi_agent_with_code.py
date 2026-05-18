import base64
import copy
from io import BytesIO
import json
import logging
import re
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image
import httpx
import backoff
import openai
from openai import OpenAI
from requests.exceptions import SSLError
import logging

logger = logging.getLogger("desktopenv.agent")
from mm_agents.anthropic.utils import SYSTEM_PROMPT_ORM
from mm_agents.utils.qwen_vl_utils import (
    KIMI_COMPUTER_USE_SYSTEM_PROMPT_FOR_OSWORLD_INFERENCE,
    QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_OSWORLD_INFERENCE,
    QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
)
from mm_agents.kimi.utils import build_qwen_sft_sample_for_kimi
from mm_agents.utils.call_api_log import log_openai_api_call

EMPTY_TOOL_CALL_RETRY_TIMES = 10
SUPPORTED_ACTIONS = {
    "left_click",
    "click",
    "right_click",
    "middle_click",
    "double_click",
    "triple_click",
    "type",
    "key",
    "scroll",
    "hscroll",
    "wait",
    "terminate",
    "mouse_move",
    "left_click_drag",
    "code",
}


def _clean_response_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return "\n".join(parts).strip()
    return ""


def _extract_tool_calls_from_content(content: str) -> tuple[list, str]:
    pattern = r"<tool_call>\s*(.*?)\s*</tool_call>"
    matches = re.findall(pattern, content, re.DOTALL)
    tool_calls = []

    for idx, match in enumerate(matches):
        try:
            parsed = json.loads(match)
        except json.JSONDecodeError:
            continue

        function_name = None
        function_arguments = None
        if isinstance(parsed, dict) and isinstance(parsed.get("function"), dict):
            function_name = parsed["function"].get("name")
            function_arguments = parsed["function"].get("arguments")
        elif isinstance(parsed, dict):
            function_name = parsed.get("name")
            function_arguments = parsed.get("arguments")

        if isinstance(function_arguments, dict):
            function_arguments = json.dumps(function_arguments, ensure_ascii=False)

        if function_name and isinstance(function_arguments, str):
            tool_calls.append(
                {
                    "id": parsed.get("id", f"fallback-tool-call-{idx}"),
                    "type": parsed.get("type", "function"),
                    "function": {
                        "name": function_name,
                        "arguments": function_arguments,
                    },
                }
            )

    clean_content = re.sub(pattern, "", content, flags=re.DOTALL)
    clean_content = re.sub(r"\n{3,}", "\n\n", clean_content).strip()
    return tool_calls, clean_content

def encode_image(image_content):
    return base64.b64encode(image_content).decode("utf-8")

class KimiAgentWithCode:
    def __init__(
        self,
        model: str,
        max_steps: int,
        max_image_history_length: int = 3,
        platform: str = "ubuntu",
        max_tokens: int = 4096,
        top_p: float = 0.95,
        temperature: float = 1,
        action_space: str = "pyautogui",
        observation_type: str = "screenshot",
        screen_size: Tuple[int, int] = (1920, 1080),
        coordinate_type: str = "relative",
        thinking: bool = False,
        base_url: str = "",
        api_key: str = "",
        keep_first_image: bool = True,
        collect_qwen_sft: bool = False,
        collect_qwen_sft_image_dir: str = "",
        **kwargs,
    ):
        assert coordinate_type in ["relative", "absolute", "qwen25"]
        assert action_space in ["pyautogui"], "Invalid action space"
        assert observation_type in ["screenshot"], "Invalid observation type"
        assert model is not None, "Model cannot be None"

        self.model = model
        self.platform = platform
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature
        self.action_space = action_space
        self.observation_type = observation_type
        self.coordinate_type = coordinate_type
        self.screen_size = screen_size
        self.max_image_history_length = max_image_history_length
        self.max_steps = max_steps
        self.thinking = thinking
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.keep_first_image = keep_first_image
        self.system_prompt = KIMI_COMPUTER_USE_SYSTEM_PROMPT_FOR_OSWORLD_INFERENCE

        self.messages: List[Dict[str, Any]] = []
        self.pending_tool_calls: List[Dict[str, Any]] = []
        self.last_code_result: Optional[str] = None

        self.collect_qwen_sft = collect_qwen_sft
        self.qwen_sft_image_hash_map: dict[str, str] = {}
        self.collect_qwen_sft_image_dir = Path(collect_qwen_sft_image_dir) if collect_qwen_sft_image_dir else Path("qwen3vl_sft_dataset/image")

    def reset(self):
        self.messages = []
        self.pending_tool_calls = []
        self.last_code_result = None
        self.qwen_sft_image_hash_map = {}

    def _scale_scroll_for_windows(self, code: str, factor: int = 50) -> str:
        if self.platform.lower() != "windows":
            return code
        pattern = re.compile(r"(pyautogui\.scroll\()\s*([-+]?\d+)\s*\)")
        return pattern.sub(lambda m: f"{m.group(1)}{int(m.group(2)) * factor})", code)

    def _cleanup_old_context(self):
        user_indices_with_img = []
        for idx, msg in enumerate(self.messages):
            if msg.get("role") != "user":
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            if any(isinstance(part, dict) and part.get("type") == "image_url" for part in content):
                user_indices_with_img.append(idx)

        if not user_indices_with_img:
            return

        keep_indices = set()
        if self.keep_first_image:
            first_idx = user_indices_with_img[0]
            keep_indices.add(first_idx)

        remaining = self.max_image_history_length
        for idx in reversed(user_indices_with_img):
            if idx in keep_indices:
                continue
            if remaining <= 0:
                break
            keep_indices.add(idx)
            remaining -= 1

        for idx in user_indices_with_img:
            if idx in keep_indices:
                continue
            msg = self.messages[idx]
            content = msg.get("content", [])
            new_content = []
            removed_image = False
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    removed_image = True
                    continue
                new_content.append(part)
            if removed_image:
                new_content.append({"type": "text", "text": "[Old Screenshot Removed]"})
            msg["content"] = new_content or [{"type": "text", "text": "[Old Screenshot Removed]"}]

    def _call_llm_with_tool_call_retry(self, payload: Dict[str, Any], model: str) -> Dict[str, Any]:
        def extract_supported_tool_calls(tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            valid_tool_calls = []
            for tool_call in tool_calls:
                try:
                    args = json.loads(tool_call.get("function", {}).get("arguments", ""))
                except Exception:
                    continue
                if args.get("action") in SUPPORTED_ACTIONS:
                    if args.get("coordinate") and isinstance(args.get("coordinate"), List) and len(args.get("coordinate")) == 2:
                        valid_tool_calls.append(tool_call)
                    else:
                        valid_tool_calls.append(tool_call)
            return valid_tool_calls

        response_message: Dict[str, Any] = {}
        for attempt in range(EMPTY_TOOL_CALL_RETRY_TIMES):
            response_message = self.call_llm(payload, model)
            tool_calls = response_message.get("tool_calls") or []
            valid_tool_calls = extract_supported_tool_calls(tool_calls)
            if valid_tool_calls:
                if len(valid_tool_calls) != len(tool_calls):
                    response_message = {**response_message, "tool_calls": valid_tool_calls}
                return response_message

            content = _clean_response_content(response_message.get("content", ""))
            if content:
                fallback_tool_calls, clean_content = _extract_tool_calls_from_content(content)
                valid_fallback_tool_calls = extract_supported_tool_calls(fallback_tool_calls)
                if valid_fallback_tool_calls:
                    response_message = {
                        **response_message,
                        "content": clean_content,
                        "tool_calls": valid_fallback_tool_calls,
                    }
                    return response_message

            logger.warning(
                f"Kimi response missing supported tool_calls on attempt {attempt + 1}/{EMPTY_TOOL_CALL_RETRY_TIMES}: {response_message}"
            )
            if attempt < EMPTY_TOOL_CALL_RETRY_TIMES - 1:
                time.sleep(1)

        return response_message

    def parse_response(
        self,
        response_message: Dict[str, Any],
        thought: str,
        original_width: int,
        original_height: int
    ) -> Tuple[List[Dict], List[str]]:
        tool_calls = response_message.get("tool_calls") or []
        if not tool_calls:
            return [], []

        def adjust_coordinates(x: float, y: float) -> Tuple[int, int]:
            # Important: Kimi 输出坐标有两种模式(同官方代码)
            # 1. 输出的是 0~1 的归一化后的小数
            if x<=1.0 and y<=1.0:
                return int(round(x * original_width)), int(round(y * original_height))
            # 2. 输出的是绝对坐标
            else:
                return int(round(x)), int(round(y))

        raw_response = "\n".join(
            [thought] + [f"<tool_call>{json.dumps(tc, ensure_ascii=False)}</tool_call>" for tc in tool_calls]
        ).strip()

        meta_data: List[Dict] = []
        pyautogui_code: List[str] = []

        for tool_call in tool_calls:
            try:
                args = json.loads(tool_call.get("function", {}).get("arguments", ""))
            except Exception as e:
                logger.error(f"Invalid tool_call structure: {e}")
                continue

            action = args.get("action")
            if not action:
                continue

            step_code = ""
            coord = None

            if action in ["left_click", "click"]:
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
                step_code = f"pyautogui.write({repr(args.get('text', ''))})"
            elif action == "key":
                keys = [key.strip() if isinstance(key, str) else key for key in args.get("keys", [])]
                keys_str = ", ".join([f"'{key}'" for key in keys])
                if len(keys) > 1:
                    step_code = f"pyautogui.hotkey({keys_str})"
                elif len(keys) == 1:
                    step_code = f"pyautogui.press({keys_str})"
            elif action == "scroll":
                pixels = args.get("pixels", 5)
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.moveTo({adj_x}, {adj_y});pyautogui.scroll({pixels})"
                else:
                    step_code = f"pyautogui.scroll({pixels})"
            elif action == "hscroll":
                pixels = args.get("pixels", 5)
                if "coordinate" in args:
                    x, y = args["coordinate"]
                    adj_x, adj_y = adjust_coordinates(x, y)
                    coord = [adj_x, adj_y]
                    step_code = f"pyautogui.moveTo({adj_x}, {adj_y});pyautogui.hscroll({pixels})"
                else:
                    step_code = f"pyautogui.hscroll({pixels})"
            elif action == "wait":
                step_code = f"time.sleep({args.get('time', 5)})"
            elif action == "terminate":
                step_code = "DONE" if args.get("status", "success") == "success" else "FAIL"
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
                language = (args.get("language") or "python").lower()
                execute_code = args.get("execute_code", "")
                step_code = f"{language.upper()}|{execute_code}"

            if not step_code:
                continue

            meta_action = {
                "name": action,
                "input": args,
                "id": tool_call.get("id", ""),
                "action_type": tool_call.get("type", "tool_call"),
                "command": step_code,
                "coordinate": coord,
            }
            pyautogui_code.append(step_code)
            meta_data.append(
                {
                    "raw_response": raw_response,
                    "thought": thought,
                    "action": step_code,
                    "meta_action": meta_action,
                    "coordinate": coord,
                }
            )

        return meta_data, pyautogui_code

    def predict(self, instruction: str, obs: Dict, **kwargs) -> Tuple[List[Dict], List[str]]:
        if "step_idx" in kwargs:
            logger.info(f"========= {self.model} Step {kwargs['step_idx']} =======")
        else:
            logger.info(f"========================== {self.model} ===================================")
        logger.info(f"Instruction: \n{instruction}")

        screenshot_bytes = obs["screenshot"]
        processed_image = encode_image(screenshot_bytes)

        if self.pending_tool_calls:
            for tool_call in self.pending_tool_calls:
                try:
                    arguments = json.loads(tool_call["function"]["arguments"])
                    name = arguments.get("action", "")
                except Exception:
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
            self.pending_tool_calls = []

        if not self.messages:
            instruction_prompt = (
                "Please generate the next move according to the UI screenshot, instruction and previous actions.\n\n"
                f"Instruction: {instruction}"
            )
            self.messages = [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": self.system_prompt}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{processed_image}"}},
                    ],
                },
            ]
        else:
            self.messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{processed_image}"}},
                    ],
                }
            )

        self._cleanup_old_context()

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

        logger.info(f"Kimi Output: {response_message}")
        self.messages.append(copy.deepcopy(response_message))

        self.pending_tool_calls = list(response_message.get("tool_calls") or [])
        content = _clean_response_content(response_message.get("content", ""))
        reasoning_content = response_message.get("reasoning_content", "")
        response_str = (("<think>" + reasoning_content + "</think>") if reasoning_content else "") + content

        meta_data, pyautogui_code = self.parse_response(
            response_message,
            response_str,
            self.screen_size[0],
            self.screen_size[1]
        )

        if not pyautogui_code:
            done_action = {
                "name": "done",
                "command": "DONE",
                "action_type": "DONE",
            }
            meta_data = [
                {
                    "raw_response": f"No tool call\n{response_message}",
                    "thought": response_str or "Completed",
                    "action": "DONE",
                    "meta_action": done_action,
                    "coordinate": None,
                }
            ]
            pyautogui_code = ["DONE"]

        pyautogui_code = [self._scale_scroll_for_windows(code) for code in pyautogui_code]

        if self.collect_qwen_sft and meta_data:
            try:
                sample, self.qwen_sft_image_hash_map = build_qwen_sft_sample_for_kimi(
                    messages=self.messages,
                    screen_size=self.screen_size,
                    image_hash_map=self.qwen_sft_image_hash_map,
                    image_root_dir=self.collect_qwen_sft_image_dir,
                )
                meta_data[0]["agent_sft"] = sample
            except Exception as e:
                logger.error(f"build_qwen_sft_sample error: {e}")

        return meta_data, pyautogui_code

    def evaluate(self, task_instruction: str, obs: Dict, **kwargs) -> Dict[str, Any]:
        try:
            eval_prompt = SYSTEM_PROMPT_ORM
            hint = kwargs.get("hint", "")
            if hint:
                eval_prompt += f"\n\n[Hint]: The following are review guidelines. Please focus on checking these points: {hint}"

            eval_messages = copy.deepcopy(self.messages)
            if eval_messages and eval_messages[0].get("role") == "system":
                eval_messages[0]["content"] = [{"type": "text", "text": eval_prompt}]
            else:
                eval_messages.insert(0, {"role": "system", "content": [{"type": "text", "text": eval_prompt}]})

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

            processed_image = encode_image(obs["screenshot"])
            eval_query = (
                f"Based on the conversation history above and this final screenshot, did the agent successfully complete the instruction: '{task_instruction}'? Please provide the JSON evaluation."
            )
            eval_messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{processed_image}"}},
                        {"type": "text", "text": eval_query},
                    ],
                }
            )

            response_message = self.call_llm(
                {
                    "model": self.model,
                    "messages": eval_messages,
                    "max_tokens": self.max_tokens,
                    "top_p": self.top_p,
                    "temperature": self.temperature,
                    "response_format": {"type": "json_object"},
                },
                self.model,
            )

            reasoning_content = response_message.get("reasoning_content", "")
            content = _clean_response_content(response_message.get("content", ""))
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
            logger.error(traceback.format_exc())
            return {"thought": f"Evaluation failed due to error: {str(e)}", "score": 0.0}

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
        custom_timeout = httpx.Timeout(600.0, read=600.0, connect=60.0)
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=custom_timeout,
        )

        request_payload = copy.deepcopy(payload)

        for _ in range(20):
            start = time.time()
            response = None
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=request_payload["messages"],
                    max_tokens=request_payload.get("max_tokens", self.max_tokens),
                    temperature=request_payload.get("temperature", self.temperature),
                    top_p=request_payload.get("top_p", self.top_p),
                    tools=json.loads(QWEN3VL_COMPUTER_USE_TOOL_SCHEMA),
                    tool_choice="auto",
                    extra_body={
                        "chat_template_kwargs": {"enable_thinking": self.thinking}
                    },
                )
                duration_ms = (time.time() - start) * 1000.0
                try:
                    log_openai_api_call(
                        model_name=model,
                        request_messages=request_payload["messages"],
                        response=response,
                        duration_ms=duration_ms,
                        success=True,
                        error=None,
                    )
                except Exception as log_e:
                    logger.warning(f"logging kimi api call failed: {log_e}")
                return response.choices[0].message.model_dump(exclude_none=True)
            except Exception as e:
                duration_ms = (time.time() - start) * 1000.0
                error_msg = str(e)
                try:
                    log_openai_api_call(
                        model_name=model,
                        request_messages=request_payload["messages"],
                        response=response,
                        duration_ms=duration_ms,
                        success=False,
                        error=error_msg,
                    )
                except Exception as log_e:
                    logger.warning(f"logging kimi api call failed: {log_e}")
                logger.error(f"Error calling Kimi model: {e}")
                time.sleep(5)
                continue

        return {}
