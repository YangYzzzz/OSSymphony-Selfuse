"""
Utility functions for the Anthropic API.
"""
import json
import os
from pathlib import Path
import textwrap
from typing import List, Optional, Union, cast, Any, Dict
import base64
from enum import Enum
from mm_agents.utils.call_api_log import CALLS_LOG_DIR, STAT_LOG_DIR, log_claude_api_call
from anthropic import (
    Anthropic,
    AnthropicBedrock,
    AnthropicVertex,
    APIError,
    APIResponseValidationError,
    APIStatusError,
)
from anthropic.types.beta import (
    BetaCacheControlEphemeralParam,
    BetaContentBlockParam,
    BetaImageBlockParam,
    BetaMessage,
    BetaMessageParam,
    BetaTextBlock,
    BetaThinkingBlock,
    BetaTextBlockParam,
    BetaToolResultBlockParam,
    BetaToolUseBlockParam,
)
from datetime import datetime

from .tools import ToolResult


# ================= Qwen3VL SFT utilities =================
import hashlib
from copy import deepcopy
from mm_agents.utils.qwen_vl_utils import QWEN3VL_COMPUTER_USE_TOOL_SCHEMA, QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN, dedup_and_save_images_for_claude


def _scale_single_coord_to_1000(coord: list[int], screen_size: tuple[int, int]) -> list[int]:
    """将像素坐标缩放到 0~1000 的相对坐标空间。"""
    if len(coord) != 2:
        return coord
    w, h = screen_size
    if not w or not h:
        return coord
    x_rel = max(0, min(1000, round(coord[0] / w * 1000)))
    y_rel = max(0, min(1000, round(coord[1] / h * 1000)))
    return [x_rel, y_rel]


def scale_coordinate_to_1000(coord: Optional[Any], screen_size: tuple[int, int]) -> Optional[Any]:
    """支持单点或拖拽两点坐标的缩放到 0~1000 空间。

    - 单点: [x, y]
    - 拖拽: [[x1, y1], [x2, y2]]
    """
    if coord is None:
        return None
    # 拖拽路径 [[x1,y1],[x2,y2]]
    if isinstance(coord, (list, tuple)) and len(coord) == 2 and all(
        isinstance(c, (list, tuple)) for c in coord
    ):
        return [
            _scale_single_coord_to_1000(list(coord[0]), screen_size),
            _scale_single_coord_to_1000(list(coord[1]), screen_size),
        ]
    # 单点 [x, y]
    if isinstance(coord, (list, tuple)):
        return _scale_single_coord_to_1000(list(coord), screen_size)
    return coord


