"""
Reward Script: Create launch.json for Python debugging of hello.py
Task ID: vscode_td_049
Domain: vscode
Scoring:
  Component 1: launch.json exists, valid JSON, version "0.2.0"  — 0.2 pts
  Component 2: type "debugpy" and request "launch"               — 0.3 pts
  Component 3: program "${workspaceFolder}/hello.py"             — 0.3 pts
  Component 4: console "integratedTerminal"                      — 0.2 pts
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_049'
PROJECT_DIR = os.path.join(WORKDIR, 'homework', 'week3')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (VSCode JSONC format)."""
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

    # Precondition: launch.json must exist and be parseable
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: version is "0.2.0" and configurations list exists (0.2 points)
    try:
        version = data.get("version")
        configs = data.get("configurations")
        if version == "0.2.0" and isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 — version={version}, {len(configs)} configuration(s) found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — version={version}, configurations={type(configs).__name__}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get the first (or matching) debug configuration for subsequent checks
    config = None
    try:
        configs = data.get("configurations", [])
        if isinstance(configs, list):
            for c in configs:
                if isinstance(c, dict) and c.get("type") == "debugpy":
                    config = c
                    break
            # If no debugpy config, use the first one
            if config is None and len(configs) > 0:
                config = configs[0]
    except Exception:
        pass

    if config is None:
        print("FAIL: No configuration object found in launch.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: type is "debugpy" and request is "launch" (0.3 points)
    try:
        cfg_type = config.get("type")
        cfg_request = config.get("request")
        if cfg_type == "debugpy" and cfg_request == "launch":
            print(f"PASS: Component 2 — type={cfg_type}, request={cfg_request} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — type={cfg_type}, request={cfg_request} (expected debugpy/launch)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: program is "${workspaceFolder}/hello.py" (0.3 points)
    try:
        program = config.get("program")
        if program == "${workspaceFolder}/hello.py":
            print(f"PASS: Component 3 — program={program} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — program={program} (expected ${{workspaceFolder}}/hello.py)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: console is "integratedTerminal" (0.2 points)
    try:
        console = config.get("console")
        if console == "integratedTerminal":
            print(f"PASS: Component 4 — console={console} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — console={console} (expected integratedTerminal)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
