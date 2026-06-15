"""
Reward Script: Create a launch.json configuration to debug a Python file
Task ID: vscode_td_046
Domain: vscode
Scoring:
  Component 1 (0.2): launch.json exists, valid JSON, version == "0.2.0"
  Component 2 (0.2): configuration type is "debugpy" or "python"
  Component 3 (0.2): configuration request is "launch"
  Component 4 (0.2): configuration program is "${file}"
  Component 5 (0.2): configuration console is "integratedTerminal"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_046'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-basics')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) that VSCode allows
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist and be parseable
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: version is "0.2.0" (0.2 points)
    try:
        version = data.get("version")
        if version == "0.2.0":
            print(f"PASS: Component 1 -- version is '0.2.0' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- expected version '0.2.0', found '{version}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Get configurations list; need at least one
    configs = data.get("configurations", [])
    if not isinstance(configs, list) or len(configs) == 0:
        print(f"FAIL: No configurations array found in launch.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find the best matching configuration (the one with type debugpy/python)
    cfg = None
    for c in configs:
        if isinstance(c, dict) and c.get("type") in ("debugpy", "python"):
            cfg = c
            break
    # Fallback to first config if none matched type
    if cfg is None:
        cfg = configs[0] if isinstance(configs[0], dict) else {}

    # Component 2: type is "debugpy" or "python" (0.2 points)
    try:
        cfg_type = cfg.get("type")
        if cfg_type in ("debugpy", "python"):
            print(f"PASS: Component 2 -- type is '{cfg_type}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- expected type 'debugpy' or 'python', found '{cfg_type}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: request is "launch" (0.2 points)
    try:
        request = cfg.get("request")
        if request == "launch":
            print(f"PASS: Component 3 -- request is 'launch' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- expected request 'launch', found '{request}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: program is "${file}" (0.2 points)
    try:
        program = cfg.get("program")
        if program == "${file}":
            print(f"PASS: Component 4 -- program is '${{file}}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- expected program '${{file}}', found '{program}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: console is "integratedTerminal" (0.2 points)
    try:
        console = cfg.get("console")
        if console == "integratedTerminal":
            print(f"PASS: Component 5 -- console is 'integratedTerminal' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 -- expected console 'integratedTerminal', found '{console}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
