import json
import logging
import re
import os
import ast
import time
import math
import httpx
import base64
import backoff
import traceback
from loguru import logger
from typing import Any, Dict, List, Tuple, Optional

def encode_image(image_content):
    return base64.b64encode(image_content).decode("utf-8")

INSTRUCTION_TEMPLATE = "# Task Instruction:\n{instruction}\n\nPlease generate the next move according to the screenshot, task instruction and previous steps (if provided).\n"

STEP_TEMPLATE = "# Step {step_num}:\n"

SYSTEM_PROMPT_THINKING = """
You are a GUI agent. You are given an instruction, a screenshot of the screen and your previous interactions with the computer. You need to perform a series of actions to complete the task. The password of the computer is {password}. 

For each step, provide your response in this format:
{thought}
## Action:
{action}
## Code:
{code}

In the code section, the code should be either pyautogui code or one of the following functions wrapped in the code block:
- {"name": "computer.wait", "description": "Make the computer wait for 20 seconds for installation, running code, etc.", "parameters": {"type": "object", "properties": {}, "required": []}}
- {"name": "computer.terminate", "description": "Terminate the current task and report its completion status", "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["success", "failure"], "description": "The status of the task"}, "answer": {"type": "string", "description": "The answer of the task"}}, "required": ["status"]}}
""".strip()

SYSTEM_PROMPT_NON_THINKING = """
You are a GUI agent. You are given an instruction, a screenshot of the screen and your previous interactions with the computer. You need to perform a series of actions to complete the task. The passoword of the computer is {password}.

For each step, provide your response in this format:
## Thought
{thought}
## Action:
{action}
## Code:
{code}

In the code section, the code should be either pyautogui code or one of the following functions wrapped in the code block:
- {"name": "computer.wait", "description": "Make the computer wait for 20 seconds for installation, running code, etc.", "parameters": {"type": "object", "properties": {}, "required": []}}
- {"name": "computer.terminate", "description": "Terminate the current task and report its completion status", "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["success", "failure"], "description": "The status of the task"}, "answer": {"type": "string", "description": "The answer of the task"}}, "required": ["status"]}}
""".strip()

THOUGHT_HISTORY_TEMPLATE_THINKING = "◁think▷{thought}◁/think▷## Action:\n{action}\n"
THOUGHT_HISTORY_TEMPLATE_NON_THINKING = "## Thought:\n{thought}\n\n## Action:\n{action}\n"


