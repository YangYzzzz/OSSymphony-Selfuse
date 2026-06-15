"""
Reward Script: Configure Python debugger to auto-open Debug Console and break on first line
Task ID: vscode_py_090
Domain: vscode
Scoring:
  - Component 1 (0.5): stopOnEntry is set to true in launch.json
  - Component 2 (0.5): console is set to "internalConsole" or "integratedTerminal" in launch.json
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_090'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'workspace', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file that may contain // comments (JSONC)."""
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

    # Precondition: launch.json must exist and be valid JSON
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

    # Get configurations array
    configurations = data.get('configurations', [])
    if not configurations:
        print("FAIL: No configurations found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # Find the Python debug configuration
    python_config = None
    for cfg in configurations:
        if cfg.get('type') == 'python' or 'python' in cfg.get('name', '').lower():
            python_config = cfg
            break

    if python_config is None:
        print("FAIL: No Python debug configuration found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found Python config: {python_config.get('name', 'unnamed')}")

    # Component 1: stopOnEntry is set to true (0.5 points)
    # This should FAIL on initial (no stopOnEntry key) and PASS on golden
    try:
        stop_on_entry = python_config.get('stopOnEntry')
        if stop_on_entry is True:
            print(f"PASS: Component 1 — stopOnEntry is true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — stopOnEntry expected true, found: {stop_on_entry}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: console is set to "internalConsole" or "integratedTerminal" (0.5 points)
    # The task says "automatically open the Debug Console" — "internalConsole" maps to the
    # Debug Console panel. "integratedTerminal" is also acceptable per task context.
    # This should FAIL on initial (no console key) and PASS on golden.
    try:
        console_val = python_config.get('console')
        valid_console_values = ['internalConsole', 'integratedTerminal']
        if console_val in valid_console_values:
            print(f"PASS: Component 2 — console is '{console_val}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — console expected one of {valid_console_values}, found: {console_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
