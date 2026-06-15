"""
Reward Script: Create a launch.json for C++ debugging with gdb
Task ID: vscode_td_058
Domain: vscode
Scoring:
  - Component 1: launch.json exists and is valid JSON with configurations array (0.15)
  - Component 2: type is cppdbg (0.15)
  - Component 3: request is launch (0.10)
  - Component 4: program is ${workspaceFolder}/bin/app (0.20)
  - Component 5: MIMode is gdb (0.15)
  - Component 6: preLaunchTask is Build (0.15)
  - Component 7: setupCommands contains -enable-pretty-printing (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_058'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'cpp-project', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
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

    # Component 1: launch.json exists and is valid JSON with configurations array (0.15 pts)
    config = None
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 -- launch.json not found at {LAUNCH_JSON_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        data = load_jsonc(LAUNCH_JSON_PATH)
        configs = data.get('configurations', [])
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- launch.json is valid JSON with {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
            # Use first configuration for subsequent checks
            config = configs[0]
        else:
            print(f"FAIL: Component 1 -- launch.json has no configurations array or it is empty")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    if config is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # If multiple configs, try to find the one with type cppdbg
    configs = data.get('configurations', [])
    for c in configs:
        if c.get('type') == 'cppdbg':
            config = c
            break

    # Component 2: type is cppdbg (0.15 pts)
    try:
        actual_type = config.get('type', '')
        if actual_type == 'cppdbg':
            print(f"PASS: Component 2 -- type is 'cppdbg' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- expected type 'cppdbg', found '{actual_type}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: request is launch (0.10 pts)
    try:
        actual_request = config.get('request', '')
        if actual_request == 'launch':
            print(f"PASS: Component 3 -- request is 'launch' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 -- expected request 'launch', found '{actual_request}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: program is ${workspaceFolder}/bin/app (0.20 pts)
    try:
        actual_program = config.get('program', '')
        if actual_program == '${workspaceFolder}/bin/app':
            print(f"PASS: Component 4 -- program is '${{workspaceFolder}}/bin/app' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- expected program '${{workspaceFolder}}/bin/app', found '{actual_program}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: MIMode is gdb (0.15 pts)
    try:
        actual_mimode = config.get('MIMode', '')
        if actual_mimode == 'gdb':
            print(f"PASS: Component 5 -- MIMode is 'gdb' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- expected MIMode 'gdb', found '{actual_mimode}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: preLaunchTask is Build (0.15 pts)
    try:
        actual_task = config.get('preLaunchTask', '')
        if actual_task == 'Build':
            print(f"PASS: Component 6 -- preLaunchTask is 'Build' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 -- expected preLaunchTask 'Build', found '{actual_task}'")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: setupCommands contains -enable-pretty-printing (0.10 pts)
    try:
        setup_commands = config.get('setupCommands', [])
        pretty_printing_found = any(
            '-enable-pretty-printing' in (cmd.get('text', '') if isinstance(cmd, dict) else str(cmd))
            for cmd in (setup_commands if isinstance(setup_commands, list) else [])
        )
        if pretty_printing_found:
            print(f"PASS: Component 7 -- setupCommands contains '-enable-pretty-printing' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 -- setupCommands does not contain '-enable-pretty-printing'")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