def _iter_image_blocks_from_messages(messages: list[BetaMessageParam]):
    """遍历 messages 中所有 image block（user 截图 + tool_result image）。"""
    for m in messages:
        content = m.get("content") if isinstance(m, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "image":
                src = block.get("source") or {}
                if isinstance(src, dict) and src.get("type") == "base64":
                    data = src.get("data")
                    media_type = src.get("media_type", "image/png")
                    if data:
                        yield data, media_type


def truncate_images_for_context(
    messages: list[BetaMessageParam],
    max_images: int = 5,
):
    """复制一份 messages，并只保留最后 max_images 张图片，其余位置替换成占位文本。

    注意：Claude 的截图都位于 tool_result block 的 content 里，需要深入查找。
    """
    messages_copy = deepcopy(messages)

    # 收集所有 image block 的 (msg_idx, tool_result_idx, img_idx)
    image_positions: list[tuple[int, int, int]] = []
    for mi, m in enumerate(messages_copy):
        content = m.get("content") if isinstance(m, dict) else None
        if not isinstance(content, list):
            continue
        for ti, block in enumerate(content):
            if not (isinstance(block, dict) and block.get("type") == "tool_result"):
                continue
            sub_content = block.get("content")
            if not isinstance(sub_content, list):
                continue
            for ci, sub in enumerate(sub_content):
                if isinstance(sub, dict) and sub.get("type") == "image":
                    image_positions.append((mi, ti, ci))

    if len(image_positions) <= max_images:
        return messages_copy

    # 需要移除的都是最早的那些
    to_remove = image_positions[: len(image_positions) - max_images]
    for mi, ti, ci in to_remove:
        m = messages_copy[mi]
        content = m.get("content")
        if not isinstance(content, list) or ti >= len(content):
            continue
        tool_result_block = content[ti]
        sub_content = tool_result_block.get("content")
        if not isinstance(sub_content, list) or ci >= len(sub_content):
            continue
        # 用直接删除
        del sub_content[ci]
        # sub_content[ci] = {
        #     "type": "text",
        #     "text": "[Screenshot has removed]",
        # }

    return messages_copy


def _merge_thinking_and_text(blocks: list[dict]) -> str:
    """将本轮 assistant 的 thinking + text block 合并为 <think>...</think> 包裹的字符串。"""
    pieces: list[str] = []
    for b in blocks:
        if not isinstance(b, dict):
            continue
        b_type = b.get("type")
        if b_type == "thinking":
            val = b.get("thinking") or ""
            pieces.append(str(val))
        elif b_type == "text":
            val = b.get("text") or ""
            pieces.append(str(val))
    merged = "".join(pieces).strip()
    if not merged:
        return ""
    return f"{merged}" # TODO: 是否添加 <think> tag 有待探究

def _convert_claude_action_to_qwen(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any] | List[Dict[str, Any]]:
    """
    将 Claude computer/code 工具的 input 转成 Qwen3VL 的动作参数空间。

    参照 mm_agents/os_symphony2/os_symphony2_agent.py 里的 tools_def：
    - action: ["key", "type", "mouse_move", "left_click", "left_click_drag",
                "right_click", "middle_click", "double_click", "scroll",
                "code", "wait", "terminate"]
    - keys / text / coordinate / pixels / time / code / language
    """
    q_args: Dict[str, Any] | List[Dict[str, Any]] = {"action": "wait"}

    if tool_name == "computer":
        action = (tool_input.get("action") or "").lower()
        text = tool_input.get("text")
        coordinate = tool_input.get("coordinate")
        start_coordinate = tool_input.get("start_coordinate")
        scroll_direction = tool_input.get("scroll_direction")
        scroll_amount = tool_input.get("scroll_amount") or 0
        duration = tool_input.get("duration") or 0.5

        # 鼠标相关
        if action in {"left_press", "left_click"}:
            q_args["action"] = "left_click"
            if coordinate is not None:
                q_args["coordinate"] = coordinate
        elif action in {"right_click"}:
            q_args["action"] = "right_click"
            if coordinate is not None:
                q_args["coordinate"] = coordinate
        elif action in {"middle_click"}:
            q_args["action"] = "middle_click"
            if coordinate is not None:
                q_args["coordinate"] = coordinate
        elif action in {"double_click"}:
            q_args["action"] = "double_click"
            if coordinate is not None:
                q_args["coordinate"] = coordinate
        elif action in {"triple_click"}:
            q_args["action"] = "triple_click"
            if coordinate is not None:
                q_args["coordinate"] = coordinate
        elif action in {"mouse_move"}:
            q_args["action"] = "mouse_move"
            if coordinate is not None:
                q_args["coordinate"] = coordinate
        elif action in {"left_click_drag"}:
            q_args["action"] = "left_click_drag"
            if coordinate is not None:
                q_args["coordinate"] = coordinate
            if start_coordinate is not None and coordinate is not None:
                # 特殊处理, 一个 Claude Action 对应两个 Qwen Action
                q_args = [
                    {
                        "action": "mouse_move",
                        "coordinate": start_coordinate
                    },
                    {
                        "action": "left_click_drag",
                        "coordinate": coordinate
                    }
                ]

        # 键盘
        elif action in {"key"}:
            q_args["action"] = "key"
            keys = []

            key_conversion = {
                "page_down": "pagedown",
                "page_up": "pageup",
                "super_l": "win",
                "super": "command",
                "escape": "esc"
            }

            if isinstance(text, str):
                # Claude 侧一般是 "ctrl+c" 或 "ctrl+shift+esc"
                for k in text.replace("+", ",").split(","):
                    k = k.strip().lower()         # ① 统一小写，与官方 key.strip().lower() 对齐
                    k = key_conversion.get(k, k)  # ② 应用键名映射，与官方 key_conversion.get(key, key) 对齐
                    if k:
                        keys.append(k)

            if keys:
                q_args["keys"] = keys

        elif action in {"type"}:
            q_args["action"] = "type"
            if isinstance(text, str):
                q_args["text"] = text

        # 滚动
        elif action in {"scroll"}:
            if scroll_direction in {"down", "up"}:
                q_args["action"] = "scroll"
            elif scroll_direction in {"left", "right"}:
                q_args["action"] = "hscroll"

            if scroll_direction in {"down", "left"}:
                pixels = -abs(scroll_amount)
            elif scroll_direction in {"up", "right"}:
                pixels = abs(scroll_amount)
            q_args["pixels"] = pixels

            # SFT 数据有位置信息
            if coordinate is not None:
                q_args["coordinate"] = coordinate

        # 等待 / 结束
        elif action in {"wait"}:
            q_args["action"] = "wait"
            q_args["time"] = duration
        # 非第一步的 screenshot 一律作为 wait 处理
        elif action in {"screenshot"}:
            q_args["action"] = "wait"
            q_args["time"] = 2
        elif action in {"done"}:
            q_args["action"] = "terminate"
            q_args["status"] = "success"
        elif action in {"fail"}:
            q_args["action"] = "terminate"
            q_args["status"] = "failure"
        else:
            # 未知动作兜底成 terminate，避免训练奇怪 action
            q_args["action"] = "terminate"
            q_args["status"] = "failure"

    elif tool_name == "code":
        # code 工具 → execute_code
        lang = (tool_input.get("language") or "python").lower()
        code = tool_input.get("execute_code") or ""
        q_args["action"] = "code"
        q_args["language"] = lang
        q_args["execute_code"] = code

    else:
        q_args["action"] = "terminate"
        q_args["status"] = "failure"
    return q_args

def build_qwen_messages_from_claude(
    step_messages: list[BetaMessageParam],
    screen_size: tuple[int, int],
) -> list[dict]:
    """将 Claude 的 message 历史转成 Qwen3VL SFT messages.

    约定：
    - user: 文本 + `<image>` 占位；
    - assistant: 普通回复 role="assistant"；
    - tool_use: role="tool_call"；
    - tool_result: role="tool_response"。
    """
    qwen_messages: list[dict] = []

    for m in step_messages:
        if not isinstance(m, dict):
            continue
        role = m.get("role")
        content = m.get("content")
        if not isinstance(content, list):
            continue

        # user / tool_result 统一走 here，再根据 block type 决定具体 role
        if role == "user":
            # 若是 tool_result，则转成 tool_response
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                # 这里一条 user 里可能只有一个 tool_result
                for b in content:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") != "tool_result": # 所有内容都在 tool_result 内
                        continue
                    # 生成 tool_response message
                    has_image = False
                    payload = {}
                    # 这部分是人为构造的, 必然是一个 text 和 一个 image 字段 或者 两个 text 字段(图像移除)
                    for sub in b.get("content", []) or []:
                        if isinstance(sub, dict) and sub.get("type") == "text":
                            if sub.get("text") == "Success":
                                payload["status"] = sub.get("text")
                            else:
                                payload["code_result"] = sub.get("text")
                        if isinstance(sub, dict) and sub.get("type") == "image":
                            has_image = True
                    # TODO: Claude -> Qwen3VL 动作空间转化中, 存在1对多tool_call转化, 此时 tool_response 仍为一个, 但应该不影响, 不额外处理
                    qwen_messages.append(
                        {
                            "role": "tool_response",
                            "content": json.dumps(payload, ensure_ascii=False),
                        }
                    )
                    if has_image:
                        # payload["images"] = "<image>"
                        qwen_messages.append(
                            {
                                "role": "user",
                                "content": "Current Screenshot: <image>",
                            }
                        )
            else:
                # 普通 user：将 image -> <image>，text 保持
                text_parts: list[str] = []
                for b in content:
                    if not isinstance(b, dict):
                        continue
                    b_type = b.get("type")
                    if b_type == "text":
                        text_parts.append(str(b.get("text") or ""))
                    elif b_type == "image":
                        text_parts.append("<image>")
                if text_parts:
                    qwen_messages.append(
                        {
                            "role": "user",
                            "content": "".join(text_parts),
                        }
                    )

        elif role == "assistant":
            # 把本条 assistant 拆成：普通回复 + tool_call 序列
            # 1) thinking+text -> 一个 assistant
            merged_think = _merge_thinking_and_text(content)
            if merged_think:
                qwen_messages.append(
                    {
                        "role": "assistant",
                        "content": merged_think,
                    }
                )

            # 2) tool_use -> 多个 tool_call
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") != "tool_use":
                    continue
                tool_id = str(b.get("id")) if b.get("id") is not None else None
                tool_name = b.get("name", "")
                tool_input = b.get("input") or {}

                if tool_input.get("coordinate"):
                    tool_input["coordinate"] = scale_coordinate_to_1000(tool_input.get("coordinate"), screen_size)
                if tool_input.get("start_coordinate"):
                    tool_input["start_coordinate"] = scale_coordinate_to_1000(tool_input.get("start_coordinate"), screen_size)
                    
                converted_args = _convert_claude_action_to_qwen(tool_name, tool_input)
                if not isinstance(converted_args, list):
                    converted_args = [converted_args]
                for arg in converted_args:
                    payload = {
                        "name": "custom_computer_use", # qwen3vl 固定为该一个工具, 下包含所有可用操作分支
                        "arguments": arg,
                    }
                    qwen_messages.append(
                        {
                            "role": "tool_call",
                            "content": json.dumps(payload, ensure_ascii=False),
                        }
                    )

    return qwen_messages


def build_qwen_sft_sample(
    messages: list[BetaMessageParam],
    screen_size: tuple[int, int],
    image_hash_map: dict[str, str],
    image_root_dir: Path
) -> tuple[dict, dict[str, str]]:
    """构造单步 Qwen3VL SFT 训练样本。
    一个典型的Claude数据(messages)如下所示 (重要重要重要):
    [
        {"role": "user", "content": [{"type": "text", "text": instruction}]},
        {"role": "assistant": "content": [{"type": "thinking", "thinking": thinking}, {"type": "text", "text": text}, {"type": "tool_use", "name": "computer", "input": {"action": "screenshot"}}]},
        {"role": "user": "content": [{"type": "tool_result", "content": [{"type": "text", "text": "Success"}, {"type": "image_placeholder", "detail": "[IMAGE_CONTENT_REMOVED_FOR_LOGGING]"}]}]}
        {"role": "assistant": "content": [{"type": "thinking", "thinking": thinking}, {"type": "text", "text": text}, {"type": "tool_use", "name": "computer/code", "input": {"action": "left_click", "coordinate": [590, 33]}}]},
        xxxxxxx 依次类推
    ]

    你需要将其组织为
    {"tools": "[{\"type\": \"function\", \"function\": {\"name\": \"click\", \"description\": \"点击屏幕中的某个位置\", \"parameters\": {\"type\": \"object\", \"properties\": {\"x\": {\"type\": \"integer\", \"description\": \"横坐标，表示屏幕上的水平位置\"}, \"y\": {\"type\": \"integer\", \"description\": \"纵坐标，表示屏幕上的垂直位置\"}}, \"required\": [\"x\", \"y\"]}}}]", "messages": [{"role": "user", "content": "<image>现在几点了？"}, {"role": "assistant", "content": "<think>\n我可以通过打开日历App来获取当前时间。\n</think>\n"}, {"role": "tool_call", "content": "{\"name\": \"click\", \"arguments\": {\"x\": 105, \"y\": 132}}"}, {"role": "tool_response", "content": "{\"images\": \"<image>\", \"status\": \"success\"}"}, {"role": "assistant", "content": "成功打开日历App，现在的时间为中午11点"}], "images": ["desktop.png", "calendar.png"]}
    - 截断上下文图片为最近 5 张；
    - 去重存盘图片；
    - 构造 messages / images 字段；
    - 生成 loss_config：最后一个 assistant 文本 loss=True，所有 tool_call loss=True。
    """
    
    # 0) 第一步前处理(重要): 去除 messages[1]和messages[2], 并将messages[2]的图像部分直接贴到messages[0]的content内
    # 注意一定不要修改原messages,创建复制来修改
    processed_messages = deepcopy(messages)
    if len(processed_messages) >= 3:
        first = processed_messages[0]
        second = processed_messages[1]
        # 只有在符合典型结构时才做裁剪，避免误伤
        # 当 second 的动作为 screenshot 时, 再进行更换
        exchange_flag = False
        for b in second["content"]:
            if not isinstance(b, dict):
                continue
            if b.get("type") != "tool_use":
                continue
            tool_name = b.get("input", {}).get("action", "")
            if tool_name == "screenshot":
                exchange_flag = True
        if (
            exchange_flag
        ):
            # 砍掉第 1、2 条（下标 1、2），粗暴跳过第一轮tool_call，直接拼接下一轮tool_call
            # user, assistant(screenshot, cut), user(多个tool_result, cut), assistant(other tool call)
            processed_messages = [first] + processed_messages[3:]

    # 后续逻辑都基于 processed_messages

    # 1) 截断图片上下文, 保留第一张初始状态图片(小巧思)
    truncated_messages = truncate_images_for_context(processed_messages, max_images=4)

    # 2) 保存图片并拿到文件名列表
    images, image_hash_map = dedup_and_save_images_for_claude(
        messages=truncated_messages,
        image_hash_map=image_hash_map,
        image_root_dir=image_root_dir
    )

    # 3) 构造 Qwen 消息
    qwen_messages = build_qwen_messages_from_claude(
        step_messages=truncated_messages,
        screen_size=screen_size,
    )

    # 4) 添加 System Prompt
    qwen_messages.insert(0, {
        "role": "system",
        "content": QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN
    })

    sample = {
        "tools": QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
        "messages": qwen_messages,
        "images": images
    }

    return sample, image_hash_map


COMPUTER_USE_BETA_FLAG = "computer-use-2025-11-24"
PROMPT_CACHING_BETA_FLAG = "prompt-caching-2024-07-31"
COMPUTER_USE_TYPE = "computer_20251124"

# computer_20250124 computer-use-2025-01-24
# computer_20251124 computer-use-2025-11-24

class APIProvider(Enum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    VERTEX = "vertex"


PROVIDER_TO_DEFAULT_MODEL_NAME: dict[(APIProvider, str), str] = {
    (APIProvider.ANTHROPIC, "claude-3-5-sonnet-20241022"): "claude-3-5-sonnet-20241022",
    (APIProvider.BEDROCK, "claude-3-5-sonnet-20241022"): "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    (APIProvider.VERTEX, "claude-3-5-sonnet-20241022"): "claude-3-5-sonnet-v1@20241022",
    (APIProvider.ANTHROPIC, "claude-3-7-sonnet-20250219"): "claude-3-7-sonnet-20250219",
    (APIProvider.BEDROCK, "claude-3-7-sonnet-20250219"): "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    (APIProvider.VERTEX, "claude-3-7-sonnet-20250219"): "claude-3-7-sonnet-v1@20250219",
    (APIProvider.ANTHROPIC, "claude-4-opus-20250514"): "claude-4-opus-20250514",
    (APIProvider.BEDROCK, "claude-4-opus-20250514"): "us.anthropic.claude-opus-4-20250514-v1:0",
    (APIProvider.VERTEX, "claude-4-opus-20250514"): "claude-4-opus-v1@20250514",
    (APIProvider.ANTHROPIC, "claude-opus-4-20250514"): "claude-opus-4-20250514",
    (APIProvider.ANTHROPIC, "claude-opus-4-1-20250805"): "claude-opus-4-1-20250805",
    (APIProvider.ANTHROPIC, "claude-4-sonnet-20250514"): "claude-4-sonnet-20250514",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-20250514"): "claude-sonnet-4-20250514",
    (APIProvider.BEDROCK, "claude-4-sonnet-20250514"): "us.anthropic.claude-sonnet-4-20250514-v1:0",
    (APIProvider.VERTEX, "claude-4-sonnet-20250514"): "claude-sonnet-4-v1@20250514",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-5-20250929"): "claude-sonnet-4-5-20250929",
    (APIProvider.BEDROCK, "claude-sonnet-4-5-20250929"): "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    (APIProvider.VERTEX, "claude-sonnet-4-5-20250929"): "claude-sonnet-4-v1@20250929",
    (APIProvider.ANTHROPIC, "claude-opus-4-5"): "claude-opus-4-5-20251101",
    (APIProvider.BEDROCK, "claude-opus-4-5"): "us.anthropic.claude-opus-4-5-20251101-v1:0",

    (APIProvider.ANTHROPIC, "claude-opus-4-6-aws"): "claude-opus-4-6-aws",
    (APIProvider.ANTHROPIC, "claude-opus-4-6"): "claude-opus-4-6",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-6"): "claude-sonnet-4-6",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-6-aws"): "claude-sonnet-4-6-aws",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-6-urg"): "claude-sonnet-4-6-urg",
    
    (APIProvider.ANTHROPIC, "claude-opus-4-7"): "claude-opus-4-7",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-7"): "claude-sonnet-4-7",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-7-aws"): "claude-sonnet-4-7-aws",
    (APIProvider.ANTHROPIC, "claude-sonnet-4-7-urg"): "claude-sonnet-4-7-urg",
}


