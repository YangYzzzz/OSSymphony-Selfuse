"""
Reward Script: Create launch.json with Python debug configuration for stdin-processor
Task ID: vscode_td_063
Domain: vscode
Scoring:
  Component 1 (0.15): launch.json exists, valid JSON with version and configurations array
  Component 2 (0.20): type == "debugpy" and request == "launch"
  Component 3 (0.20): program references src/process.py via workspaceFolder
  Component 4 (0.25): console == "integratedTerminal"
  Component 5 (0.20): redirectInput references data/input.txt
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_063'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'stdin-processor')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with Comments) by stripping comments first."""
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

    # Precondition: launch.json must be valid JSON(C)
    try:
        launch_data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has "version" and "configurations" array with at least one entry (0.15 pts)
    try:
        has_version = "version" in launch_data
        configs = launch_data.get("configurations", [])
        has_configs = isinstance(configs, list) and len(configs) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 - launch.json has version and {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - version={has_version}, configurations valid={has_configs}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Get the first configuration (or a matching Python one) for further checks
    config = None
    try:
        configs = launch_data.get("configurations", [])
        # Prefer a config with type containing "python" or "debugpy"
        for c in configs:
            ctype = str(c.get("type", "")).lower()
            if "debugpy" in ctype or "python" in ctype:
                config = c
                break
        # Fall back to first config
        if config is None and configs:
            config = configs[0]
    except Exception:
        pass

    if config is None:
        print("FAIL: No configuration found in launch.json for remaining checks")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: type == "debugpy" and request == "launch" (0.20 pts)
    try:
        cfg_type = str(config.get("type", "")).lower()
        cfg_request = str(config.get("request", "")).lower()
        type_ok = cfg_type == "debugpy"
        request_ok = cfg_request == "launch"
        if type_ok and request_ok:
            print(f"PASS: Component 2 - type='debugpy', request='launch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 - type='{config.get('type')}' (expected 'debugpy'), request='{config.get('request')}' (expected 'launch')")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: program references src/process.py (0.20 pts)
    try:
        program = str(config.get("program", ""))
        # Accept various forms: ${workspaceFolder}/src/process.py, src/process.py, etc.
        if "src/process.py" in program:
            print(f"PASS: Component 3 - program='{program}' references src/process.py (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - program='{program}' does not reference src/process.py")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: console == "integratedTerminal" (0.25 pts)
    try:
        console = config.get("console", "")
        if console == "integratedTerminal":
            print(f"PASS: Component 4 - console='integratedTerminal' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - console='{console}' (expected 'integratedTerminal')")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: redirectInput references data/input.txt (0.20 pts)
    try:
        redirect_input = config.get("redirectInput", "")
        # Accept various forms: ${workspaceFolder}/data/input.txt, data/input.txt, etc.
        if redirect_input and "data/input.txt" in str(redirect_input):
            print(f"PASS: Component 5 - redirectInput='{redirect_input}' references data/input.txt (0.20 pts)")
            total_score += 0.20
        else:
            # Also check args for "< data/input.txt" as an alternative approach
            args = config.get("args", [])
            args_str = " ".join(args) if isinstance(args, list) else str(args)
            if "data/input.txt" in args_str:
                print(f"PASS: Component 5 - args contain reference to data/input.txt (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 - redirectInput='{redirect_input}', args='{args}' -- neither references data/input.txt")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
