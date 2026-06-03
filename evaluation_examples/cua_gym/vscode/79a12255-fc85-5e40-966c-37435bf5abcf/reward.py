"""
Reward Script: Configure Vim extension settings in VSCode
Task ID: vscode_we_086
Domain: vscode
Scoring:
  - Component 1: vim.leader set to "<space>" (0.2 pts)
  - Component 2: vim.useSystemClipboard set to true (0.2 pts)
  - Component 3: editor.lineNumbers set to "relative" (0.2 pts)
  - Component 4: vim.normalModeKeyBindingsNonRecursive contains leader+w -> :w (0.2 pts)
  - Component 5: vim.normalModeKeyBindingsNonRecursive contains leader+q -> :q (0.2 pts)
"""

import os
import json
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")

def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None

def verify_task():
    """
    Verify Vim extension configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: vim.leader set to "<space>" (0.2 points)
    try:
        leader = settings.get("vim.leader")
        if leader == "<space>":
            print(f"PASS: Component 1 — vim.leader is '<space>' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected vim.leader='<space>', found: {leader!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: vim.useSystemClipboard set to true (0.2 points)
    try:
        clipboard = settings.get("vim.useSystemClipboard")
        if clipboard is True:
            print(f"PASS: Component 2 — vim.useSystemClipboard is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected vim.useSystemClipboard=true, found: {clipboard!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.lineNumbers set to "relative" (0.2 points)
    try:
        line_numbers = settings.get("editor.lineNumbers")
        if line_numbers == "relative":
            print(f"PASS: Component 3 — editor.lineNumbers is 'relative' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected editor.lineNumbers='relative', found: {line_numbers!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: normalModeKeyBindingsNonRecursive contains leader+w -> :w (0.2 points)
    try:
        bindings = settings.get("vim.normalModeKeyBindingsNonRecursive", [])
        found_w = False
        if isinstance(bindings, list):
            for binding in bindings:
                before = binding.get("before", [])
                commands = binding.get("commands", [])
                if before == ["<leader>", "w"] and ":w" in commands:
                    found_w = True
                    break
        if found_w:
            print(f"PASS: Component 4 — leader+w -> :w binding found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — leader+w -> :w binding not found in normalModeKeyBindingsNonRecursive")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: normalModeKeyBindingsNonRecursive contains leader+q -> :q (0.2 points)
    try:
        bindings = settings.get("vim.normalModeKeyBindingsNonRecursive", [])
        found_q = False
        if isinstance(bindings, list):
            for binding in bindings:
                before = binding.get("before", [])
                commands = binding.get("commands", [])
                if before == ["<leader>", "q"] and ":q" in commands:
                    found_q = True
                    break
        if found_q:
            print(f"PASS: Component 5 — leader+q -> :q binding found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — leader+q -> :q binding not found in normalModeKeyBindingsNonRecursive")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
