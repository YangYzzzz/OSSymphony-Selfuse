import json
import re
import time
from io import BytesIO
from typing import Tuple, Dict, List, Union
import io
import os
from PIL import Image, ImageDraw
from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
from mm_agents.interngui.utils.process_context import get_current_result_dir
import logging

logger = logging.getLogger("desktopenv.agent")


def create_pyautogui_code(agent, code: str, obs: Dict) -> Tuple[str, dict | None]:
    """
    Attempts to evaluate the code into a pyautogui code snippet with grounded actions using the observation screenshot.

    Args:
        agent (ACI): The grounding agent to use for evaluation.
        code (str): The code string to evaluate.
        obs (Dict): The current observation containing the screenshot.

    Returns:
        exec_code (str): The pyautogui code to execute the grounded action.
        coordinate (List): The coordinate of the action, a list such as [x1, y1, x2, y2, x3, y3...]. Because may appear more than one coordinate in one action.
        Modified by Yang. 
    Raises:
        Exception: If there is an error in evaluating the code.
    """
    agent.assign_screenshot(obs)  # Necessary for grounding
    response = eval(code)
    if isinstance(response, Tuple):
        return response
    elif isinstance(response, str):
        return response, None
    else:
        return "", None

def draw_coordinates(image_bytes: bytes, coordinates: List[Union[int, float]], save_path: str):
    """
    在给定的图像上绘制坐标点，并将其保存到新文件。

    该函数接收一个以字节流形式存在的图像，一个包含 [x1, y1, x2, y2, ...] 格式的坐标列表，
    并在每个 (x, y) 坐标点上绘制一个红色的叉。最后将结果图像保存到指定的路径。

    Args:
        image_bytes (bytes): 图像的原始字节数据 (例如，从PNG或JPEG文件读取的内容)。
        coordinates (List[Union[int, float]]): 扁平化的坐标列表，必须为偶数个元素。
                                                例如: [x1, y1, x2, y2]。
        save_path (str): 绘制了标记后，新图像的保存路径。
    """
    # --- 步骤 1: 从字节流加载图像 ---
    # Pillow 的 Image.open() 可以直接处理文件路径，但不能直接处理字节流。
    # 我们使用 io.BytesIO 将内存中的字节数据包装成一个类似文件的对象，
    # 这样 Image.open() 就可以像读取文件一样读取它。
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # 确保图像是 RGB 模式，这样才能绘制彩色标记。PNG 可能有 RGBA（带透明度）模式。
        image = image.convert("RGB")
    except Exception as e:
        return

    # --- 步骤 2: 创建一个绘图对象 ---
    # ImageDraw.Draw() 会返回一个可以在该图像上进行2D绘图的对象。
    draw = ImageDraw.Draw(image)

    # 定义叉的样式
    cross_size = 15      # 叉的臂长的一半（整个叉的大小为 30x30 像素）
    cross_color = "red"  # 颜色
    cross_width = 3      # 线条宽度

    # 每次迭代步长为 2，以同时获取 x 和 y
    for i in range(0, len(coordinates) - 1, 2):
        x, y = coordinates[i], coordinates[i+1]

        # 计算构成叉的两条线的端点
        # 线1: 从左上到右下
        line1_start = (x - cross_size, y - cross_size)
        line1_end = (x + cross_size, y + cross_size)
        
        # 线2: 从右上到左下
        line2_start = (x + cross_size, y - cross_size)
        line2_end = (x - cross_size, y + cross_size)

        # 使用 draw.line() 绘制两条线来形成一个叉
        draw.line([line1_start, line1_end], fill=cross_color, width=cross_width)
        draw.line([line2_start, line2_end], fill=cross_color, width=cross_width)

    # --- 步骤 4: 保存修改后的图像 ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    image.save(save_path)

def call_llm_safe(
    agent, temperature: float = 0.0, use_thinking: bool = False, **kwargs
) -> str:
    # 通过 .get() 方法安全地获取当前线程的上下文值
    try:
        example_result_dir = get_current_result_dir()
    except Exception:
        example_result_dir = "logs/tokens"
    # Retry if fails
    max_retries = 3  # Set the maximum number of retries
    attempt = 0
    response = ""
    while attempt < max_retries:
        try:
            response = agent.get_response(
                temperature=temperature, use_thinking=use_thinking, **kwargs
            )
            assert response is not None, "Response from agent should not be None"
            # print("Response success!")
            break  # If successful, break out of the loop
        except Exception as e:
            attempt += 1
            print(f"{agent.engine} Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("Max retries reached. Handling failure.")
        time.sleep(1.0)
    # 记录使用Token数
    if isinstance(response, tuple):
        response, usage = response
        agent_name = agent.agent_name
        with open(os.path.join(example_result_dir, "token.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "agent_name": agent_name,
                "completion_tokens": usage.completion_tokens,
                "prompt_tokens": usage.prompt_tokens,
                "total_tokens": usage.total_tokens
            }))
            f.write("\n")

    return response if response is not None else ""

