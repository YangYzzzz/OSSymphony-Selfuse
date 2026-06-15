"""
Reward Script: Add Go debug test configuration to launch.json
Task ID: vscode_lang_011
Domain: vs_code
Scoring:
  Component 1 (0.2): "Debug Tests" configuration exists
  Component 2 (0.3): type=go, request=launch, mode=test
  Component 3 (0.2): program set to ${workspaceFolder}/pkg/utils
  Component 4 (0.3): args contains ["-v", "-timeout", "30s"]
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_011'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'mygoapp', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) that are not inside strings
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def find_debug_tests_config(configurations):
    """Find configuration named 'Debug Tests' (case-insensitive match)."""
    for cfg in configurations:
        if isinstance(cfg, dict) and cfg.get('name', '').strip().lower() == 'debug tests':
            return cfg
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist and be valid JSON
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, ValueError) as e:
        print(f"CRITICAL: launch.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    configurations = data.get('configurations', [])
    if not isinstance(configurations, list):
        print("CRITICAL: 'configurations' is not a list")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: "Debug Tests" configuration exists (0.2 points)
    try:
        debug_cfg = find_debug_tests_config(configurations)
        if debug_cfg is not None:
            print(f"PASS: Component 1 — 'Debug Tests' configuration found (0.2 pts)")
            total_score += 0.2
        else:
            config_names = [c.get('name', '<unnamed>') for c in configurations if isinstance(c, dict)]
            print(f"FAIL: Component 1 — 'Debug Tests' not found. Existing configs: {config_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if debug_cfg is None:
        # No point checking further components
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: type=go, request=launch, mode=test (0.3 points)
    # Each sub-check is worth 0.1 points
    try:
        comp2_score = 0.0
        actual_type = debug_cfg.get('type', '')
        actual_request = debug_cfg.get('request', '')
        actual_mode = debug_cfg.get('mode', '')

        if str(actual_type).lower() == 'go':
            comp2_score += 0.1
            print(f"  PASS: type == 'go'")
        else:
            print(f"  FAIL: type expected 'go', found '{actual_type}'")

        if str(actual_request).lower() == 'launch':
            comp2_score += 0.1
            print(f"  PASS: request == 'launch'")
        else:
            print(f"  FAIL: request expected 'launch', found '{actual_request}'")

        if str(actual_mode).lower() == 'test':
            comp2_score += 0.1
            print(f"  PASS: mode == 'test'")
        else:
            print(f"  FAIL: mode expected 'test', found '{actual_mode}'")

        if comp2_score > 0:
            print(f"PASS: Component 2 — type/request/mode checks ({comp2_score} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — all type/request/mode checks failed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: program set to "${workspaceFolder}/pkg/utils" (0.2 points)
    try:
        actual_program = debug_cfg.get('program', '')
        expected_program = '${workspaceFolder}/pkg/utils'
        if str(actual_program) == expected_program:
            print(f"PASS: Component 3 — program == '{expected_program}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — program expected '{expected_program}', found '{actual_program}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: args contains ["-v", "-timeout", "30s"] (0.3 points)
    try:
        actual_args = debug_cfg.get('args', [])
        expected_args = ["-v", "-timeout", "30s"]

        if not isinstance(actual_args, list):
            print(f"FAIL: Component 4 — args is not a list, found: {type(actual_args)}")
        else:
            # Check that all expected args are present in order
            # The expected args must appear as a contiguous subsequence or exact match
            if actual_args == expected_args:
                print(f"PASS: Component 4 — args == {expected_args} (0.3 pts)")
                total_score += 0.3
            else:
                # Partial credit: check if all three elements exist in args
                has_v = '-v' in actual_args
                has_timeout = '-timeout' in actual_args
                has_30s = '30s' in actual_args
                partial = sum([has_v, has_timeout, has_30s])
                if partial == 3:
                    # All elements present but in different order or with extras
                    print(f"PASS: Component 4 — args contains all required elements (0.2 pts partial)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — args expected {expected_args}, found {actual_args}")
                    print(f"  -v: {has_v}, -timeout: {has_timeout}, 30s: {has_30s}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
