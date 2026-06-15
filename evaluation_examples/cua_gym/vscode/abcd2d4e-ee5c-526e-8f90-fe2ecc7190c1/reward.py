"""
Reward Script: Create .vscode/launch.json with Playwright debug configuration
Task ID: vscode_gf3_057
Domain: vscode
Scoring:
  - Component 1: File exists and is valid JSON with configurations array (0.15)
  - Component 2: Configuration name is "Debug Playwright Tests" (0.15)
  - Component 3: type is "node" and request is "launch" (0.15)
  - Component 4: program is "${workspaceFolder}/node_modules/.bin/playwright" (0.20)
  - Component 5: args contains "test", "--debug", "${file}" (0.20)
  - Component 6: env.PWDEBUG is "1" (0.15)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_057'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'playwright-project', '.vscode', 'launch.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist and be valid JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Invalid JSON in {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has configurations array with at least one entry (0.15 points)
    try:
        configs = data.get('configurations', None)
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 — configurations array exists with {len(configs)} entry(ies) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected 'configurations' array with entries, found: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the target configuration (look for one matching the expected name or the first one)
    config = None
    if isinstance(data.get('configurations'), list):
        for c in data['configurations']:
            if isinstance(c, dict) and c.get('name') == 'Debug Playwright Tests':
                config = c
                break
        # Fallback: use first config if name not found
        if config is None and len(data['configurations']) > 0:
            config = data['configurations'][0]

    if config is None:
        print("CRITICAL: No configuration found to evaluate")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Configuration name is "Debug Playwright Tests" (0.15 points)
    try:
        name = config.get('name', '')
        if name == 'Debug Playwright Tests':
            print(f"PASS: Component 2 — name is 'Debug Playwright Tests' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected name 'Debug Playwright Tests', found: '{name}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: type is "node" and request is "launch" (0.15 points)
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if cfg_type == 'node' and cfg_request == 'launch':
            print(f"PASS: Component 3 — type='node', request='launch' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — expected type='node' and request='launch', found type='{cfg_type}', request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: program is "${workspaceFolder}/node_modules/.bin/playwright" (0.20 points)
    try:
        program = config.get('program', '')
        expected_program = '${workspaceFolder}/node_modules/.bin/playwright'
        if program == expected_program:
            print(f"PASS: Component 4 — program is '{expected_program}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — expected program '{expected_program}', found: '{program}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: args contains "test", "--debug", "${file}" (0.20 points)
    try:
        args = config.get('args', [])
        required_args = ['test', '--debug', '${file}']
        if isinstance(args, list):
            # Check all required args are present
            missing = [a for a in required_args if a not in args]
            if len(missing) == 0:
                print(f"PASS: Component 5 — args contains all required values: {required_args} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — missing args: {missing}, found: {args}")
        else:
            print(f"FAIL: Component 5 — expected args to be a list, found: {type(args)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: env.PWDEBUG is "1" (0.15 points)
    try:
        env = config.get('env', {})
        if isinstance(env, dict):
            pwdebug_val = env.get('PWDEBUG', None)
            if pwdebug_val == '1':
                print(f"PASS: Component 6 — env.PWDEBUG='1' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — expected env.PWDEBUG='1', found: '{pwdebug_val}'")
        else:
            print(f"FAIL: Component 6 — expected env to be a dict, found: {type(env)}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