def get_model_name(provider: APIProvider, model_name: str) -> str:
    """
    Get the actual model name to use for API calls.
    
    Simply returns the model name as-is for direct API usage.
    """
    # Look up in the mapping table
    key = (provider, model_name)
    if key in PROVIDER_TO_DEFAULT_MODEL_NAME:
        return PROVIDER_TO_DEFAULT_MODEL_NAME[key]
    
    # If not found and using Anthropic direct API, return as-is (may work for new models)
    if provider == APIProvider.ANTHROPIC:
        return model_name
    
    # For Bedrock/Vertex, show available models if not found
    available_models = [k[1] for k in PROVIDER_TO_DEFAULT_MODEL_NAME.keys() if k[0] == provider]
    raise ValueError(
        f"❌ Model '{model_name}' is not configured for {provider.value}.\n"
        f"📋 Available models for {provider.value}: {available_models}"
    )


# This system prompt is optimized for the Docker environment in this repository and
# specific tool combinations enabled.
# We encourage modifying this system prompt to ensure the model has context for the
# environment it is running in, and to provide any additional information that may be
# helpful for the task at hand.
SYSTEM_PROMPT = f"""<SYSTEM_CAPABILITY>
* You are utilising an Ubuntu virtual machine using x86_64 architecture with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open browser, please just click on the Chrome icon.  Note, Chrome is what is installed on your system.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell. For example "(DISPLAY=:1 xterm &)". GUI apps run with bash tool will appear within your desktop environment, but they may take some time to appear. Take a screenshot to confirm it did.
* When using your bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file and use str_replace_editor or `grep -n -B <lines before> -A <lines after> <query> <filename>` to confirm output.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.  Either that, or make sure you scroll down to see everything before deciding something isn't available.
* DO NOT ask users for clarification during task execution. DO NOT stop to request more information from users. Always take action using available tools.
* When using your computer function calls, they take a while to run and send back to you.  Where possible/feasible, try to chain multiple of these calls all into one function calls request.
* TASK FEASIBILITY: You can declare a task infeasible at any point during execution - whether at the beginning after taking a screenshot, or later after attempting some actions and discovering barriers. Carefully evaluate whether the task is feasible given the current system state, available applications, and task requirements. If you determine that a task cannot be completed due to:
  - Missing required applications or dependencies that cannot be installed
  - Insufficient permissions or system limitations
  - Contradictory or impossible requirements
  - Any other fundamental barriers that make completion impossible
  Then you MUST output exactly "[INFEASIBLE]" (including the square brackets) anywhere in your response to trigger the fail action. The system will automatically detect this pattern and terminate the task appropriately.
* The current date is {datetime.today().strftime('%A, %B %d, %Y')}.
* Home directory of this Ubuntu system is '/home/user'.
* If you need a password for sudo, the password of the computer is 'password'. 
</SYSTEM_CAPABILITY>

<IMPORTANT>
* If the item you are looking at is a pdf, if after taking a single screenshot of the pdf it seems that you want to read the entire document instead of trying to continue to read the pdf from your screenshots + navigation, determine the URL, use curl to download the pdf, install and use pdftotext to convert it to a text file, and then read that text file directly with your StrReplaceEditTool.
</IMPORTANT>"""

