"""
Reward Script: Create launch.json for Django debugging in VSCode
Task ID: vscode_dbg_032
Domain: vs_code
Scoring:
  Component 1: .vscode/launch.json exists with valid JSON structure (0.20)
  Component 2: Configuration has type='debugpy' and request='launch' (0.30)
  Component 3: Configuration has program='${workspaceFolder}/manage.py' (0.30)
  Component 4: Configuration args include 'runserver' and '--noreload' (0.20)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_032'
LAUNCH_JSON_PATH = '/home/user/projects/django-site/.vscode/launch.json'


def verify_task():
    """
    Verify that the agent created a valid .vscode/launch.json for Django
    debugging with the required configuration properties.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/launch.json exists and contains valid JSON with
    # a 'configurations' array (0.20 points)
    # NOTE: initial_env has NO .vscode folder — this FAILS on initial, PASSES on golden.
    launch_data = None
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — {LAUNCH_JSON_PATH} does not exist")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(LAUNCH_JSON_PATH, 'r') as f:
            content = f.read()

        try:
            launch_data = json.loads(content)
        except json.JSONDecodeError as je:
            print(f"FAIL: Component 1 — launch.json is not valid JSON: {je}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        configurations = launch_data.get('configurations', None)
        if not isinstance(configurations, list) or len(configurations) == 0:
            print(f"FAIL: Component 1 — 'configurations' array is missing or empty")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        print(f"PASS: Component 1 — launch.json exists with valid JSON and {len(configurations)} configuration(s) (0.20 pts)")
        total_score += 0.20

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: At least one configuration has type='debugpy' AND request='launch'
    # (0.30 points)
    # The task specifically requires type='debugpy' and request='launch'.
    # FAILS on initial (no file), PASSES on golden.
    try:
        matching_configs = [
            cfg for cfg in launch_data['configurations']
            if cfg.get('type') == 'debugpy' and cfg.get('request') == 'launch'
        ]
        if matching_configs:
            print(f"PASS: Component 2 — found configuration with type='debugpy' and request='launch' (0.30 pts)")
            total_score += 0.30
        else:
            found_types = [cfg.get('type') for cfg in launch_data['configurations']]
            found_requests = [cfg.get('request') for cfg in launch_data['configurations']]
            print(f"FAIL: Component 2 — no configuration with type='debugpy' and request='launch'; "
                  f"found types={found_types}, requests={found_requests}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Configuration has program='${workspaceFolder}/manage.py'
    # (0.30 points)
    # The task requires program to point to manage.py using the workspace variable.
    # FAILS on initial (no file), PASSES on golden.
    try:
        program_configs = [
            cfg for cfg in launch_data['configurations']
            if cfg.get('program') == '${workspaceFolder}/manage.py'
        ]
        if program_configs:
            print(f"PASS: Component 3 — found program='${{workspaceFolder}}/manage.py' (0.30 pts)")
            total_score += 0.30
        else:
            found_programs = [cfg.get('program') for cfg in launch_data['configurations']]
            print(f"FAIL: Component 3 — no configuration with program='${{workspaceFolder}}/manage.py'; "
                  f"found programs={found_programs}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Configuration args contain 'runserver' and '--noreload'
    # (0.20 points)
    # The task specifically requires args=['runserver', '--noreload'].
    # FAILS on initial (no file), PASSES on golden.
    try:
        args_configs = [
            cfg for cfg in launch_data['configurations']
            if isinstance(cfg.get('args'), list)
            and 'runserver' in cfg.get('args', [])
            and '--noreload' in cfg.get('args', [])
        ]
        if args_configs:
            print(f"PASS: Component 4 — found args containing 'runserver' and '--noreload' (0.20 pts)")
            total_score += 0.20
        else:
            found_args = [cfg.get('args') for cfg in launch_data['configurations']]
            print(f"FAIL: Component 4 — no configuration with args containing 'runserver' and '--noreload'; "
                  f"found args={found_args}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
