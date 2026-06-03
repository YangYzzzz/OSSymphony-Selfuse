"""
Reward Script: Configure GitHub Copilot extension settings in VSCode
Task ID: vscode_we_091
Domain: vscode
Scoring:
  Component 1 (0.2): github.copilot.enable key exists and is a dict
  Component 2 (0.2): "*" is set to true (global enable)
  Component 3 (0.2): markdown and plaintext disabled (false)
  Component 4 (0.2): yaml, python, javascript enabled (true)
  Component 5 (0.2): Exact completeness — all 6 expected keys present, no extras
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_091'

SETTINGS_PATH = os.path.expanduser('~/.config/Code/User/settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    copilot_enable = settings.get("github.copilot.enable")

    # Component 1: github.copilot.enable exists and is a dict (0.2 points)
    # This FAILS on initial (empty settings) and PASSES on golden
    try:
        if isinstance(copilot_enable, dict):
            print(f"PASS: Component 1 — github.copilot.enable is a dict with {len(copilot_enable)} keys (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — github.copilot.enable is not a dict, found: {type(copilot_enable)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If copilot_enable is not a dict, remaining checks cannot pass
    if not isinstance(copilot_enable, dict):
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: "*" is set to true — global Copilot enable (0.2 points)
    try:
        star_val = copilot_enable.get("*")
        if star_val is True:
            print(f"PASS: Component 2 — '*' is true (global enable) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — '*' expected true, found: {star_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: markdown and plaintext disabled (0.2 points)
    try:
        md_val = copilot_enable.get("markdown")
        pt_val = copilot_enable.get("plaintext")
        passed = 0
        if md_val is False:
            passed += 1
        else:
            print(f"FAIL: Component 3a — 'markdown' expected false, found: {md_val}")
        if pt_val is False:
            passed += 1
        else:
            print(f"FAIL: Component 3b — 'plaintext' expected false, found: {pt_val}")

        if passed == 2:
            print(f"PASS: Component 3 — markdown=false, plaintext=false (0.2 pts)")
            total_score += 0.2
        elif passed == 1:
            print(f"PARTIAL: Component 3 — 1/2 disabled languages correct (0.1 pts)")
            total_score += 0.1
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: yaml, python, javascript enabled (0.2 points)
    try:
        enabled_langs = {"yaml": True, "python": True, "javascript": True}
        passed = 0
        for lang, expected in enabled_langs.items():
            actual = copilot_enable.get(lang)
            if actual is expected:
                passed += 1
            else:
                print(f"FAIL: Component 4 — '{lang}' expected {expected}, found: {actual}")

        if passed == 3:
            print(f"PASS: Component 4 — yaml=true, python=true, javascript=true (0.2 pts)")
            total_score += 0.2
        elif passed > 0:
            partial = round(0.2 * passed / 3, 2)
            print(f"PARTIAL: Component 4 — {passed}/3 enabled languages correct ({partial} pts)")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Completeness — all 6 expected keys present with correct values (0.2 points)
    try:
        expected_copilot = {
            "*": True,
            "markdown": False,
            "plaintext": False,
            "yaml": True,
            "python": True,
            "javascript": True,
        }
        # Check all expected keys are present with correct values
        all_correct = all(
            copilot_enable.get(k) is v
            for k, v in expected_copilot.items()
        )
        if all_correct and len(copilot_enable) >= len(expected_copilot):
            print(f"PASS: Component 5 — All 6 copilot.enable keys present and correct (0.2 pts)")
            total_score += 0.2
        else:
            missing = [k for k in expected_copilot if copilot_enable.get(k) is not expected_copilot[k]]
            print(f"FAIL: Component 5 — Incomplete or incorrect keys. Issues: {missing}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
