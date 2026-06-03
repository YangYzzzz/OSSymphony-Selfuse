"""
Reward Script: Configure a tasks.json build task for a CMake project
Task ID: vscode_td_028
Domain: vscode
Scoring:
  Component 1: tasks.json exists and is valid JSON with version 2.0.0 (0.15)
  Component 2: Build command contains cmake and make steps (0.30)
  Component 3: Task is default build task (0.20)
  Component 4: options.cwd set to ${workspaceFolder}/build (0.20)
  Component 5: problemMatcher includes $gcc (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_028'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'physics-sim')
TASKS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON with version "2.0.0" (0.15 points)
    try:
        if not os.path.exists(TASKS_PATH):
            print(f"FAIL: Component 1 -- tasks.json not found at {TASKS_PATH}")
            print("REWARD: 0.0")
            return 0.0

        tasks_data = load_jsonc(TASKS_PATH)

        if tasks_data.get("version") == "2.0.0":
            print(f"PASS: Component 1 -- tasks.json exists and has version 2.0.0 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- version is '{tasks_data.get('version')}', expected '2.0.0'")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 -- Could not parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the build task(s) among defined tasks
    tasks_list = tasks_data.get("tasks", [])
    if not tasks_list:
        print("FAIL: No tasks defined in tasks.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find a task that looks like a CMake build task
    build_task = None
    for t in tasks_list:
        cmd = t.get("command", "")
        # Accept if the command references cmake and make
        if "cmake" in cmd.lower() and "make" in cmd.lower():
            build_task = t
            break

    # If no cmake+make task found, try to find any build task
    if build_task is None:
        for t in tasks_list:
            group = t.get("group", {})
            if isinstance(group, dict) and group.get("kind") == "build":
                build_task = t
                break

    if build_task is None:
        # Fall back to first task
        build_task = tasks_list[0]

    # Component 2: Build command contains cmake and make steps (0.30 points)
    try:
        command = build_task.get("command", "")
        has_cmake = "cmake" in command.lower()
        has_make = "make" in command.lower()
        has_mkdir = "mkdir" in command.lower() or "build" in command.lower()

        if has_cmake and has_make:
            print(f"PASS: Component 2 -- Command contains cmake and make: '{command}' (0.30 pts)")
            total_score += 0.30
        elif has_cmake:
            print(f"PARTIAL: Component 2 -- Command has cmake but missing make: '{command}' (0.15 pts)")
            total_score += 0.15
        elif has_make:
            print(f"PARTIAL: Component 2 -- Command has make but missing cmake: '{command}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Command missing cmake/make: '{command}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Task is set as default build task (0.20 points)
    try:
        group = build_task.get("group", {})
        if isinstance(group, dict):
            is_build = group.get("kind") == "build"
            is_default = group.get("isDefault") is True
            if is_build and is_default:
                print(f"PASS: Component 3 -- Task is default build task (0.20 pts)")
                total_score += 0.20
            elif is_build:
                print(f"PARTIAL: Component 3 -- Task is build group but not default (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- group.kind is '{group.get('kind')}', expected 'build'")
        elif isinstance(group, str) and group == "build":
            # Simple form: "group": "build" (makes it build but not explicitly default)
            print(f"PARTIAL: Component 3 -- group is 'build' string (not explicit default) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 -- No build group found: {group}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: options.cwd set to ${workspaceFolder}/build (0.20 points)
    try:
        options = build_task.get("options", {})
        cwd = options.get("cwd", "")
        if "${workspaceFolder}/build" in cwd:
            print(f"PASS: Component 4 -- options.cwd is '{cwd}' (0.20 pts)")
            total_score += 0.20
        elif "build" in cwd.lower():
            print(f"PARTIAL: Component 4 -- cwd references build but not standard form: '{cwd}' (0.10 pts)")
            total_score += 0.10
        else:
            # Also check if the command itself cd's into build dir
            command = build_task.get("command", "")
            if "cd build" in command or "cd ${workspaceFolder}/build" in command:
                print(f"PARTIAL: Component 4 -- Command cd's to build dir but no options.cwd (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 -- options.cwd not set to workspaceFolder/build: '{cwd}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: problemMatcher includes $gcc (0.15 points)
    try:
        matcher = build_task.get("problemMatcher", None)
        matcher_str = str(matcher).lower() if matcher is not None else ""
        if "$gcc" in str(build_task.get("problemMatcher", "")).lower():
            print(f"PASS: Component 5 -- problemMatcher includes $gcc (0.15 pts)")
            total_score += 0.15
        elif matcher is not None:
            print(f"PARTIAL: Component 5 -- problemMatcher present but not $gcc: {matcher} (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 5 -- No problemMatcher defined")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
