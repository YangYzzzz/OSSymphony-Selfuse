"""
Reward Script: Configure Flake8 linter extension in VSCode
Task ID: vscode_we_064
Domain: vscode
Scoring:
  Component 1 (0.35): flake8.args contains --max-line-length=120
  Component 2 (0.35): flake8.args contains --ignore=E501,W503
  Component 3 (0.30): flake8.path set to virtualenv path
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip JSONC-style comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify Flake8 configuration in VSCode settings.json.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: flake8.args contains --max-line-length=120 (0.35 points)
    try:
        flake8_args = settings.get("flake8.args", [])
        if isinstance(flake8_args, list) and "--max-line-length=120" in flake8_args:
            print(f"PASS: Component 1 -- flake8.args contains --max-line-length=120 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- expected --max-line-length=120 in flake8.args, found: {flake8_args}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: flake8.args contains --ignore=E501,W503 (0.35 points)
    try:
        flake8_args = settings.get("flake8.args", [])
        if isinstance(flake8_args, list):
            # Extract all --ignore= args, parse codes, compare as sets for order independence
            ignore_codes = set()
            for arg in flake8_args:
                if isinstance(arg, str) and arg.startswith("--ignore="):
                    ignore_codes = set(c.strip() for c in arg.split("=", 1)[1].split(","))
                    break
            if ignore_codes == {"E501", "W503"}:
                print(f"PASS: Component 2 -- flake8.args contains --ignore=E501,W503 (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- expected ignore codes {{E501, W503}}, found: {ignore_codes} in {flake8_args}")
        else:
            print(f"FAIL: Component 2 -- flake8.args is not a list: {flake8_args}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: flake8.path set to virtualenv path (0.30 points)
    try:
        flake8_path = settings.get("flake8.path", None)
        # Expected: ["${workspaceFolder}/.venv/bin/flake8"]
        # Accept both list and string forms; the key element is the venv path
        expected_path = "${workspaceFolder}/.venv/bin/flake8"
        if isinstance(flake8_path, list) and len(flake8_path) > 0:
            if expected_path in flake8_path:
                print(f"PASS: Component 3 -- flake8.path contains {expected_path} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 -- expected '{expected_path}' in flake8.path list, found: {flake8_path}")
        elif isinstance(flake8_path, str) and flake8_path == expected_path:
            print(f"PASS: Component 3 -- flake8.path is {expected_path} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- expected flake8.path with venv path, found: {flake8_path}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