SYSTEM_PROMPT_WITH_CODE = f"""
<SYSTEM_CAPABILITY>
* You are utilising an Ubuntu virtual machine using x86_64 architecture with internet access. The Ubuntu's home path is /home/user, desktop path is /home/user/Desktop.
* You have two main ways to act: (1) low-level GUI control via the `computer` tool (mouse, keyboard, scrolling, window management), and (2) high-level automation via the `code` tool (Python or Bash scripts).
* The `code` tool is for generating complete scripts, not just one-liners. The string you output will be written into a file and executed as a standalone program (e.g. a multi-line Python file or Bash script). You can and should use multiple lines, define functions, and structure the code as needed.
* Use GUI (`computer` tool) when you need to directly manipulate windows, click buttons, type into fields, navigate menus, or visually inspect application state.
* Use `code` when it is more efficient or reliable to:
  - Process or transform files (e.g. parsing logs, converting formats, searching and replacing in many files).
  - Generate new files or directory structures needed for the task.
  - Create shortcuts or small utilities that can be reused in later steps.
  - Automate shell workflows (e.g. chaining several commands, handling errors, or complex logic) as a script rather than many single Bash calls.
* Code and GUI should work together: for example, you can use the `code` tool to prepare data or configure the environment (creating/editing files, running batch operations), and then use GUI actions to open applications, verify results, or perform steps that require a graphical interface.
* When using your bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file and use `grep -n -B <lines before> -A <lines after> <query> <filename>` to confirm output.
* To open browser, please just click on the Chrome icon. Note, Chrome is what is installed on your system.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.  Either that, or make sure you scroll down to see everything before deciding something isn't available.
* DO NOT ask users for clarification during task execution. DO NOT stop to request more information from users. Always take action using available tools.
* When using your computer function calls, they take a while to run and send back to you.
* TASK FEASIBILITY: You can declare a task infeasible at any point during execution - whether at the beginning after taking a screenshot, or later after attempting some actions and discovering barriers. Carefully evaluate whether the task is feasible given the current system state, available applications, and task requirements. If you determine that a task cannot be completed due to:
  - Missing required applications or dependencies that cannot be installed
  - Insufficient permissions or system limitations
  - Contradictory or impossible requirements
  - Any other fundamental barriers that make completion impossible
  Then you MUST output exactly "[INFEASIBLE]" anywhere in your response to trigger the fail action. The system will automatically detect this pattern and terminate the task appropriately.
* The current date is {datetime.today().strftime('%A, %B %d, %Y')}.
* If you need a password for sudo, the password of the computer is 'password'.
</SYSTEM_CAPABILITY>

<IMPORTANT>
* When generating code with the `code` tool, prefer scripts that are idempotent and safe to re-run. Check paths carefully and avoid destructive operations (like `rm -rf`) unless absolutely necessary and clearly justified by the task.
* The execution time limit for any single `code` tool run is 30 seconds. Avoid commands that may run for too long (such as traversing the user home directory or heavy long-running computations). If you need to launch GUI applications or persistent background processes, you MUST fully detach them from the parent process's output pipes to prevent blocking. Always use the format `nohup <command> > /dev/null 2>&1 &` to ensure the script returns immediately without hitting the timeout.
* Do not chain multiple coordinate-based actions simultaneously. Because a single click can alter the visual state of the UI, any subsequent coordinates in the same turn will likely be invalid.
* Do NOT include `DISPLAY` in any generated commands or scripts, as this will not take effect. Please just run commands directly without modifying DISPLAY.
* Always output your reasoning before tool call. Do not output a tool call alone.

* Choose GUI actions, code actions, or a mixture of both according to what most reliably achieves and verifies the exact task semantics. Do not unconditionally prefer either code-first or gui-first behavior.
* Treat both GUI and code as tools for both execution and verification. Use whichever combination best maintains the correct target object, state, and constraints for the task.
* Do not silently rewrite the task into an easier nearby task. Preserve the exact object, target, scope, and modality requested by the user. If the instruction is underspecified, ground the target from the current environment before acting, rather than inventing a convenient substitute.
* Treat task completion as requiring explicit verification of the user-requested end state, not just a plausible intermediate state. Before calling DONE, verify the critical constraint fields that define success for this task.
* If new evidence conflicts with your earlier belief that the task is completed, do not call DONE. Use the conflicting evidence to continue, repair, or re-check the task.
* When using code to create or modify artifacts, verify not only that the artifact exists, but that its semantics match the instruction: the correct target object was changed, required formatting or values are correct, no obvious side effects were introduced, and the result is visible or effective in the target application when relevant.
* DO NOT take any screenshot action, and DO NOT produce any reasoning or thought that attempts to obtain, request, or infer the current screen state. A screenshot is already provided to you at every single step — treat the provided image as the definitive and complete view of the current state. Any action or chain-of-thought that implies "let me take a screenshot to check..." or "I need to see the current state first..." is strictly forbidden.
</IMPORTANT>
"""

