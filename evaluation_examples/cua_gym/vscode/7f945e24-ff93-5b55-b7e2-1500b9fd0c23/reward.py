"""
Reward Script: Create launch.json for debugging Python Celery worker
Task ID: vscode_td_077
Domain: vscode
Scoring:
  Component 1 (0.20): launch.json exists, valid JSON, has configurations array
  Component 2 (0.20): type == "debugpy" and request == "launch"
  Component 3 (0.20): module == "celery"
  Component 4 (0.25): args == ["worker", "-A", "tasks", "--loglevel=info", "--pool=solo"]
  Component 5 (0.15): justMyCode == false and console == "integratedTerminal"
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_077'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'task-queue', '.vscode', 'launch.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON with configurations
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        data = json.loads(content)
    except FileNotFoundError:
        print(f"FAIL: launch.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"FAIL: launch.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has configurations array with at least one entry (0.20 points)
    try:
        configs = data.get('configurations', None)
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- configurations array found with {len(configs)} entries (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- expected non-empty 'configurations' array, found: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find the Celery-related configuration (look for one with module == "celery" or name containing "celery")
    config = None
    if isinstance(data.get('configurations'), list):
        for c in data['configurations']:
            if isinstance(c, dict) and c.get('module') == 'celery':
                config = c
                break
        # Fallback: first config
        if config is None and len(data['configurations']) > 0:
            config = data['configurations'][0]

    if config is None:
        print("FAIL: No configuration entry found to evaluate")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: type == "debugpy" and request == "launch" (0.20 points)
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if cfg_type == 'debugpy' and cfg_request == 'launch':
            print(f"PASS: Component 2 -- type='debugpy', request='launch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- expected type='debugpy' request='launch', found type='{cfg_type}' request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: module == "celery" (0.20 points)
    try:
        cfg_module = config.get('module', '')
        if cfg_module == 'celery':
            print(f"PASS: Component 3 -- module='celery' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- expected module='celery', found '{cfg_module}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: args == ["worker", "-A", "tasks", "--loglevel=info", "--pool=solo"] (0.25 points)
    try:
        expected_args = ["worker", "-A", "tasks", "--loglevel=info", "--pool=solo"]
        cfg_args = config.get('args', [])
        if cfg_args == expected_args:
            print(f"PASS: Component 4 -- args match exactly (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- expected args={expected_args}, found {cfg_args}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: justMyCode == false and console == "integratedTerminal" (0.15 points)
    try:
        jmc = config.get('justMyCode')
        console = config.get('console', '')
        if jmc is False and console == 'integratedTerminal':
            print(f"PASS: Component 5 -- justMyCode=false, console='integratedTerminal' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- expected justMyCode=false console='integratedTerminal', found justMyCode={jmc} console='{console}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
