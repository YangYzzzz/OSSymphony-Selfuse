"""
Reward Script: Configure Git settings in VSCode
Task ID: vscode_we_036
Domain: vscode
Scoring:
  Component 1: git.autoStash == true          (0.25 pts)
  Component 2: git.defaultCloneDirectory == "~/repos" (0.25 pts)
  Component 3: git.inputValidationLength == 0  (0.25 pts)
  Component 4: git.postCommitCommand == "push" (0.25 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_we_036"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments (// style)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load VSCode settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: git.autoStash is true (0.25 points)
    try:
        val = settings.get("git.autoStash")
        if val is True:
            print(f"PASS: Component 1 -- git.autoStash is true (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- expected git.autoStash=true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: git.defaultCloneDirectory is "~/repos" (0.25 points)
    try:
        val = settings.get("git.defaultCloneDirectory")
        if val == "~/repos":
            print(f"PASS: Component 2 -- git.defaultCloneDirectory is '~/repos' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- expected git.defaultCloneDirectory='~/repos', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: git.inputValidationLength is 0 (0.25 points)
    try:
        val = settings.get("git.inputValidationLength")
        if val == 0:
            print(f"PASS: Component 3 -- git.inputValidationLength is 0 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- expected git.inputValidationLength=0, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: git.postCommitCommand is "push" (0.25 points)
    try:
        val = settings.get("git.postCommitCommand")
        if val == "push":
            print(f"PASS: Component 4 -- git.postCommitCommand is 'push' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- expected git.postCommitCommand='push', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
