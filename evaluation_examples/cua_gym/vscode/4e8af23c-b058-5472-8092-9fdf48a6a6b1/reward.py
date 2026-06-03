"""
Reward Script: VSCode Node.js CPU Profiling Launch Config + Task
Task ID: vscode_gf3_048
Domain: vscode
Scoring:
  - Component 1 (0.15): launch.json exists and is valid JSON with configurations array
  - Component 2 (0.20): Launch config named "Profile: CPU Sampling"
  - Component 3 (0.25): Launch config has "--prof" in runtimeArgs
  - Component 4 (0.10): Launch config references /tmp/node-profile.log
  - Component 5 (0.10): tasks.json exists and is valid JSON with tasks array
  - Component 6 (0.20): Task command contains "node --prof-process /tmp/node-profile.log > profile-report.txt"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_048'
VSCODE_DIR = os.path.join(WORKDIR, 'projects', 'node-service', '.vscode')
LAUNCH_PATH = os.path.join(VSCODE_DIR, 'launch.json')
TASKS_PATH = os.path.join(VSCODE_DIR, 'tasks.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) but not inside strings
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================
    # Component 1: launch.json exists and is valid JSON (0.15)
    # =========================================================
    launch_data = None
    try:
        if not os.path.exists(LAUNCH_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_PATH}")
        else:
            launch_data = load_jsonc(LAUNCH_PATH)
            if isinstance(launch_data, dict) and 'configurations' in launch_data and isinstance(launch_data['configurations'], list):
                print(f"PASS: Component 1 — launch.json is valid with configurations array (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — launch.json missing 'configurations' array")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================
    # Component 2: Config named "Profile: CPU Sampling" (0.20)
    # =========================================================
    target_config = None
    try:
        if launch_data and 'configurations' in launch_data:
            for cfg in launch_data['configurations']:
                if isinstance(cfg, dict) and cfg.get('name') == 'Profile: CPU Sampling':
                    target_config = cfg
                    break
            if target_config:
                print(f"PASS: Component 2 — Found config named 'Profile: CPU Sampling' (0.20 pts)")
                total_score += 0.20
            else:
                names = [c.get('name', '<no name>') for c in launch_data['configurations'] if isinstance(c, dict)]
                print(f"FAIL: Component 2 — No config named 'Profile: CPU Sampling'. Found: {names}")
        else:
            print(f"FAIL: Component 2 — No launch data to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================
    # Component 3: runtimeArgs contains "--prof" (0.25)
    # =========================================================
    try:
        if target_config:
            runtime_args = target_config.get('runtimeArgs', [])
            if isinstance(runtime_args, list) and '--prof' in runtime_args:
                print(f"PASS: Component 3 — '--prof' found in runtimeArgs (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — '--prof' not in runtimeArgs. Found: {runtime_args}")
        else:
            print(f"FAIL: Component 3 — No target config to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================
    # Component 4: Config references /tmp/node-profile.log (0.10)
    # =========================================================
    try:
        if target_config:
            # Check env vars, args, or any string value for the path
            config_str = json.dumps(target_config)
            if '/tmp/node-profile.log' in config_str:
                print(f"PASS: Component 4 — '/tmp/node-profile.log' referenced in launch config (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — '/tmp/node-profile.log' not found in config. Config: {config_str[:200]}")
        else:
            print(f"FAIL: Component 4 — No target config to check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================
    # Component 5: tasks.json exists and valid with tasks array (0.10)
    # =========================================================
    tasks_data = None
    try:
        if not os.path.exists(TASKS_PATH):
            print(f"FAIL: Component 5 — tasks.json not found at {TASKS_PATH}")
        else:
            tasks_data = load_jsonc(TASKS_PATH)
            if isinstance(tasks_data, dict) and 'tasks' in tasks_data and isinstance(tasks_data['tasks'], list) and len(tasks_data['tasks']) > 0:
                print(f"PASS: Component 5 — tasks.json is valid with tasks array (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — tasks.json missing 'tasks' array or empty")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # =========================================================
    # Component 6: Task command contains prof-process command (0.20)
    # =========================================================
    try:
        if tasks_data and 'tasks' in tasks_data:
            found_task = False
            for task in tasks_data['tasks']:
                if not isinstance(task, dict):
                    continue
                cmd = task.get('command', '')
                if isinstance(cmd, str) and 'node' in cmd and '--prof-process' in cmd and '/tmp/node-profile.log' in cmd and 'profile-report.txt' in cmd:
                    found_task = True
                    print(f"PASS: Component 6 — Task command matches: '{cmd}' (0.20 pts)")
                    total_score += 0.20
                    break
            if not found_task:
                cmds = [t.get('command', '<none>') for t in tasks_data['tasks'] if isinstance(t, dict)]
                print(f"FAIL: Component 6 — No task with required prof-process command. Found commands: {cmds}")
        else:
            print(f"FAIL: Component 6 — No tasks data to check")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
