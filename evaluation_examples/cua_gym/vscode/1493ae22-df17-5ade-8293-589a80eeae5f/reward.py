"""
Reward Script: Configure Python debug launch configuration in VSCode
Task ID: vscode_wf_013
Domain: vscode
Scoring:
  Component 1 (0.20): launch.json exists and is valid JSON with version and configurations
  Component 2 (0.30): Configuration has type=debugpy, request=launch, program=${workspaceFolder}/app.py
  Component 3 (0.25): args include --port, 8080, --debug
  Component 4 (0.25): env includes APP_ENV=development
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_013'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'launch.json')


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

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Try to load the file
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has correct structure (0.2 points)
    # Checks: version field present, configurations is a non-empty list
    try:
        has_version = isinstance(data.get("version"), str) and len(data["version"]) > 0
        has_configs = isinstance(data.get("configurations"), list) and len(data["configurations"]) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 — launch.json has version='{data['version']}' and {len(data['configurations'])} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — version present: {has_version}, configurations non-empty list: {has_configs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get the first configuration (or find one matching debugpy)
    config = None
    try:
        configs = data.get("configurations", [])
        # Prefer a config with type=debugpy; fall back to first config
        for c in configs:
            if isinstance(c, dict) and c.get("type") == "debugpy":
                config = c
                break
        if config is None and len(configs) > 0:
            config = configs[0]
    except Exception as e:
        print(f"ERROR: Could not extract configuration: {e}")

    if config is None:
        print("FAIL: No configuration found in launch.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: type=debugpy, request=launch, program=${workspaceFolder}/app.py (0.3 points)
    try:
        type_ok = config.get("type") == "debugpy"
        request_ok = config.get("request") == "launch"
        program_val = config.get("program", "")
        # Accept both ${workspaceFolder}/app.py and absolute path
        program_ok = program_val == "${workspaceFolder}/app.py" or program_val.endswith("/app.py")

        passed = 0
        if type_ok:
            passed += 1
        if request_ok:
            passed += 1
        if program_ok:
            passed += 1

        if passed == 3:
            print(f"PASS: Component 2 — type={config.get('type')}, request={config.get('request')}, program={program_val} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — type_ok={type_ok} (got '{config.get('type')}'), request_ok={request_ok} (got '{config.get('request')}'), program_ok={program_ok} (got '{program_val}')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: args include --port, 8080, --debug (0.25 points)
    try:
        args = config.get("args", [])
        if isinstance(args, list):
            args_str = [str(a) for a in args]
            has_port_flag = "--port" in args_str
            has_port_val = "8080" in args_str
            has_debug = "--debug" in args_str

            if has_port_flag and has_port_val and has_debug:
                print(f"PASS: Component 3 — args contain --port, 8080, --debug (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — --port: {has_port_flag}, 8080: {has_port_val}, --debug: {has_debug}. Full args: {args_str}")
        else:
            print(f"FAIL: Component 3 — args is not a list: {type(args)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: env includes APP_ENV=development (0.25 points)
    try:
        env = config.get("env", {})
        if isinstance(env, dict) and env.get("APP_ENV") == "development":
            print(f"PASS: Component 4 — env contains APP_ENV='development' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — env APP_ENV: got '{env.get('APP_ENV') if isinstance(env, dict) else env}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
