"""
Reward Script: Create launch.json for debugging a Go application with build flags
Task ID: vscode_td_081
Domain: vscode
Scoring:
  Component 1 (0.20): launch.json exists and is valid JSON with configurations array
  Component 2 (0.25): Configuration has type="go", request="launch", mode="debug"
  Component 3 (0.20): program is "${workspaceFolder}/cmd/app"
  Component 4 (0.20): buildFlags is "-tags=integration"
  Component 5 (0.15): env contains GO111MODULE="on"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_081'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'go-service', '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON with configurations array (0.20 points)
    config = None
    configurations = None
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        config = load_jsonc(LAUNCH_JSON_PATH)
        configurations = config.get('configurations', [])
        if isinstance(configurations, list) and len(configurations) > 0:
            print(f"PASS: Component 1 — launch.json is valid JSON with {len(configurations)} configuration(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — launch.json has no configurations array or it is empty")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find the Go debug configuration (look for any config that could match)
    go_config = None
    for cfg in configurations:
        if isinstance(cfg, dict) and cfg.get('type') == 'go':
            go_config = cfg
            break
    # If no exact type match, use first config
    if go_config is None and len(configurations) > 0:
        go_config = configurations[0]

    if go_config is None:
        print(f"FAIL: No Go configuration found in launch.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: type="go", request="launch", mode="debug" (0.25 points)
    try:
        cfg_type = go_config.get('type', '')
        cfg_request = go_config.get('request', '')
        cfg_mode = go_config.get('mode', '')

        checks_passed = 0
        if cfg_type == 'go':
            checks_passed += 1
        else:
            print(f"FAIL: Component 2 — type is '{cfg_type}', expected 'go'")
        if cfg_request == 'launch':
            checks_passed += 1
        else:
            print(f"FAIL: Component 2 — request is '{cfg_request}', expected 'launch'")
        if cfg_mode == 'debug':
            checks_passed += 1
        else:
            print(f"FAIL: Component 2 — mode is '{cfg_mode}', expected 'debug'")

        if checks_passed == 3:
            print(f"PASS: Component 2 — type='go', request='launch', mode='debug' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — only {checks_passed}/3 basic config checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: program is "${workspaceFolder}/cmd/app" (0.20 points)
    try:
        program = go_config.get('program', '')
        if program == '${workspaceFolder}/cmd/app':
            print(f"PASS: Component 3 — program='{program}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — program is '{program}', expected '${{workspaceFolder}}/cmd/app'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: buildFlags is "-tags=integration" (0.20 points)
    try:
        build_flags = go_config.get('buildFlags', '')
        if build_flags == '-tags=integration':
            print(f"PASS: Component 4 — buildFlags='{build_flags}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — buildFlags is '{build_flags}', expected '-tags=integration'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: env contains GO111MODULE="on" (0.15 points)
    try:
        env = go_config.get('env', {})
        if isinstance(env, dict) and env.get('GO111MODULE') == 'on':
            print(f"PASS: Component 5 — env contains GO111MODULE='on' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — env is {env}, expected GO111MODULE='on'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
