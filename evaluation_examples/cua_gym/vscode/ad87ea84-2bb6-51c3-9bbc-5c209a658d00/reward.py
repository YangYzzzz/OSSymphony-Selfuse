"""
Reward Script: Configure tasks.json build task for C++ project with g++
Task ID: vscode_td_013
Domain: vs_code
Scoring:
  Component 1: tasks.json exists and is valid JSON with tasks array (0.15)
  Component 2: g++ command with flags -std=c++17 -Wall -Wextra -g (0.30)
  Component 3: Source is src/main.cpp and output is bin/app (0.20)
  Component 4: Task is default build task (0.15)
  Component 5: problemMatcher captures file, line, and message (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'cpp-game')
TASKS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
TASK_ID = 'vscode_td_013'


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

    # ---- Component 1: tasks.json exists and is valid JSON with tasks array (0.15 pts) ----
    tasks_data = None
    try:
        if not os.path.exists(TASKS_PATH):
            print(f"FAIL: Component 1 -- {TASKS_PATH} does not exist")
            print("REWARD: 0.0")
            return 0.0

        tasks_data = load_jsonc(TASKS_PATH)

        if not isinstance(tasks_data, dict):
            print(f"FAIL: Component 1 -- tasks.json root is not a dict")
            print("REWARD: 0.0")
            return 0.0

        tasks_list = tasks_data.get('tasks', None)
        if not isinstance(tasks_list, list) or len(tasks_list) == 0:
            print(f"FAIL: Component 1 -- 'tasks' key missing or empty")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 -- tasks.json is valid with {len(tasks_list)} task(s) (0.15 pts)")
        total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the build task (first task that uses g++ or has build group)
    build_task = None
    for t in tasks_data.get('tasks', []):
        cmd = t.get('command', '')
        args = t.get('args', [])
        # Check if command is g++ or args reference g++
        full_cmd = cmd + ' ' + ' '.join(str(a) for a in args)
        if 'g++' in full_cmd:
            build_task = t
            break
    if build_task is None:
        # Fallback: just use first task
        build_task = tasks_data['tasks'][0]

    # ---- Component 2: g++ with correct flags (0.30 pts) ----
    try:
        cmd = build_task.get('command', '')
        args = build_task.get('args', [])
        args_str = [str(a) for a in args]

        # Build the full command string to check for flags
        full_cmd = cmd + ' ' + ' '.join(args_str)

        required_flags = ['-std=c++17', '-Wall', '-Wextra', '-g']
        found_flags = []
        missing_flags = []

        for flag in required_flags:
            if flag in full_cmd:
                found_flags.append(flag)
            else:
                missing_flags.append(flag)

        # Also check that g++ is the command
        has_gpp = ('g++' in cmd) or ('g++' in ' '.join(args_str))

        if has_gpp and len(missing_flags) == 0:
            print(f"PASS: Component 2 -- g++ with all flags: {found_flags} (0.30 pts)")
            total_score += 0.30
        else:
            if not has_gpp:
                print(f"FAIL: Component 2 -- command is not g++ (found: {cmd})")
            if missing_flags:
                print(f"FAIL: Component 2 -- missing flags: {missing_flags}, found: {found_flags}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ---- Component 3: Source is src/main.cpp, output is bin/app (0.20 pts) ----
    try:
        args_str = [str(a) for a in build_task.get('args', [])]
        full_args = ' '.join(args_str)

        # Check source file references src/main.cpp (may use ${workspaceFolder}/src/main.cpp)
        has_source = any('src/main.cpp' in a for a in args_str)

        # Check output is bin/app: look for -o followed by bin/app
        has_output = False
        for i, a in enumerate(args_str):
            if a == '-o' and i + 1 < len(args_str):
                if 'bin/app' in args_str[i + 1]:
                    has_output = True
                    break

        if has_source and has_output:
            print(f"PASS: Component 3 -- source=src/main.cpp, output=bin/app (0.20 pts)")
            total_score += 0.20
        else:
            if not has_source:
                print(f"FAIL: Component 3 -- src/main.cpp not found in args: {args_str}")
            if not has_output:
                print(f"FAIL: Component 3 -- bin/app not found as -o target in args: {args_str}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ---- Component 4: Default build task (0.15 pts) ----
    try:
        group = build_task.get('group', {})
        is_default_build = False

        if isinstance(group, dict):
            is_default_build = (group.get('kind') == 'build' and group.get('isDefault') is True)
        elif isinstance(group, str):
            # Simple form: "group": "build" (but not default)
            pass

        if is_default_build:
            print(f"PASS: Component 4 -- task is default build task (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- task group is not default build, got: {group}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # ---- Component 5: problemMatcher captures file, line, message (0.20 pts) ----
    try:
        pm = build_task.get('problemMatcher', None)

        if pm is None:
            print(f"FAIL: Component 5 -- no problemMatcher defined")
        else:
            # problemMatcher can be a string like "$gcc", an object, or a list
            captures_file = False
            captures_line = False
            captures_message = False

            if isinstance(pm, str):
                # Built-in matchers like "$gcc" capture file, line, message
                if pm in ('$gcc', '$g++'):
                    captures_file = True
                    captures_line = True
                    captures_message = True

            elif isinstance(pm, dict):
                # Custom matcher - check pattern
                pattern = pm.get('pattern', {})
                # pattern can be a dict or list of dicts
                if isinstance(pattern, list):
                    patterns = pattern
                else:
                    patterns = [pattern]

                for p in patterns:
                    if isinstance(p, dict):
                        if 'file' in p:
                            captures_file = True
                        if 'line' in p:
                            captures_line = True
                        if 'message' in p:
                            captures_message = True

            elif isinstance(pm, list):
                # List of matchers
                for m in pm:
                    if isinstance(m, str) and m in ('$gcc', '$g++'):
                        captures_file = True
                        captures_line = True
                        captures_message = True
                    elif isinstance(m, dict):
                        pattern = m.get('pattern', {})
                        if isinstance(pattern, list):
                            patterns = pattern
                        else:
                            patterns = [pattern]
                        for p in patterns:
                            if isinstance(p, dict):
                                if 'file' in p:
                                    captures_file = True
                                if 'line' in p:
                                    captures_line = True
                                if 'message' in p:
                                    captures_message = True

            if captures_file and captures_line and captures_message:
                print(f"PASS: Component 5 -- problemMatcher captures file, line, message (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not captures_file:
                    missing.append('file')
                if not captures_line:
                    missing.append('line')
                if not captures_message:
                    missing.append('message')
                print(f"FAIL: Component 5 -- problemMatcher missing captures: {missing}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
