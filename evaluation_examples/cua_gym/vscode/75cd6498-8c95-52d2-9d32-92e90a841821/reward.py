"""
Reward Script: Install Python Test Explorer and configure CodeLens annotations
Task ID: vscode_py_035
Domain: vscode
Scoring:
  Component 1 (0.4): python.testing.pytestEnabled is true
  Component 2 (0.3): editor.codeLens is true (enables inline test annotations)
  Component 3 (0.3): python.testing.pytestArgs configured
"""

import os
import json
import re

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
TASK_ID = 'vscode_py_035'


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: python.testing.pytestEnabled is true (0.4 points)
    # Initial state has this as false; golden state has it as true.
    # This is the core task requirement for enabling pytest-based test discovery.
    try:
        pytest_enabled = settings.get('python.testing.pytestEnabled')
        if pytest_enabled is True:
            print(f"PASS: Component 1 — python.testing.pytestEnabled is true (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — python.testing.pytestEnabled expected true, found: {pytest_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.codeLens is true (0.3 points)
    # Initial state does not have this setting; golden state sets it to true.
    # CodeLens enables inline "Run Test | Debug Test" annotations above test functions.
    try:
        code_lens = settings.get('editor.codeLens')
        if code_lens is True:
            print(f"PASS: Component 2 — editor.codeLens is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — editor.codeLens expected true, found: {code_lens}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: python.testing.pytestArgs is configured (0.3 points)
    # Initial state does not have this setting; golden state sets it to ["tests"].
    # This configures the test directory for pytest discovery.
    try:
        pytest_args = settings.get('python.testing.pytestArgs')
        if isinstance(pytest_args, list) and len(pytest_args) > 0:
            print(f"PASS: Component 3 — python.testing.pytestArgs is configured: {pytest_args} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — python.testing.pytestArgs expected non-empty list, found: {pytest_args}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
