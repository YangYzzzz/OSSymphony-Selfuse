"""
Reward Script: Create Jest debug launch configuration for VSCode
Task ID: vscode_web_056
Domain: vscode
Scoring:
  Component 1 (0.20): launch.json exists with valid JSON structure
  Component 2 (0.20): Configuration named 'Jest: Debug Current File' exists
  Component 3 (0.20): Type is 'node' and request is 'launch'
  Component 4 (0.25): runtimeArgs includes --runInBand and ${file}
  Component 5 (0.15): runtimeExecutable references jest/npx and console is set
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_056'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-ts-app')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) but not inside strings
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def find_jest_debug_config(configurations):
    """Find a configuration that matches Jest debug naming patterns."""
    for config in configurations:
        name = config.get('name', '').lower()
        if 'jest' in name and ('debug' in name or 'test' in name):
            return config
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON (0.20 points)
    # This check FAILS on initial_env (no launch.json) and PASSES on golden_env
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 -- launch.json not found at {LAUNCH_JSON_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        launch_data = load_jsonc(LAUNCH_JSON_PATH)
        if 'configurations' in launch_data and isinstance(launch_data['configurations'], list):
            print(f"PASS: Component 1 -- launch.json exists with {len(launch_data['configurations'])} configuration(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- launch.json missing 'configurations' array")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    configurations = launch_data['configurations']

    # Component 2: A Jest debug configuration exists (0.20 points)
    try:
        jest_config = find_jest_debug_config(configurations)
        if jest_config is not None:
            print(f"PASS: Component 2 -- Found Jest debug config: '{jest_config.get('name')}' (0.20 pts)")
            total_score += 0.20
        else:
            config_names = [c.get('name', '<unnamed>') for c in configurations]
            print(f"FAIL: Component 2 -- No Jest debug config found. Config names: {config_names}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    if jest_config is None:
        # Cannot proceed with remaining checks without the config
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: Type is 'node' and request is 'launch' (0.20 points)
    try:
        config_type = jest_config.get('type', '')
        config_request = jest_config.get('request', '')
        if config_type == 'node' and config_request == 'launch':
            print(f"PASS: Component 3 -- type='node', request='launch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- Expected type='node' request='launch', found type='{config_type}' request='{config_request}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: runtimeArgs includes --runInBand and ${file} (0.25 points)
    try:
        runtime_args = jest_config.get('runtimeArgs', [])
        # Also check 'args' as some configs use that instead
        args = jest_config.get('args', [])
        all_args = runtime_args + args

        has_run_in_band = any('--runInBand' in str(a) for a in all_args)
        has_file_var = any('${file}' in str(a) for a in all_args)

        partial = 0.0
        if has_run_in_band:
            partial += 0.125
        if has_file_var:
            partial += 0.125

        if has_run_in_band and has_file_var:
            print(f"PASS: Component 4 -- runtimeArgs contains --runInBand and ${{file}} (0.25 pts)")
            total_score += 0.25
        elif partial > 0:
            print(f"PARTIAL: Component 4 -- runInBand={has_run_in_band}, ${{file}}={has_file_var} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- runtimeArgs missing --runInBand and ${{file}}. Found: {all_args}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: runtimeExecutable references jest/npx and console is configured (0.15 points)
    try:
        runtime_exec = jest_config.get('runtimeExecutable', '')
        console_val = jest_config.get('console', '')

        # runtimeExecutable should be jest, npx, or a path containing jest/npx
        exec_ok = any(kw in str(runtime_exec).lower() for kw in ['jest', 'npx'])
        # Also check if jest appears in runtimeArgs when runtimeExecutable is npx
        if runtime_exec == 'npx':
            runtime_args = jest_config.get('runtimeArgs', [])
            exec_ok = exec_ok and any('jest' in str(a).lower() for a in runtime_args)

        # Console should be set (integratedTerminal or internalConsole)
        console_ok = len(console_val) > 0

        if exec_ok and console_ok:
            print(f"PASS: Component 5 -- runtimeExecutable='{runtime_exec}', console='{console_val}' (0.15 pts)")
            total_score += 0.15
        elif exec_ok:
            print(f"PARTIAL: Component 5 -- exec_ok but no console. runtimeExecutable='{runtime_exec}', console='{console_val}' (0.10 pts)")
            total_score += 0.10
        elif console_ok:
            print(f"PARTIAL: Component 5 -- console set but exec not jest/npx. runtimeExecutable='{runtime_exec}', console='{console_val}' (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 -- runtimeExecutable='{runtime_exec}', console='{console_val}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