def call_func_safe(
    func, **kwargs
) -> str:
    # Retry if fails
    max_retries = 3  # Set the maximum number of retries
    attempt = 0
    response = ""
    while attempt < max_retries:
        try:
            response = func(**kwargs)
            break
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("Max retries reached. Handling failure.")
        time.sleep(1.0)
    
    return response if response is not None else ""

def extract_coords_from_action_dict(action_dict: Dict | None) -> List:
    coords = []
    coords_num = 0
    if action_dict:
        for k, v in action_dict["args"].items():
            # 先判断是0/2/4个坐标, 2个坐标一定是x,y，4个坐标一定是x1,y1,x2,y2
            if (k == "x" and v) or (k == "y" and v) or (k == "x1" and v) or (k == "x2" and v) or (k == "y1" and v) or (k == "y2" and v):
                coords_num += 1
        if coords_num == 2:
            coords.append(action_dict["args"]["x"])
            coords.append(action_dict["args"]["y"])
        if coords_num == 4:
            coords.append(action_dict["args"]["x1"])
            coords.append(action_dict["args"]["y1"])
            coords.append(action_dict["args"]["x2"])
            coords.append(action_dict["args"]["y2"])
    return coords

def call_llm_formatted(generator, format_checkers, **kwargs):
    """
    Calls the generator agent's LLM and ensures correct formatting.

    Args:
        generator (ACI): The generator agent to call.
        obs (Dict): The current observation containing the screenshot.
        format_checkers (Callable): Functions that take the response and return a tuple of (success, feedback).
        **kwargs: Additional keyword arguments for the LLM call.

    Returns:
        response (str): The formatted response from the generator agent.
    """
    max_retries = 3  # Set the maximum number of retries
    attempt = 0
    response = ""
    if kwargs.get("messages") is None:
        messages = (
            generator.messages.copy()
        )  # Copy messages to avoid modifying the original
    else:
        messages = kwargs["messages"]
        del kwargs["messages"]  # Remove messages from kwargs to avoid passing it twice
    while attempt < max_retries:
        response = call_llm_safe(generator, messages=messages, **kwargs)
        # Prepare feedback messages for incorrect formatting
        feedback_msgs = []
        for format_checker in format_checkers:
            success, feedback = format_checker(response)
            if not success:
                feedback_msgs.append(feedback)
        if not feedback_msgs:
            # logger.info(f"Response formatted correctly on attempt {attempt} for {generator.engine.model}")
            break
        logger.error(
            f"Response formatting error on attempt {attempt} for {generator.engine.model}. Response: {response} {', '.join(feedback_msgs)}"
        )
        messages.append(
            {
                "role": "assistant",
                "content": [{"type": "text", "text": response}],
            }
        )
        logger.info(f"Bad response: {response}")
        delimiter = "\n- "
        formatting_feedback = f"- {delimiter.join(feedback_msgs)}"
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PROCEDURAL_MEMORY.FORMATTING_FEEDBACK_PROMPT.replace(
                            "FORMATTING_FEEDBACK", formatting_feedback
                        ),
                    }
                ],
            }
        )
        logger.info("Feedback:\n%s", formatting_feedback)

        attempt += 1
        if attempt == max_retries:
            logger.error(
                "Max retries reached when formatting response. Handling failure."
            )
        time.sleep(1.0)
    return response


def split_thinking_response(full_response: str) -> Tuple[str, str]:
    try:
        # Extract thoughts section
        thoughts = full_response.split("<thoughts>")[-1].split("</thoughts>")[0].strip()

        # Extract answer section
        answer = full_response.split("<answer>")[-1].split("</answer>")[0].strip()

        return answer, thoughts
    except Exception as e:
        return full_response, ""


