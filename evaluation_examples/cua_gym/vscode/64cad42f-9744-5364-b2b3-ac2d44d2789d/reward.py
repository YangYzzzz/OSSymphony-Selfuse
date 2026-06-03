"""
Reward Script: Create a multi-file C++ build task in tasks.json
Task ID: vscode_lang_087
Domain: vscode
Scoring:
  Component 1: tasks.json exists and is valid JSON with a task entry (0.15)
  Component 2: Build command compiles all three source files with correct flags (0.35)
  Component 3: Task is set as default build task (0.25)
  Component 4: problemMatcher is set to "$gcc" (0.25)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_087'
TASKS_JSON_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'tasks.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist and be valid JSON
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Handle JSONC (strip comments)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        tasks_config = json.loads(cleaned)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tasks.json has valid structure with at least one task (0.15 points)
    try:
        tasks_list = tasks_config.get('tasks', [])
        if isinstance(tasks_list, list) and len(tasks_list) > 0:
            print(f"PASS: Component 1 — tasks.json has {len(tasks_list)} task(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — tasks.json has no tasks array or it is empty")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the build task (look for one that compiles the C++ files)
    build_task = None
    for task in tasks_config.get('tasks', []):
        cmd = task.get('command', '')
        if 'g++' in cmd or 'gcc' in cmd or 'cpp' in cmd.lower():
            build_task = task
            break
    # Fallback: just use first task if no g++ task found
    if build_task is None and len(tasks_config.get('tasks', [])) > 0:
        build_task = tasks_config['tasks'][0]

    if build_task is None:
        print("FAIL: No build task found in tasks.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Build command compiles all three source files with correct flags (0.35 points)
    try:
        command = build_task.get('command', '')
        sub_score = 0.0

        # Check all three source files are referenced
        required_files = ['src/main.cpp', 'src/utils.cpp', 'src/parser.cpp']
        files_found = 0
        for src_file in required_files:
            if src_file in command:
                files_found += 1

        if files_found == 3:
            sub_score += 0.15
            print(f"  PASS: All 3 source files found in command")
        else:
            print(f"  FAIL: Only {files_found}/3 source files found in command: {command}")

        # Check for g++ compiler
        if 'g++' in command:
            sub_score += 0.05
            print(f"  PASS: g++ compiler used")
        else:
            print(f"  FAIL: g++ compiler not found in command: {command}")

        # Check for -Iinclude flag
        if '-Iinclude' in command or '-I include' in command:
            sub_score += 0.05
            print(f"  PASS: -Iinclude flag present")
        else:
            print(f"  FAIL: -Iinclude flag not found in command: {command}")

        # Check for output executable
        if '-o ' in command and ('build/myapp' in command or 'myapp' in command):
            sub_score += 0.05
            print(f"  PASS: Output to build/myapp")
        else:
            print(f"  FAIL: Output executable not properly specified in command: {command}")

        # Check for C++17 standard
        if '-std=c++17' in command:
            sub_score += 0.05
            print(f"  PASS: C++17 standard flag present")
        else:
            print(f"  FAIL: -std=c++17 not found in command: {command}")

        if sub_score > 0:
            print(f"PASS: Component 2 — build command verification ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 2 — build command does not match requirements")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Task is set as default build task (0.25 points)
    try:
        group = build_task.get('group', {})
        if isinstance(group, dict):
            is_build = group.get('kind', '') == 'build'
            is_default = group.get('isDefault', False) is True
            if is_build and is_default:
                print(f"PASS: Component 3 — task is default build task (group.kind='build', isDefault=true) (0.25 pts)")
                total_score += 0.25
            elif is_build:
                print(f"FAIL: Component 3 — task has kind='build' but isDefault is not true (isDefault={group.get('isDefault')})")
            else:
                print(f"FAIL: Component 3 — group.kind is '{group.get('kind', 'missing')}', expected 'build'")
        elif isinstance(group, str) and group == 'build':
            # Partial: it's a build task but not explicitly default
            print(f"FAIL: Component 3 — group is string 'build', not object with isDefault=true")
        else:
            print(f"FAIL: Component 3 — no valid group configuration found: {group}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: problemMatcher is set to "$gcc" (0.25 points)
    try:
        problem_matcher = build_task.get('problemMatcher', None)
        # problemMatcher can be a string or a list
        if problem_matcher == '$gcc':
            print(f"PASS: Component 4 — problemMatcher is '$gcc' (0.25 pts)")
            total_score += 0.25
        elif isinstance(problem_matcher, list) and '$gcc' in problem_matcher:
            print(f"PASS: Component 4 — problemMatcher list contains '$gcc' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — problemMatcher is '{problem_matcher}', expected '$gcc'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
