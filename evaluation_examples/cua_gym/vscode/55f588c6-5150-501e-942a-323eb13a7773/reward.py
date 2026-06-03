"""
Reward Script: Configure VSCode vertical rulers at columns 80 and 120 with distinct colors
Task ID: vscode_prod_024
Domain: vscode
Scoring:
  Component 1: editor.rulers contains ruler at column 80 (0.3 pts)
  Component 2: editor.rulers contains ruler at column 120 (0.3 pts)
  Component 3: The two rulers have distinct colors (0.2 pts)
  Component 4: workbench.colorCustomizations has ruler color customization (0.2 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def get_ruler_info(rulers):
    """Extract column and color info from rulers list.
    Rulers can be integers (just column) or dicts with column/color keys.
    Returns list of (column, color_or_None) tuples.
    """
    result = []
    for r in rulers:
        if isinstance(r, int):
            result.append((r, None))
        elif isinstance(r, dict):
            col = r.get("column")
            color = r.get("color")
            result.append((col, color))
    return result


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

    rulers = settings.get("editor.rulers", [])
    ruler_info = get_ruler_info(rulers)
    columns = [col for col, _ in ruler_info]

    # Component 1: editor.rulers contains ruler at column 80 (0.3 points)
    try:
        if 80 in columns:
            print(f"PASS: Component 1 — Ruler at column 80 found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No ruler at column 80. Columns found: {columns}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.rulers contains ruler at column 120 (0.3 points)
    try:
        if 120 in columns:
            print(f"PASS: Component 2 — Ruler at column 120 found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No ruler at column 120. Columns found: {columns}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The two rulers have distinct colors (0.2 points)
    # Both rulers must exist and have different color values
    try:
        color_80 = None
        color_120 = None
        for col, color in ruler_info:
            if col == 80:
                color_80 = color
            elif col == 120:
                color_120 = color

        if color_80 is not None and color_120 is not None and color_80 != color_120:
            print(f"PASS: Component 3 — Rulers have distinct colors: 80={color_80}, 120={color_120} (0.2 pts)")
            total_score += 0.2
        elif color_80 is not None and color_120 is not None:
            print(f"FAIL: Component 3 — Rulers have same color: 80={color_80}, 120={color_120}")
        else:
            print(f"FAIL: Component 3 — Missing color on one or both rulers: 80={color_80}, 120={color_120}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: workbench.colorCustomizations has ruler-related color entry (0.2 points)
    try:
        color_customs = settings.get("workbench.colorCustomizations", {})
        if isinstance(color_customs, dict) and len(color_customs) > 0:
            # Check for any ruler-related color key
            ruler_keys = [k for k in color_customs.keys() if "ruler" in k.lower()]
            if ruler_keys:
                print(f"PASS: Component 4 — workbench.colorCustomizations has ruler color keys: {ruler_keys} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — workbench.colorCustomizations exists but no ruler-related keys. Keys: {list(color_customs.keys())}")
        else:
            print(f"FAIL: Component 4 — workbench.colorCustomizations is empty or missing")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
