from __future__ import annotations

import os
from typing import Optional
from urllib.parse import unquote, urlparse

DEFAULT_BASE_URL = "https://huggingface.co/datasets/xlangai/osworld_v2_assets/resolve/main"


def resolve_local_source(url: str) -> Optional[str]:
    if not url:
        return None
    if url.startswith("file://"):
        path = unquote(urlparse(url).path)
        return path if os.path.exists(path) else None
    if "://" not in url and os.path.exists(url):
        return url
    return None


def get_base_url() -> str:
    return os.environ.get("OSWORLD_FILE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def asset(path: str) -> str:
    if not path:
        raise ValueError("asset() requires a non-empty relative path")
    rel = path.lstrip("/")
    base = get_base_url()
    if "://" not in base:
        return os.path.join(base, rel)
    return f"{base}/{rel}"