SYSTEM_PROMPT_WINDOWS = f"""<SYSTEM_CAPABILITY>
* You are utilising a Windows virtual machine using x86_64 architecture with internet access.
* To open browser, please just click on the Chrome icon.  Note, Chrome is what is installed on your system.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.  Either that, or make sure you scroll down to see everything before deciding something isn't available.
* The current date is {datetime.today().strftime('%A, %B %d, %Y')}.
* Home directory of this Windows system is 'C:\\Users\\user'.
* When you want to open some applications on Windows, please use Double Click on it instead of clicking once.
* If you need a password for sudo, The password of the computer is 'osworld-public-evaluation'. 
</SYSTEM_CAPABILITY>"""

SYSTEM_PROMPT_ORM = textwrap.dedent("""
You are an expert Outcome Reward Model designed to evaluate the performance of a Computer Use Agent (CUA). 
You will be provided with a User Instruction and the CUA's Historical Trajectory, which consists of interleaved agent actions (e.g., shell commands, Python scripts, mouse/keyboard GUI interactions), text responses, and environment observations (screenshots).

Your task is to analyze the trajectory and assign a continuous reward score between 0.0 and 1.0.

### Evaluation Criteria
Please evaluate the agent based on the following comprehensive dimensions:

1. Task Completion & Correctness (Primary)
- Did the agent successfully fulfill the user's core instruction?
- Analyze both the final screenshot AND the action history. The final screenshot often reveals the end state, but do NOT rely on it exclusively. If a correct action (e.g., executing a script, saving a file) was performed but the UI did not refresh in time for the final screenshot, you must still credit the agent for that logical action.

2. Efficiency & Elegance (Secondary)
- Did the agent choose an effective and reliable path?
- Do not reward one modality unconditionally. Prefer the method or mixture of methods that best fits the task and most reliably achieves and verifies the exact task semantics. Both GUI and programmatic methods can be good choices when they support a correct, stable, app-visible / evaluator-visible result; penalize method choices that drift from task semantics or leave the final state insufficiently verified.
- Penalize redundant actions, meaningless loops, excessive hesitation, or method choices that make the result less trustworthy for the actual task.

3. Process & Partial Credit (Crucial for RL)
- Do NOT give a binary 0 or 1. Award partial credit for reaching logical milestones.
- If the agent successfully navigated to the right directory, opened the correct software, or wrote 80% of the correct code but failed at the very last step, it should still receive a moderate score (e.g., 0.4 - 0.7) depending on the progress made.

4. Safety & Side Effects
- Did the agent perform any destructive actions not requested by the user? (e.g., deleting unrelated files, closing user's personal windows, exposing sensitive data). Severe penalties apply for unsafe behavior.

### Scoring Rubric Reference
- [0.0 - 0.1]: Total failure. The agent did nothing useful, completely hallucinated, or executed dangerous/destructive actions.
- [0.2 - 0.4]: Poor. Made some initial correct steps (e.g., opened the app) but fundamentally failed the core logic or got stuck in an endless loop.
- [0.5 - 0.7]: Acceptable/Partial Success. Completed the majority of the task but failed the final validation, OR completed the task but used highly inefficient/fragile methods (e.g., tedious GUI clicking instead of code).
- [0.8 - 0.9]: Good. Successfully completed the task with minor sub-optimal steps or slight UI misalignments.
- [0.95 - 1.0]: Excellent. Perfect completion, utilizing elegant, efficient, and robust methods.

### Output Constraints
You must output the evaluation as a valid JSON object wrapped strictly within a markdown code block (```json ... ```). Do not add any conversational text before or after the markdown block. 

The JSON must contain exactly two keys:
- "thought" (string): A concise step-by-step reasoning. Briefly cover: 1. Core intent, 2. Key milestones achieved in trajectory, 3. Efficiency/Safety analysis, 4. Justification for the final score.
- "score" (float): A single number between 0.0 and 1.0.

Example Output:
```json
{
  "thought": "The user wanted to extract data from data.csv to a new Excel file. The agent successfully opened the terminal and wrote a Python pandas script to handle this, which is highly efficient compared to manual GUI copying. However, the agent forgot to execute the script in the final step. Because the programmatic approach was excellent and the script is fully correct, it deserves high partial credit despite the execution failure.",
  "score": 0.65
}
```
"""
)

