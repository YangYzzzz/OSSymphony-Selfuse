"""
Reward Script: Set up Python project for type-safe development via Pylance settings
Task ID: vscode_py_079
Domain: vscode
Scoring:
  Component 1 — typeCheckingMode set to "strict"          (0.35 pts)
  Component 2 — autoImportCompletions set to true         (0.25 pts)
  Component 3 — diagnosticSeverityOverrides configured    (0.40 pts)
"""

import json
import os
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")
TASK_ID = "vscode_py_079"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


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

    # Component 1: typeCheckingMode is set to "strict" (0.35 points)
    # Initial has "off"; golden has "strict". This is the core task change.
    try:
        mode = settings.get("python.analysis.typeCheckingMode")
        if mode == "strict":
            print(f"PASS: Component 1 -- typeCheckingMode is 'strict' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- typeCheckingMode expected 'strict', found: {mode!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: autoImportCompletions is set to true (0.25 points)
    # Not present in initial; must be true in golden.
    try:
        auto_import = settings.get("python.analysis.autoImportCompletions")
        if auto_import is True:
            print(f"PASS: Component 2 -- autoImportCompletions is true (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- autoImportCompletions expected true, found: {auto_import!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: diagnosticSeverityOverrides with expected entries (0.40 points)
    # Not present in initial; golden has 10 specific overrides.
    # Award partial credit: 0.04 per correct override entry.
    try:
        overrides = settings.get("python.analysis.diagnosticSeverityOverrides")
        if not isinstance(overrides, dict) or len(overrides) == 0:
            print(f"FAIL: Component 3 -- diagnosticSeverityOverrides missing or empty, found: {overrides!r}")
        else:
            expected_overrides = {
                "reportMissingTypeStubs": "warning",
                "reportUnknownMemberType": "warning",
                "reportUnknownParameterType": "warning",
                "reportUnknownVariableType": "warning",
                "reportUnknownArgumentType": "warning",
                "reportMissingParameterType": "error",
                "reportUnnecessaryTypeIgnoreComment": "warning",
                "reportPrivateUsage": "error",
                "reportUnusedImport": "error",
                "reportUnusedVariable": "warning",
            }
            matched = 0
            for key, expected_val in expected_overrides.items():
                actual_val = overrides.get(key)
                if actual_val == expected_val:
                    matched += 1
                else:
                    print(f"  FAIL: Override '{key}' expected '{expected_val}', found: {actual_val!r}")

            # Each of the 10 overrides is worth 0.04 pts (total 0.40)
            if matched == len(expected_overrides):
                print(f"PASS: Component 3 -- all {matched}/{len(expected_overrides)} overrides correct (0.40 pts)")
                total_score += 0.40
            elif matched > 0:
                component3_score = round(matched * 0.04, 2)
                print(f"PARTIAL: Component 3 -- {matched}/{len(expected_overrides)} overrides correct ({component3_score} pts)")
                total_score += component3_score
            else:
                print(f"FAIL: Component 3 -- 0/{len(expected_overrides)} overrides matched")
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
