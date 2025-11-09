import re
import time
from io import BytesIO
from typing import Tuple, Dict, List, Union
import io
import os
from PIL import Image, ImageDraw
from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY

import logging

logger = logging.getLogger("desktopenv.agent")


def create_pyautogui_code(agent, code: str, obs: Dict) -> Tuple:
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
    coords = None
    if isinstance(response, tuple):
        exec_code, coords = response
    else:
        exec_code = response
    return exec_code, coords

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
    print(f'[parse_code_from_string].relevant_code: {relevant_code}')
    return relevant_code


def extract_agent_functions(code):
    """Extracts all agent function calls from the given code.

    Args:
        code (str): The code string to search for agent function calls.

    Returns:
        list: A list of all agent function calls found in the code.
    """
    pattern = r"(agent\.\w+\(\s*.*\))"  # Matches
    return re.findall(pattern, code)


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

if __name__=="__main__":
    height = 1080
    width = 1920
    # (1080, 1920) -> (1092, 1932)
    print(smart_resize(height, width))