def parse_code_from_string(input_string):
    """Parses a string to extract each line of code enclosed in triple backticks (```)

    Args:
        input_string (str): The input string containing code snippets.

    Returns:
        str: The last code snippet found in the input string, or an empty string if no code is found.
    """
    input_string = input_string.strip()

    # This regular expression will match both ```code``` and ```python code```
    # and capture the `code` part. It uses a non-greedy match for the content inside.
    pattern = r"```(?:\w+\s+)?(.*?)```"
    print(f'[parse_code_from_string].input_string: {input_string}')
    # Find all non-overlapping matches in the string
    matches = re.findall(pattern, input_string, re.DOTALL)
    if len(matches) == 0:
        # return []
        return ""
    relevant_code = matches[
        -1
    ]  # We only care about the last match given it is the grounded action
    # print(f'[parse_code_from_string].relevant_code: {relevant_code}')
    return relevant_code


def extract_agent_functions(code):
    """
    Extracts all agent function names from the given code.
    
    Args:
        code (str): The code string to search.

    Returns:
        list: A list of strings like ['agent.click', 'agent.type'].
    """
    pattern = r"agent\.\w+" 
    
    return re.findall(pattern, code)

# def extract_agent_functions(input_string):
#     """
#     从输入字符串中提取最后一个代码块，并从中找出所有的 agent 函数调用。

#     此函数执行两步操作：
#     1. 它首先使用正则表达式搜索被三个反引号 (```) 包围的代码块。
#        如果找到多个代码块，它只关心最后一个，因为这通常代表最终的“Grounded Action”。
#     2. 在提取出的代码块中，它再使用另一个正则表达式来查找并返回所有
#        以 "agent." 开头的函数调用。

#     Args:
#         input_string (str): 包含代码块的完整字符串。

#     Returns:
#         list: 在最后一个代码块中找到的所有 agent 函数调用的字符串列表。
#               如果没有找到代码块或代码块中没有 agent 函数调用，则返回空列表。
#     """
#     if not isinstance(input_string, str):
#         return []

#     # 步骤 1: 从输入字符串中提取最后一个代码块的内容。
#     # 这个正则表达式匹配 ```code``` 或 ```python code``` 这样的格式，
#     # 并捕获其中的代码。re.DOTALL 标志让 `.` 可以匹配包括换行符在内的任意字符。
#     code_block_pattern = r"```(?:\w+\s*)?(.*?)```"
#     matches = re.findall(code_block_pattern, input_string, re.DOTALL)
    
#     with open(f'logs/extract_agent_functions.txt', "a", encoding="utf-8") as f:
#         f.write(f"len: {len(matches)} " + input_string + "\n")

#     # 如果没有找到任何代码块，则返回空列表。
#     if not matches:
#         return []

#     # 我们只关心最后一个匹配项，因为它通常是 Grounded Action。
#     # .strip() 用于移除代码块内容两端可能存在的空白字符。
#     relevant_code = matches[-1].strip()

#     # 步骤 2: 在提取出的代码块中查找 agent 函数调用。
#     # 这个正则表达式匹配 "agent." 开头，后跟函数名和圆括号内的所有内容。
#     # 同样使用 re.DOTALL 以支持跨越多行的函数调用。
#     agent_call_pattern = r"(agent\.\w+\(\s*.*\))"  # Matches
#     agent_calls = re.findall(agent_call_pattern, relevant_code, re.DOTALL)

#     return agent_calls

def compress_image(image_bytes: bytes = None, image: Image = None) -> bytes:
    """Compresses an image represented as bytes.

    Compression involves resizing image into half its original size and saving to webp format.

    Args:
        image_bytes (bytes): The image data to compress.

    Returns:
        bytes: The compressed image data.
    """
    if not image:
        image = Image.open(BytesIO(image_bytes))
    output = BytesIO()
    image.save(output, format="WEBP")
    compressed_image_bytes = output.getvalue()
    return compressed_image_bytes

import math

IMAGE_FACTOR = 28
MIN_PIXELS = 100 * 28 * 28
MAX_PIXELS = 16384 * 28 * 28
MAX_RATIO = 200

def round_by_factor(number: int, factor: int) -> int:
    """Returns the closest integer to 'number' that is divisible by 'factor'."""
    return round(number / factor) * factor


def ceil_by_factor(number: int, factor: int) -> int:
    """Returns the smallest integer greater than or equal to 'number' that is divisible by 'factor'."""
    return math.ceil(number / factor) * factor


