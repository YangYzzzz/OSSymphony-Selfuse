from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

from mm_agents.utils.qwen_vl_utils import (
    QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN,
    QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
    dedup_and_save_images_for_gemini,
)

QWEN_ACTIONS = {
    "key",
    "type",
    "mouse_move",
    "left_click",
    "left_click_drag",
    "right_click",
    "middle_click",
    "double_click",
    "triple_click",
    "scroll",
    "hscroll",
    "wait",
    "terminate",
    "code",
}


def truncate_images_for_ossymphony_context(
    messages: List[Dict[str, Any]],
    max_images: int = 4,
) -> List[Dict[str, Any]]:
    msgs = deepcopy(messages)
    image_positions: List[tuple[int, int]] = []
    first_image_position: tuple[int, int] | None = None

    for mi, message in enumerate(msgs):
        if not isinstance(message, dict) or message.get("role") != "user":
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for ci, block in enumerate(content):
            if isinstance(block, dict) and block.get("type") == "image_url":
                if first_image_position is None:
                    first_image_position = (mi, ci)
                else:
                    image_positions.append((mi, ci))

    if len(image_positions) <= max_images:
        return msgs

    for mi, ci in reversed(image_positions[: len(image_positions) - max_images]):
        content = msgs[mi].get("content")
        if isinstance(content, list) and ci < len(content):
            del content[ci]

    return msgs


def build_qwen_tool_call_message(arguments: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "role": "tool_call",
        "content": json.dumps(
            {"name": "custom_computer_use", "arguments": arguments},
            ensure_ascii=False,
        ),
    }


def build_qwen_tool_response_message(result_text: str) -> Dict[str, Any]:
    payload: Dict[str, Any]
    if result_text == "Success":
        payload = {"status": result_text}
    else:
        payload = {"code_result": result_text}
    return {"role": "tool_response", "content": json.dumps(payload, ensure_ascii=False)}


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text") or ""))
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts)
    return ""


def _normalize_ossymphony_action_arguments(args: Dict[str, Any]) -> Dict[str, Any]:
    q_args = deepcopy(args)
    action = q_args.get("action")

    if action == "click":
        q_args["action"] = "left_click"
    elif action == "left_press":
        q_args["action"] = "left_click"
    elif action == "done":
        q_args = {"action": "terminate", "status": "success"}
    elif action == "fail":
        q_args = {"action": "terminate", "status": "failure"}
    elif action == "keys" and isinstance(q_args.get("keys"), str):
        q_args["keys"] = [key.strip().lower() for key in q_args["keys"].replace("+", ",").split(",") if key.strip()]
    elif action == "scroll" and q_args.get("direction") in {"left", "right"}:
        q_args["action"] = "hscroll"
    elif action == "code":
        language = (q_args.get("language") or "python").lower()
        q_args["language"] = "python" if "py" in language else "bash"
    elif action not in QWEN_ACTIONS:
        q_args = {"action": "terminate", "status": "failure"}

    return q_args


def build_qwen_messages_from_ossymphony(step_messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    qwen_messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN,
        }
    ]

    for message in step_messages:
        if not isinstance(message, dict):
            continue

        role = message.get("role")
        content = message.get("content")

        if role == "system":
            continue

        if role == "user":
            if isinstance(content, str):
                user_text = content
            elif isinstance(content, list):
                parts: List[str] = []
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "text":
                        parts.append(str(block.get("text") or ""))
                    elif block.get("type") == "image_url":
                        parts.append("<image>")
                user_text = "".join(parts)
            else:
                user_text = ""

            if user_text == "[Old Screenshot Removed]":
                user_text = ""

            if user_text:
                qwen_messages.append({"role": "user", "content": user_text})

        elif role == "assistant":
            assistant_text = ""
            reasoning_content = message.get("reasoning_content") or ""
            if reasoning_content:
                assistant_text = str(reasoning_content)
            else:
                assistant_text = _content_to_text(content)
            if assistant_text:
                qwen_messages.append({"role": "assistant", "content": assistant_text})

            tool_calls = message.get("tool_calls") or []
            for tool_call in tool_calls:
                function = tool_call.get("function") or {}
                raw_args = function.get("arguments") or "{}"
                try:
                    args = json.loads(raw_args) if isinstance(raw_args, str) else dict(raw_args)
                except Exception:
                    args = {"action": "terminate", "status": "failure"}

                qwen_messages.append(build_qwen_tool_call_message(_normalize_ossymphony_action_arguments(args)))

            if not tool_calls and "[INFEASIBLE]" in assistant_text:
                qwen_messages.append(build_qwen_tool_call_message({"action": "terminate", "status": "failure"}))

        elif role == "tool":
            qwen_messages.append(build_qwen_tool_response_message(_content_to_text(content)))

    return qwen_messages


def build_qwen_sft_sample_for_ossymphony(
    messages: List[Dict[str, Any]],
    image_hash_map: Dict[str, str],
    image_root_dir: Path,
):
    truncated_messages = truncate_images_for_ossymphony_context(messages, max_images=4)
    image_root_dir.mkdir(parents=True, exist_ok=True)

    images, image_hash_map = dedup_and_save_images_for_gemini(
        messages=truncated_messages,
        image_hash_map=image_hash_map,
        image_root_dir=image_root_dir,
    )

    sample = {
        "tools": QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
        "messages": build_qwen_messages_from_ossymphony(truncated_messages),
        "images": images,
    }

    return sample, image_hash_map