def parse_response_to_cot_and_action(response, screen_size, coordinate_type, thinking:bool) -> Tuple[str, List[str], dict]:
    """Parse response including Observation, Thought, Action and code block"""
    logger.warning(f"Response: {response}")
    input_string = response['content'].lstrip()

    sections = {}
    try:
        if thinking:
            thought = response.get('reasoning_content', '').strip()
            sections['thought'] = thought
            sections['raw_response'] = '<reasoning_content>' + thought + '</reasoning_content>' + input_string
            logger.info(f"Extracted thought (thinking): {sections['thought']}")
            m = re.search(r"^##\s*Action\b", input_string, flags=re.MULTILINE) # remove extra content before ## Action
            if m:
                input_string = input_string[m.start():]
        else:
            thought = re.search(r'^##\s*Thought\s*:?[\n\r]+(.*?)(?=^##\s*Action:|^##|\Z)', input_string, re.DOTALL | re.MULTILINE)
            if thought:
                sections['thought'] = thought.group(1).strip()
            else:
                sections['thought'] = ""
            sections['raw_response'] = input_string
            logger.info(f"Extracted thought (non-thinking): {sections['thought']}")
        
        code_blocks = re.findall(r'```(?:code|python)?\s*(.*?)\s*```', input_string, re.DOTALL | re.IGNORECASE)
        if not code_blocks:
            logger.error("No code blocks found in the input string")
            return f"<Error>: no code blocks found in the input string: {input_string}", ["FAIL"], sections

        code_block = code_blocks[-1].strip()
        sections['original_code'] = code_block

        # FIX: 去除正则前的^
        # FIX: 若认为 code_blocks[-1] 是真正执行的 code, 则 action 字段也应取最后一个匹配到的结果
        action_matches = re.findall(
            r'\s*##\s*Action\s*:?\s*[\n\r]+(.*?)(?=^\s*##|\Z)',
            input_string, re.DOTALL | re.MULTILINE
        )
        if action_matches:
            action = action_matches[-1].strip()
            sections['action'] = action + "\n" + sections['original_code'] # Action + Code

        if "computer.wait" in code_block.lower():
            sections["code"] = "WAIT"
            return sections['action'], ["WAIT"], sections
        elif "computer.terminate" in code_block.lower():
            lower_block = code_block.lower()
            if ("failure" in lower_block) or ("fail" in lower_block):
                sections['code'] = "FAIL"
                return code_block, ["FAIL"], sections
            elif "success" in lower_block:
                sections['code'] = "DONE"
                return code_block, ["DONE"], sections
            else:
                logger.error("Terminate action found but no specific status provided in code block")
                return f"<Error>: terminate action found but no specific status provided in code block: {input_string}", ["FAIL"], sections

        corrected_code, extracted_coordinates = project_coordinate_to_absolute_scale(
            code_block, 
            screen_width=screen_size[0], 
            screen_height=screen_size[1], 
            coordinate_type=coordinate_type
        )
        
        sections['code'] = corrected_code
        sections['coordinate'] = extracted_coordinates # 将绝对坐标存入 meta_action (sections)

        if ('code' not in sections or sections['code'] is None or sections['code'] == "") or ('action' not in sections or sections['action'] is None or sections['action'] == ""):
            logger.error("Missing required action or code section")
            return f"<Error>: no code parsed: {input_string}", ["FAIL"], sections

        return sections['action'], [sections['code']], sections
        
    except Exception as e:
        error_message = f"<Error>: parsing response: {str(e)}\nTraceback:\n{traceback.format_exc()}\nInput string: {input_string}"
        logger.exception(error_message)
        return error_message, ['FAIL'], sections