def floor_by_factor(number: int, factor: int) -> int:
    """Returns the largest integer less than or equal to 'number' that is divisible by 'factor'."""
    return math.floor(number / factor) * factor


def smart_resize(
    height: int,
    width: int,
    factor: int = IMAGE_FACTOR,
    min_pixels: int = MIN_PIXELS,
    max_pixels: int = MAX_PIXELS,
) -> tuple[int, int]:
    """
    Rescales the image so that the following conditions are met:

    1. Both dimensions (height and width) are divisible by 'factor'.

    2. The total number of pixels is within the range ['min_pixels', 'max_pixels'].

    3. The aspect ratio of the image is maintained as closely as possible.
    """
    min_pixels = MIN_PIXELS if not min_pixels else min_pixels
    max_pixels = MAX_PIXELS if not max_pixels else max_pixels
    if max(height, width) / min(height, width) > MAX_RATIO:
        raise ValueError(
            f"absolute aspect ratio must be smaller than {MAX_RATIO}, got {max(height, width) / min(height, width)}"
        )
    h_bar = max(factor, round_by_factor(height, factor))
    w_bar = max(factor, round_by_factor(width, factor))
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = floor_by_factor(height / beta, factor)
        w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar

def enhance_observation(image_data: bytes, coordinates: List, expansion_pixels: int = 400, draw=True) -> Tuple[bytes, int, int, int, int]:
        """
        根据给定的坐标点，在截图上绘制标记并裁剪一个“聚焦”区域。

        Returns:
            Tuple[bytes, int, int, int, int]: 
                - new_image_data (bytes): 裁剪后的图片数据
                - crop_left (int): X轴偏移量
                - crop_top (int): Y轴偏移量
                - new_width (int): 裁剪后的图片宽度
                - new_height (int): 裁剪后的图片高度
        """
        image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        draw_ctx = ImageDraw.Draw(image)

        img_width, img_height = image.size

        X_MARKER_SIZE = 40
        X_MARKER_WIDTH = 5
        
        def _draw_x(draw_context, center_x, center_y, size=X_MARKER_SIZE, color="red", width=X_MARKER_WIDTH):
            half_size = size // 2
            draw_context.line((center_x - half_size, center_y - half_size, center_x + half_size, center_y + half_size), fill=color, width=width)
            draw_context.line((center_x - half_size, center_y + half_size, center_x + half_size, center_y - half_size), fill=color, width=width)

        # --- 计算裁剪框 ---
        crop_left, crop_top, crop_right, crop_bottom = 0, 0, img_width, img_height

        if len(coordinates) == 2:
            x, y = coordinates[0], coordinates[1]
            if draw:
                _draw_x(draw_ctx, x, y)
            
            crop_left = x - expansion_pixels
            crop_top = y - expansion_pixels
            crop_right = x + expansion_pixels
            crop_bottom = y + expansion_pixels

        elif len(coordinates) >= 4:
            x1, y1 = coordinates[0], coordinates[1]
            x2, y2 = coordinates[2], coordinates[3]
            
            if draw:
                _draw_x(draw_ctx, x1, y1, color="red")
                _draw_x(draw_ctx, x2, y2, color="blue")
                draw_ctx.line((x1, y1, x2, y2), fill="green", width=5)
            
            box_left = min(x1, x2)
            box_top = min(y1, y2)
            box_right = max(x1, x2)
            box_bottom = max(y1, y2)
            
            crop_left = box_left - expansion_pixels
            crop_top = box_top - expansion_pixels
            crop_right = box_right + expansion_pixels
            crop_bottom = box_bottom + expansion_pixels

        # --- 安全裁剪边界检查 ---
        crop_left = max(0, int(crop_left))
        crop_top = max(0, int(crop_top))
        crop_right = min(img_width, int(crop_right))
        crop_bottom = min(img_height, int(crop_bottom))

        # --- 执行裁剪 ---
        crop_box = (crop_left, crop_top, crop_right, crop_bottom)
        cropped_image = image.crop(crop_box)
        
        # [新增] 获取裁剪后的新尺寸
        new_width, new_height = cropped_image.size

        buffered = io.BytesIO()
        cropped_image.save(buffered, format="PNG")
        
        # 返回: 图片数据, X偏移, Y偏移, 新宽, 新高
        return buffered.getvalue(), crop_left, crop_top, new_width, new_height

if __name__=="__main__":
    height = 1080
    width = 1920
    # (1080, 1920) -> (1092, 1932)
    print(smart_resize(height, width))
