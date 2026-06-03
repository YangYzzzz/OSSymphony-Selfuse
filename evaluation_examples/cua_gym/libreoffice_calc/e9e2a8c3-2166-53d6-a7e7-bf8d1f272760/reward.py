"""
Reward Script: Configure Markdownlint extension settings in VSCode
Task ID: vscode_we_094
Domain: libreoffice_calc (VSCode settings task)
Scoring:
  Component 1: MD013 rule disabled (0.35 pts)
  Component 2: MD033 rule disabled (0.35 pts)
  Component 3: MD003 heading style set to ATX (0.30 pts)
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments (VSCode settings may have // comments)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that markdownlint.config is properly configured in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Get the markdownlint.config block
    ml_config = settings.get("markdownlint.config")
    if not isinstance(ml_config, dict):
        print(f"FAIL: 'markdownlint.config' not found or not a dict in settings.json. Found: {ml_config}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: MD013 (line-length) is disabled (0.35 points)
    try:
        md013_value = ml_config.get("MD013")
        if md013_value is False:
            print(f"PASS: Component 1 -- MD013 is set to false (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- Expected MD013: false, found: {md013_value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: MD033 (inline HTML) is allowed / disabled (0.35 points)
    try:
        md033_value = ml_config.get("MD033")
        if md033_value is False:
            print(f"PASS: Component 2 -- MD033 is set to false (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- Expected MD033: false, found: {md033_value!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: MD003 heading style set to ATX (0.30 points)
    try:
        md003_value = ml_config.get("MD003")
        if isinstance(md003_value, dict) and md003_value.get("style") == "atx":
            print(f"PASS: Component 3 -- MD003 style is 'atx' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- Expected MD003: {{\"style\": \"atx\"}}, found: {md003_value!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
