"""
Reward Script: Create .vscode/launch.json for Bash Debug configuration
Task ID: vscode_ops_091
Domain: vscode
Scoring:
  Component 1 (0.15): launch.json exists and is valid JSON with version + configurations
  Component 2 (0.25): Configuration has type=bashdb and request=launch
  Component 3 (0.30): program is set to ${workspaceFolder}/scripts/deploy.sh
  Component 4 (0.30): args is ["--env", "staging"]
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_091'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (JSONC format used by VSCode)."""
    with open(path, 'r') as f:
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

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: launch.json must be valid JSON
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has version and configurations array (0.15 points)
    # This FAILS on initial_env (file doesn't exist, caught above)
    try:
        has_version = isinstance(data.get("version"), str) and data["version"] == "0.2.0"
        has_configs = isinstance(data.get("configurations"), list) and len(data["configurations"]) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 — launch.json has version '0.2.0' and {len(data['configurations'])} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — version={data.get('version')}, configurations type/len={type(data.get('configurations'))}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the bash debug configuration among all configurations
    configs = data.get("configurations", [])
    bash_config = None
    for cfg in configs:
        if isinstance(cfg, dict) and cfg.get("type") == "bashdb":
            bash_config = cfg
            break

    # Component 2: Configuration has type=bashdb and request=launch (0.25 points)
    try:
        if bash_config is not None:
            cfg_type = bash_config.get("type")
            cfg_request = bash_config.get("request")
            if cfg_type == "bashdb" and cfg_request == "launch":
                print(f"PASS: Component 2 — type='bashdb', request='launch' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — type='{cfg_type}', request='{cfg_request}'")
        else:
            print(f"FAIL: Component 2 — No configuration with type='bashdb' found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: program is set to ${workspaceFolder}/scripts/deploy.sh (0.30 points)
    try:
        if bash_config is not None:
            program = bash_config.get("program", "")
            expected_program = "${workspaceFolder}/scripts/deploy.sh"
            if program == expected_program:
                print(f"PASS: Component 3 — program='{program}' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — expected program='{expected_program}', found '{program}'")
        else:
            print(f"FAIL: Component 3 — No bashdb configuration found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: args is ["--env", "staging"] (0.30 points)
    try:
        if bash_config is not None:
            args = bash_config.get("args")
            expected_args = ["--env", "staging"]
            if isinstance(args, list) and args == expected_args:
                print(f"PASS: Component 4 — args={args} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 4 — expected args={expected_args}, found {args}")
        else:
            print(f"FAIL: Component 4 — No bashdb configuration found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