def project_coordinate_to_absolute_scale(pyautogui_code_relative_coordinates, screen_width, screen_height, coordinate_type="relative"):
    """
    Convert the relative coordinates in the pyautogui code to absolute coordinates based on the logical screen size.
    """
    def _coordinate_projection(x, y, screen_width, screen_height, coordinate_type):
        if x<=1.0 and y<=1.0:
            return int(round(x * screen_width)), int(round(y * screen_height))
        else:
            return int(round(x)), int(round(y))
            
    pattern = r'(pyautogui\.\w+\([^\)]*\))'
    matches = re.findall(pattern, pyautogui_code_relative_coordinates)

    new_code = pyautogui_code_relative_coordinates
    last_extracted_coordinates = None # 用于存储提取到的绝对坐标

    for full_call in matches:
        func_name_pattern = r'(pyautogui\.\w+)\((.*)\)'
        func_match = re.match(func_name_pattern, full_call, re.DOTALL)
        if not func_match:
            continue

        func_name = func_match.group(1)
        args_str = func_match.group(2)

        try:
            parsed = ast.parse(f"func({args_str})").body[0].value
            parsed_args = parsed.args
            parsed_keywords = parsed.keywords

        except SyntaxError:
            return pyautogui_code_relative_coordinates, None

        function_parameters = {
            'click': ['x', 'y', 'clicks', 'interval', 'button', 'duration', 'pause'],
            'rightClick':  ['x', 'y', 'duration', 'tween', 'pause'],
            'middleClick': ['x', 'y', 'duration', 'tween', 'pause'],
            'doubleClick': ['x', 'y', 'interval', 'button', 'duration', 'pause'],
            'tripleClick': ['x', 'y', 'interval', 'button', 'duration', 'pause'],
            'moveTo': ['x', 'y', 'duration', 'tween', 'pause'],
            'dragTo': ['x', 'y', 'duration', 'button', 'mouseDownUp', 'pause'],
        }

        func_base_name = func_name.split('.')[-1]

        param_names = function_parameters.get(func_base_name, [])

        args = {}
        for idx, arg in enumerate(parsed_args):
            if idx < len(param_names):
                param_name = param_names[idx]
                arg_value = ast.literal_eval(arg)
                args[param_name] = arg_value

        try:
            for kw in parsed_keywords:
                param_name = kw.arg
                arg_value = ast.literal_eval(kw.value)
                args[param_name] = arg_value
        except Exception as e:
            logger.error(f"Error parsing keyword arguments: {e}")
            return pyautogui_code_relative_coordinates, None

        updated = False
        if 'x' in args and 'y' in args:
            try:
                x_rel = float(args['x'])
                y_rel = float(args['y'])
                x_abs, y_abs = _coordinate_projection(x_rel, y_rel, screen_width, screen_height, coordinate_type)
                args['x'] = x_abs
                args['y'] = y_abs
                last_extracted_coordinates = [x_abs, y_abs]
                updated = True
            except ValueError:
                pass

        if updated:
            reconstructed_args = []
            for idx, param_name in enumerate(param_names):
                if param_name in args:
                    arg_value = args[param_name]
                    if isinstance(arg_value, str):
                        arg_repr = f"'{arg_value}'"
                    else:
                        arg_repr = str(arg_value)
                    reconstructed_args.append(arg_repr)
                else:
                    break

            used_params = set(param_names[:len(reconstructed_args)])
            for kw in parsed_keywords:
                if kw.arg not in used_params:
                    arg_value = args[kw.arg]
                    if isinstance(arg_value, str):
                        arg_repr = f"{kw.arg}='{arg_value}'"
                    else:
                        arg_repr = f"{kw.arg}={arg_value}"
                    reconstructed_args.append(arg_repr)

            new_args_str = ', '.join(reconstructed_args)
            new_full_call = f"{func_name}({new_args_str})"
            new_code = new_code.replace(full_call, new_full_call)

    return new_code, last_extracted_coordinates

def transform_action_to_code_block(action):
    if any(keyword in action for keyword in ["computer.terminate", "computer.wait", "browser.select_option", "browser.clear"]):
        return f"```code\n{action}\n```"
    else:
        return f"```python\n{action}\n```"

