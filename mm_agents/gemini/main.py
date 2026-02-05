import base64
import os
import time
from PIL import Image
import io
from typing import Literal, Optional, Union, Any

from google import genai
from google.genai import types
import termcolor
from google.genai.types import (
    Part,
    GenerateContentConfig,
    Content,
    Candidate,
    FunctionResponse,
    FinishReason,
)
from rich.console import Console
from rich.table import Table


MAX_RECENT_TURN_WITH_SCREENSHOTS = 3
PREDEFINED_COMPUTER_USE_FUNCTIONS = [
    "open_web_browser",
    "click_at",
    "hover_at",
    "type_text_at",
    "scroll_document",
    "scroll_at",
    "wait_5_seconds",
    "go_back",
    "go_forward",
    "search",
    "navigate",
    "key_combination",
    "drag_and_drop",
]


import logging
logger = logging.getLogger("desktopenv.agent")


class GeminiAgent:
    def __init__(
        self,
        platform: str = "Ubuntu",
        model: str = "gemini-3-flash-preview",
        max_tokens: int = 4096,
        api_key: str = "",
        base_url: str = "",
        action_space: str = "pyautogui",
        screen_size: tuple[int, int] = (1920, 1080),
    ):
        pass
    