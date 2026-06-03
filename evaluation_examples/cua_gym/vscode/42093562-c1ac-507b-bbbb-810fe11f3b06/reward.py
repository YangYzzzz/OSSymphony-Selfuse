"""
Reward Script: Create tasks.json with debug and release build tasks for g++
Task ID: vscode_lang_084
Domain: vscode
Scoring:
  - Component 1: tasks.json exists and is valid with 2 tasks (0.15)
  - Component 2: Build Debug task with correct command (0.30)
  - Component 3: Build Release task with correct command (0.30)
  - Component 4: Debug task is default build task (0.15)
  - Component 5: Both tasks have gcc/g++ problem matcher (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_084'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'cppapp', '.vscode', 'tasks.json')


def normalize_command(cmd):
    """Normalize a compiler command for comparison: collapse whitespace, strip."""
    if not cmd:
        return ''
    return re.sub(r'\s+', ' ', cmd.strip())


def find_task_by_label(tasks, label_pattern):
    """Find a task whose label matches (case-insensitive contains)."""
    for task in tasks:
        task_label = task.get('label', '').lower()
        if label_pattern.lower() in task_label:
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: tasks.json must be valid JSON
    try:
        with open(TASKS_JSON_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments (VSCode allows them)
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content_clean = re.sub(r'/\*.*?\*/', '', content_clean, flags=re.DOTALL)
        data = json.loads(content_clean)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Component 1: tasks.json has version 2.0.0 and contains exactly 2 tasks (0.15 points)
    try:
        version_ok = data.get('version') == '2.0.0'
        has_two_tasks = len(tasks) >= 2
        if version_ok and has_two_tasks:
            print(f"PASS: Component 1 -- tasks.json has version 2.0.0 and {len(tasks)} tasks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- version={data.get('version')}, task_count={len(tasks)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Build Debug task with correct g++ command (0.30 points)
    try:
        debug_task = find_task_by_label(tasks, 'debug')
        if debug_task:
            cmd = normalize_command(debug_task.get('command', ''))
            # Check key flags: -g, -O0, -std=c++17, main.cpp, build/debug/myapp
            has_g_flag = '-g ' in cmd or cmd.endswith('-g')
            has_o0 = '-O0' in cmd
            has_std = '-std=c++17' in cmd
            has_input = 'main.cpp' in cmd
            has_output_debug = 'build/debug/myapp' in cmd
            has_gpp = cmd.startswith('g++')

            checks_passed = sum([has_g_flag, has_o0, has_std, has_input, has_output_debug, has_gpp])
            if checks_passed == 6:
                print(f"PASS: Component 2 -- Build Debug command correct: {cmd} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 -- Build Debug command: {cmd}")
                print(f"  g++={has_gpp}, -g={has_g_flag}, -O0={has_o0}, -std=c++17={has_std}, main.cpp={has_input}, build/debug/myapp={has_output_debug}")
        else:
            print(f"FAIL: Component 2 -- No task with 'debug' in label found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Build Release task with correct g++ command (0.30 points)
    try:
        release_task = find_task_by_label(tasks, 'release')
        if release_task:
            cmd = normalize_command(release_task.get('command', ''))
            # Check key flags: -O2, -DNDEBUG, -std=c++17, main.cpp, build/release/myapp
            has_o2 = '-O2' in cmd
            has_ndebug = '-DNDEBUG' in cmd
            has_std = '-std=c++17' in cmd
            has_input = 'main.cpp' in cmd
            has_output_release = 'build/release/myapp' in cmd
            has_gpp = cmd.startswith('g++')

            checks_passed = sum([has_o2, has_ndebug, has_std, has_input, has_output_release, has_gpp])
            if checks_passed == 6:
                print(f"PASS: Component 3 -- Build Release command correct: {cmd} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 -- Build Release command: {cmd}")
                print(f"  g++={has_gpp}, -O2={has_o2}, -DNDEBUG={has_ndebug}, -std=c++17={has_std}, main.cpp={has_input}, build/release/myapp={has_output_release}")
        else:
            print(f"FAIL: Component 3 -- No task with 'release' in label found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Debug task is the default build task (0.15 points)
    try:
        debug_task = find_task_by_label(tasks, 'debug')
        if debug_task:
            group = debug_task.get('group', {})
            is_default = False
            if isinstance(group, dict):
                is_default = group.get('kind') == 'build' and group.get('isDefault') is True
            if is_default:
                print(f"PASS: Component 4 -- Debug task is default build task (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- Debug task group: {group}, not default build")
        else:
            print(f"FAIL: Component 4 -- No debug task found to check default status")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Both tasks have appropriate gcc/g++ problem matchers (0.10 points)
    try:
        debug_task = find_task_by_label(tasks, 'debug')
        release_task = find_task_by_label(tasks, 'release')
        debug_matcher = False
        release_matcher = False

        if debug_task:
            pm = debug_task.get('problemMatcher', [])
            if isinstance(pm, list):
                debug_matcher = any('gcc' in str(m).lower() for m in pm)
            elif isinstance(pm, str):
                debug_matcher = 'gcc' in pm.lower()

        if release_task:
            pm = release_task.get('problemMatcher', [])
            if isinstance(pm, list):
                release_matcher = any('gcc' in str(m).lower() for m in pm)
            elif isinstance(pm, str):
                release_matcher = 'gcc' in pm.lower()

        if debug_matcher and release_matcher:
            print(f"PASS: Component 5 -- Both tasks have gcc problem matcher (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- debug_matcher={debug_matcher}, release_matcher={release_matcher}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