class KimiAgent:
    """
    KimiAgent: a desktop-automation agent powered by Kimi K2.5.

    This agent observes a desktop environment via screenshots and generates
    executable actions (e.g., mouse/keyboard operations) that can be applied
    through a GUI executor (such as PyAutoGUI) to complete automation tasks.

    Notes:
        - This is a beta feature of Kimi K2.5. APIs, prompt formats, and runtime
          behaviors may change, and occasional instability is expected.
    """
    def __init__(
            self,
            model: str, # Kimi model name, e.g. "kimi-k2.5"
            max_steps: int, # The max number of steps to finish the task
            max_image_history_length: int = 3, # The max number of images in the history
            platform: str = "ubuntu", # The platform of the computer
            max_tokens: int = 4096, # The max number of tokens in the response
            top_p: float = 0.95, # The top p value in the response
            temperature: float = 1, # The temperature value in the response
            action_space: str = "pyautogui", # The action space: pyautogui
            observation_type: str = "screenshot", # The observation type: screenshot
            screen_size: Tuple[int, int] = (1920, 1080), # The screen size
            coordinate_type: str = "relative", # The coordinate type: relative, absolute, qwen25
            password="osworld-public-evaluation", # The password for the ubuntu platform
            thinking: bool = True, # Whether to use thinking mode
            base_url: str = "",
            api_key: str = "",
            collect_qwen_sft: bool = False,
            collect_qwen_sft_image_dir: str = "",
            **kwargs
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
        self.password = password
        self.thinking = thinking
        self.base_url = base_url
        self.api_key = api_key
        if self.thinking:
            self.system_prompt = SYSTEM_PROMPT_THINKING.replace("{password}", self.password)
            self.history_template = THOUGHT_HISTORY_TEMPLATE_THINKING
        else:
            self.system_prompt = SYSTEM_PROMPT_NON_THINKING.replace("{password}", self.password)
            self.history_template = THOUGHT_HISTORY_TEMPLATE_NON_THINKING

        self.actions = []
        self.observations = []
        self.cots = []

        self.collect_qwen_sft = collect_qwen_sft
        self.collect_qwen_sft_image_dir = collect_qwen_sft_image_dir
        
    def reset(self, _logger=None):
        global logger
        logger = _logger if _logger is not None else logging.getLogger("desktopenv.agent")
        
        self.observations = []
        self.cots = []
        self.actions = []
    
    def _scale_scroll_for_windows(self, code: str, factor: int = 50) -> str:
        """ pyautogui.scroll has a different scale on Ubuntu and Windows, multiple 'factor' when scrolling on Windows system"""
        if self.platform.lower() != "windows":
            return code

        pattern_pos = re.compile(r'(pyautogui\.scroll\()\s*([-+]?\d+)\s*\)')
        code = pattern_pos.sub(lambda m: f"{m.group(1)}{int(m.group(2))*factor})", code)
        return code
    
    def _build_history_messages(self) -> List[Dict]:
        """
        Construct the history messages (User/Assistant pairs) based on previous steps.
        This logic is shared between predict() and evaluate().
        """
        messages = []
        history_step_texts = []
        
        for i in range(len(self.actions)):
            # Determine thought/action content
            thought = self.cots[i].get('thought', '')
            action = self.cots[i].get('action', '')
            
            # Format the assistant's response part
            history_content = STEP_TEMPLATE.format(step_num=i+1) + self.history_template.format(
                thought=thought,
                action=action
            )

            # Logic: If the step is within the recent window (max_image_history_length), 
            # we include the image. Otherwise, we just accumulate the text.
            if i > len(self.actions) - self.max_image_history_length:
                # Add User message with Image
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{encode_image(self.observations[i]['screenshot'])}"}
                        }
                    ]
                })
                # Add Assistant message
                messages.append({
                    "role": "assistant",
                    "content": history_content
                })
            else:
                # Accumulate text for older steps
                history_step_texts.append(history_content)
                # If this is the last step before the image window starts, dump all text history
                if i == len(self.actions) - self.max_image_history_length:
                    messages.append({
                        "role": "assistant",
                        "content": "\n".join(history_step_texts)
                    })
        
        return messages
        
    def predict(self, instruction: str, obs: Dict, **kwargs) -> Tuple[List[Dict], List[str]]:
        """
        Predict the next action(s) based on the current observation.
        """
        if "step_idx" in kwargs:
            logger.info(f"========= {self.model} Step {kwargs['step_idx']} =======")
        else:
            logger.info(f"========================== {self.model} ===================================")
        logger.info(f"Instruction: \n{instruction}")

        messages = []
        messages.append({
                "role": "system",
                "content": self.system_prompt
            })

        messages.extend(self._build_history_messages())

        instruction_prompt = INSTRUCTION_TEMPLATE.format(instruction=instruction)

        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encode_image(obs['screenshot'])}"}
                },
                {
                    "type": "text",
                    "text": instruction_prompt
                }
            ]
        })

        max_retry = 5
        retry_count = 0
        low_level_instruction = None
        pyautogui_actions = None
        other_cot = {}

        while retry_count < max_retry:
            try:
                response = self.call_llm({
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": self.max_tokens,
                    "top_p": self.top_p,
                    "temperature": self.temperature if retry_count==0 else max(0.2, self.temperature)
                }, self.model)

                logger.info(f"Model Output: \n{response}")
                if not response:
                    logger.error("No response found in the response.")
                    raise ValueError(f"No response found in the response:\n{response}.")

                low_level_instruction, pyautogui_actions, other_cot = parse_response_to_cot_and_action(response, self.screen_size, self.coordinate_type, thinking=self.thinking)
                if "<Error>" in low_level_instruction or not pyautogui_actions:
                    logger.error(f"Error parsing response: {low_level_instruction}")
                    raise ValueError(f"Error parsing response: {low_level_instruction}")
                break
                
            except Exception as e:
                logger.error(f"Error during message preparation: {e}")
                retry_count += 1
                if retry_count == max_retry:
                    logger.error("Maximum retries reached. Exiting.")
                    return str(e), ['FAIL']

        pyautogui_actions = [
            self._scale_scroll_for_windows(code) for code in pyautogui_actions
        ]
        logger.info(f"Action: \n{low_level_instruction}")
        logger.info(f"Code: \n{pyautogui_actions}")

        self.observations.append(obs)
        self.actions.append(low_level_instruction)
        self.cots.append(other_cot)

        current_step = len(self.actions)
        if current_step >= self.max_steps and 'computer.terminate' not in pyautogui_actions[0].lower():
            logger.warning(f"Reached maximum steps {self.max_steps}. Forcing termination.")
            low_level_instruction = 'Fail the task because reaching the maximum step limit.'
            pyautogui_actions = ['FAIL']
            other_cot['code'] = 'FAIL'

        # response = {"response": response} | other_cot
        # 因为 Kimi 每次只生成一步，所以列表长度通常为 1
        response_meta_list = []
        for _ in pyautogui_actions:
            meta_item = {
                "raw_response": other_cot.get("raw_response", ""),
                "thought": other_cot.get("thought", ""),
                "action": other_cot.get("action", ""),
                "meta_action": other_cot.get("code", {}),
                "coordinate": other_cot.get("coordinate", None)
            }
            response_meta_list.append(meta_item)


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
            messages = [{
                "role": "system",
                "content": EVALUATION_SYSTEM_PROMPT.format(instruction=task_instruction)
            }]

            # 2. Reuse the exact same history construction as predict
            # This ensures the judge sees the same context the agent had
            messages.extend(self._build_history_messages())

            # 3. Add Final Observation and Evaluation Query
            # Note: Unlike predict, we don't ask for the next move, we ask for a verdict.
            eval_query = f"Based on the conversation history above and this final screenshot, did the agent successfully complete the instruction: '{task_instruction}'? Please provide the JSON evaluation."
            
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encode_image(obs['screenshot'])}"}
                    },
                    {
                        "type": "text",
                        "text": eval_query
                    }
                ] # type: ignore
            })

            logger.info(f"Starting evaluation for: {task_instruction}")
            
            # 4. Call LLM
            response_msg = self.call_llm({
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "temperature": self.temperature, # Usually evaluation can use lower temp, but reusing self.temperature is fine
                "response_format": {"type": "json_object"} # Kimi supports json_object, helpful if available
            }, self.model)

            response_content = response_msg['content']
            logger.info(f"Evaluation Raw Output: {response_content}")

            # 5. Parse JSON
            # Handle potential markdown wrappers
            if "```json" in response_content:
                json_str = response_content.split("```json")[1].split("```")[0].strip()
            elif "```" in response_content:
                json_str = response_content.split("```")[1].strip()
            else:
                json_str = response_content.strip()

            result = json.loads(json_str)
            
            # Ensure required fields exist
            if "thought" not in result:
                result["thought"] = response_content
            if "score" not in result:
                # Fallback logic if score is missing but status is present (sometimes models do this)
                result["score"] = 0.0
            
            return result

        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            logger.error(traceback.format_exc())
            return {
                "thought": f"Evaluation failed due to error: {str(e)}",
                "score": 0.0
            }

    def call_llm(self, payload, model):
        """Call the LLM API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        for _ in range(20):
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=1200,
                verify=False
            )

            if response.status_code != 200:
                logger.error("Failed to call LLM: " + response.text)
                logger.error("Retrying...")
                time.sleep(5)
            else:
                response = response.json()
                finish_reason = response["choices"][0].get("finish_reason")
                if finish_reason is not None and finish_reason == "stop": # for most of the time, length will not exceed max_tokens
                    return response['choices'][0]['message']
                else:
                    logger.error("LLM did not finish properly, retrying...")
                    time.sleep(5)