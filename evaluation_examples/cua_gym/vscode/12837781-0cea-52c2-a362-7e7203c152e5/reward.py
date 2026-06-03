"""
Reward Script: Create launch.json for C/C++ GDB debugging
Task ID: vscode_lang_078
Domain: vscode
Scoring:
  - Component 1: launch.json exists and is valid JSON with configurations array (0.15)
  - Component 2: Configuration type is cppdbg and request is launch (0.20)
  - Component 3: program is ${workspaceFolder}/build/main (0.25)
  - Component 4: MIMode is gdb (0.15)
  - Component 5: stopAtEntry is true (0.15)
  - Component 6: preLaunchTask is present and non-empty (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_078'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'mycapp', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) but not inside strings
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be valid JSON with configurations
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get("configurations", [])
    if not isinstance(configs, list) or len(configs) == 0:
        print("CRITICAL: No configurations array or empty configurations")
        print("REWARD: 0.0")
        return 0.0

    # Find the best matching configuration (one with type cppdbg)
    config = None
    for c in configs:
        if isinstance(c, dict) and c.get("type") == "cppdbg":
            config = c
            break
    # Fallback to first config if no cppdbg found
    if config is None:
        config = configs[0] if isinstance(configs[0], dict) else {}

    # Component 1: launch.json has valid structure with version and configurations (0.15 pts)
    # This checks the file was CREATED (doesn't exist in initial_env)
    try:
        has_version = "version" in data
        has_configs = len(configs) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 - launch.json has version '{data.get('version')}' and {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Missing version ({has_version}) or empty configurations ({has_configs})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: type is cppdbg and request is launch (0.20 pts)
    try:
        cfg_type = config.get("type", "")
        cfg_request = config.get("request", "")
        if cfg_type == "cppdbg" and cfg_request == "launch":
            print(f"PASS: Component 2 - type='{cfg_type}', request='{cfg_request}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 - Expected type='cppdbg' request='launch', found type='{cfg_type}' request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: program is ${workspaceFolder}/build/main (0.25 pts)
    try:
        program = config.get("program", "")
        expected_program = "${workspaceFolder}/build/main"
        if program == expected_program:
            print(f"PASS: Component 3 - program='{program}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Expected program='{expected_program}', found '{program}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: MIMode is gdb (0.15 pts)
    try:
        mimode = config.get("MIMode", "")
        if mimode == "gdb":
            print(f"PASS: Component 4 - MIMode='{mimode}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Expected MIMode='gdb', found '{mimode}'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: stopAtEntry is true (0.15 pts)
    try:
        stop_at_entry = config.get("stopAtEntry")
        if stop_at_entry is True:
            print(f"PASS: Component 5 - stopAtEntry={stop_at_entry} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - Expected stopAtEntry=true, found {stop_at_entry}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: preLaunchTask is present and non-empty (0.10 pts)
    try:
        pre_launch = config.get("preLaunchTask", "")
        if isinstance(pre_launch, str) and len(pre_launch.strip()) > 0:
            print(f"PASS: Component 6 - preLaunchTask='{pre_launch}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 - Expected non-empty preLaunchTask, found '{pre_launch}'")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
