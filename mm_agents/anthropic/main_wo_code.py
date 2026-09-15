"""
Claude Official
"""
import base64
from copy import deepcopy
import os
import time
from typing import Any, cast, Optional, Dict
from pathlib import Path
import json
from PIL import Image
import io

from anthropic import (
    Anthropic,
    AnthropicBedrock,
    AnthropicVertex,
    APIError,
    APIResponseValidationError,
    APIStatusError,
)
from anthropic.types.beta import (
    BetaMessageParam,
    BetaTextBlockParam,
)
from .utils import COMPUTER_USE_BETA_FLAG, SYSTEM_PROMPT, SYSTEM_PROMPT_ORM, SYSTEM_PROMPT_WINDOWS, APIProvider, PROVIDER_TO_DEFAULT_MODEL_NAME, COMPUTER_USE_TYPE
from .utils import _response_to_params, _inject_prompt_caching, _maybe_filter_to_n_most_recent_images, build_qwen_sft_sample
from mm_agents.utils.call_api_log import log_claude_api_call

import logging
logger = logging.getLogger("desktopenv.agent")

# MAX_HISTORY = 10
API_RETRY_TIMES = 500
API_RETRY_INTERVAL = 5

BATCHED_ACTION_PROMPT = """CRITICAL - ALWAYS BATCH ACTIONS: You MUST combine as many actions as possible into a SINGLE tool call.
Each tool call has significant latency overhead, so batching is essential for efficiency.
Do NOT make separate tool calls for actions you can predict the outcome of.

You do NOT need a fresh observation after every action. The environment automatically
returns the latest observation after each tool call; batch predictable action sequences.

"""

QWEN3_BATCHED_ACTIONS = [
    "key", "type", "mouse_move", "left_click", "left_click_drag",
    "right_click", "middle_click", "double_click", "triple_click",
    "scroll", "wait", "screenshot",
]

CLAUDE_EXTENDED_BATCHED_ACTIONS = QWEN3_BATCHED_ACTIONS + [
    "hold_key", "left_mouse_down", "left_mouse_up", "zoom",
]

def _build_batched_tool_schema(qwen3_tools: bool) -> dict:
    action_enum = QWEN3_BATCHED_ACTIONS if qwen3_tools else CLAUDE_EXTENDED_BATCHED_ACTIONS
    properties = {
        "action": {
            "type": "string",
            "enum": action_enum,
        },
        "text": {"type": "string"},
        "coordinate": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "start_coordinate": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "scroll_direction": {
            "type": "string",
            "enum": ["up", "down", "left", "right"],
        },
        "scroll_amount": {"type": "integer"},
        "duration": {"type": "integer"},
        "repeat": {
            "type": "integer",
            "minimum": 1,
            "description": "Only valid for action=key. Repeat the key press this many times.",
        },
    }
    if not qwen3_tools:
        properties["region"] = {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 4,
            "maxItems": 4,
        }

    description = (
        "Execute one or more computer use actions in sequence. Batch multiple actions "
        "into a single call to minimize round trips. Actions use the supported desktop "
        "action set: " + ", ".join(action_enum) + "."
    )
    if not qwen3_tools:
        description += " zoom is an observation-only crop returned in the next tool result."

    return {
        "name": "computer",
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": {
                "actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": properties,
                        "required": ["action"],
                    },
                    "description": "List of actions to execute in sequence. Batch as many as possible.",
                },
            },
            "required": ["actions"],
        },
    }

