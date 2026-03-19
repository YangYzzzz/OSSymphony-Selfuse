import base64
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from openai import OpenAI


logger = logging.getLogger("desktopenv.agent")

LOG_DIR = Path("logs/gpt_api_logs")

OPERATOR_PROMPT = """

Here are some helpful tips:
- You are operating an {PLATFORM} desktop with internet access.
- My computer password is "{CLIENT_PASSWORD}" when sudo is needed.
- The current date is {CURRENT_DATE}.
- The home directory is "{HOME_DIR}".
- Stick to the website or application already opened for the task when possible.
- Prefer Chrome over Firefox/Chromium unless the task says otherwise.
- You can act without asking for confirmation.
- If content may be off-screen, scroll or zoom out before deciding it is unavailable.
- When possible, bundle multiple GUI actions into one computer-use turn.
- If the task is infeasible because of missing apps, permissions, contradictory requirements, or other hard blockers, output exactly "[INFEASIBLE]".
"""


def _model_dump(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, list):
        return [_model_dump(item) for item in value]
    if isinstance(value, dict):
        return {key: _model_dump(item) for key, item in value.items()}
    return value


def _sanitize_for_log(value: Any) -> Any:
    """Strip oversized payloads like base64 screenshots before logging."""
    value = _model_dump(value)
    if isinstance(value, dict):
        sanitized = {}
        for key, item in value.items():
            if key == "image_url" and isinstance(item, str) and item.startswith("data:image/"):
                sanitized[key] = "<image>"
            else:
                sanitized[key] = _sanitize_for_log(item)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_for_log(item) for item in value]
    return value


def _get_field(value: Any, field: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(field, default)
    return getattr(value, field, default)


def _preview_text(text: str, limit: int = 120) -> str:
    sanitized = text.replace("\n", "\\n")
    if len(sanitized) <= limit:
        return sanitized
    return sanitized[:limit] + "..."


def encode_image(image_content: bytes) -> str:
    return base64.b64encode(image_content).decode("utf-8")


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.duration = time.time() - self.start


class StepError(Exception):
    pass


class Action:
    """Minimal wrapper matching the existing OpenAI CUA agent contract."""

    def __init__(self, raw_action: Union[Dict[str, Any], str], action_space: str):
        self._action_space = None
        self._action = None
        self.action_space = action_space
        self.action = raw_action

    @property
    def action(self) -> Any:
        return self._action

    @property
    def action_space(self) -> str:
        return self._action_space

    @action_space.setter
    def action_space(self, value: str) -> None:
        if value != "pyautogui":
            raise ValueError("GPT54Agent only supports pyautogui actions")
        self._action_space = value

    @action.setter
    def action(self, value: Union[Dict[str, Any], str]) -> None:
        if value in (None, ""):
            raise ValueError("action cannot be empty")
        self._action = value

    def get_action(self) -> Any:
        return self._action


def log_gpt_api_call(
    *,
    model_name: str,
    request_input,
    response,
    duration_ms: float,
    success: bool,
    error: Optional[str] = None,
) -> None:
    """记录 GPT API 调用日志到 logs/gpt_api_logs，图片用占位符。"""
    try:
        from datetime import datetime

        now = datetime.utcnow()
        month_dir = LOG_DIR / now.strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)

        ts = now.strftime("%Y%m%d_%H%M%S_%f")
        filename = month_dir / "gpt_api_logs.jsonl"

        safe_request = _sanitize_for_log(request_input)

        usage = None
        if response is not None:
            usage_obj = _get_field(response, "usage") or {}
            usage = {
                "input_tokens": _get_field(usage_obj, "input_tokens", 0),
                "output_tokens": _get_field(usage_obj, "output_tokens", 0),
                "total_tokens": _get_field(usage_obj, "total_tokens", 0),
            }

        response_summary = None
        output = _get_field(response, "output", []) if response is not None else []
        if output:
            texts: List[str] = []
            for item in output:
                item_type = _get_field(item, "type")
                if item_type == "message":
                    content = _get_field(item, "content", [])
                    if isinstance(content, list):
                        for part in content:
                            if _get_field(part, "type") == "output_text":
                                txt = _get_field(part, "text", "")
                                if txt:
                                    texts.append(txt)
            if texts:
                merged = "\n".join(texts)
                response_summary = merged[:2000]

        log_record = {
            "timestamp_utc": ts,
            "model": model_name,
            "success": success,
            "error": error,
            "duration_ms": duration_ms,
            "request": {
                "input": safe_request,
            },
            "response": {
                "usage": usage,
                "summary_text": response_summary,
            },
        }

        import json as _json

        with filename.open("a", encoding="utf-8") as f:
            f.write(_json.dumps(log_record, ensure_ascii=False) + "\n")

        logger.info(f"[gpt_api_logs] saved log to {filename}")
    except Exception as e:  # pragma: no cover - logging failure should not break main flow
        logger.warning(f"failed to write gpt api log: {e}")


