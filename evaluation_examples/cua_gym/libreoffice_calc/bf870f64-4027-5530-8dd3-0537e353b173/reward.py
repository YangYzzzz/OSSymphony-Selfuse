"""
Reward Script: Create a launch.json with Node.js debug configuration using envFile
Task ID: vscode_td_068
Domain: vs-code (libreoffice_calc listed but actually VSCode task)
Scoring:
  Component 1: launch.json exists and is valid JSON with configurations array (0.2 pts)
  Component 2: Configuration has type "node" and request "launch" (0.3 pts)
  Component 3: program is set to "${workspaceFolder}/src/app.js" (0.2 pts)
  Component 4: envFile is set to "${workspaceFolder}/.env" (0.3 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_068'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'env-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (VSCode JSONC support)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([\]}])', r'\1', content)
    return json.loads(content)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        data = load_jsonc(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has valid structure with configurations array (0.2 pts)
    try:
        configs = data.get("configurations")
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- launch.json has {len(configs)} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected non-empty 'configurations' array, found: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find the Node.js configuration (look through all configs)
    node_config = None
    if isinstance(data.get("configurations"), list):
        for cfg in data["configurations"]:
            if isinstance(cfg, dict) and cfg.get("type") == "node":
                node_config = cfg
                break

    # Component 2: Configuration has type "node" and request "launch" (0.3 pts)
    try:
        if node_config is not None:
            cfg_type = node_config.get("type", "")
            cfg_request = node_config.get("request", "")
            if cfg_type == "node" and cfg_request == "launch":
                print(f"PASS: Component 2 -- type='node', request='launch' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Expected type='node' and request='launch', found type='{cfg_type}', request='{cfg_request}'")
        else:
            print(f"FAIL: Component 2 -- No configuration with type='node' found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: program is set to "${workspaceFolder}/src/app.js" (0.2 pts)
    try:
        if node_config is not None:
            program = node_config.get("program", "")
            if program == "${workspaceFolder}/src/app.js":
                print(f"PASS: Component 3 -- program='{program}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 -- Expected program='${{workspaceFolder}}/src/app.js', found: '{program}'")
        else:
            print(f"FAIL: Component 3 -- No node configuration to check program")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: envFile is set to "${workspaceFolder}/.env" (0.3 pts)
    try:
        if node_config is not None:
            env_file = node_config.get("envFile", "")
            if env_file == "${workspaceFolder}/.env":
                print(f"PASS: Component 4 -- envFile='{env_file}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 -- Expected envFile='${{workspaceFolder}}/.env', found: '{env_file}'")
        else:
            print(f"FAIL: Component 4 -- No node configuration to check envFile")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
