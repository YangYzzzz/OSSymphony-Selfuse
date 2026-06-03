"""
Reward Script: Create Python launch configuration for module debugging with .env
Task ID: vscode_py_040
Domain: vscode
Scoring:
  Component 1 (0.2): launch.json exists and is valid JSON with configurations array
  Component 2 (0.3): Configuration has "module": "mypackage"
  Component 3 (0.2): Configuration has "type": "debugpy"
  Component 4 (0.3): Configuration has "envFile": "${workspaceFolder}/.env"
"""

import os
import json
import re

WORKDIR = '/home/user'
WORKSPACE = os.path.join(WORKDIR, 'workspace')
LAUNCH_JSON_PATH = os.path.join(WORKSPACE, '.vscode', 'launch.json')
TASK_ID = 'vscode_py_040'


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_matching_config(configurations):
    """
    Find the first configuration that has module == 'mypackage'.
    Returns the config dict or None.
    """
    for cfg in configurations:
        if isinstance(cfg, dict) and cfg.get('module') == 'mypackage':
            return cfg
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON with configurations array (0.2 points)
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        data = load_jsonc(LAUNCH_JSON_PATH)
        configurations = data.get('configurations', None)
        if isinstance(configurations, list) and len(configurations) > 0:
            print(f"PASS: Component 1 — launch.json exists with {len(configurations)} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 — 'configurations' is missing or empty in launch.json")
            print("REWARD: 0.0")
            return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 — Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant configuration (must have module == mypackage)
    config = find_matching_config(configurations)

    # Component 2: Configuration has "module": "mypackage" (0.3 points)
    try:
        if config is not None:
            print(f"PASS: Component 2 — Found configuration with \"module\": \"mypackage\" (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No configuration has \"module\": \"mypackage\"")
            # Check all configs for module field
            for i, cfg in enumerate(configurations):
                mod_val = cfg.get('module', '<missing>')
                print(f"  Config {i}: module = {mod_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Configuration has "type": "debugpy" (0.2 points)
    try:
        if config is not None:
            cfg_type = config.get('type', None)
            if cfg_type == 'debugpy':
                print(f"PASS: Component 3 — Configuration type is \"debugpy\" (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected type \"debugpy\", found \"{cfg_type}\"")
        else:
            print(f"FAIL: Component 3 — No matching configuration found (depends on Component 2)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Configuration has "envFile": "${workspaceFolder}/.env" (0.3 points)
    try:
        if config is not None:
            env_file = config.get('envFile', None)
            if env_file == '${workspaceFolder}/.env':
                print(f"PASS: Component 4 — envFile is \"${{workspaceFolder}}/.env\" (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 — Expected envFile \"${{workspaceFolder}}/.env\", found \"{env_file}\"")
        else:
            print(f"FAIL: Component 4 — No matching configuration found (depends on Component 2)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