def _make_api_tool_result(
        result: ToolResult, tool_use_id: str
    ) -> BetaToolResultBlockParam:
        """Convert an agent ToolResult to an API ToolResultBlockParam."""
        tool_result_content: Union[List[Union[BetaTextBlockParam,
                                              BetaImageBlockParam]], str] = []
        is_error = False

        if not result or (result.get('error') is not None and result.get('error') != ""):
            is_error = True
            error_message = str(result.get('error', 'Unknown error occurred')) if result else 'No result received'
            tool_result_content = [{
                "type": "text",
                "text": _maybe_prepend_system_tool_result(result, error_message)
            }]
            
        else:
            if result.get('output'):
                tool_result_content.append({
                    "type": "text",
                    "text": _maybe_prepend_system_tool_result(
                        result,
                        str(result.get('output', '')
                            if result else '') 
                    ),
                })

            if result.get('base64_image'):
                tool_result_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": result.get('base64_image', ''),
                    },
                })
            
            if not tool_result_content:
                tool_result_content.append({
                    "type": "text",
                    "text": "Action completed successfully"
                })

        return {
            "type": "tool_result",
            "content": tool_result_content,
            "tool_use_id": tool_use_id,
            "is_error": is_error,
        }

def _maybe_prepend_system_tool_result(result: ToolResult, result_text: str):
    if not result:
        return result_text

    if result.get('system', False):
        result_text = f"<system>{result.get('system','')}</system>\n{result_text}"
    return result_text



