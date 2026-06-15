"""
Reward Script: Create launch.json for Chrome extension debugging
Task ID: vscode_td_072
Domain: vscode
Scoring:
  Component 1 (0.2): launch.json exists and is valid JSON with version and configurations
  Component 2 (0.3): Configuration has type "chrome" and request "launch"
  Component 3 (0.3): runtimeArgs contains "--load-extension=${workspaceFolder}/dist"
  Component 4 (0.2): url is set to "about:blank"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_072'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'chrome-extension')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
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

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: launch.json must be valid JSON(C)
    try:
        launch_data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has proper structure with version and configurations array (0.2 points)
    try:
        has_version = "version" in launch_data
        has_configs = "configurations" in launch_data and isinstance(launch_data["configurations"], list)
        has_at_least_one = has_configs and len(launch_data["configurations"]) >= 1
        if has_version and has_at_least_one:
            print(f"PASS: Component 1 - launch.json has version and {len(launch_data['configurations'])} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - version={has_version}, configurations_array={has_configs}, at_least_one={has_at_least_one}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Find the chrome configuration among all configurations
    chrome_config = None
    if "configurations" in launch_data and isinstance(launch_data["configurations"], list):
        for config in launch_data["configurations"]:
            if isinstance(config, dict) and config.get("type") == "chrome":
                chrome_config = config
                break

    # Component 2: Configuration has type "chrome" and request "launch" (0.3 points)
    try:
        if chrome_config is not None:
            config_type = chrome_config.get("type")
            config_request = chrome_config.get("request")
            if config_type == "chrome" and config_request == "launch":
                print(f"PASS: Component 2 - type='chrome', request='launch' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - type='{config_type}', request='{config_request}'")
        else:
            print(f"FAIL: Component 2 - No configuration with type 'chrome' found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: runtimeArgs contains "--load-extension=${workspaceFolder}/dist" (0.3 points)
    try:
        if chrome_config is not None:
            runtime_args = chrome_config.get("runtimeArgs", [])
            expected_arg = "--load-extension=${workspaceFolder}/dist"
            if isinstance(runtime_args, list) and expected_arg in runtime_args:
                print(f"PASS: Component 3 - runtimeArgs contains '{expected_arg}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 - runtimeArgs={runtime_args}, expected to contain '{expected_arg}'")
        else:
            print(f"FAIL: Component 3 - No chrome configuration found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: url is set to "about:blank" (0.2 points)
    try:
        if chrome_config is not None:
            url_value = chrome_config.get("url")
            if url_value == "about:blank":
                print(f"PASS: Component 4 - url='about:blank' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - url='{url_value}', expected 'about:blank'")
        else:
            print(f"FAIL: Component 4 - No chrome configuration found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
