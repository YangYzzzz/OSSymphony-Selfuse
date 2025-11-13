"""This file contains various formatting checks used to reprompt an agent for correctly formatted responses."""
from typing import Tuple, List, Callable
import json
from mm_agents.interngui.utils.common_utils import (
    extract_agent_functions,
    parse_code_from_string,
    create_pyautogui_code,
    split_thinking_response,
)

single_action_check = (
    lambda response: len(extract_agent_functions(parse_code_from_string(response))) == 1
)
single_action_error_msg = (
    "Incorrect code: There must be a single agent action in the code response."
)
SINGLE_ACTION_FORMATTER = lambda response: (
    single_action_check(response),
    single_action_error_msg,
)

# 也就是说要调用 grounder 两遍？？
def _attempt_code_creation(agent, code, obs):
    """Attempts to create a pyautogui code snippet from the response code"""
    try:
        return create_pyautogui_code(agent, code, obs)
    except Exception as e:
        print(f'[Attempt code creation error]: {e}')
        return None


# code_valid_check = (
#     lambda agent, obs, response: _attempt_code_creation(
#         agent, parse_code_from_string(response), obs
#     )
#     is not None
# )
def code_valid_check(agent, obs, response):
    code = parse_code_from_string(response)
    # print(f'[code_valid_check]: {code}')
    result = _attempt_code_creation(
        agent, code, obs
    ) is not None

    # 查看解析到的code
    if not result:
        with open("logs/code_valid_check.txt", "a", encoding="utf-8") as f:
            f.write(f"Response: {response}\nCode: {code}\n")

    # print(f"[code_valid_check]: {result}")
    return result

code_valid_error_msg = "Incorrect code: The agent action must be a valid function and use valid parameters from the docstring list."
CODE_VALID_FORMATTER = lambda agent, obs, response: (
    code_valid_check(agent, obs, response),
    code_valid_error_msg,
)

thoughts_answer_tag_check = lambda response: split_thinking_response(response)[1] != ""
thoughts_answer_tag_error_msg = "Incorrect response: The response must contain both <thoughts>...</thoughts> and <answer>...</answer> tags."
THOUGHTS_ANSWER_TAG_FORMATTER = lambda response: (
    thoughts_answer_tag_check(response),
    thoughts_answer_tag_error_msg,
)

integer_answer_check = (
    lambda response: split_thinking_response(response)[0].strip().isdigit()
)
integer_answer_error_msg = (
    "Incorrect response: The <answer>...</answer> tag must contain a single integer."
)
INTEGER_ANSWER_FORMATTER = lambda response: (
    integer_answer_check(response),
    integer_answer_error_msg,
)

def json_answer_check(response: str, required_fields: List[str]) -> bool:
    """
    一个只返回 True/False 的检查函数。
    """
    try:
        # 1. 解析 ``` 块内部的string
        answer_str = parse_code_from_string(response)
        
        if len(answer_str) == 0:
            return False

        # 2. 检查 JSON
        data = json.loads(answer_str)

        # 3. 检查是否为字典
        if not isinstance(data, dict):
            return False

        # 4. 检查字段
        if set(required_fields) - set(data.keys()):
            return False
        
        # 所有检查都通过
        return True
        
    except Exception:
        return False

json_answer_error_msg = (
    "Incorrect response: The (Answer) part must contain a valid JSON object that includes ALL required keys and need to be wrapped by ```json and ```"
)

JSON_ANSWER_FORMATTER = lambda response, required_fields: (
    json_answer_check(required_fields, response),
    json_answer_error_msg,
)
