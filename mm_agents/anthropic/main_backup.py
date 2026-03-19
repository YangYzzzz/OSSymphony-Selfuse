import base64
import os
import time
from typing import Any, cast, Optional, Dict
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
from .utils import get_model_name, COMPUTER_USE_BETA_FLAG, PROMPT_CACHING_BETA_FLAG, SYSTEM_PROMPT, SYSTEM_PROMPT_WINDOWS, APIProvider, PROVIDER_TO_DEFAULT_MODEL_NAME, COMPUTER_USE_TYPE
from .utils import _response_to_params, _inject_prompt_caching, _maybe_filter_to_n_most_recent_images

import logging
logger = logging.getLogger("desktopenv.agent")

# MAX_HISTORY = 10
API_RETRY_TIMES = 500  
API_RETRY_INTERVAL = 5

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
                no_thinking: bool = False,
                use_isp: bool = False,
                temperature: Optional[float] = None,
                top_p: Optional[float] = None,
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
        self.no_thinking = no_thinking
        self.use_isp = use_isp
        self.temperature = temperature
        self.top_p = top_p
        self.resize_factor = (
            screen_size[0] / 1280,  # Assuming 1280 is the base width
            screen_size[1] / 720   # Assuming 720 is the base height
        )

    def _get_sampling_params(self):
        """Get sampling parameters (temperature and/or top_p) - let API validate exclusivity"""
        params = {}
        if self.temperature is not None:
            params['temperature'] = self.temperature
        if self.top_p is not None:
            params['top_p'] = self.top_p
        return params
    
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
    
    def add_tool_result(self, tool_call_id: str, result: str, screenshot: bytes = None):
        """Add tool result to message history"""
        tool_result_content = [
            {
                "type": "tool_result",
                "tool_use_id": tool_call_id,
                "content": [{"type": "text", "text": result}]
            }
        ]
        
        # Add screenshot if provided
        if screenshot is not None:
            screenshot_base64 = base64.b64encode(screenshot).decode('utf-8')
            tool_result_content[0]["content"].append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png", 
                    "data": screenshot_base64
                }
            })
        
        self.messages.append({
            "role": "user",
            "content": tool_result_content
        })
    
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
            result += "pyautogui.sleep(0.5)\n"
        elif action == "fail":
            result += "FAIL"
        elif action == "done":
            result += "DONE"
        elif action == "call_user":
            result += "CALL_USER"
        elif action == "screenshot":
            result += "pyautogui.sleep(0.1)\n"
        else:
            raise ValueError(f"Invalid action: {action}")

        return result, return_coord
            
    def predict(self, task_instruction: str, obs: Dict = None, system: Any = None):
        system = BetaTextBlockParam(
            type="text",
            text=f"{SYSTEM_PROMPT_WINDOWS if self.platform == 'Windows' else SYSTEM_PROMPT}{' ' + self.system_prompt_suffix if self.system_prompt_suffix else ''}"
        )
        
        # resize screenshot if resize_factor is set
        if obs and "screenshot" in obs:
            # Convert bytes to PIL Image
            screenshot_bytes = obs["screenshot"]
            screenshot_image = Image.open(io.BytesIO(screenshot_bytes))
            
            # Calculate new size based on resize factor
            new_width, new_height = 1280, 720
            
            # Resize the image
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format='PNG')
            obs["screenshot"] = output_buffer.getvalue()
            

        if not self.messages:
            
            init_screenshot = obs
            init_screenshot_base64 = base64.b64encode(init_screenshot["screenshot"]).decode('utf-8')
            self.messages.append({
                "role": "user",
                "content": [
                    {
                    "type": "image",
                    "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": init_screenshot_base64,
                        },
                    },
                    {"type": "text", "text": task_instruction},
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
                
                if obs:
                    if action == "screenshot":
                        # Screenshot action always gets regular screenshot
                        include_screenshot = obs.get("screenshot")
                    elif is_last_tool:
                        # Auto-screenshot: last tool gets regular screenshot (unless it's zoom, handled above)
                        include_screenshot = obs.get("screenshot")
                
                self.add_tool_result(
                    tool_block["id"],
                    f"Success",
                    screenshot=include_screenshot
                )
            
        enable_prompt_caching = False
        betas = [COMPUTER_USE_BETA_FLAG]

        # Add interleaved thinking beta if ISP is requested
        if self.use_isp:
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
        elif self.provider == APIProvider.VERTEX:
            client = AnthropicVertex()
        elif self.provider == APIProvider.BEDROCK:
            client = AnthropicBedrock(
                # Authenticate by either providing the keys below or use the default AWS credential providers, such as
                # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
                aws_access_key=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
                # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
                aws_region=os.getenv('AWS_DEFAULT_REGION'),
            )

        if enable_prompt_caching:
            # betas.append(PROMPT_CACHING_BETA_FLAG)
            _inject_prompt_caching(self.messages)
            image_truncation_threshold = 50
            # system["cache_control"] = {"type": "ephemeral"}

        if self.only_n_most_recent_images:
            _maybe_filter_to_n_most_recent_images(
                self.messages,
                self.only_n_most_recent_images,
                min_removal_threshold=image_truncation_threshold,
            )

        # Configure tool settings - use modern computer tool for all models
        tool_config = {
            'name': 'computer', 
            'type': COMPUTER_USE_TYPE,
            'display_width_px': 1280, 
            'display_height_px': 720, 
            'display_number': 1
        }
        
        tools = [
            tool_config,
        ] if self.platform == 'Ubuntu' else [
            tool_config,
        ]

        if self.no_thinking:
            # Disable thinking mode - omit the thinking parameter
            extra_body = {}
            actual_max_tokens = self.max_tokens  # Use default when no thinking
            logger.info("Thinking mode: DISABLED")
        else:
            # Enable thinking mode (regular or interleaved)
            # Use consistent 2048 budget for both regular and ISP thinking
            budget_tokens = 2048
            
            # For regular thinking: max_tokens > budget_tokens (API requirement)
            # For ISP: budget_tokens can exceed max_tokens (represents total across all thinking blocks)
            if self.max_tokens <= budget_tokens:
                required_max_tokens = budget_tokens + 500  # Give some headroom
                logger.warning(f"Regular thinking requires max_tokens > budget_tokens. Increasing max_tokens from {self.max_tokens} to {required_max_tokens}")
                actual_max_tokens = required_max_tokens
            else:
                actual_max_tokens = self.max_tokens
            
            extra_body = {
                "thinking": {"type": "enabled", "budget_tokens": budget_tokens}
            }
            if self.use_isp:
                logger.info("Thinking mode: INTERLEAVED SCRATCHPAD (ISP)")
            else:
                logger.info("Thinking mode: REGULAR SCRATCHPAD")

        try:
            response = None
            
            for attempt in range(API_RETRY_TIMES):
                try:
                    with client.beta.messages.stream(
                            max_tokens=actual_max_tokens,
                            messages=self.messages,
                            model=PROVIDER_TO_DEFAULT_MODEL_NAME[self.provider, self.model_name],
                            system=[system],
                            cache_control={"type": "ephemeral"},
                            tools=tools,
                            betas=betas,
                            extra_body=extra_body,
                            **self._get_sampling_params()
                        ) as stream:
                            response = stream.get_final_message()
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
        
        response_params = _response_to_params(response)

        # Convert raw response to concatenated string for trajectory logging
        raw_response_str = self._extract_raw_response_string(response)

        # Store response in message history
        self.messages.append({
            "role": "assistant",
            "content": response_params
        })

        max_parse_retry = 3
        for parse_retry in range(max_parse_retry):
            actions: list[Any] = []
            reasonings: list[str] = []
            try:
                for content_block in response_params:
                    if content_block["type"] == "tool_use":
                        command, return_coord = self.parse_actions_from_tool_call(content_block)
                        actions.append({
                            "name": content_block["name"],
                            "input": cast(dict[str, Any], content_block["input"]),
                            "id": content_block["id"],
                            "action_type": content_block.get("type"),
                            "command": command,
                            "coordinate": return_coord
                        })
                    elif content_block["type"] == "text":
                        reasonings.append(content_block["text"])

                if isinstance(reasonings, list) and len(reasonings) > 0:
                    reasonings = reasonings[0]
                else:
                    reasonings = ""

                logger.info(f"Received actions: {actions}")
                logger.info(f"Received reasonings: {reasonings}")

                # Check if the model indicated the task is infeasible
                if raw_response_str and "[INFEASIBLE]" in raw_response_str:
                    logger.info("Detected [INFEASIBLE] pattern in response, triggering FAIL action")
                    # Override actions with FAIL
                    actions = [{
                        "command": "FAIL",
                        "action_type": "FAIL"
                    }]
                
                if len(actions) == 0:
                    actions = [{
                        "command": "DONE",
                        "action_type": "DONE"
                    }]

                response_meta_list = []
                # If there are tool calls, create a meta_item for each
                for action in actions:
                    meta_item = {
                        "raw_response": str(response_params),
                        "thought": reasonings,
                        "action": action.get("command", ""),
                        "meta_action": action,
                        "coordinate": action.get("coordinate")
                    }
                    response_meta_list.append(meta_item)


                pyautogui_actions = []
                if isinstance(actions, list) and all(isinstance(a, dict) for a in actions):
                    pyautogui_actions = [a["command"] for a in actions]
                else:
                    pyautogui_actions = actions

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
                                cache_control={"type": "ephemeral"},
                                tools=tools,
                                betas=betas,
                                extra_body=extra_body,
                                **self._get_sampling_params()
                        ) as stream:
                            response = stream.get_final_message()

                        logger.info(f"Response: {response}")
                        break  # Success, exit retry loop
                    except (APIError, APIStatusError, APIResponseValidationError) as e2:
                        error_msg = str(e2)
                        logger.warning(f"Anthropic API error (attempt {attempt+1}/{API_RETRY_TIMES}): {error_msg}")
                        if attempt < API_RETRY_TIMES - 1:
                            time.sleep(API_RETRY_INTERVAL)
                        else:
                            raise

                response_params = _response_to_params(response)
                logger.info(f"Received response params: {response_params}")

                # Update raw response string for retry case (will be used in next loop iteration)
                raw_response_str = self._extract_raw_response_string(response)

                self.messages.append({
                    "role": "assistant",
                    "content": response_params
                })
                if parse_retry == max_parse_retry - 1:
                    logger.error(f"parse_actions_from_tool_call parsing failed 3 times consecutively, terminating: {e}")
                    actions = [{
                        "action_type": "FAIL",
                        "command": "FAIL"
                    }]

                    response_meta_list = []
                    for action in actions:
                        meta_item = {
                            "raw_response": str(response_params),
                            "thought": f"Failed to parse actions from tool call after {max_parse_retry} attempts: {e}",
                            "action": f"Failed to parse actions from tool call after {max_parse_retry} attempts: {e}",
                            "meta_action": action,
                            "coordinate": None
                        }
                        response_meta_list.append(meta_item)
                    if isinstance(actions, list) and all(isinstance(a, dict) for a in actions):
                        pyautogui_actions = [a["command"] for a in actions]
                    return response_meta_list, pyautogui_actions

    def evaluate(self, task_instruction: str, obs: Dict) -> Dict[str, Any]:
        """
        Self-judge function to evaluate if the task was completed successfully.
        """
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
        Only return the JSON object, do not add any other text.
        """

        try:
            # 1. Start with Evaluation System Prompt
            eval_system = BetaTextBlockParam(
                type="text",
                text=EVALUATION_SYSTEM_PROMPT.format(instruction=task_instruction)
            )

            # 2. Reuse the exact same history construction as predict
            # We copy the existing messages so we don't pollute the agent's history
            eval_messages = list(self.messages)

            # 3. Add Final Observation and Evaluation Query
            eval_query = f"Based on the conversation history above and this final screenshot, did the agent successfully complete the instruction: '{task_instruction}'? Please provide the JSON evaluation."

            # Use base64 encoded screenshot if it's not already
            screenshot_data = obs["screenshot"]
            if isinstance(screenshot_data, bytes):
                screenshot_base64 = base64.b64encode(screenshot_data).decode('utf-8')
            else:
                screenshot_base64 = screenshot_data

            eval_messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": screenshot_base64,
                        },
                    },
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

            if self.no_thinking:
                extra_body = {}
            else:
                extra_body = {
                    "thinking": {"type": "enabled", "budget_tokens": 2048}
                }
        
            with client.beta.messages.stream(
                max_tokens=self.max_tokens,
                messages=self.messages,
                model=PROVIDER_TO_DEFAULT_MODEL_NAME[self.provider, self.model_name],
                system=[eval_system],
                extra_body=extra_body,
                **self._get_sampling_params()
            ) as stream:
                response = stream.get_final_message()

            raw_response_str = self._extract_raw_response_string(response=response)
            logger.info(f"Evaluation Raw Output: {raw_response_str}")

            import json
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
        logger.info(f"{self.class_name} reset.")

