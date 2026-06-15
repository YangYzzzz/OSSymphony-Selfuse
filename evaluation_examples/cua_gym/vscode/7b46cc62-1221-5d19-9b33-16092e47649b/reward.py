"""
Reward Script: Create launch.json for attaching to a Python process using its process ID.
Task ID: vscode_td_067
Domain: vscode
Scoring:
  Component 1 (0.20) - launch.json file exists under .vscode/
  Component 2 (0.15) - Valid JSON with "version" and "configurations" array
  Component 3 (0.20) - Configuration has type "debugpy"
  Component 4 (0.20) - Configuration has request "attach"
  Component 5 (0.25) - Configuration has processId "${command:pickProcess}"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_067'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'daemon-service')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json file exists under .vscode/ (0.20 points)
    # This is a task-introduced change: initial_env has no .vscode dir at all
    try:
        if os.path.isfile(LAUNCH_JSON_PATH):
            print(f"PASS: Component 1 - launch.json exists at {LAUNCH_JSON_PATH} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - launch.json not found at {LAUNCH_JSON_PATH}")
            # No file means nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the JSON content (precondition for remaining checks)
    try:
        with open(LAUNCH_JSON_PATH, 'r') as f:
            raw_content = f.read()
        # Handle JSONC (JSON with comments) - strip single-line comments
        cleaned = re.sub(r'//.*$', '', raw_content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        cleaned = re.sub(r',\s*([\]}])', r'\1', cleaned)
        launch_data = json.loads(cleaned)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Valid JSON with "version" and "configurations" array (0.15 points)
    try:
        has_version = "version" in launch_data
        has_configs = isinstance(launch_data.get("configurations"), list) and len(launch_data["configurations"]) > 0
        if has_version and has_configs:
            print(f"PASS: Component 2 - Valid structure with version='{launch_data['version']}' and {len(launch_data['configurations'])} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - Missing version ({has_version}) or configurations array ({has_configs})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Find the attach configuration among all configurations
    configs = launch_data.get("configurations", [])
    attach_config = None
    for cfg in configs:
        if isinstance(cfg, dict):
            # Look for the attach config by request type or by type
            req = str(cfg.get("request", "")).lower()
            typ = str(cfg.get("type", "")).lower()
            if req == "attach" or typ == "debugpy":
                attach_config = cfg
                break
    if attach_config is None and len(configs) > 0:
        # Fallback: use the first config
        attach_config = configs[0] if isinstance(configs[0], dict) else None

    if attach_config is None:
        print(f"FAIL: No suitable configuration found in launch.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Configuration has type "debugpy" (0.20 points)
    try:
        cfg_type = str(attach_config.get("type", "")).lower().strip()
        if cfg_type == "debugpy":
            print(f"PASS: Component 3 - type is 'debugpy' (0.20 pts)")
            total_score += 0.20
        elif cfg_type == "python":
            # "python" is an older but sometimes acceptable alias
            print(f"PARTIAL: Component 3 - type is 'python' (accepted as partial, 0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 - type is '{attach_config.get('type')}', expected 'debugpy'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Configuration has request "attach" (0.20 points)
    try:
        cfg_request = str(attach_config.get("request", "")).lower().strip()
        if cfg_request == "attach":
            print(f"PASS: Component 4 - request is 'attach' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - request is '{attach_config.get('request')}', expected 'attach'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Configuration has processId "${command:pickProcess}" (0.25 points)
    try:
        process_id = attach_config.get("processId", "")
        if isinstance(process_id, str) and process_id.strip() == "${command:pickProcess}":
            print(f"PASS: Component 5 - processId is '${{command:pickProcess}}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 - processId is '{process_id}', expected '${{command:pickProcess}}'")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
