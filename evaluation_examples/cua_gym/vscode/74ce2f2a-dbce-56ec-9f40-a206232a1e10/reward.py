"""
Reward Script: Configure Auto Rename Tag and Auto Close Tag extensions for HTML/JSX
Task ID: vscode_we_089
Domain: vscode
Scoring:
  - Component 1: auto-rename-tag extension installed (0.2 pts)
  - Component 2: auto-close-tag extension installed (0.2 pts)
  - Component 3: auto-rename-tag.activationOnLanguage setting correct (0.3 pts)
  - Component 4: auto-close-tag.activationOnLanguage setting correct (0.3 pts)
  Total: 1.0
"""

import os
import json
import re
import subprocess

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

EXPECTED_LANGUAGES = ["html", "xml", "javascript", "javascriptreact", "typescriptreact"]


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return {}


def check_extension_installed(ext_id):
    """Check if a VSCode extension is installed via CLI."""
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        installed = [line.strip().lower() for line in result.stdout.strip().split("\n") if line.strip()]
        return ext_id.lower() in installed
    except Exception as e:
        print(f"WARN: Could not list extensions: {e}")
        return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: auto-rename-tag extension installed (0.2 points)
    try:
        ext_installed = check_extension_installed("formulahendry.auto-rename-tag")
        if ext_installed:
            print("PASS: Component 1 -- auto-rename-tag extension is installed (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 -- auto-rename-tag extension is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: auto-close-tag extension installed (0.2 points)
    try:
        ext_installed = check_extension_installed("formulahendry.auto-close-tag")
        if ext_installed:
            print("PASS: Component 2 -- auto-close-tag extension is installed (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 2 -- auto-close-tag extension is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Load settings once for components 3 and 4
    settings = load_settings()

    # Component 3: auto-rename-tag.activationOnLanguage setting (0.3 points)
    try:
        rename_lang = settings.get("auto-rename-tag.activationOnLanguage", None)
        if rename_lang is not None and sorted(rename_lang) == sorted(EXPECTED_LANGUAGES):
            print(f"PASS: Component 3 -- auto-rename-tag.activationOnLanguage = {rename_lang} (0.3 pts)")
            total_score += 0.3
        elif rename_lang is not None:
            # Partial: setting exists but wrong value
            # Check overlap
            overlap = set(rename_lang) & set(EXPECTED_LANGUAGES)
            if len(overlap) >= 3:
                partial = 0.15
                total_score += partial
                print(f"PARTIAL: Component 3 -- auto-rename-tag.activationOnLanguage has {len(overlap)}/{len(EXPECTED_LANGUAGES)} expected languages ({partial} pts). Found: {rename_lang}")
            else:
                print(f"FAIL: Component 3 -- auto-rename-tag.activationOnLanguage has wrong value: {rename_lang}")
        else:
            print("FAIL: Component 3 -- auto-rename-tag.activationOnLanguage not found in settings")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: auto-close-tag.activationOnLanguage setting (0.3 points)
    try:
        close_lang = settings.get("auto-close-tag.activationOnLanguage", None)
        if close_lang is not None and sorted(close_lang) == sorted(EXPECTED_LANGUAGES):
            print(f"PASS: Component 4 -- auto-close-tag.activationOnLanguage = {close_lang} (0.3 pts)")
            total_score += 0.3
        elif close_lang is not None:
            overlap = set(close_lang) & set(EXPECTED_LANGUAGES)
            if len(overlap) >= 3:
                partial = 0.15
                total_score += partial
                print(f"PARTIAL: Component 4 -- auto-close-tag.activationOnLanguage has {len(overlap)}/{len(EXPECTED_LANGUAGES)} expected languages ({partial} pts). Found: {close_lang}")
            else:
                print(f"FAIL: Component 4 -- auto-close-tag.activationOnLanguage has wrong value: {close_lang}")
        else:
            print("FAIL: Component 4 -- auto-close-tag.activationOnLanguage not found in settings")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