def _inject_prompt_caching(
    messages: list[BetaMessageParam],
):
    """
    Set cache breakpoints for the 3 most recent turns
    one cache breakpoint is left for tools/system prompt, to be shared across sessions
    """

    breakpoints_remaining = 2  # Use full budget for recent messages
    messages_processed = 0
    
    for message in reversed(messages):
        if message["role"] == "user" and isinstance(
            content := message["content"], list
        ):
            messages_processed += 1
            # Check if this message would fit within the remaining budget
            if breakpoints_remaining >= len(content):
                # We have enough budget, spend it and add cache_control
                breakpoints_remaining -= len(content)
                # Use type ignore to bypass TypedDict check until SDK types are updated
                content[-1]["cache_control"] = BetaCacheControlEphemeralParam(  # type: ignore
                    {"type": "ephemeral"}
                )
            else:
                # Check if this is the first message (contains image + text with task description)
                is_first_message = messages_processed == len([msg for msg in messages if msg["role"] == "user"])
                
                if not is_first_message:
                    # Not enough budget, remove any existing cache_control from this message
                    content[-1].pop("cache_control", None)
                # Continue to clean up older messages that might have cache_control from previous turns


def _maybe_filter_to_n_most_recent_images(
    messages: list[BetaMessageParam],
    images_to_keep: int,
    min_removal_threshold: int,
):
    """
    With the assumption that images are screenshots that are of diminishing value as
    the conversation progresses, remove all but the final `images_to_keep` tool_result
    images in place, with a chunk of min_removal_threshold to reduce the amount we
    break the implicit prompt cache.
    """
    if images_to_keep is None:
        return messages

    tool_result_blocks = cast(
        list[BetaToolResultBlockParam],
        [
            item
            for message in messages
            for item in (
                message["content"] if isinstance(message["content"], list) else []
            )
            if isinstance(item, dict) and item.get("type") == "tool_result"
        ],
    )

    total_images = sum(
        1
        for tool_result in tool_result_blocks
        for content in tool_result.get("content", [])
        if isinstance(content, dict) and content.get("type") == "image"
    )

    images_to_remove = total_images - images_to_keep
    # for better cache behavior, we want to remove in chunks
    images_to_remove -= images_to_remove % min_removal_threshold

    for tool_result in tool_result_blocks:
        if isinstance(tool_result.get("content"), list):
            new_content = []
            for content in tool_result.get("content", []):
                if isinstance(content, dict) and content.get("type") == "image":
                    if images_to_remove > 0:
                        images_to_remove -= 1
                        continue
                new_content.append(content)
            tool_result["content"] = new_content


def validate_model_support(model_name: str, provider: APIProvider = APIProvider.BEDROCK, api_key: str = None, temperature: float = None, top_p: float = None, no_thinking: bool = False, use_isp: bool = False) -> bool:
    """
    Validate model support with the same API call pattern as the main agent.
    
    Args:
        model_name: The model name to validate
        provider: API provider (ANTHROPIC, BEDROCK, or VERTEX)
        api_key: Optional API key (only for ANTHROPIC provider), defaults to ANTHROPIC_API_KEY env var
        temperature: Optional temperature parameter for testing
        top_p: Optional top_p parameter for testing
        no_thinking: Disable thinking mode (matches AnthropicAgent)
        use_isp: Use interleaved scratchpad mode (matches AnthropicAgent)
        
    Returns:
        True if model is supported and API call succeeds, False otherwise
    """
    print(f"🔍 Validating model support: {model_name} (provider: {provider.value})")
    
    try:
        from anthropic import Anthropic, AnthropicBedrock, AnthropicVertex
        import os
        import time
        
        # Same client setup as main agent - choose based on provider
        if provider == APIProvider.ANTHROPIC:
            client = Anthropic(
                api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"), 
                max_retries=4
            ).with_options(default_headers={"anthropic-beta": COMPUTER_USE_BETA_FLAG})
        elif provider == APIProvider.BEDROCK:
            client = AnthropicBedrock(
                aws_access_key=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                aws_region=os.getenv('AWS_DEFAULT_REGION'),
            )
        elif provider == APIProvider.VERTEX:
            client = AnthropicVertex()
        
        # Same message format as main agent - always use structured format with cache_control
        messages = [{"role": "user", "content": [{"type": "text", "text": "Respond with 'OK'", "cache_control": {"type": "ephemeral"}}]}]
        
        # Same betas configuration as main agent
        betas = [COMPUTER_USE_BETA_FLAG]
        if use_isp:
            betas.append("interleaved-thinking-2025-05-14")
            
        system = [{"type": "text", "text": "You are Claude. Respond with 'OK'."}]
        
        # Same tools configuration as main agent - use modern computer tool for all models
        tools = [{"name": "computer", "type": COMPUTER_USE_TYPE, 
                 "display_width_px": 1280, "display_height_px": 720, "display_number": 1}]
        
        # Same thinking configuration as main agent
        max_tokens = 50  # Base validation max_tokens
        if no_thinking:
            extra_body = {}
            actual_max_tokens = max_tokens
        else:
            budget_tokens = 2048
            # Same logic as main agent: if max_tokens <= budget_tokens, increase it
            if max_tokens <= budget_tokens:
                actual_max_tokens = budget_tokens + 500
            else:
                actual_max_tokens = max_tokens
            extra_body = {
                "thinking": {"type": "enabled", "budget_tokens": budget_tokens}
            }
        
        # Sampling parameters (same logic as main agent)
        sampling_params = {}
        if temperature is not None:
            sampling_params['temperature'] = temperature
        if top_p is not None:
            sampling_params['top_p'] = top_p
        
        # Retry logic with 5 attempts, 5 second delays
        for attempt in range(5):
            try:
                # Same API call pattern as main agent
                client.beta.messages.create(
                    max_tokens=actual_max_tokens,
                    messages=messages,
                    model=get_model_name(provider, model_name),
                    system=system,
                    tools=tools,
                    betas=betas,
                    extra_body=extra_body,
                    **sampling_params
                )
                
                print(f"✅ Model {model_name} validated successfully with {provider.value}")
                return True
            except Exception as e:
                error_msg = str(e)
                if attempt < 4:  # Don't print error on final attempt
                    print(f"🔄 Validation attempt {attempt + 1}/5 failed: \"{error_msg}\"")
                    print(f"⏳ Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"❌ All validation attempts failed. Final error: \"{error_msg}\"")
        
        return False
        
    except ValueError:
        return False
    except Exception as e:
        print(f"❌ API validation setup failed: {e}")
        return False

