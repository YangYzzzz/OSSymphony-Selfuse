"""
Reward Script: Create VSCode launch.json for Mocha debug configuration
Task ID: vscode_dbg_039
Domain: vs_code
Scoring:
  Component 1: .vscode/launch.json file exists (0.2 pts)
  Component 2: Configuration has type 'node' and request 'launch' (0.2 pts)
  Component 3: Configuration has correct program path to mocha binary (0.3 pts)
  Component 4: Configuration has correct args ['--recursive', 'test/'] (0.3 pts)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_039'

PROJECT_DIR = f'{WORKDIR}/projects/mocha-debug'
LAUNCH_JSON_PATH = f'{PROJECT_DIR}/.vscode/launch.json'

# Expected values from task context
EXPECTED_TYPE = 'node'
EXPECTED_REQUEST = 'launch'
EXPECTED_PROGRAM = '${workspaceFolder}/node_modules/mocha/bin/_mocha'
EXPECTED_ARGS = ['--recursive', 'test/']


def _is_subset(expected, actual) -> bool:
    """Recursive subset check for nested dict/list/scalar comparison."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task(launch_json_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/launch.json file exists (0.2 points)
    # This FAILS on initial_env (no .vscode/) -> PASSES on golden_env
    try:
        if os.path.exists(launch_json_path):
            print(f"PASS: Component 1 — launch.json exists at {launch_json_path} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — launch.json not found at {launch_json_path}")
            # If file doesn't exist, skip all further checks
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load launch.json for further verification
    try:
        with open(launch_json_path, 'r') as f:
            content = f.read()
        # Strip JSONC comments just in case
        import re
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        launch_config = json.loads(content_clean)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Extract configurations list
    configurations = launch_config.get('configurations', [])
    if not isinstance(configurations, list) or len(configurations) == 0:
        print(f"FAIL: No configurations array found in launch.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find a matching configuration (by type=node and request=launch)
    # This handles the case of multiple configurations
    matching_configs = [
        cfg for cfg in configurations
        if cfg.get('type') == EXPECTED_TYPE and cfg.get('request') == EXPECTED_REQUEST
    ]

    # Component 2: Configuration has type 'node' and request 'launch' (0.2 points)
    # This FAILS on initial_env (file doesn't exist) -> PASSES on golden_env
    try:
        if len(matching_configs) > 0:
            print(f"PASS: Component 2 — configuration with type='{EXPECTED_TYPE}' and request='{EXPECTED_REQUEST}' found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — no configuration with type='{EXPECTED_TYPE}' and request='{EXPECTED_REQUEST}' found")
            print(f"  Found configurations: {[{'type': c.get('type'), 'request': c.get('request')} for c in configurations]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Configuration has correct program path to mocha binary (0.3 points)
    # This FAILS on initial_env -> PASSES on golden_env
    try:
        matching_programs = [
            cfg.get('program', '')
            for cfg in matching_configs
            if cfg.get('program', '') == EXPECTED_PROGRAM
        ]
        if len(matching_programs) > 0:
            print(f"PASS: Component 3 — program set to '{matching_programs[0]}' (0.3 pts)")
            total_score += 0.3
        else:
            actual_programs = [cfg.get('program', '<not set>') for cfg in matching_configs]
            print(f"FAIL: Component 3 — expected program='{EXPECTED_PROGRAM}', found: {actual_programs}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Configuration has correct args ['--recursive', 'test/'] (0.3 points)
    # This FAILS on initial_env -> PASSES on golden_env
    try:
        matching_args_configs = [
            cfg for cfg in matching_configs
            if '--recursive' in cfg.get('args', []) and 'test/' in cfg.get('args', [])
        ]
        if len(matching_args_configs) > 0:
            actual_args = matching_args_configs[0].get('args', [])
            print(f"PASS: Component 4 — args contain '--recursive' and 'test/' (actual: {actual_args}) (0.3 pts)")
            total_score += 0.3
        else:
            actual_args_list = [cfg.get('args', []) for cfg in matching_configs]
            print(f"FAIL: Component 4 — expected args to include '--recursive' and 'test/', found: {actual_args_list}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(f'{PROJECT_DIR}'):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
