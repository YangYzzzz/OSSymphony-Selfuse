"""
Reward Script: Create launch.json with LLDB debug configuration for C program
Task ID: vscode_td_092
Domain: vscode
Scoring:
  - Component 1: launch.json exists and is valid JSON with configurations array (0.1)
  - Component 2: type is "cppdbg" (0.15)
  - Component 3: MIMode is "lldb" (0.2)
  - Component 4: program is "${workspaceFolder}/build/app" (0.2)
  - Component 5: preLaunchTask is "make" (0.2)
  - Component 6: request is "launch" and externalConsole is false (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_092'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'macos-app')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load JSON file, stripping // comments (VSCode JSONC format)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist — if not, nothing to verify
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse launch.json
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the first configuration (or None)
    configs = data.get("configurations", [])

    # Component 1: launch.json has a configurations array with at least one entry (0.1 points)
    try:
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 — launch.json has {len(configs)} configuration(s) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — configurations array is empty or missing")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(configs) == 0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first configuration for all subsequent checks
    config = configs[0]

    # Component 2: type is "cppdbg" (0.15 points)
    try:
        actual_type = config.get("type", "")
        if actual_type == "cppdbg":
            print(f"PASS: Component 2 — type is 'cppdbg' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected type 'cppdbg', found '{actual_type}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: MIMode is "lldb" (0.2 points)
    try:
        actual_mimode = config.get("MIMode", "")
        if actual_mimode == "lldb":
            print(f"PASS: Component 3 — MIMode is 'lldb' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected MIMode 'lldb', found '{actual_mimode}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: program is "${workspaceFolder}/build/app" (0.2 points)
    try:
        actual_program = config.get("program", "")
        if actual_program == "${workspaceFolder}/build/app":
            print(f"PASS: Component 4 — program is '${{workspaceFolder}}/build/app' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — expected program '${{workspaceFolder}}/build/app', found '{actual_program}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: preLaunchTask is "make" (0.2 points)
    try:
        actual_task = config.get("preLaunchTask", "")
        if actual_task == "make":
            print(f"PASS: Component 5 — preLaunchTask is 'make' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — expected preLaunchTask 'make', found '{actual_task}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: request is "launch" AND externalConsole is false (0.15 points)
    try:
        actual_request = config.get("request", "")
        actual_console = config.get("externalConsole")
        request_ok = (actual_request == "launch")
        console_ok = (actual_console is False)  # must be boolean False, not just falsy
        if request_ok and console_ok:
            print(f"PASS: Component 6 — request='launch' and externalConsole=false (0.15 pts)")
            total_score += 0.15
        else:
            details = []
            if not request_ok:
                details.append(f"request='{actual_request}' (expected 'launch')")
            if not console_ok:
                details.append(f"externalConsole={actual_console} (expected false)")
            print(f"FAIL: Component 6 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
