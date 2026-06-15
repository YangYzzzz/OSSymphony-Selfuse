"""
Reward Script: Create a launch.json for debugging a Go application
Task ID: vscode_td_065
Domain: vs_code
Scoring:
  Component 1 (0.2): launch.json exists, is valid JSON with version and configurations array
  Component 2 (0.3): Configuration has type "go" and request "launch"
  Component 3 (0.2): Configuration has mode "debug" or "auto"
  Component 4 (0.3): Configuration has program "${workspaceFolder}/cmd/server"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_065'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'go-api', '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSON file, stripping JSONC-style comments if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
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

    # Load the file
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid structure with version and configurations array (0.2 points)
    try:
        has_version = "version" in data
        has_configs = isinstance(data.get("configurations"), list) and len(data["configurations"]) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 — launch.json has version '{data['version']}' and {len(data['configurations'])} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — version present: {has_version}, configurations array with items: {has_configs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get the first configuration for subsequent checks
    configs = data.get("configurations", [])
    if not configs:
        print("CRITICAL: No configurations found, cannot check remaining components")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find a Go debug configuration (check all configs, use the first matching one)
    go_config = None
    for cfg in configs:
        if isinstance(cfg, dict) and cfg.get("type") == "go":
            go_config = cfg
            break
    if go_config is None:
        # Fall back to first config
        go_config = configs[0] if isinstance(configs[0], dict) else {}

    # Component 2: type "go" and request "launch" (0.3 points)
    try:
        cfg_type = go_config.get("type", "")
        cfg_request = go_config.get("request", "")
        if cfg_type == "go" and cfg_request == "launch":
            print(f"PASS: Component 2 — type='{cfg_type}', request='{cfg_request}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected type='go' and request='launch', found type='{cfg_type}' and request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: mode "debug" or "auto" (0.2 points)
    try:
        cfg_mode = go_config.get("mode", "")
        if cfg_mode in ("debug", "auto"):
            print(f"PASS: Component 3 — mode='{cfg_mode}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected mode='debug' or 'auto', found mode='{cfg_mode}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: program "${workspaceFolder}/cmd/server" (0.3 points)
    try:
        cfg_program = go_config.get("program", "")
        if cfg_program == "${workspaceFolder}/cmd/server":
            print(f"PASS: Component 4 — program='{cfg_program}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — expected program='${{workspaceFolder}}/cmd/server', found program='{cfg_program}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
