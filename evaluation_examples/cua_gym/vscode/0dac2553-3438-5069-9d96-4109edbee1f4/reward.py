"""
Reward Script: Create launch.json for C++ CMake debugging with cppdbg/gdb
Task ID: vscode_td_071
Domain: vscode
Scoring:
  Component 1: launch.json exists and has cppdbg configuration type (0.20)
  Component 2: program path is ${workspaceFolder}/build/bin/myapp (0.20)
  Component 3: MIMode is gdb (0.15)
  Component 4: preLaunchTask is "CMake Build" (0.15)
  Component 5: setupCommands includes -enable-pretty-printing (0.20)
  Component 6: cwd is ${workspaceFolder} (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_071'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'cmake-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping // comments."""
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

    # Get first configuration (or search all)
    configs = data.get("configurations", [])
    if not configs:
        print("CRITICAL: No configurations found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # Find a cppdbg configuration
    cppdbg_config = None
    for cfg in configs:
        if cfg.get("type") == "cppdbg":
            cppdbg_config = cfg
            break

    # Component 1: launch.json has cppdbg configuration type (0.20 points)
    try:
        if cppdbg_config is not None:
            print(f"PASS: Component 1 -- cppdbg configuration found (0.20 pts)")
            total_score += 0.20
        else:
            types_found = [cfg.get("type") for cfg in configs]
            print(f"FAIL: Component 1 -- expected 'cppdbg' type, found types: {types_found}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if cppdbg_config is None:
        # Can't check further components without a cppdbg config
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: program path is ${workspaceFolder}/build/bin/myapp (0.20 points)
    try:
        program = cppdbg_config.get("program", "")
        if program == "${workspaceFolder}/build/bin/myapp":
            print(f"PASS: Component 2 -- program path correct: {program} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- expected '${{workspaceFolder}}/build/bin/myapp', found: {program}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: MIMode is gdb (0.15 points)
    try:
        mimode = cppdbg_config.get("MIMode", "")
        if mimode == "gdb":
            print(f"PASS: Component 3 -- MIMode is gdb (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- expected MIMode 'gdb', found: {mimode}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: preLaunchTask is "CMake Build" (0.15 points)
    try:
        pre_launch = cppdbg_config.get("preLaunchTask", "")
        if pre_launch == "CMake Build":
            print(f"PASS: Component 4 -- preLaunchTask is 'CMake Build' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- expected preLaunchTask 'CMake Build', found: {pre_launch}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: setupCommands includes -enable-pretty-printing with ignoreFailures true (0.20 points)
    try:
        setup_cmds = cppdbg_config.get("setupCommands", [])
        matching_cmds = [
            cmd for cmd in setup_cmds
            if cmd.get("text") == "-enable-pretty-printing" and cmd.get("ignoreFailures") is True
        ]
        if len(matching_cmds) > 0:
            print(f"PASS: Component 5 -- setupCommands has -enable-pretty-printing with ignoreFailures:true (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 -- expected setupCommand with text '-enable-pretty-printing' and ignoreFailures:true, found: {setup_cmds}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: cwd is ${workspaceFolder} (0.10 points)
    try:
        cwd = cppdbg_config.get("cwd", "")
        if cwd == "${workspaceFolder}":
            print(f"PASS: Component 6 -- cwd is '${{workspaceFolder}}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- expected cwd '${{workspaceFolder}}', found: {cwd}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
