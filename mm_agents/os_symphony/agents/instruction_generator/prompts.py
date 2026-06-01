from __future__ import annotations

import os
from typing import Dict

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")
_PROMPT_CACHE: Dict[str, str] = {}


def load_prompt(filename: str) -> str:
    if filename not in _PROMPT_CACHE:
        with open(os.path.join(PROMPT_DIR, filename), "r", encoding="utf-8") as f:
            _PROMPT_CACHE[filename] = f.read().strip()
    return _PROMPT_CACHE[filename]
