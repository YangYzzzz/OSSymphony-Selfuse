"""
Reward Script: VSCode Live Share Code Review Session Configuration
Task ID: vscode_gf3_080
Domain: vscode
Scoring:
  - 5 Live Share settings in User Settings JSON (0.15 + 0.15 + 0.15 + 0.10 + 0.10 = 0.65)
  - .vsls.json excludeFiles configuration (0.35)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_080'

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
VSLS_PATH = os.path.join(WORKDIR, "projects", "api-service", ".vsls.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings once
    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: liveshare.codeLens is set to true (0.15 points)
    # This key does NOT exist in initial_env settings, so checking explicit presence + value
    try:
        key = "liveshare.codeLens"
        if key in settings and settings[key] is True:
            print(f"PASS: Component 1 — {key} is true (0.15 pts)")
            total_score += 0.15
        else:
            actual = settings.get(key, "<NOT SET>")
            print(f"FAIL: Component 1 — expected {key}=true, found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: liveshare.diagnosticLogging is set to false (0.15 points)
    # Key must EXIST (not just be absent). Initial env does not have this key.
    try:
        key = "liveshare.diagnosticLogging"
        if key in settings and settings[key] is False:
            print(f"PASS: Component 2 — {key} is false (0.15 pts)")
            total_score += 0.15
        else:
            actual = settings.get(key, "<NOT SET>")
            print(f"FAIL: Component 2 — expected {key}=false (explicitly set), found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: liveshare.joinDebugSessionOption is set to "Prompt" (0.15 points)
    try:
        key = "liveshare.joinDebugSessionOption"
        if key in settings and settings[key] == "Prompt":
            print(f"PASS: Component 3 — {key} is 'Prompt' (0.15 pts)")
            total_score += 0.15
        else:
            actual = settings.get(key, "<NOT SET>")
            print(f"FAIL: Component 3 — expected {key}='Prompt', found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: liveshare.shareExternalFiles is set to false (0.10 points)
    # Key must EXIST explicitly. Initial env does not have this key.
    try:
        key = "liveshare.shareExternalFiles"
        if key in settings and settings[key] is False:
            print(f"PASS: Component 4 — {key} is false (0.10 pts)")
            total_score += 0.10
        else:
            actual = settings.get(key, "<NOT SET>")
            print(f"FAIL: Component 4 — expected {key}=false (explicitly set), found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: liveshare.allowGuestDebugControl is set to false (0.10 points)
    # Key must EXIST explicitly. Initial env does not have this key.
    try:
        key = "liveshare.allowGuestDebugControl"
        if key in settings and settings[key] is False:
            print(f"PASS: Component 5 — {key} is false (0.10 pts)")
            total_score += 0.10
        else:
            actual = settings.get(key, "<NOT SET>")
            print(f"FAIL: Component 5 — expected {key}=false (explicitly set), found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vsls.json exists with correct excludeFiles (0.35 points)
    # The file must exist at /home/user/projects/api-service/.vsls.json
    # and contain excludeFiles with exactly: node_modules, .env, .env.*, dist, *.log
    try:
        if not os.path.exists(VSLS_PATH):
            print(f"FAIL: Component 6 — .vsls.json not found at {VSLS_PATH}")
        else:
            with open(VSLS_PATH, "r") as f:
                vsls_content = f.read()
            # Strip comments if any
            vsls_content = re.sub(r'//.*$', '', vsls_content, flags=re.MULTILINE)
            vsls_data = json.loads(vsls_content)

            exclude_files = vsls_data.get("excludeFiles", [])
            expected_excludes = {"node_modules", ".env", ".env.*", "dist", "*.log"}

            if not isinstance(exclude_files, list):
                print(f"FAIL: Component 6 — excludeFiles is not a list: {type(exclude_files)}")
            else:
                actual_set = set(exclude_files)
                missing = expected_excludes - actual_set
                extra = actual_set - expected_excludes

                if not missing:
                    # All required patterns present
                    print(f"PASS: Component 6 — .vsls.json has all required excludeFiles (0.35 pts)")
                    if extra:
                        print(f"  NOTE: Extra entries present (acceptable): {extra}")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 6 — missing excludeFiles entries: {missing}")
                    # Partial credit: award proportionally for found patterns
                    found_count = len(expected_excludes) - len(missing)
                    partial = round(0.35 * (found_count / len(expected_excludes)), 2)
                    if partial > 0:
                        print(f"  Partial credit: {found_count}/{len(expected_excludes)} patterns found ({partial} pts)")
                        total_score += partial
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 6 — .vsls.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
