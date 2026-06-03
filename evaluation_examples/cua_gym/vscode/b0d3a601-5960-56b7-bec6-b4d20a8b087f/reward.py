"""
Reward Script: Install Indent Rainbow extension and configure custom colors
Task ID: vscode_ext_031
Domain: vs_code
Scoring:
  Component 1: Indent Rainbow extension installed (0.5 pts)
  Component 2: indentRainbow.colors configured with exact custom RGBA array (0.5 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_031'

EXTENSIONS_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')

# Expected extension identifier prefix
EXTENSION_ID = 'oderwat.indent-rainbow'

# Expected custom colors (exact match required)
EXPECTED_COLORS = [
    "rgba(255,255,64,0.07)",
    "rgba(127,255,127,0.07)",
    "rgba(255,127,255,0.07)",
    "rgba(79,236,236,0.07)"
]


def load_settings(path):
    """Load settings.json, stripping JSONC comments if needed."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not parse settings.json: {e}")
        return {}


def normalize_rgba(color_str):
    """Normalize rgba string by removing spaces around commas for comparison."""
    return re.sub(r'\s+', '', color_str.lower())


def check_extension_installed():
    """
    Check if the Indent Rainbow extension directory exists under .vscode/extensions/.
    Returns the matched entry name if found, or None otherwise.
    Derived from real filesystem listing — no hardcoded result.
    """
    if not os.path.isdir(EXTENSIONS_DIR):
        return None
    entries = os.listdir(EXTENSIONS_DIR)
    for entry in entries:
        if entry.lower().startswith(EXTENSION_ID.lower()):
            return entry
    # Fallback: check extensions.json manifest
    ext_json_path = os.path.join(EXTENSIONS_DIR, 'extensions.json')
    if os.path.isfile(ext_json_path):
        with open(ext_json_path, 'r') as f:
            ext_list = json.load(f)
        for ext in ext_list:
            ext_id = ext.get('identifier', {}).get('id', '')
            if ext_id.lower() == EXTENSION_ID.lower():
                return ext_id
    return None


def check_colors_configured():
    """
    Read settings.json and verify indentRainbow.colors is set to the expected list.
    Returns (ok: bool, message: str).
    """
    settings = load_settings(SETTINGS_PATH)
    actual_colors = settings.get('indentRainbow.colors', None)

    if actual_colors is None:
        return False, "'indentRainbow.colors' key not found in settings.json"
    if not isinstance(actual_colors, list):
        return False, f"'indentRainbow.colors' is not a list, got: {type(actual_colors)}"
    if len(actual_colors) != len(EXPECTED_COLORS):
        return False, f"expected {len(EXPECTED_COLORS)} colors, got {len(actual_colors)}: {actual_colors}"

    # Compare each color (normalize whitespace for robustness)
    mismatches = []
    for i, (actual, expected) in enumerate(zip(actual_colors, EXPECTED_COLORS)):
        if normalize_rgba(str(actual)) != normalize_rgba(expected):
            mismatches.append(f"  index {i}: expected '{expected}', got '{actual}'")
    if mismatches:
        return False, "color mismatch:\n" + "\n".join(mismatches)

    return True, "indentRainbow.colors correctly set to 4 custom RGBA values"


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Indent Rainbow extension is installed (0.5 points)
    # FAILS on initial_env (no extension dir entry) → PASSES on golden_env
    try:
        matched_entry = check_extension_installed()
        if matched_entry is not None:
            print(f"PASS: Component 1 — Indent Rainbow extension found: {matched_entry} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Indent Rainbow extension NOT found in {EXTENSIONS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: indentRainbow.colors is configured with the exact 4 RGBA colors (0.5 points)
    # FAILS on initial_env (key absent) → PASSES on golden_env (key present with correct values)
    try:
        colors_ok, msg = check_colors_configured()
        if colors_ok:
            print(f"PASS: Component 2 — {msg} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — {msg}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
