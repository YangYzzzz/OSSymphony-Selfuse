"""
Reward Script: Modify multi-root workspace settings for font config
Task ID: vscode_we_029
Domain: vscode
Scoring:
  - Component 1: editor.fontFamily == "JetBrains Mono" (0.35)
  - Component 2: editor.fontSize == 14 (0.35)
  - Component 3: editor.fontLigatures == true (0.30)
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_029'
WORKSPACE_PATH = os.path.join(WORKDIR, 'projects', 'fullstack.code-workspace')


def load_workspace_settings(ws_path):
    """Load the settings dict from a .code-workspace file, handling JSONC comments."""
    with open(ws_path, 'r') as f:
        content = f.read()
    # Strip JSONC-style comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    data = json.loads(content)
    return data.get('settings', {})


def verify_task(ws_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: workspace file must exist and be valid JSON
    try:
        settings = load_workspace_settings(ws_path)
        print(f"INFO: Loaded workspace settings with {len(settings)} keys: {list(settings.keys())}")
    except FileNotFoundError:
        print(f"CRITICAL: Workspace file not found: {ws_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse workspace file {ws_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.fontFamily == "JetBrains Mono" (0.35 points)
    try:
        font_family = settings.get('editor.fontFamily')
        if isinstance(font_family, str) and font_family.strip() == 'JetBrains Mono':
            print(f"PASS: Component 1 — editor.fontFamily is 'JetBrains Mono' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected editor.fontFamily='JetBrains Mono', found: {font_family!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.fontSize == 14 (0.35 points)
    try:
        font_size = settings.get('editor.fontSize')
        if font_size == 14:
            print(f"PASS: Component 2 — editor.fontSize is 14 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — expected editor.fontSize=14, found: {font_size!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.fontLigatures == true (0.30 points)
    try:
        font_ligatures = settings.get('editor.fontLigatures')
        if font_ligatures is True:
            print(f"PASS: Component 3 — editor.fontLigatures is true (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — expected editor.fontLigatures=true, found: {font_ligatures!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(WORKSPACE_PATH):
    print(f"File not found: {WORKSPACE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(WORKSPACE_PATH)
