"""
Reward Script: Configure Rust Analyzer extension settings in VSCode
Task ID: vscode_we_083
Domain: vscode
Scoring:
  - Component 1: rust-analyzer.procMacro.enable == true (0.35 pts)
  - Component 2: rust-analyzer.check.command == "clippy" (0.35 pts)
  - Component 3: rust-analyzer.cargo.features == "all" (0.30 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify Rust Analyzer extension configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: rust-analyzer.procMacro.enable is true (0.35 points)
    try:
        value = settings.get("rust-analyzer.procMacro.enable")
        if value is True:
            print(f"PASS: Component 1 — rust-analyzer.procMacro.enable is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected rust-analyzer.procMacro.enable == true, found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: rust-analyzer.check.command is "clippy" (0.35 points)
    try:
        value = settings.get("rust-analyzer.check.command")
        if value == "clippy":
            print(f"PASS: Component 2 — rust-analyzer.check.command is 'clippy' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — expected rust-analyzer.check.command == 'clippy', found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: rust-analyzer.cargo.features is "all" (0.30 points)
    try:
        value = settings.get("rust-analyzer.cargo.features")
        if value == "all":
            print(f"PASS: Component 3 — rust-analyzer.cargo.features is 'all' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — expected rust-analyzer.cargo.features == 'all', found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