class GPT54Agent:
    def __init__(
        self,
        env,
        platform: str = "ubuntu",
        model: str = "gpt-5.4",
        max_tokens: Optional[int] = None,
        top_p: float = 0.9,
        temperature: float = 0.5,
        action_space: str = "pyautogui",
        observation_type: str = "screenshot",
        max_trajectory_length: int = 100,
        a11y_tree_max_tokens: int = 10000,
        client_password: str = "",
        provider_name: str = "docker",
        screen_width: int = 1920,
        screen_height: int = 1080,
        sleep_after_execution: float = 0.0,
        reasoning_effort: str = "xhigh",
        base_url: str = "",
        api_key: str = ""
    ):
        if action_space != "pyautogui":
            raise ValueError("GPT54Agent only supports pyautogui action space")
        if observation_type != "screenshot":
            raise ValueError("GPT54Agent currently supports screenshot observation only")

        self.env = env
        self.platform = platform
        self.model = model
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature
        self.action_space = action_space
        self.observation_type = observation_type
        self.max_trajectory_length = max_trajectory_length
        self.a11y_tree_max_tokens = a11y_tree_max_tokens
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sleep_after_execution = sleep_after_execution
        self.reasoning_effort = reasoning_effort
        self.client_password = client_password or (
            "osworld-public-evaluation" if provider_name == "aws" else "password"
        )

        self.tools = [{"type": "computer"}]

        self.previous_response_id: Optional[str] = None
        self.pending_input_items: List[Dict[str, Any]] = []
        self.current_batch_call_id: Optional[str] = None
        self.current_batch_expected_outputs = 0

        self.base_url = base_url
        self.api_key = api_key

    def _create_response(self, request_input: List[Dict[str, Any]], instructions: str):
        retry_count = 0
        last_error = None
        start_time = time.time()
        response = None
        while retry_count < 5:
            try:
                client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                logger.info(
                    "Sending GPT-5.4 request with previous_response_id=%s and %d input item(s)",
                    self.previous_response_id,
                    len(request_input),
                )
                logger.debug("Request input items: %s", _sanitize_for_log(request_input))
                request: Dict[str, Any] = {
                    "model": self.model,
                    "instructions": instructions,
                    "input": request_input,
                    "tools": self.tools,
                    "parallel_tool_calls": False,
                    "reasoning": {
                        "effort": self.reasoning_effort,
                        "summary": "concise",
                    },
                    "truncation": "auto",
                }
                if self.max_tokens is not None:
                    request["max_output_tokens"] = self.max_tokens
                if self.previous_response_id:
                    request["previous_response_id"] = self.previous_response_id
                response = client.responses.create(**request)
                response_error = _get_field(_get_field(response, "error", {}), "message")
                if response_error:
                    raise RuntimeError(response_error)
                if _get_field(response, "status") == "failed":
                    raise RuntimeError("Responses API request failed.")
                logger.info("Received GPT-5.4 computer-use response")
                logger.debug(
                    "Raw response output: %s",
                    _sanitize_for_log(_get_field(response, "output", [])),
                )
                break
            except Exception as exc:
                last_error = exc
                retry_count += 1
                logger.error("OpenAI API error on GPT54Agent call: %s", exc)
                time.sleep(min(5, retry_count * 2))
        duration_ms = (time.time() - start_time) * 1000.0
        log_gpt_api_call(
            model_name=self.model,
            request_input=request_input,
            response=response,
            duration_ms=duration_ms,
            success=response is not None and last_error is None,
            error=str(last_error) if last_error else None,
        )
        if response is None:
            raise RuntimeError(f"OpenAI API failed too many times: {last_error}")
        return response

    def _action_to_dict(self, action: Any) -> Dict[str, Any]:
        if isinstance(action, dict):
            action_type = action.get("type")
            action_args = {k: _model_dump(v) for k, v in action.items() if k != "type"}
            return {"type": action_type, "args": action_args}

        if hasattr(action, "model_dump"):
            raw = action.model_dump()
            action_type = raw.get("type")
            action_args = {k: _model_dump(v) for k, v in raw.items() if k != "type"}
            return {"type": action_type, "args": action_args}

        if hasattr(action, "to_dict"):
            raw = action.to_dict()
            action_type = raw.get("type")
            action_args = {k: _model_dump(v) for k, v in raw.items() if k != "type"}
            return {"type": action_type, "args": action_args}

        action_type = getattr(action, "type", None)
        action_args: Dict[str, Any] = {}
        for attr in dir(action):
            if attr.startswith("_") or attr == "type":
                continue
            try:
                action_args[attr] = _model_dump(getattr(action, attr))
            except Exception:
                continue
        return {"type": action_type, "args": action_args}

    def _convert_drag_path(self, args: Dict[str, Any]) -> Optional[str]:
        path = args.get("path")
        if not path and args.get("from") and args.get("to"):
            path = [args["from"], args["to"]]
        if not path or len(path) < 2:
            return None

        def point_xy(point: Any) -> Tuple[Any, Any]:
            if isinstance(point, (list, tuple)) and len(point) == 2:
                return point[0], point[1]
            if isinstance(point, dict):
                return point.get("x"), point.get("y")
            return getattr(point, "x", None), getattr(point, "y", None)

        first_x, first_y = point_xy(path[0])
        if first_x is None or first_y is None:
            return None

        commands = [f"import pyautogui\npyautogui.moveTo({first_x}, {first_y})"]
        for point in path[1:]:
            x, y = point_xy(point)
            if x is None or y is None:
                return None
            commands.append(f"pyautogui.dragTo({x}, {y}, duration=0.2, button='left')")
        return "\n".join(commands)

    def _typing_strategy(self, text: str) -> str:
        if text == "":
            return "empty"
        if not text.isascii():
            return "clipboard"
        if "\n" in text:
            return "multiline_ascii"
        if text.isascii():
            return "single_line_ascii"
        return "clipboard"

    def _summarize_type_payload(self, text: str) -> Dict[str, Any]:
        return {
            "strategy": self._typing_strategy(text),
            "chars": len(text),
            "lines": len(text.split("\n")) if text else 0,
            "ascii": text.isascii(),
            "trailing_newline": text.endswith("\n"),
            "preview": _preview_text(text),
        }

    def _build_multiline_ascii_type_command(self, text: str) -> str:
        commands = ["import pyautogui"]
        lines = text.split("\n")
        for index, line in enumerate(lines):
            if line:
                commands.append(f"pyautogui.typewrite({repr(line)}, interval=0.03)")
            if index < len(lines) - 1:
                commands.append("pyautogui.press('enter')")
        return "\n".join(commands)

    def _build_clipboard_paste_command(self, text: str, paste_keys: Tuple[str, ...] = ("ctrl", "v")) -> str:
        encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
        keys = ", ".join(repr(key) for key in paste_keys)
        return (
            "import base64, time, pyautogui, pyperclip\n"
            f"_text = base64.b64decode('{encoded}').decode('utf-8')\n"
            "pyperclip.copy(_text)\n"
            "time.sleep(0.1)\n"
            f"pyautogui.hotkey({keys})\n"
            "time.sleep(0.1)"
        )

    def _convert_action_to_pyautogui(self, action_type: str, args: Dict[str, Any]) -> Optional[str]:
        if not action_type:
            return None

        key_mapping = {
            "alt": "alt",
            "arrowdown": "down",
            "arrowleft": "left",
            "arrowright": "right",
            "arrowup": "up",
            "backspace": "backspace",
            "capslock": "capslock",
            "cmd": "command",
            "command": "command",
            "ctrl": "ctrl",
            "delete": "delete",
            "end": "end",
            "enter": "enter",
            "esc": "esc",
            "home": "home",
            "insert": "insert",
            "option": "option",
            "pagedown": "pagedown",
            "pageup": "pageup",
            "shift": "shift",
            "space": "space",
            "super": "super",
            "tab": "tab",
            "win": "win",
        }

        try:
            if action_type == "click":
                x = args.get("x")
                y = args.get("y")
                button = args.get("button", "left")
                if x is None or y is None:
                    return None
                if button not in ["left", "middle", "right"]:
                    button = "left"
                return (
                    f"import pyautogui\n"
                    f"pyautogui.moveTo({x}, {y})\n"
                    f"pyautogui.click(button='{button}')"
                )

            if action_type == "double_click":
                x = args.get("x")
                y = args.get("y")
                if x is None or y is None:
                    return None
                return (
                    f"import pyautogui\n"
                    f"pyautogui.moveTo({x}, {y})\n"
                    f"pyautogui.doubleClick()"
                )

            if action_type == "move":
                x = args.get("x")
                y = args.get("y")
                if x is None or y is None:
                    return None
                return "import pyautogui\npyautogui.moveTo({x}, {y})".format(x=x, y=y)

            if action_type == "drag":
                return self._convert_drag_path(args)

            if action_type == "type":
                text = args.get("text", "")
                summary = self._summarize_type_payload(text)
                logger.info("Type action payload: %s", summary)
                if text == "":
                    return "import time\ntime.sleep(0.1)"
                strategy = summary["strategy"]
                if strategy == "multiline_ascii":
                    return self._build_multiline_ascii_type_command(text)
                if strategy == "clipboard":
                    return self._build_clipboard_paste_command(text)
                return f"import pyautogui\npyautogui.typewrite({repr(text)}, interval=0.03)"

            if action_type == "keypress":
                keys = args.get("keys")
                if not keys and args.get("key"):
                    keys = [args.get("key")]
                if not keys:
                    return None
                if not isinstance(keys, (list, tuple)):
                    keys = [keys]
                mapped_keys = []
                for key in keys:
                    normalized = key_mapping.get(str(key).lower(), str(key).lower())
                    mapped_keys.append(normalized)
                keys_str = ", ".join([repr(key) for key in mapped_keys])
                return f"import pyautogui\npyautogui.hotkey({keys_str})"

            if action_type == "scroll":
                x = args.get("x")
                y = args.get("y")
                scroll_x = int(
                    args.get("scroll_x")
                    or args.get("delta_x")
                    or args.get("deltaX")
                    or 0
                )
                scroll_y = int(
                    args.get("scroll_y")
                    or args.get("delta_y")
                    or args.get("deltaY")
                    or 0
                )
                position = f", x={x}, y={y}" if x is not None and y is not None else ""
                if scroll_y:
                    return f"import pyautogui\npyautogui.scroll({scroll_y * -1}{position})"
                if scroll_x:
                    return f"import pyautogui\npyautogui.hscroll({scroll_x * -1}{position})"
                return None

            if action_type == "wait":
                secs = max(0.1, float(args.get("ms", 1000)) / 1000.0)
                return f"import time\ntime.sleep({secs})"

            if action_type == "screenshot":
                return "import time\ntime.sleep(0.1)"
        except Exception:
            logger.exception("Failed to convert GPT-5.4 computer action: %s", action_type)
            return None

        logger.warning("Unsupported GPT-5.4 computer action: %s", action_type)
        return None

    def _message_text(self, item: Any) -> str:
        content = _get_field(item, "content", [])
        if not content:
            return ""
        if isinstance(content, list):
            parts = []
            for part in content:
                part_type = _get_field(part, "type")
                if part_type == "output_text":
                    parts.append(_get_field(part, "text", ""))
            return "\n".join([part for part in parts if part])
        return str(content)

    def _reasoning_text(self, item: Any) -> str:
        summary = _get_field(item, "summary", [])
        if not summary:
            return ""
        if isinstance(summary, list):
            parts = []
            for part in summary:
                text = _get_field(part, "text", "")
                if text:
                    parts.append(text)
            return "\n".join(parts)
        return str(summary)

    def _extract_raw_response_string(self, raw_output: List[Any]) -> str:
        """将模型输出的 message / reasoning / computer_call 等内容串联成一个原始字符串。"""
        snippets: List[str] = []
        for item in raw_output:
            item_type = _get_field(item, "type")
            if item_type == "message":
                text = self._message_text(item)
                if text:
                    snippets.append(f"[MESSAGE] {text}")
            elif item_type == "reasoning":
                text = self._reasoning_text(item)
                if text:
                    snippets.append(f"[REASONING] {text}")
            elif item_type == "computer_call":
                snippets.append(f"[COMPUTER_CALL] {_sanitize_for_log(item)}")
            else:
                snippets.append(f"[OTHER] {_sanitize_for_log(item)}")
        return "\n".join(snippets).strip()

    def predict(self, instruction: str, obs: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str]]:
        """调用 GPT-5.4 生成动作。

        返回:
          - predict_info_list: List[Dict]，每个元素都包含至少 thought, action, raw_response, coordinate 字段
          - actions: List[str]，pyautogui 代码字符串列表
        """
        home_dir = "C:\\Users\\user" if self.platform.lower().startswith("win") else "/home/user"
        instructions = OPERATOR_PROMPT.format(
            CLIENT_PASSWORD=self.client_password,
            CURRENT_DATE=datetime.now().strftime("%A, %B %d, %Y"),
            HOME_DIR=home_dir,
            PLATFORM=self.platform,
        )
        screenshot_b64 = encode_image(obs["screenshot"])

        if not self.previous_response_id:
            request_input = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": instruction,
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{screenshot_b64}",
                            "detail": "original",
                        },
                    ],
                }
            ]
        else:
            request_input = list(self.pending_input_items)
            if not request_input:
                request_input = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "Continue from the latest screenshot.",
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/png;base64,{screenshot_b64}",
                                "detail": "original",
                            },
                        ],
                    }
                ]

        with Timer() as model_timer:
            response = self._create_response(request_input, instructions)

        self.previous_response_id = _get_field(response, "id")
        self.pending_input_items = []

        raw_output = _get_field(response, "output", []) or []
        actions_meta: List[Dict[str, Any]] = []
        pyautogui_actions: List[str] = []
        unsupported_action = False
        infeasible_message = False

        # 累积整体思考文本，便于 meta 中使用
        all_reasonings: List[str] = []

        for item in raw_output:
            item_type = _get_field(item, "type")
            if item_type == "message":
                message_text = self._message_text(item)
                if message_text:
                    lower = message_text.lower()
                    if "[infeasible]" in lower or any(
                        token in lower
                        for token in [
                            "infeasible",
                            "unfeasible",
                            "impossible",
                            "cannot be done",
                            "not feasible",
                        ]
                    ):
                        infeasible_message = True
            elif item_type == "reasoning":
                reasoning_text = self._reasoning_text(item)
                if reasoning_text:
                    all_reasonings.append(reasoning_text)
            elif item_type == "computer_call":
                logger.info("Raw computer_call item: %s", _sanitize_for_log(item))
                raw_actions = _get_field(item, "actions")
                if raw_actions is None:
                    single_action = _get_field(item, "action")
                    raw_actions = [single_action] if single_action is not None else []

                call_id = _get_field(item, "call_id", "")
                pending_checks = _model_dump(_get_field(item, "pending_safety_checks", []))
                raw_actions = list(raw_actions)
                batch_size = len(raw_actions)

                for index, raw_action in enumerate(raw_actions):
                    action_info = self._action_to_dict(raw_action)
                    logger.info(
                        "Raw tool action %d/%d for call_id=%s: %s",
                        index + 1,
                        batch_size,
                        call_id,
                        _sanitize_for_log(action_info),
                    )
                    pyautogui_code = self._convert_action_to_pyautogui(
                        action_info["type"],
                        action_info["args"],
                    )
                    if not pyautogui_code:
                        unsupported_action = True
                        continue

                    actions_meta.append(
                        {
                            "action_space": "pyautogui",
                            "action": pyautogui_code,
                            "pending_checks": pending_checks,
                            "call_id": call_id,
                            "batch_index": index,
                            "batch_size": batch_size,
                            "batch_last": index == batch_size - 1,
                            # Anthropic 风格必需字段
                            "coordinate": [
                                action_info["args"].get("x"),
                                action_info["args"].get("y"),
                            ]
                            if "x" in action_info["args"] and "y" in action_info["args"]
                            else None,
                        }
                    )
                    pyautogui_actions.append(pyautogui_code)

        state_correct = bool(actions_meta) and not unsupported_action and not infeasible_message
        if unsupported_action:
            pyautogui_actions = []

        # 构造与 AnthropicAgent 兼容的 predict_info list
        thought_text = "\n".join(all_reasonings) if all_reasonings else ""
        raw_response_str = self._extract_raw_response_string(raw_output)

        predict_info_list: List[Dict[str, Any]] = []
        for meta in actions_meta or [{}]:
            predict_info_list.append(
                {
                    # 必需字段
                    "thought": thought_text,
                    "action": meta.get("action", ""),
                    "coordinate": meta.get("coordinate"),
                    "raw_response": raw_response_str,
                    "meta_action": meta,
                }
            )

        logger.info("Model returned %d action(s)", len(actions_meta))
        logger.debug(
            "Model raw output messages: %s", _sanitize_for_log(_model_dump(raw_output))
        )

        return predict_info_list, pyautogui_actions

    def evaluate(self, task_instruction: str, obs: Dict[str, Any]) -> Dict[str, Any]:
        """自评当前任务是否完成，返回 {thought: str, score: float}。"""
        import json as _json

        EVALUATION_SYSTEM_PROMPT = """
        You are an impartial judge evaluating the performance of a computer agent.
        Your task is to determine if the agent successfully completed the user's instruction based on the model's internal reasoning, actions, and the final screenshot.

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
        Only return the JSON object, do not add any other text.
        """

        try:
            prompt = EVALUATION_SYSTEM_PROMPT.format(instruction=task_instruction)

            screenshot_data = obs.get("screenshot")
            if isinstance(screenshot_data, bytes):
                screenshot_base64 = base64.b64encode(screenshot_data).decode("utf-8")
            else:
                screenshot_base64 = str(screenshot_data)

            input_blocks = [
                {
                    "type": "input_text",
                    "text": prompt,
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{screenshot_base64}",
                    "detail": "original",
                },
            ]

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            with Timer() as eval_timer:
                response = client.responses.create(
                    model=self.model,
                    instructions="You are a JSON-only evaluation assistant.",
                    input=[{"role": "user", "content": input_blocks}],
                    max_output_tokens=self.max_tokens or 1024,
                    reasoning={"effort": "low", "summary": "concise"},
                )

            logger.info("GPT54Agent evaluation response: %s", _sanitize_for_log(response))

            raw_output = _get_field(response, "output", []) or []
            raw_response_str = self._extract_raw_response_string(raw_output)

            if "```json" in raw_response_str:
                json_str = raw_response_str.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in raw_response_str:
                json_str = raw_response_str.split("```", 1)[1].strip()
            else:
                json_str = raw_response_str.strip()

            result = _json.loads(json_str)

            if "thought" not in result:
                result["thought"] = raw_response_str
            if "score" not in result:
                result["score"] = 0.0

            result["eval_model_time"] = eval_timer.duration
            return result
        except Exception as e:  # pragma: no cover - evaluation failure is non-critical
            import traceback as _tb

            logger.error(f"Evaluation failed: {e}")
            logger.error(_tb.format_exc())
            return {
                "thought": f"Evaluation failed due to error: {str(e)}",
                "score": 0.0,
            }

    def reset(self, _logger=None):
        global logger
        logger = _logger if _logger is not None else logging.getLogger("desktopenv.agent")
        self.previous_response_id = None
        self.pending_input_items = []
        self.current_batch_call_id = None
        self.current_batch_expected_outputs = 0

    # def step(self, action: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    #     try:
    #         if not action:
    #             raise StepError("Empty action received")

    #         with Timer() as step_timer:
    #             step_action = Action(action["action"], self.action_space)
    #             obs, reward, terminated, info = self.env.step(
    #                 step_action.get_action(),
    #                 self.sleep_after_execution,
    #             )

    #             if action.get("batch_last"):
    #                 screenshot_base64 = encode_image(obs["screenshot"])
    #                 output_item = {
    #                     "type": "computer_call_output",
    #                     "call_id": action.get("call_id", ""),
    #                     "output": {
    #                         "type": "computer_screenshot",
    #                         "image_url": f"data:image/png;base64,{screenshot_base64}",
    #                         "detail": "original",
    #                     },
    #                 }
    #                 pending_checks = action.get("pending_checks") or []
    #                 if pending_checks:
    #                     output_item["acknowledged_safety_checks"] = pending_checks
    #                 self.pending_input_items.append(output_item)

    #         return obs, reward, terminated, info, {
    #             "step_time": step_timer.duration,
    #             "action": action,
    #         }
    #     except Exception as exc:
    #         logger.exception("GPT54Agent step failed: %s", exc)
    #         raise StepError(f"Failed to execute step: {exc}")
