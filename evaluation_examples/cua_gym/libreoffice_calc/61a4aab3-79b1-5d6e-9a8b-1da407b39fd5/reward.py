"""
Reward Script: Debug configuration for pytest integration tests
Task ID: vscode_py_044
Domain: vscode (launch.json)
Scoring:
  - Component 1 (0.3): New config named 'Debug Integration Tests' exists
  - Component 2 (0.3): Config uses module 'pytest'
  - Component 3 (0.4): Config has correct args ["-m", "integration", "tests/", "-v"]
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_044'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'launch.json')


def load_launch_json(file_path):
    """Load launch.json, stripping JSONC comments if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_config_by_name(configurations, name):
    """Find a configuration by its name field (case-insensitive)."""
    for cfg in configurations:
        if isinstance(cfg, dict) and cfg.get('name', '').strip().lower() == name.strip().lower():
            return cfg
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load launch.json
    try:
        data = load_launch_json(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load launch.json at {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    configurations = data.get('configurations', [])
    if not isinstance(configurations, list):
        print("CRITICAL: 'configurations' is not a list")
        print("REWARD: 0.0")
        return 0.0

    # Find the target configuration
    target_cfg = find_config_by_name(configurations, 'Debug Integration Tests')

    # Component 1: New config named 'Debug Integration Tests' exists (0.3 points)
    try:
        if target_cfg is not None:
            print(f"PASS: Component 1 - Config 'Debug Integration Tests' found (0.3 pts)")
            total_score += 0.3
        else:
            config_names = [c.get('name', '<unnamed>') for c in configurations if isinstance(c, dict)]
            print(f"FAIL: Component 1 - 'Debug Integration Tests' not found. Existing configs: {config_names}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Config uses "module": "pytest" (0.3 points)
    try:
        if target_cfg is not None:
            module_val = target_cfg.get('module', None)
            if module_val == 'pytest':
                print(f"PASS: Component 2 - module is 'pytest' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Expected module 'pytest', found: {module_val!r}")
        else:
            print(f"FAIL: Component 2 - Target config not found, cannot check module")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Config has correct args ["-m", "integration", "tests/", "-v"] (0.4 points)
    try:
        if target_cfg is not None:
            args_val = target_cfg.get('args', None)
            expected_args = ["-m", "integration", "tests/", "-v"]
            if isinstance(args_val, list):
                # Check that the required args are present:
                # -m, integration (after -m), tests/, -v
                checks_passed = sum([
                    '-m' in args_val,
                    any(args_val[i + 1] == 'integration' for i in range(len(args_val) - 1) if args_val[i] == '-m'),
                    any(a.rstrip('/') == 'tests' for a in args_val),
                    ('-v' in args_val or '--verbose' in args_val),
                ])

                if checks_passed == 4:
                    print(f"PASS: Component 3 - args contain required pytest flags (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 - Only {checks_passed}/4 required arg checks passed. Actual args: {args_val}")
            else:
                print(f"FAIL: Component 3 - Expected list for args, found: {type(args_val).__name__}")
        else:
            print(f"FAIL: Component 3 - Target config not found, cannot check args")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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
