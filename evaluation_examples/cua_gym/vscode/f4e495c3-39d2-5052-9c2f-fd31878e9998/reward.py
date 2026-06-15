"""
Reward Script: C/GDB debug configuration setup
Task ID: vscode_stu_065
Domain: vscode
Scoring:
  Component 1 (0.30): tasks.json has a gcc build task with -g flag
  Component 2 (0.30): launch.json has a cppdbg/gdb debug configuration
  Component 3 (0.20): preLaunchTask in launch.json matches tasks.json label
  Component 4 (0.20): Debug config has program path and gdb debugger path
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_065'
PROJECT_DIR = os.path.join(WORKDIR, 'cs201', 'project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
LAUNCH_PATH = os.path.join(VSCODE_DIR, 'launch.json')
TASKS_PATH = os.path.join(VSCODE_DIR, 'tasks.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    tasks_data = None
    launch_data = None
    task_label = None

    # Component 1: tasks.json has a gcc build task with -g debug flag (0.30 points)
    try:
        tasks_data = load_jsonc(TASKS_PATH)
        tasks_list = tasks_data.get('tasks', [])
        gcc_task_found = False
        for task in tasks_list:
            cmd = str(task.get('command', '')).lower()
            args = task.get('args', [])
            args_str = ' '.join(str(a) for a in args).lower()
            label = task.get('label', '')
            # Check: command references gcc and args include -g for debug symbols
            if 'gcc' in cmd and '-g' in args_str:
                gcc_task_found = True
                task_label = label
                print(f"PASS: Component 1 -- gcc build task found (label='{label}', has -g flag) (0.30 pts)")
                total_score += 0.30
                break
        if not gcc_task_found:
            print(f"FAIL: Component 1 -- No gcc build task with -g flag in tasks.json")
    except FileNotFoundError:
        print(f"FAIL: Component 1 -- tasks.json not found at {TASKS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: launch.json has a C/C++ debug configuration with GDB (0.30 points)
    try:
        launch_data = load_jsonc(LAUNCH_PATH)
        configs = launch_data.get('configurations', [])
        debug_config_found = False
        for cfg in configs:
            cfg_type = str(cfg.get('type', '')).lower()
            mi_mode = str(cfg.get('MIMode', '')).lower()
            request = str(cfg.get('request', '')).lower()
            # cppdbg type with gdb mode and launch request
            if cfg_type == 'cppdbg' and mi_mode == 'gdb' and request == 'launch':
                debug_config_found = True
                print(f"PASS: Component 2 -- cppdbg/gdb launch configuration found (0.30 pts)")
                total_score += 0.30
                break
        if not debug_config_found:
            print(f"FAIL: Component 2 -- No cppdbg/gdb launch config in launch.json (configs: {[c.get('type') for c in configs]})")
    except FileNotFoundError:
        print(f"FAIL: Component 2 -- launch.json not found at {LAUNCH_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: preLaunchTask in launch.json matches a task label in tasks.json (0.20 points)
    try:
        if launch_data and tasks_data:
            configs = launch_data.get('configurations', [])
            tasks_list = tasks_data.get('tasks', [])
            all_labels = [t.get('label', '') for t in tasks_list]
            prelaunch_linked = False
            for cfg in configs:
                pre_task = cfg.get('preLaunchTask', '')
                if pre_task and pre_task in all_labels:
                    prelaunch_linked = True
                    print(f"PASS: Component 3 -- preLaunchTask '{pre_task}' matches task label (0.20 pts)")
                    total_score += 0.20
                    break
            if not prelaunch_linked:
                pre_tasks = [cfg.get('preLaunchTask', '') for cfg in configs]
                print(f"FAIL: Component 3 -- preLaunchTask {pre_tasks} does not match any task label {all_labels}")
        else:
            print(f"FAIL: Component 3 -- Cannot check preLaunchTask (missing launch.json or tasks.json data)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Debug config has program path and gdb debugger path (0.20 points)
    try:
        if launch_data:
            configs = launch_data.get('configurations', [])
            proper_paths = False
            for cfg in configs:
                cfg_type = str(cfg.get('type', '')).lower()
                if cfg_type != 'cppdbg':
                    continue
                program = cfg.get('program', '')
                debugger = cfg.get('miDebuggerPath', '')
                has_program = bool(program and len(program.strip()) > 0)
                has_debugger = bool(debugger and 'gdb' in debugger.lower())
                if has_program and has_debugger:
                    proper_paths = True
                    print(f"PASS: Component 4 -- program='{program}', miDebuggerPath='{debugger}' (0.20 pts)")
                    total_score += 0.20
                    break
            if not proper_paths:
                print(f"FAIL: Component 4 -- Debug config missing program path or gdb debugger path")
        else:
            print(f"FAIL: Component 4 -- Cannot check paths (missing launch.json data)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
