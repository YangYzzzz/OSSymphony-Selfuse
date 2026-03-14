"""Shared test fixtures."""

import sys
import os
from unittest.mock import MagicMock

import pytest

# Ensure the package root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def make_mock_desktop_env(vnc_port: int = 5900):
    """Create a MagicMock that behaves like DesktopEnv."""
    env = MagicMock()
    env.vnc_port = vnc_port
    env.start.return_value = None
    env.close.return_value = None
    env.reset.return_value = {
        "screenshot": b"\x89PNG fake screenshot bytes",
        "accessibility_tree": "<tree><node/></tree>",
        "terminal": "$ ",
        "instruction": "Open the terminal",
    }
    env.step.return_value = (
        {
            "screenshot": b"\x89PNG step screenshot",
            "accessibility_tree": "<tree/>",
            "terminal": "$ ls",
            "instruction": "Open the terminal",
        },
        0.0,   # reward
        False,  # done
        {},     # info
    )
    env.evaluate.return_value = 1.0
    return env


@pytest.fixture
def mock_desktop_env():
    return make_mock_desktop_env()


@pytest.fixture
def env_factory():
    """Factory that produces mock DesktopEnv instances with unique VNC ports."""
    counter = {"n": 0}

    def _factory():
        port = 5900 + counter["n"]
        counter["n"] += 1
        return make_mock_desktop_env(vnc_port=port)

    return _factory