class AnthropicAgent:
    def __init__(self,
                platform: str = "Ubuntu",
                model: str = "claude-sonnet-4-5-20250929",
                provider: APIProvider = APIProvider.ANTHROPIC,
                max_tokens: int = 32768,
                api_key: str = os.environ.get("ANTHROPIC_API_KEY", ""),
                base_url: str = "",
                system_prompt_suffix: str = "",
                only_n_most_recent_images: Optional[int] = 10,
                action_space: str = "claude_computer_use",
                screen_size: tuple[int, int] = (1920, 1080),
                thinking_mode: str = "adaptive",
                effort: Optional[str] = None,
                temperature: Optional[float] = None,
                top_p: Optional[float] = None,
                input_screen_size: tuple[int, int] = (1280, 720),
                batch_tool_prompt: bool = True,
                auto_screenshot: bool = True,
                qwen3_tools: bool = False,
                collect_qwen_sft: bool = False,
                collect_qwen_sft_image_dir: str = "qwen3vl_sft_dataset/image",
                *args, **kwargs
            ):
        self.platform = platform
        self.action_space = action_space
        self.logger = logger
        self.class_name = self.__class__.__name__
        self.model_name = model
        self.provider = provider
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.base_url = base_url
        self.system_prompt_suffix = system_prompt_suffix
        self.only_n_most_recent_images = only_n_most_recent_images
        self.messages: list[BetaMessageParam] = []
        self.screen_size = screen_size
        if thinking_mode not in ("none", "regular", "isp", "adaptive"):
            raise ValueError("thinking_mode must be one of: none, regular, isp, adaptive")
        self.thinking_mode = thinking_mode
        if effort is None and model == "claude-opus-4-8":
            effort = "max"
        if effort not in (None, "low", "medium", "high", "max"):
            raise ValueError("effort must be one of: low, medium, high, max")
        self.effort = effort
        self.temperature = temperature
        self.top_p = top_p
        self.input_screen_width, self.input_screen_height = input_screen_size
        self.batch_tool_prompt = batch_tool_prompt
        self.auto_screenshot = auto_screenshot
        self.qwen3_tools = qwen3_tools
        self.max_steps = kwargs.get("max_steps", 15)
        self.current_step = 0
        self.resize_factor = (
            screen_size[0] / self.input_screen_width,
            screen_size[1] / self.input_screen_height
        )

        # Distill
        self.collect_qwen_sft = collect_qwen_sft
        self.qwen_sft_image_hash_map: dict[str, str] = {}
        self.collect_qwen_sft_image_dir = Path(collect_qwen_sft_image_dir)

    def _get_sampling_params(self):
        """Get sampling parameters (temperature and/or top_p) - let API validate exclusivity"""
        params = {}
        if self.temperature is not None:
            params['temperature'] = self.temperature
        # if self.top_p is not None:
        #     params['top_p'] = self.top_p
        return params

    def _get_output_config(self) -> dict[str, Any]:
        """Return SDK kwargs for Claude's effort control when requested."""
        if self.effort is None:
            return {}
        return {"output_config": {"effort": self.effort}}

    def _get_thinking_request(self) -> tuple[dict[str, Any], int]:
        extra_body: dict[str, Any] = {}
        actual_max_tokens = self.max_tokens

        if self.thinking_mode == "none":
            logger.info("Thinking mode: DISABLED")
        elif self.thinking_mode == "adaptive":
            extra_body["thinking"] = {
                "type": "adaptive",
                "display": "summarized",
            }
            logger.info("Thinking mode: ADAPTIVE (model decides budget, summarized thinking enabled)")
        else:
            budget_tokens = 2048
            if self.thinking_mode == "regular" and self.max_tokens <= budget_tokens:
                required_max_tokens = budget_tokens + 500
                logger.warning(f"Regular thinking requires max_tokens > budget_tokens. Increasing max_tokens from {self.max_tokens} to {required_max_tokens}")
                actual_max_tokens = required_max_tokens
            else:
                actual_max_tokens = self.max_tokens

            extra_body["thinking"] = {"type": "enabled", "budget_tokens": budget_tokens}
            if self.thinking_mode == "isp":
                logger.info("Thinking mode: INTERLEAVED SCRATCHPAD (ISP)")
            else:
                logger.info("Thinking mode: REGULAR SCRATCHPAD")

        return extra_body, actual_max_tokens

    def _call_model_with_logging(
        self,
        client,
        messages,
        system,
        tools,
        betas,
        extra_body,
        actual_max_tokens: int,
        **extra_create_kwargs,
    ):
        """封装一次模型调用，增加耗时统计与日志记录。"""
        start = time.time()
        response = None
        error_msg = None
        try:
            logger.info(f"Claude API request messages size: {len(json.dumps(messages, ensure_ascii=False).encode('utf-8')) / (1024 * 1024):.3f} MB")
            with client.beta.messages.stream(
                max_tokens=actual_max_tokens,
                messages=messages,
                model=PROVIDER_TO_DEFAULT_MODEL_NAME[self.provider, self.model_name],
                system=[system],
                cache_control={"type": "ephemeral"},
                tools=tools,
                betas=betas,
                extra_body=extra_body,
                **extra_create_kwargs,
                **self._get_sampling_params(),
            ) as stream:
                response = stream.get_final_message()
            success = True
            return response
        except Exception as e:
            error_msg = str(e)
            success = False
            raise
        finally:
            duration_ms = (time.time() - start) * 1000.0
            try:
                log_claude_api_call(
                    model_name=self.model_name,
                    provider=self.provider,
                    request_messages=messages,
                    response=response,
                    duration_ms=duration_ms,
                    success=success,
                    error=error_msg,
                )
            except Exception as log_e:
                logger.warning(f"logging claude api call failed: {log_e}")

    def _extract_raw_response_string(self, response) -> str:
        """Extract and concatenate raw response content into a single string."""
        raw_response_str = ""
        if response.content:
            for block in response.content:
                if hasattr(block, 'text') and block.text:
                    raw_response_str += f"[TEXT] {block.text}\n"
                elif hasattr(block, 'thinking') and block.thinking:
                    raw_response_str += f"[THINKING] {block.thinking}\n"
                elif hasattr(block, 'name') and hasattr(block, 'input'):
                    raw_response_str += f"[TOOL_USE] {block.name}: {block.input}\n"
                else:
                    raw_response_str += f"[OTHER] {str(block)}\n"
        return raw_response_str.strip()

    def _make_image_block(self, png_bytes: bytes) -> dict:
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": base64.b64encode(png_bytes).decode("utf-8"),
            },
        }

    def add_tool_result(self, tool_call_id: str, result: str, screenshot: bytes = None, extra_screenshots: list = None):
        """Add tool result to message history. Supports multiple screenshots."""
        tool_result_content = [
            {
                "type": "tool_result",
                "tool_use_id": tool_call_id,
                "content": [{"type": "text", "text": result}]
            }
        ]

        if screenshot is not None:
            tool_result_content[0]["content"].append(self._make_image_block(screenshot))

        if extra_screenshots:
            for extra in extra_screenshots:
                tool_result_content[0]["content"].append(self._make_image_block(extra))

        self.messages.append({
            "role": "user",
            "content": tool_result_content
        })

    def _process_zoom_screenshot(self, original_screenshot: bytes, tool_input: dict):
        if not original_screenshot:
            return {"error": "No screenshot available for zoom action"}

        region = tool_input.get("region")
        if not region or not isinstance(region, (list, tuple)) or len(region) != 4:
            return {"error": "region must be a tuple of 4 integers (x0, y0, x1, y1)"}

        try:
            image = Image.open(io.BytesIO(original_screenshot))
            x0, y0, x1, y1 = region
            if self.resize_factor:
                x0, y0 = int(x0 * self.resize_factor[0]), int(y0 * self.resize_factor[1])
                x1, y1 = int(x1 * self.resize_factor[0]), int(y1 * self.resize_factor[1])

            if x0 < 0 or y0 < 0 or x1 < 0 or y1 < 0:
                return {"error": "region coordinates must be non-negative"}
            if x1 <= x0 or y1 <= y0:
                return {"error": "region must have positive width and height"}
            if x1 > image.width or y1 > image.height:
                return {"error": f"region exceeds image bounds ({image.width}x{image.height})"}

            cropped = image.crop((x0, y0, x1, y1))
            scale_factor = min(self.input_screen_width / cropped.width, self.input_screen_height / cropped.height)
            new_size = (max(1, int(cropped.width * scale_factor)), max(1, int(cropped.height * scale_factor)))
            scaled = cropped.resize(new_size, Image.Resampling.LANCZOS)
            output_buffer = io.BytesIO()
            scaled.save(output_buffer, format='PNG')
            return output_buffer.getvalue()
        except Exception as e:
            return {"error": f"Failed to process zoom: {str(e)}"}

    def parse_actions_from_tool_call(self, tool_call: Dict) -> tuple[str, Optional[list]]:
        result = ""
        function_args = (
            tool_call["input"]
        )

        action = function_args.get("action")
        if not action:
            action = tool_call.get("name")
        action_conversion = {
            "left click": "click",
            "right click": "right_click"
        }
        action = action_conversion.get(action, action)

        text = function_args.get("text")
        coordinate = function_args.get("coordinate")
        start_coordinate = function_args.get("start_coordinate")
        scroll_direction = function_args.get("scroll_direction")
        scroll_amount = function_args.get("scroll_amount")
        duration = function_args.get("duration")
        if self.qwen3_tools:
            unsupported_actions = {"hold_key", "left_mouse_down", "left_mouse_up", "zoom"}
            if action in unsupported_actions:
                raise ValueError(f"{action} is not supported when qwen3_tools=True")
        repeat = int(function_args.get("repeat") or 1)
        scroll_amount = int(scroll_amount or 0)

        # resize coordinates if resize_factor is set
        if coordinate and self.resize_factor:
            coordinate = [
                int(coordinate[0] * self.resize_factor[0]),
                int(coordinate[1] * self.resize_factor[1])
            ]
        elif coordinate:
            coordinate = list(coordinate)

        if start_coordinate and self.resize_factor:
            start_coordinate = [
                int(start_coordinate[0] * self.resize_factor[0]),
                int(start_coordinate[1] * self.resize_factor[1])
            ]
        elif start_coordinate:
            start_coordinate = list(start_coordinate)

        return_coord = coordinate

        if action == "left_mouse_down":
            result += "pyautogui.mouseDown()\n"
        elif action == "left_mouse_up":
            result += "pyautogui.mouseUp()\n"

        elif action == "hold_key":
            if not isinstance(text, str):
                raise ValueError(f"{text} must be a string")

            keys = text.split('+')
            for key in keys:
                key = key.strip().lower()
                result += f"pyautogui.keyDown('{key}')\n"

        # Handle mouse move and drag actions
        elif action in ("mouse_move", "left_click_drag"):
            if coordinate is None:
                raise ValueError(f"coordinate is required for {action}")
            if text is not None:
                raise ValueError(f"text is not accepted for {action}")
            if not isinstance(coordinate, (list, tuple)) or len(coordinate) != 2:
                raise ValueError(f"{coordinate} must be a tuple of length 2")
            if not all(isinstance(i, int) for i in coordinate):
                raise ValueError(f"{coordinate} must be a tuple of ints")

            x, y = coordinate[0], coordinate[1]
            if action == "mouse_move":
                result += (
                    f"pyautogui.moveTo({x}, {y}, duration={duration or 0.5})\n"
                )
            elif action == "left_click_drag":
                # If start_coordinate is provided, validate and move to start before dragging
                if start_coordinate:
                    if not isinstance(start_coordinate, (list, tuple)) or len(start_coordinate) != 2:
                        raise ValueError(f"{start_coordinate} must be a tuple of length 2")
                    if not all(isinstance(i, int) for i in start_coordinate):
                        raise ValueError(f"{start_coordinate} must be a tuple of ints")
                    start_x, start_y = start_coordinate[0], start_coordinate[1]
                    result += (
                        f"pyautogui.moveTo({start_x}, {start_y}, duration={duration or 0.5})\n"
                    )
                    return_coord = [start_coordinate, coordinate]
                result += (
                    f"pyautogui.dragTo({x}, {y}, duration={duration or 0.5})\n"
                )

        # Handle keyboard actions
        elif action in ("key", "type"):
            if text is None:
                raise ValueError(f"text is required for {action}")
            if coordinate is not None:
                raise ValueError(f"coordinate is not accepted for {action}")
            if not isinstance(text, str):
                raise ValueError(f"{text} must be a string")

            if action == "key":
                key_conversion = {
                    "page_down": "pagedown",
                    "page_up": "pageup",
                    "super_l": "win",
                    "super": "command",
                    "escape": "esc"
                }
                keys = text.split('+')
                for _ in range(repeat):
                    for key in keys:
                        key = key.strip().lower()
                        key = key_conversion.get(key, key)
                        result += (f"pyautogui.keyDown('{key}')\n")
                    for key in reversed(keys):
                        key = key.strip().lower()
                        key = key_conversion.get(key, key)
                        result += (f"pyautogui.keyUp('{key}')\n")
            elif action == "type":
                result += (
                    f"pyautogui.typewrite(\"\"\"{text}\"\"\", interval=0.01)\n"
                )

        # Handle scroll actions
        elif action == "scroll":
            if coordinate is None:
                if scroll_direction in ("up", "down"):
                    result += (
                        f"pyautogui.scroll({scroll_amount if scroll_direction == 'up' else -scroll_amount})\n"
                    )
                elif scroll_direction in ("left", "right"):
                    result += (
                        f"pyautogui.hscroll({scroll_amount if scroll_direction == 'right' else -scroll_amount})\n"
                    )
            else:
                if scroll_direction in ("up", "down"):
                    x, y = coordinate[0], coordinate[1]
                    result += (
                        f"pyautogui.scroll({scroll_amount if scroll_direction == 'up' else -scroll_amount}, {x}, {y})\n"
                    )
                elif scroll_direction in ("left", "right"):
                    x, y = coordinate[0], coordinate[1]
                    result += (
                        f"pyautogui.hscroll({scroll_amount if scroll_direction == 'right' else -scroll_amount}, {x}, {y})\n"
                    )

        # Handle click actions
        elif action in ("left_click", "right_click", "double_click", "middle_click", "left_press", "triple_click"):
            # Handle modifier keys during click if specified
            if text:
                keys = text.split('+')
                for key in keys:
                    key = key.strip().lower()
                    result += f"pyautogui.keyDown('{key}')\n"
            if coordinate is not None:
                x, y = coordinate
                if action == "left_click":
                    result += (f"pyautogui.click({x}, {y})\n")
                elif action == "right_click":
                    result += (f"pyautogui.rightClick({x}, {y})\n")
                elif action == "double_click":
                    result += (f"pyautogui.doubleClick({x}, {y})\n")
                elif action == "middle_click":
                    result += (f"pyautogui.middleClick({x}, {y})\n")
                elif action == "left_press":
                    result += (f"pyautogui.mouseDown({x}, {y})\n")
                    result += ("time.sleep(1)\n")
                    result += (f"pyautogui.mouseUp({x}, {y})\n")
                elif action == "triple_click":
                    result += (f"pyautogui.tripleClick({x}, {y})\n")

            else:
                if action == "left_click":
                    result += ("pyautogui.click()\n")
                elif action == "right_click":
                    result += ("pyautogui.rightClick()\n")
                elif action == "double_click":
                    result += ("pyautogui.doubleClick()\n")
                elif action == "middle_click":
                    result += ("pyautogui.middleClick()\n")
                elif action == "left_press":
                    result += ("pyautogui.mouseDown()\n")
                    result += ("time.sleep(1)\n")
                    result += ("pyautogui.mouseUp()\n")
                elif action == "triple_click":
                    result += ("pyautogui.tripleClick()\n")
            # Release modifier keys after click
            if text:
                keys = text.split('+')
                for key in reversed(keys):
                    key = key.strip().lower()
                    result += f"pyautogui.keyUp('{key}')\n"

        elif action == "wait":
            result += f"pyautogui.sleep({duration or 0.5})\n"
        elif action == "screenshot":
            result += "pyautogui.sleep(0.1)\n"
        elif action == "zoom":
            result += "pyautogui.sleep(0.1)\n"
        elif action == "fail":
            result += "FAIL"
        elif action == "done":
            result += "DONE"
        elif action == "call_user":
            result += "CALL_USER"
        else:
            raise ValueError(f"Invalid action: {action}")

        return result, return_coord

    def predict(self, task_instruction: str, obs: Dict = None, system: Any = None):
        self.current_step += 1

        prompt_text = SYSTEM_PROMPT_WINDOWS if self.platform == 'Windows' else SYSTEM_PROMPT
        if self.batch_tool_prompt:
            prompt_text += f"\n\n{BATCHED_ACTION_PROMPT}"
        if self.system_prompt_suffix:
            prompt_text += ' ' + self.system_prompt_suffix
        system = BetaTextBlockParam(type="text", text=prompt_text)

        if obs and "screenshot" in obs and obs["screenshot"] is not None:
            screenshot_bytes = obs["screenshot"]
            obs["screenshot_original"] = screenshot_bytes
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes))
            resized_image = screenshot_image.resize(
                (self.input_screen_width, self.input_screen_height),
                Image.Resampling.LANCZOS
            )
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format='PNG')
            obs["screenshot"] = output_buffer.getvalue()
        elif obs and "screenshot" in obs and obs["screenshot"] is None:
            raise RuntimeError("Screenshot is None. Environment HTTP server may be unavailable or get_screenshot() failed.")

        # Handle user response from run loop (user simulator answer).
        if obs and obs.get("user_response") and self.messages:
            self.messages.append({
                "role": "user",
                "content": [{"type": "text", "text": obs["user_response"]}],
            })

        if not self.messages:
            init_screenshot = obs
            self.messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": 'Task: ' + task_instruction},
                    self._make_image_block(init_screenshot["screenshot"]),
                ]
            })

        # Add tool_result for ALL tool_use blocks in the last message
        if self.messages:
            last_message_content = self.messages[-1]["content"]
            tool_use_blocks = [block for block in last_message_content if block.get("type") == "tool_use"]

            for i, tool_block in enumerate(tool_use_blocks):
                tool_input = tool_block.get("input", {})
                action = tool_input.get("action")
                is_last_tool = i == len(tool_use_blocks) - 1

                include_screenshot = None
                extra_screenshots = None

                if obs and isinstance(tool_input.get("actions"), list):
                    batch_actions = tool_input["actions"]
                    zoom_action = None
                    zoom_index = None
                    if not self.qwen3_tools:
                        for idx, ba in enumerate(batch_actions):
                            if isinstance(ba, dict) and ba.get("action") == "zoom":
                                zoom_action = ba
                                zoom_index = idx
                    if zoom_action:
                        zoom_result = self._process_zoom_screenshot(obs.get("screenshot_original"), zoom_action)
                        if isinstance(zoom_result, dict) and "error" in zoom_result:
                            self.add_tool_result(tool_block["id"], zoom_result["error"], screenshot=None)
                            continue
                        include_screenshot = zoom_result
                        if zoom_index is not None and zoom_index < len(batch_actions) - 1 and obs.get("screenshot"):
                            extra_screenshots = [obs.get("screenshot")]
                    else:
                        last_action = batch_actions[-1].get("action") if batch_actions else None
                        if last_action == "screenshot":
                            include_screenshot = obs.get("screenshot")
                        elif self.auto_screenshot and is_last_tool:
                            include_screenshot = obs.get("screenshot")
                elif obs and not self.qwen3_tools and action == "zoom":
                    zoom_result = self._process_zoom_screenshot(obs.get("screenshot_original"), tool_input)
                    if isinstance(zoom_result, dict) and "error" in zoom_result:
                        self.add_tool_result(tool_block["id"], zoom_result["error"], screenshot=None)
                        continue
                    include_screenshot = zoom_result
                elif obs and self.auto_screenshot and is_last_tool:
                    include_screenshot = obs.get("screenshot")

                self.add_tool_result(
                    tool_block["id"],
                    result="Success",
                    screenshot=include_screenshot,
                    extra_screenshots=extra_screenshots,
                )

        enable_prompt_caching = False
        betas = [] if self.batch_tool_prompt else [COMPUTER_USE_BETA_FLAG]

        # Add interleaved thinking beta if ISP is requested
        if self.thinking_mode == "isp":
            betas.append("interleaved-thinking-2025-05-14")
            logger.info(f"Added interleaved thinking beta. Betas: {betas}")

        image_truncation_threshold = 10
        if self.provider == APIProvider.ANTHROPIC:
            client = Anthropic(
                base_url=self.base_url,
                api_key=self.api_key,
                max_retries=4
            )
            enable_prompt_caching = True
        # elif self.provider == APIProvider.VERTEX:
        #     client = AnthropicVertex()
        # elif self.provider == APIProvider.BEDROCK:
        #     client = AnthropicBedrock(
        #         # Authenticate by either providing the keys below or use the default AWS credential providers, such as
        #         # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
        #         aws_access_key=os.getenv('AWS_ACCESS_KEY_ID'),
        #         aws_secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        #         # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
        #         # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
        #         aws_region=os.getenv('AWS_DEFAULT_REGION'),
        #     )

        if enable_prompt_caching:
            # betas.append(PROMPT_CACHING_BETA_FLAG)
            _inject_prompt_caching(self.messages)
            image_truncation_threshold = 5
            # system["cache_control"] = {"type": "ephemeral"}

        if self.only_n_most_recent_images:
            _maybe_filter_to_n_most_recent_images(
                self.messages,
                self.only_n_most_recent_images,
                min_removal_threshold=image_truncation_threshold,
            )

        if self.batch_tool_prompt:
            tools = [_build_batched_tool_schema(self.qwen3_tools)]
            logger.info(f"Using custom batched computer tool schema (qwen3_tools={self.qwen3_tools})")
        else:
            tools = [{
                'name': 'computer',
                'type': COMPUTER_USE_TYPE,
                'display_width_px': self.input_screen_width,
                'display_height_px': self.input_screen_height,
                'display_number': 0,
            }]

        extra_body, actual_max_tokens = self._get_thinking_request()

        try:
            response = None

            for attempt in range(API_RETRY_TIMES):
                try:
                    response = self._call_model_with_logging(
                        client=client,
                        messages=self.messages,
                        system=system,
                        tools=tools,
                        betas=betas,
                        extra_body=extra_body,
                        actual_max_tokens=actual_max_tokens,
                        **self._get_output_config(),
                    )
                    logger.info(f"Response: {response}")
                    break
                except (APIError, APIStatusError, APIResponseValidationError) as e:
                    error_msg = str(e)
                    logger.warning(f"Anthropic API error (attempt {attempt+1}/{API_RETRY_TIMES}): {error_msg}")

                    if "25000000" in error_msg or "Member must have length less than or equal to" in error_msg:
                        logger.warning("Detected 25MB limit error, automatically reducing image count")
                        current_image_count = self.only_n_most_recent_images
                        new_image_count = max(1, current_image_count // 2)  # Keep at least 1 image
                        self.only_n_most_recent_images = new_image_count

                        _maybe_filter_to_n_most_recent_images(
                            self.messages,
                            new_image_count,
                            min_removal_threshold=image_truncation_threshold,
                        )
                        logger.info(f"Image count reduced from {current_image_count} to {new_image_count}")

                    if attempt < API_RETRY_TIMES - 1:
                        time.sleep(API_RETRY_INTERVAL)
                    else:
                        raise  # All attempts failed, raise exception to enter existing except logic

        except (APIError, APIStatusError, APIResponseValidationError) as e:
            logger.exception(f"Anthropic API error: {str(e)}")
            try:
                logger.warning("Retrying with backup API key...")

                backup_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY_BACKUP"), max_retries=4).with_options(
                    default_headers={"anthropic-beta": COMPUTER_USE_BETA_FLAG}
                )
                with backup_client.beta.messages.stream(
                        max_tokens=actual_max_tokens,
                        messages=self.messages,
                        model=PROVIDER_TO_DEFAULT_MODEL_NAME[self.provider, self.model_name],
                        system=[system],
                        cache_control={"type": "ephemeral"},
                        tools=tools,
                        betas=betas,
                        extra_body=extra_body,
                        **self._get_output_config(),
                        **self._get_sampling_params()
                ) as stream:
                    response = stream.get_final_message()

                logger.info("Successfully used backup API key")

            except Exception as backup_e:
                backup_error_msg = str(backup_e)
                logger.exception(f"Backup API call also failed: {backup_error_msg}")

                # Check if backup API also has 25MB limit error
                if "25000000" in backup_error_msg or "Member must have length less than or equal to" in backup_error_msg:
                    logger.warning("Backup API also encountered 25MB limit error, further reducing image count")
                    # Reduce image count by half again
                    current_image_count = self.only_n_most_recent_images
                    new_image_count = max(1, current_image_count // 2)  # Keep at least 1 image
                    self.only_n_most_recent_images = new_image_count

                    # Reapply image filtering
                    _maybe_filter_to_n_most_recent_images(
                        self.messages,
                        new_image_count,
                        min_removal_threshold=image_truncation_threshold,
                    )
                    logger.info(f"Backup API image count reduced from {current_image_count} to {new_image_count}")

                return None, None

        except Exception as e:
            logger.exception(f"Error in Anthropic API: {str(e)}")
            return None, None

        if response is None:
            logger.error("Response is None after API call - this should not happen")
            return None, None

        response_params = _response_to_params(response) # 用于构建训练数据
        # Bedrock API 与 最新 Anthropic 包兼容
        # for p in response_params:
        #     if "caller" in p:
        #         del p["caller"]
            # if "signature" in p:
            #     del p["signature"]

        # Store response in message history
        self.messages.append({
            "role": "assistant",
            "content": response_params
        })


        # Convert raw response to concatenated string for trajectory logging
        raw_response_str = self._extract_raw_response_string(response)

        max_parse_retry = 3
        for parse_retry in range(max_parse_retry):
            actions: list[Any] = []
            reasonings: list[str] = []
            try:
                for content_block in response_params:
                    if content_block["type"] == "tool_use":
                        tool_name = content_block.get("name")
                        tool_input = cast(dict[str, Any], content_block.get("input") or {})

                        if tool_name == "computer":
                            if isinstance(tool_input.get("actions"), list):
                                combined_command = ""
                                coordinates = []
                                for sub_action in tool_input["actions"]:
                                    sub_tool_call = {"name": "computer", "input": sub_action}
                                    command, return_coord = self.parse_actions_from_tool_call(sub_tool_call)
                                    combined_command += command
                                    if return_coord is not None:
                                        coordinates.append(return_coord)
                                coordinate = coordinates[0] if len(coordinates) == 1 else (coordinates or None)
                            else:
                                combined_command, coordinate = self.parse_actions_from_tool_call(content_block)
                            actions.append({
                                "name": tool_name,
                                "input": tool_input,
                                "id": content_block["id"],
                                "action_type": content_block.get("type"),
                                "command": combined_command,
                                "coordinate": coordinate,
                                "kind": "gui",
                                "assistant_content": response_params,
                            })
                    elif content_block["type"] == "text" or content_block["type"] == "thinking":
                        reasonings.append(content_block[content_block["type"]])

                if isinstance(reasonings, list) and len(reasonings) > 0:
                    reasonings = ''.join(reasonings)
                else:
                    reasonings = ""

                logger.info(f"Received actions: {actions}")
                logger.info(f"Received reasonings: {reasonings}")

                # Check if the model indicated the task is infeasible
                if raw_response_str and "[INFEASIBLE]" in raw_response_str:
                    logger.info("Detected [INFEASIBLE] pattern in response, triggering FAIL action")
                    # Override actions with FAIL
                    actions = [{
                        "name": "fail",
                        "command": "FAIL",
                        "action_type": "FAIL",
                        "kind": "general",
                        "assistant_content": response_params,
                    }]

                # if len(actions) == 0 and obs and obs.get("allow_ask_user"):
                #     return [{
                #         "raw_response": raw_response_str,
                #         "thought": reasonings,
                #         "action": "ASK_USER",
                #         "meta_action": None,
                #         "coordinate": None,
                #     }], []

                if len(actions) == 0:
                    actions = [{
                        "name": "done",
                        "command": "DONE",
                        "action_type": "DONE",
                        "kind": "general",
                        "assistant_content": response_params,
                    }]

                response_meta_list = []
                qwen_unsupported_action_flag = False
                qwen_has_trainable_action = False
                # If there are tool calls, create a meta_item for each
                for action in actions:
                    action_input = action.get("input", {})
                    action_inputs = action_input.get("actions") if isinstance(action_input.get("actions"), list) else [action_input]
                    for single_input in action_inputs:
                        if not isinstance(single_input, dict):
                            continue
                        if single_input.get("action") in {"hold_key", "left_mouse_down", "left_mouse_up", "zoom"}:
                            qwen_unsupported_action_flag = True
                        elif single_input.get("action") != "screenshot":
                            qwen_has_trainable_action = True

                    meta_item = {
                        "raw_response": raw_response_str,
                        "thought": reasonings,
                        "action": action.get("command", ""),
                        "meta_action": action,
                        "coordinate": action.get("coordinate")
                    }
                    response_meta_list.append(meta_item)

                pyautogui_actions = []
                for a in actions:
                    cmd = a.get("command", "")
                    kind = a.get("kind", "")

                    if kind == "bash":
                        pyautogui_actions.append(f"BASH|{cmd}")
                    elif kind == "python":
                        pyautogui_actions.append(f"PYTHON|{cmd}")
                    else:
                        pyautogui_actions.append(cmd)

                # ===== Qwen3VL SFT 收集（可选）=====
                if self.collect_qwen_sft and response_meta_list and not qwen_unsupported_action_flag and qwen_has_trainable_action:
                    try:
                        sft_messages = deepcopy(self.messages)
                        if len(actions) == 1 and actions[0].get("command") in {"FAIL", "DONE"}:
                            terminate_block = {
                                "type": "tool_use",
                                "name": "terminate",
                                "input": {
                                    "status": "success" if actions[0].get("command") == "DONE" else "failure"
                                },
                            }
                            if sft_messages and sft_messages[-1].get("role") == "assistant":
                                sft_messages[-1].setdefault("content", []).append(terminate_block)

                        sample, self.qwen_sft_image_hash_map = build_qwen_sft_sample(
                            messages=sft_messages, # 包含所有历史信息与当前步模型的输出, 但不包含 System
                            screen_size=(self.input_screen_width, self.input_screen_height),
                            image_hash_map=self.qwen_sft_image_hash_map,
                            image_root_dir=self.collect_qwen_sft_image_dir,
                            max_history_images=8
                        )
                        response_meta_list[0]["agent_sft"] = sample
                    except Exception as e:
                        logger.error(f'build_qwen_sft_sample error: {e}')

                return response_meta_list, pyautogui_actions
            except Exception as e:
                logger.warning(f"parse_actions_from_tool_call parsing failed (attempt {parse_retry+1}/3), will retry API request: {e}")
                # Remove the recently appended assistant message to avoid polluting history
                self.messages.pop()
                # Retry API request
                response = None
                for attempt in range(API_RETRY_TIMES):
                    try:
                        with client.beta.messages.stream(
                                max_tokens=actual_max_tokens,
                                messages=self.messages,
                                model=PROVIDER_TO_DEFAULT_MODEL_NAME[self.provider, self.model_name],
                                system=[system],
                                # cache_control={"type": "ephemeral"},
                                tools=tools,
                                betas=betas,
                                extra_body=extra_body,
                                **self._get_output_config(),
                                **self._get_sampling_params()
                        ) as stream:
                            response = stream.get_final_message()

                        # logger.info(f"Response: {response}")
                        break  # Success, exit retry loop
                    except (APIError, APIStatusError, APIResponseValidationError) as e2:
                        error_msg = str(e2)
                        logger.warning(f"Anthropic API error (attempt {attempt+1}/{API_RETRY_TIMES}): {error_msg}")
                        if attempt < API_RETRY_TIMES - 1:
                            time.sleep(API_RETRY_INTERVAL)
                        else:
                            raise

                response_params = _response_to_params(response)
                for p in response_params:
                    if "caller" in p:
                        del p["caller"]        # ← Bedrock 兼容处理
                    # if "signature" in p:
                    #     del p["signature"]

                # logger.info(f"Received response params: {response_params}")

                # Update raw response string for retry case (will be used in next loop iteration)
                raw_response_str = self._extract_raw_response_string(response)

                self.messages.append({
                    "role": "assistant",
                    "content": response_params
                })
                if parse_retry == max_parse_retry - 1:
                    logger.error(f"parse_actions_from_tool_call parsing failed 3 times consecutively, terminating: {e}")
                    actions = [{
                        "name": "fail",
                        "action_type": "FAIL",
                        "command": "FAIL",
                        "kind": "general",
                        "assistant_content": response_params,
                    }]

                    response_meta_list = []
                    for action in actions:
                        meta_item = {
                            "raw_response": raw_response_str,
                            "thought": f"Failed to parse actions from tool call after {max_parse_retry} attempts: {e}",
                            "action": f"Failed to parse actions from tool call after {max_parse_retry} attempts: {e}",
                            "meta_action": action,
                            "coordinate": None
                        }
                        response_meta_list.append(meta_item)
                    if isinstance(actions, list) and all(isinstance(a, dict) for a in actions):
                        pyautogui_actions = [a["command"] for a in actions]
                    return response_meta_list, pyautogui_actions

    def evaluate(self, task_instruction: str, obs: Dict, **kwargs) -> Dict[str, Any]:
        """
        Self-judge function to evaluate if the task was completed successfully.
        """
        try:
            # 1. Start with Evaluation System Prompt
            eval_system = BetaTextBlockParam(
                type="text",
                text=SYSTEM_PROMPT_ORM
            )

            # 1.5 Add obs as the tool result **Important**
            if self.messages:
                last_message_content = self.messages[-1]["content"]
                tool_use_blocks = [block for block in last_message_content if block.get("type") == "tool_use"]

                for i, tool_block in enumerate(tool_use_blocks):
                    tool_input = tool_block.get("input", {})
                    action = tool_input.get("action")
                    is_last_tool = i == len(tool_use_blocks) - 1

                    include_screenshot = None

                    if obs and is_last_tool:
                        include_screenshot = obs.get("screenshot")

                    self.add_tool_result(
                        tool_block["id"],
                        f"Success",
                        screenshot=include_screenshot
                    )

            # 2. Reuse the exact same history construction as predict
            # We copy the existing messages so we don't pollute the agent's history
            eval_messages = list(self.messages)

            # 3. Add Final Observation and Evaluation Query
            eval_query = f"Based on the conversation history above and this final screenshot, did the agent successfully complete the instruction: '{task_instruction}'? Please provide the JSON evaluation."

            eval_messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": eval_query
                    }
                ]
            })

            logger.info(f"Starting evaluation for: {task_instruction}")

            # 4. Call LLM
            if self.provider == APIProvider.ANTHROPIC:
                client = Anthropic(
                    base_url=self.base_url,
                    api_key=self.api_key,
                    max_retries=4
                )
            elif self.provider == APIProvider.VERTEX:
                client = AnthropicVertex()
            elif self.provider == APIProvider.BEDROCK:
                client = AnthropicBedrock(
                    aws_access_key=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    aws_region=os.getenv('AWS_DEFAULT_REGION'),
                )

            extra_body, actual_max_tokens = self._get_thinking_request()

            with client.beta.messages.stream(
                max_tokens=actual_max_tokens,
                messages=eval_messages,
                model=PROVIDER_TO_DEFAULT_MODEL_NAME[self.provider, self.model_name],
                system=[eval_system],
                extra_body=extra_body,
                **self._get_output_config(),
                **self._get_sampling_params()
            ) as stream:
                response = stream.get_final_message()

            raw_response_str = self._extract_raw_response_string(response=response)
            logger.info(f"Evaluation Raw Output: {raw_response_str}")

            # 5. Parse JSON
            # Handle potential markdown wrappers
            if "```json" in raw_response_str:
                json_str = raw_response_str.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_response_str:
                json_str = raw_response_str.split("```")[1].strip()
            else:
                json_str = raw_response_str.strip()

            result = json.loads(json_str)

            # Ensure required fields exist
            if "thought" not in result:
                result["thought"] = raw_response_str
            if "score" not in result:
                # Fallback logic if score is missing but status is present
                result["score"] = 0.0

            return result

        except Exception as e:
            import traceback
            logger.error(f"Evaluation failed: {e}")
            logger.error(traceback.format_exc())
            return {
                "thought": f"Evaluation failed due to error: {str(e)}",
                "score": 0.0
            }

    def reset(self, _logger = None, *args, **kwargs):
        """
        Reset the agent's state.
        """
        global logger
        if _logger:
            logger = _logger
        else:
            logger = logging.getLogger("desktopenv.agent")
        self.messages = []
        self.current_step = 0
        logger.info(f"{self.class_name} reset.")
