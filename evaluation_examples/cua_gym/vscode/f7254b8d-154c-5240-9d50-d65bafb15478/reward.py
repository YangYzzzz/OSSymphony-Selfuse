"""
Reward Script: Configure tasks.json with pickString input for CMake build configuration
Task ID: vscode_td_040
Domain: vscode
Scoring:
  Component 1: tasks.json exists and is valid JSON (0.1 pts)
  Component 2: pickString input with id "buildConfig" (0.25 pts)
  Component 3: Input options contain "Debug" and "Release" (0.2 pts)
  Component 4: Task command uses cmake --build build --config ${input:buildConfig} (0.25 pts)
  Component 5: Task is in the build group (0.2 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_040'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'cpp-engine', '.vscode', 'tasks.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON with version 2.0.0 (0.1 points)
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 -- tasks.json does not exist at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        with open(file_path, 'r') as f:
            content = f.read()

        # Strip JSONC comments before parsing
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        stripped = re.sub(r'/\*.*?\*/', '', stripped, flags=re.DOTALL)

        data = json.loads(stripped)

        if data.get("version") == "2.0.0":
            print(f"PASS: Component 1 -- tasks.json is valid JSON with version 2.0.0 (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- tasks.json version is '{data.get('version')}', expected '2.0.0'")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 -- Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: pickString input with id "buildConfig" exists (0.25 points)
    try:
        inputs = data.get("inputs", [])
        build_config_input = None
        for inp in inputs:
            if isinstance(inp, dict) and inp.get("id") == "buildConfig":
                build_config_input = inp
                break

        if build_config_input is not None and build_config_input.get("type") == "pickString":
            print(f"PASS: Component 2 -- Found pickString input with id 'buildConfig' (0.25 pts)")
            total_score += 0.25
        elif build_config_input is not None:
            print(f"FAIL: Component 2 -- Input 'buildConfig' exists but type is '{build_config_input.get('type')}', expected 'pickString'")
        else:
            print(f"FAIL: Component 2 -- No input with id 'buildConfig' found in inputs array")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Input options contain "Debug" and "Release" (0.2 points)
    try:
        if build_config_input is not None:
            options = build_config_input.get("options", [])
            has_debug = "Debug" in options
            has_release = "Release" in options
            if has_debug and has_release:
                print(f"PASS: Component 3 -- Options contain both 'Debug' and 'Release' (0.2 pts)")
                total_score += 0.2
            else:
                missing = []
                if not has_debug:
                    missing.append("Debug")
                if not has_release:
                    missing.append("Release")
                print(f"FAIL: Component 3 -- Options missing: {missing}. Found: {options}")
        else:
            print(f"FAIL: Component 3 -- Cannot check options, no 'buildConfig' input found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Task command uses cmake --build build --config ${input:buildConfig} (0.25 points)
    try:
        tasks = data.get("tasks", [])
        command_found = False
        expected_cmd = "cmake --build build --config ${input:buildConfig}"
        for task in tasks:
            if isinstance(task, dict):
                cmd = task.get("command", "")
                if isinstance(cmd, str) and expected_cmd in cmd:
                    command_found = True
                    break
        if command_found:
            print(f"PASS: Component 4 -- Task command contains '{expected_cmd}' (0.25 pts)")
            total_score += 0.25
        else:
            found_cmds = [t.get("command", "") for t in tasks if isinstance(t, dict)]
            print(f"FAIL: Component 4 -- No task with expected command. Found commands: {found_cmds}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Task is in the build group (0.2 points)
    try:
        tasks = data.get("tasks", [])
        build_group_found = False
        for task in tasks:
            if isinstance(task, dict):
                group = task.get("group", {})
                # group can be a string "build" or a dict with "kind": "build"
                if group == "build":
                    build_group_found = True
                    break
                elif isinstance(group, dict) and group.get("kind") == "build":
                    build_group_found = True
                    break
        if build_group_found:
            print(f"PASS: Component 5 -- Task is in build group (0.2 pts)")
            total_score += 0.2
        else:
            groups = [t.get("group", "N/A") for t in tasks if isinstance(t, dict)]
            print(f"FAIL: Component 5 -- No task in build group. Found groups: {groups}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
