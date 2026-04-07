"""Qwen3VL SFT wrapper for Gemini trajectories.

This adapts Gemini's OpenAI-style messages into the Claude-like structure
expected by `mm_agents.anthropic.utils.build_qwen_sft_sample`:
- Reasoning content + per-tool `thought` arguments -> <think> ... </think>
- Tool calls -> Claude-style tool_use blocks with `computer` / `code` semantics
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple
from copy import deepcopy
from mm_agents.utils.qwen_vl_utils import (
    QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
    QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN,
    dedup_and_save_images_for_gemini,
)

def truncate_images_for_gemini_context(
      messages: List[Dict[str, Any]],
      max_images: int = 4,                                                                                                                                                             
  ) -> List[Dict[str, Any]]:                                                                                                                                                           
    """复制一份 messages，并只保留最后 max_images 张图片，其余 image block 直接删除。                                                                                                
                                                                                                                                                                                    
    Gemini 的截图位于 user.content 里的 {"type": "image_url", ...}，                                                                                                                     
    这里不区分首屏 / 后续，只按时间顺序截断。
    """                                                                                                                                                                              
    msgs = deepcopy(messages)                             
    if msgs[0]["role"] == "system":
        del msgs[0]

    # 收集所有 image 的 (msg_idx, content_idx)            
    image_positions: List[Tuple[int, int]] = []
    for mi, m in enumerate(msgs):
        # 第一张截图永远保留
        if mi == 0:
            continue

        if isinstance(m, dict) and m.get("role") == "user":                 
            content = m.get("content")
        else:
            continue         
        if not isinstance(content, list):
            continue
        for ci, b in enumerate(content):
            if isinstance(b, dict) and b.get("type") == "image_url":
                image_positions.append((mi, ci))                                                                                                                                     

    if len(image_positions) <= max_images:                                                                                                                                           
        return msgs                                       
                                                                                             
    # 删除最早的那些 image（从后往前删，避免 index 变化）                                                                                                                            
    to_remove = image_positions[: len(image_positions) - max_images]
    for mi, ci in reversed(to_remove):                                                                                                                                               
        m = msgs[mi]                                      
        content = m.get("content")                                                                                                          
        if isinstance(content, list) and ci < len(content):
            del content[ci]

    return msgs

def build_qwen_tool_call_message(action: Dict[str, Any]) -> Dict[str, Any]:
    """根据已映射好的 Qwen 动作，构造单条 tool_call message。

    action: 形如 {"action": "left_click", "coordinate": [x, y]} 等，
    会被包装进 Qwen3VL 的统一工具 schema：name="custom_computer_use"。
    """

    payload = {
        "name": "custom_computer_use",
        "arguments": action,
    }
    return {
        "role": "tool_call",
        "content": json.dumps(payload, ensure_ascii=False),
    }


def build_qwen_tool_response_message(result_text: str) -> Dict[str, Any]:
    """根据工具执行结果构造单条 tool_response message。

    result_text: 工具输出文本（例如 code 结果），可为空字符串。
    has_image: 是否有对应截图，如果有，则在 payload 里加上 "images": "<image>"。
    """

    payload: Dict[str, Any] = {}
    if result_text != "Success":
        payload["code_result"] = result_text
    else:
        payload["status"] = result_text

    return {
        "role": "tool_response",
        "content": json.dumps(payload, ensure_ascii=False),
    }

def build_qwen_messages_from_gemini(
    step_messages: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """将截断后的 Gemini messages 转成 Qwen3VL SFT messages（多轮）。

    规则：
    - 第一条 Qwen message 永远是统一的 system；
    - 之后按顺序遍历每一条 Gemini message：
      - system: 跳过（我们已经写了统一 system）；
      - user: 每条 user -> 一条 Qwen user（文本 + 可选 <image>）；
      - assistant: 每条 assistant -> 一条 <think>（如果有 reasoning_content），
        然后它内部的 tool_calls 被展开成多条 tool_call；
      - tool:  tool_results + images 调用 build_qwen_tool_response_message 追加。
    """

    qwen_messages: List[Dict[str, Any]] = []

    # 1) system：固定一条
    qwen_messages.append(
        {
            "role": "system",
            "content": {
                "type": "text",
                "text": QWEN3VL_COMPUTER_USE_SYSTEM_PROMPT_FOR_TRAIN,
            },
        }
    )

    # 2) 顺序遍历每一条 Gemini message
    for m in step_messages:
        if not isinstance(m, dict):
            continue

        role = m.get("role")
        content = m.get("content")

        # --- user ---
        if role == "user":
            text_parts: List[str] = []
            user_str = ""
            has_image = False
            if isinstance(content, list):
                for b in content:
                    if not isinstance(b, dict):
                        continue
                    t = b.get("type")
                    if t == "text":
                        text_parts.append(str(b.get("text") or ""))
                    elif t == "image_url":
                        has_image = True

            user_str = "".join(text_parts)
            if has_image:
                user_str += "<image>"

            qwen_messages.append(
                {
                    "role": "user",
                    "content": user_str,
                }
            )

        # --- assistant ---
        elif role == "assistant":
            # 1) reasoning_content -> <think>
            reasoning = m.get("reasoning_content") or content or ""
            if reasoning:
                qwen_messages.append(
                    {
                        "role": "assistant",
                        "content": f"{reasoning}", # TODO: 是否添加 <think> tag 有待探究
                    }
                )

            # 2) tool_calls -> 多条 tool_call
            tool_calls = m.get("tool_calls") or []
            for tc in tool_calls:
                func = tc.get("function") or {}
                name = func.get("name") or ""
                raw_args = func.get("arguments") or "{}"
                try:
                    args: Dict[str, Any] = json.loads(raw_args)
                except Exception:
                    args = {}

                # thought 已在 agent 侧加进 reasoning，这里不再使用
                args.pop("thought", None)

                q_actions: List[Dict[str, Any]] = []

                if name == "click_at":
                    q_actions.append({"action": "left_click", "coordinate": [args.get("x", 0), args.get("y", 0)]})
                elif name == "hover_at":
                    q_actions.append({"action": "mouse_move", "coordinate": [args.get("x", 0), args.get("y", 0)]})
                elif name == "type_text_at":
                    q_actions.append({"action": "left_click", "coordinate": [args.get("x", 0), args.get("y", 0)]})
                    q_actions.append({"action": "type", "text": args.get("text", "")})
                elif name == "scroll_document":
                    direction = args.get("direction") or "down"
                    if direction in ("left", "right"):
                        q_actions.append({"action": "hscroll", "pixels": 2, "direction": direction})
                    else:
                        q_actions.append({"action": "scroll", "pixels": 2, "direction": direction})
                elif name == "scroll_at":
                    x = args.get("x", 0)
                    y = args.get("y", 0)
                    direction = args.get("direction") or "down"
                    q_actions.append({"action": "mouse_move", "coordinate": [x, y]})
                    if direction in ("left", "right"):
                        q_actions.append({"action": "hscroll", "pixels": 2, "direction": direction, "coordinate": [x, y]})
                    else:
                        q_actions.append({"action": "scroll", "pixels": 2, "direction": direction, "coordinate": [x, y]})
                elif name == "wait_5_seconds":
                    q_actions.append({"action": "wait", "time": 5})
                elif name == "key_combination":
                    keys_str = args.get("keys", "")
                    keys = [k.strip() for k in keys_str.split("+") if k.strip()]
                    q_actions.append({"action": "key", "keys": keys})
                elif name == "drag_and_drop":
                    sx = args.get("x", 0)
                    sy = args.get("y", 0)
                    dx = args.get("destination_x", 0)
                    dy = args.get("destination_y", 0)
                    q_actions.append({"action": "mouse_move", "coordinate": [sx, sy]})
                    q_actions.append({"action": "left_click_drag", "coordinate": [dx, dy], "start_coordinate": [sx, sy]})
                elif name == "code":
                    lang = (args.get("language") or "python").lower()
                    code_str = args.get("execute_code") or ""
                    q_actions.append({
                        "action": "execute_code",
                        "language": "python" if "py" in lang else "bash",
                        "code": code_str,
                    })
                else:
                    q_actions.append({"action": "terminate", "status": "failure"})

                for q_arg in q_actions:
                    qwen_messages.append(build_qwen_tool_call_message(q_arg))

            if not tool_calls:
                if "[INFEASIBLE]" in reasoning:
                    qwen_messages.append(build_qwen_tool_call_message({"action": "terminate", "status": "failure"}))
                else:
                    qwen_messages.append(build_qwen_tool_call_message({"action": "terminate", "status": "success"}))

        # --- tool ---
        elif role == "tool":
            qwen_messages.append(
                build_qwen_tool_response_message(result_text=content or "")
            )


    return qwen_messages

def build_qwen_sft_sample_for_gemini(
    messages: List[Dict[str, Any]],
    image_hash_map: Dict[str, str],
    image_root_dir,
):
    """
    messages 为当前全部 message, OpenAI/Gemini chat 格式，形如：
        system
        user(text + image)
        assistant(tool_calls)
        tool(result)
        user(image),
        重复
        ...

    输出一条 Qwen3VL SFT sample：
    - tools: QWEN3VL_COMPUTER_USE_TOOL_SCHEMA
    - messages: system + user + assistant(<think>) + tool_call(+tool_response)
    - images: 对应截图文件名列表

    动作映射：
    click_at       -> left_click
    hover_at       -> mouse_move
    type_text_at   -> left_click + type
    scroll_document-> scroll / hscroll
    scroll_at      -> mouse_move + scroll / hscroll
    wait_5_seconds -> wait
    key_combination-> key
    drag_and_drop  -> mouse_move + left_click_drag
    code           -> execute_code
    """
     # 0) 先做截图截断：全局只保留最近 5 张
    messages = truncate_images_for_gemini_context(messages, max_images=4)
    
    # 1) 保存图片并拿到文件名列表
    images, image_hash_map = dedup_and_save_images_for_gemini(
        messages=messages,
        image_hash_map=image_hash_map,
        image_root_dir=image_root_dir
    )

    # 2) 构造 Qwen 消息
    qwen_messages = build_qwen_messages_from_gemini(
        step_messages=messages
    )
    
    sample = {
        "tools": QWEN3VL_COMPUTER_USE_TOOL_SCHEMA,
        "messages": qwen_messages,
        "images": images,
    }

    return sample, image_hash_map