import logging
logger = logging.getLogger("desktopenv.agent")
def _response_to_params(
    response: BetaMessage,
) -> list[BetaContentBlockParam]:
    res: list[BetaContentBlockParam] = []
    if response.content:
        for block in response.content:
            if isinstance(block, BetaTextBlock):
                if block.text:
                    res.append(BetaTextBlockParam(type="text", text=block.text))

            elif isinstance(block, BetaThinkingBlock) and getattr(block, "type", None) == "thinking":
                logger.warning(f'出现 thinking block: {block}')
                # Handle thinking blocks - include signature field
                thinking_block = {
                    "type": "thinking",
                    "thinking": getattr(block, "thinking", None),
                }
                if hasattr(block, "signature"):
                    thinking_block["signature"] = getattr(block, "signature", "[placeholder]")
                
                cast_thinking_block = cast(BetaThinkingBlock, thinking_block)
                cast_thinking_block["signature"] = "[placeholder]" # TODO: 可能需要继续check下
                logger.warning(f'Thinking block 处理后: {cast_thinking_block}')
                res.append(cast_thinking_block)

            else:
                # Handle tool use blocks normally
                res.append(cast(BetaToolUseBlockParam, block.model_dump()))
        return res
    else:
        return []
    

def _normalize_messages_for_log(messages):
    """将 messages 中的图片内容替换为占位符，避免日志写入大量 base64 图片。"""
    if not messages:
        return messages

    def _normalize_content(content):
        if isinstance(content, list):
            normalized = []
            placeholder = {
                "type": "image_placeholder",
                "detail": "[IMAGE_CONTENT_REMOVED_FOR_LOGGING]",
            }
            for block in content:
                if isinstance(block, dict) and block.get("type") == "image":
                    normalized.append(placeholder)
                elif block.get("type") == "tool_result":
                    new_block = dict(block)
                    if "content" in new_block:
                        new_block['content'] = _normalize_content(new_block["content"])
                    normalized.append(new_block)
                else:
                    normalized.append(block)
            return normalized
        return content

    normalized_messages = []
    for m in messages:
        """
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call_id,
                        "content": [{"type": "text", "text": result}]
                    }
                ]
            }

            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {xxx}
                    }
                ]
            }
        """
        if not isinstance(m, dict):
            normalized_messages.append(m)
            continue
        new_m = dict(m)
        if "content" in new_m:
            new_m["content"] = _normalize_content(new_m["content"])
        normalized_messages.append(new_m)
    return normalized_messages

def log_claude_api_call(
    *,
    model_name: str,
    provider: APIProvider,
    request_messages,
    response,
    duration_ms: float,
    success: bool,
    error: Optional[str] = None,
):
    """记录 Claude API 调用日志到 api_logs，图片用占位符。"""
    from datetime import datetime

    # 以月份作为子目录，例如 2026-02, 2026-03
    now = datetime.utcnow()
    month_calls_model_jsonl_dir = CALLS_LOG_DIR / now.strftime("%Y-%m") / model_name
    month_stats_model_jsonl_dir = STAT_LOG_DIR / now.strftime("%Y-%m") / model_name
    month_calls_model_jsonl_filename = CALLS_LOG_DIR / now.strftime("%Y-%m") / model_name / f'{model_name}.jsonl'
    month_stats_model_jsonl_filename = STAT_LOG_DIR / now.strftime("%Y-%m") / model_name / f'{model_name}.jsonl'

    month_calls_model_jsonl_dir.mkdir(exist_ok=True)
    month_stats_model_jsonl_dir.mkdir(exist_ok=True)
    month_calls_model_jsonl_filename.touch(exist_ok=True)
    month_stats_model_jsonl_filename.touch(exist_ok=True)

    ts = now.strftime("%Y%m%d_%H%M%S_%f")


    safe_messages = _normalize_messages_for_log(request_messages)

    usage = None
    if hasattr(response, "usage") and response.usage:
        usage = response.usage.model_dump()

    response_summary = None
    if response and getattr(response, "content", None):
        texts = []
        for block in response.content:
            if hasattr(block, "text") and block.text:
                texts.append(block.text)
        if texts:
            merged = "\n".join(texts)
            response_summary = merged[:2000]

    stats_log_record = {
        "timestamp_utc": ts,
        "duration_ms": duration_ms,
        "success": success,
        "usage": usage
    }

    calls_log_record = {
        "timestamp_utc": ts,
        "provider": provider.name if hasattr(provider, "name") else str(provider),
        "model": model_name,
        "success": success,
        "error": error,
        "duration_ms": duration_ms,
        "request": {
            "messages": safe_messages,
        },
        "response": {
            "usage": usage,
            "summary_text": response_summary,
        },
    }

    # 追加写入当月 jsonl 文件
    with month_calls_model_jsonl_filename.open("a", encoding="utf-8") as f:
        f.write(json.dumps(calls_log_record, ensure_ascii=False) + "\n")
    with month_stats_model_jsonl_filename.open("a", encoding="utf-8") as f:
        f.write(json.dumps(stats_log_record, ensure_ascii=False) + "\n")
