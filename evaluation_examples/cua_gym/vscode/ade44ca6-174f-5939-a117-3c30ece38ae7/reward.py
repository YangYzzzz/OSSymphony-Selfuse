"""
Reward Script: Create launch.json for debugging Node.js with env vars
Task ID: vscode_td_053
Domain: vscode
Scoring:
  Component 1 (0.25): Valid launch.json with node launch configuration
  Component 2 (0.25): program field points to ${workspaceFolder}/src/server.js
  Component 3 (0.50): env field contains NODE_ENV=development, DB_HOST=localhost, DB_PORT=5432
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_053'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'node-api', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(stripped)


def find_node_launch_config(data):
    """Find the first configuration with type=node and request=launch."""
    configs = data.get('configurations', [])
    if not isinstance(configs, list):
        return None
    for cfg in configs:
        if isinstance(cfg, dict):
            cfg_type = str(cfg.get('type', '')).lower()
            cfg_request = str(cfg.get('request', '')).lower()
            if cfg_type == 'node' and cfg_request == 'launch':
                return cfg
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the launch.json file
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid node launch configuration exists (0.25 points)
    # This checks that launch.json has a configurations array with type=node, request=launch
    try:
        config = find_node_launch_config(data)
        if config is not None:
            print(f"PASS: Component 1 -- Node launch config found (type={config.get('type')}, request={config.get('request')}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- No configuration with type=node and request=launch found")
            print(f"  configurations: {data.get('configurations', 'MISSING')}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: program field is "${workspaceFolder}/src/server.js" (0.25 points)
    try:
        config = find_node_launch_config(data)
        if config is not None:
            program = config.get('program', '')
            expected_program = '${workspaceFolder}/src/server.js'
            if program == expected_program:
                print(f"PASS: Component 2 -- program = '{program}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- expected program='{expected_program}', found '{program}'")
        else:
            print(f"FAIL: Component 2 -- No node launch config to check program field")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: env field has all three required variables (0.50 points)
    # Sub-scores: NODE_ENV (~0.167), DB_HOST (~0.167), DB_PORT (~0.167)
    try:
        config = find_node_launch_config(data)
        if config is not None:
            env = config.get('env', {})
            if not isinstance(env, dict):
                print(f"FAIL: Component 3 -- env field is not a dict: {type(env)}")
            else:
                env_checks = {
                    'NODE_ENV': 'development',
                    'DB_HOST': 'localhost',
                    'DB_PORT': '5432',
                }
                env_score = 0.0
                per_var = 0.50 / 3.0  # ~0.1667 each

                for var_name, expected_val in env_checks.items():
                    actual_val = env.get(var_name)
                    # DB_PORT could be stored as int or string
                    if actual_val is not None and str(actual_val) == expected_val:
                        print(f"PASS: Component 3.{var_name} -- {var_name}='{actual_val}' ({per_var:.4f} pts)")
                        env_score += per_var
                    else:
                        print(f"FAIL: Component 3.{var_name} -- expected {var_name}='{expected_val}', found '{actual_val}'")

                if env_score > 0:
                    total_score += env_score
        else:
            print(f"FAIL: Component 3 -- No node launch config to check env field")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
