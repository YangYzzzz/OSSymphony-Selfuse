"""
Reward Script: Create a launch.json configuration to attach the Node.js debugger
Task ID: vscode_td_050
Domain: vs_code
Scoring:
  Component 1 (0.2): launch.json exists and is valid JSON with correct structure
  Component 2 (0.3): Configuration has type "node" and request "attach"
  Component 3 (0.3): Port is 9229
  Component 4 (0.2): Configuration has a descriptive name
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_050'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'node-service', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip block comments
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
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has correct top-level structure (0.2 points)
    # Must have "version" and "configurations" array with at least one entry
    try:
        has_version = isinstance(data.get("version"), str)
        configs = data.get("configurations")
        has_configs = isinstance(configs, list) and len(configs) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 - Valid launch.json structure with {len(configs)} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - Missing version ({has_version}) or configurations ({has_configs})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Find the attach configuration (look through all configurations)
    attach_config = None
    if isinstance(data.get("configurations"), list):
        for cfg in data["configurations"]:
            if isinstance(cfg, dict) and cfg.get("request") == "attach":
                attach_config = cfg
                break
        # Fallback: if no attach config, use first config
        if attach_config is None and len(data["configurations"]) > 0:
            attach_config = data["configurations"][0]

    # Component 2: Configuration has type "node" and request "attach" (0.3 points)
    try:
        if attach_config is None:
            print("FAIL: Component 2 - No configuration found")
        else:
            cfg_type = attach_config.get("type", "")
            cfg_request = attach_config.get("request", "")
            # Accept type "node" or "pwa-node" (newer VSCode uses pwa-node)
            type_ok = cfg_type in ("node", "pwa-node")
            request_ok = cfg_request == "attach"
            if type_ok and request_ok:
                print(f"PASS: Component 2 - type={cfg_type}, request={cfg_request} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Expected type=node/pwa-node and request=attach, "
                      f"found type={cfg_type}, request={cfg_request}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Port is 9229 (0.3 points)
    try:
        if attach_config is None:
            print("FAIL: Component 3 - No configuration found")
        else:
            port_val = attach_config.get("port")
            if port_val == 9229:
                print(f"PASS: Component 3 - port=9229 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 - Expected port=9229, found port={port_val}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Configuration has a descriptive name (0.2 points)
    try:
        if attach_config is None:
            print("FAIL: Component 4 - No configuration found")
        else:
            name_val = attach_config.get("name", "")
            if isinstance(name_val, str) and len(name_val.strip()) > 0:
                print(f"PASS: Component 4 - name='{name_val}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - No name or empty name found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
