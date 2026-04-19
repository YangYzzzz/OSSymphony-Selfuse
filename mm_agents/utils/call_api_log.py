import json
from pathlib import Path
from typing import Any, Dict, List, Optional


CALLS_LOG_DIR = Path("api_logs/calls")
STAT_LOG_DIR = Path("api_logs/stats")


def _normalize_openai_messages_for_log(messages: List[Dict[str, Any]]):
    """Normalize OpenAI-style messages, removing large image payloads.

    Expected format (simplified):
    [
        {"role": "user", "content": [
            {"type": "text", "text": "..."},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
        ]},
        {"role": "assistant", "content": "..."},
    ]
    """
    if not messages:
        return messages

    def _normalize_content(content):
        # OpenAI responses can be either list-of-parts or a plain string
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            normalized = []
            placeholder = {
                "type": "image_placeholder",
                "detail": "[IMAGE_CONTENT_REMOVED_FOR_LOGGING]",
            }
            for part in content:
                if not isinstance(part, dict):
                    normalized.append(part)
                    continue

                # Vision content
                if part.get("type") == "image_url":
                    normalized.append(placeholder)
                else:
                    # Shallow copy to avoid mutating original
                    new_part = dict(part)
                    image_url = new_part.get("image_url")
                    if isinstance(image_url, dict) and isinstance(image_url.get("url"), str) and image_url["url"].startswith("data:image/"):
                        new_part["image_url"] = {
                            "url": "[IMAGE_CONTENT_REMOVED_FOR_LOGGING]"
                        }
                    normalized.append(new_part)
            return normalized

        return content

    normalized_messages: List[Dict[str, Any]] = []
    for m in messages:
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
    provider,
    request_messages,
    response,
    duration_ms: float,
    success: bool,
    error: Optional[str] = None,
):
    """Record Claude API call logs to api_logs, replacing images with placeholders.

    This is a thin wrapper so existing Anthropic code can import from this
    shared module instead of mm_agents/anthropic/utils.py.
    """
    from mm_agents.anthropic.utils import log_claude_api_call as _impl  # type: ignore

    return _impl(
        model_name=model_name,
        provider=provider,
        request_messages=request_messages,
        response=response,
        duration_ms=duration_ms,
        success=success,
        error=error,
    )


def log_openai_api_call(
    *,
    model_name: str,
    request_messages: List[Dict[str, Any]],
    response: Any,
    duration_ms: float,
    success: bool,
    error: Optional[str] = None,
):
    """Record OpenAI/Gemini-style API call logs to api_logs.

    - Messages are normalized to strip inline base64 images.
    - Response usage is extracted if present (OpenAI-style response.usage).
    - A short text summary is extracted from the first choice if available.
    """
    try:
        from datetime import datetime

        now = datetime.utcnow()
        # Use model name as directory under month folder, consistent with Claude
        month_calls_model_jsonl_filename = CALLS_LOG_DIR / now.strftime("%Y-%m") / model_name / f"{model_name}.jsonl"
        month_stats_model_jsonl_filename = STAT_LOG_DIR / now.strftime("%Y-%m") / model_name / f"{model_name}.jsonl"
        month_calls_model_jsonl_filename.parent.mkdir(parents=True, exist_ok=True)
        month_stats_model_jsonl_filename.parent.mkdir(parents=True, exist_ok=True)
        month_calls_model_jsonl_filename.touch(exist_ok=True)
        month_stats_model_jsonl_filename.touch(exist_ok=True)

        ts = now.strftime("%Y%m%d_%H%M%S_%f")

        safe_messages = _normalize_openai_messages_for_log(request_messages)

        usage = None
        try:
            if getattr(response, "usage", None) is not None:
                # OpenAI python client usage object has model_dump() in v1-style
                usage_attr = response.usage
                usage = usage_attr.model_dump() if hasattr(usage_attr, "model_dump") else usage_attr
        except Exception:
            usage = None

        response_summary = None
        try:
            # OpenAI-compatible chat completion
            if response is not None and getattr(response, "choices", None):
                first = response.choices[0]
                msg = getattr(first, "message", None) or getattr(first, "delta", None)
                if msg is not None:
                    content = getattr(msg, "content", None)
                    if isinstance(content, str):
                        response_summary = content[:2000]
                    elif isinstance(content, list):
                        texts = []
                        for part in content:
                            if isinstance(part, dict) and part.get("type") == "text" and part.get("text"):
                                texts.append(part["text"])
                        if texts:
                            merged = "\n".join(texts)
                            response_summary = merged[:2000]
        except Exception:
            response_summary = None

        stats_log_record = {
            "timestamp_utc": ts,
            "duration_ms": duration_ms,
            "success": success,
            "usage": usage,
        }

        calls_log_record = {
            "timestamp_utc": ts,
            "provider": "openai/gemini",
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

        with month_calls_model_jsonl_filename.open("a", encoding="utf-8") as f:
            f.write(json.dumps(calls_log_record, ensure_ascii=False) + "\n")
        with month_stats_model_jsonl_filename.open("a", encoding="utf-8") as f:
            f.write(json.dumps(stats_log_record, ensure_ascii=False) + "\n")
    except Exception:
        # Best-effort logging only
        return None
