"""
Reward Script: Create launch.json compound configuration for Go build + debug
Task ID: vscode_lang_025
Domain: vscode
Scoring:
  Component 1 (0.30) - "compounds" array exists in launch.json with a "Build and Debug" entry
  Component 2 (0.25) - Compound has preLaunchTask referencing "Go Build"
  Component 3 (0.25) - Compound references a debug configuration in its configurations list
  Component 4 (0.20) - A launch config exists that runs the built binary from bin/myapp
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_025'
LAUNCH_JSON = os.path.join(WORKDIR, 'projects', 'mygoapp', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist and be valid JSON
    try:
        data = load_jsonc(LAUNCH_JSON)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: "compounds" array exists with a "Build and Debug" entry (0.30 points)
    try:
        compounds = data.get("compounds", [])
        build_and_debug = None
        if isinstance(compounds, list):
            for c in compounds:
                if isinstance(c, dict) and c.get("name") == "Build and Debug":
                    build_and_debug = c
                    break
        if build_and_debug is not None:
            print(f"PASS: Component 1 - 'compounds' has 'Build and Debug' entry (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - No compound named 'Build and Debug' found in compounds: {compounds}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Compound has preLaunchTask referencing "Go Build" (0.25 points)
    try:
        if build_and_debug is not None:
            pre_launch = build_and_debug.get("preLaunchTask", "")
            if pre_launch == "Go Build":
                print(f"PASS: Component 2 - preLaunchTask is 'Go Build' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - preLaunchTask is '{pre_launch}', expected 'Go Build'")
        else:
            print(f"FAIL: Component 2 - No compound found, cannot check preLaunchTask")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Compound references at least one debug configuration (0.25 points)
    try:
        if build_and_debug is not None:
            configs_list = build_and_debug.get("configurations", [])
            if isinstance(configs_list, list) and len(configs_list) > 0:
                print(f"PASS: Component 3 - Compound references configurations: {configs_list} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - Compound has no configurations list or it is empty: {configs_list}")
        else:
            print(f"FAIL: Component 3 - No compound found, cannot check configurations")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: A launch configuration exists that runs the built binary from bin/myapp (0.20 points)
    # This checks that there's a config with program pointing to bin/myapp (exec mode)
    try:
        configurations = data.get("configurations", [])
        matching_configs = [
            cfg for cfg in (configurations if isinstance(configurations, list) else [])
            if isinstance(cfg, dict) and "bin/myapp" in str(cfg.get("program", ""))
        ]
        if len(matching_configs) > 0:
            cfg = matching_configs[0]
            print(f"PASS: Component 4 - Found config targeting bin/myapp: name='{cfg.get('name', '?')}', program='{cfg.get('program', '')}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - No launch configuration found with program referencing bin/myapp")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON):
    print(f"File not found: {LAUNCH_JSON}")
    print("REWARD: 0.0")
else:
    verify_task()
