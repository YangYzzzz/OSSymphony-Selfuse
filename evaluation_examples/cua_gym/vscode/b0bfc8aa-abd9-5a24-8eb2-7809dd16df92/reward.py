"""
Reward Script: Create launch.json with two Node.js launch configurations in VSCode project
Task ID: vscode_dbg_042
Domain: vs_code
Scoring:
  - Component 1: launch.json exists AND has exactly 2 configurations (0.3 pts)
  - Component 2: 'Launch API' config has correct type='node', request='launch', program='${workspaceFolder}/api/index.js' (0.35 pts)
  - Component 3: 'Launch Worker' config has correct type='node', request='launch', program='${workspaceFolder}/worker/index.js' (0.35 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_042'
LAUNCH_JSON_PATH = '/home/user/projects/multi-target/.vscode/launch.json'


def verify_task(launch_json_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be valid JSON
    if not os.path.exists(launch_json_path):
        print(f"FAIL: launch.json not found at {launch_json_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(launch_json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Configurations array exists and has exactly 2 entries (0.3 points)
    try:
        configs = data.get('configurations', None)
        comp1_pass = (configs is not None) and isinstance(configs, list) and (len(configs) == 2)
        if comp1_pass:
            print(f"PASS: Component 1 — configurations array contains exactly 2 entries (0.3 pts)")
            total_score += 0.3
        else:
            if configs is None:
                print("FAIL: Component 1 — 'configurations' key not found in launch.json")
            elif not isinstance(configs, list):
                print(f"FAIL: Component 1 — 'configurations' is not a list, found: {type(configs)}")
            else:
                print(f"FAIL: Component 1 — expected 2 configurations, found {len(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Launch API' configuration has correct type, request, and program (0.35 points)
    try:
        configs = data.get('configurations', [])
        launch_api = None
        for cfg in configs:
            if isinstance(cfg, dict) and cfg.get('name') == 'Launch API':
                launch_api = cfg
                break

        if launch_api is None:
            print("FAIL: Component 2 — No configuration named 'Launch API' found")
        else:
            api_type = launch_api.get('type', '')
            api_request = launch_api.get('request', '')
            api_program = launch_api.get('program', '')

            expected_program = '${workspaceFolder}/api/index.js'
            if api_type == 'node' and api_request == 'launch' and api_program == expected_program:
                print(f"PASS: Component 2 — 'Launch API' config correct: type='{api_type}', request='{api_request}', program='{api_program}' (0.35 pts)")
                total_score += 0.35
            else:
                details = []
                if api_type != 'node':
                    details.append(f"type expected 'node', found '{api_type}'")
                if api_request != 'launch':
                    details.append(f"request expected 'launch', found '{api_request}'")
                if api_program != expected_program:
                    details.append(f"program expected '{expected_program}', found '{api_program}'")
                print(f"FAIL: Component 2 — 'Launch API' config incorrect: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Launch Worker' configuration has correct type, request, and program (0.35 points)
    try:
        configs = data.get('configurations', [])
        launch_worker = None
        for cfg in configs:
            if isinstance(cfg, dict) and cfg.get('name') == 'Launch Worker':
                launch_worker = cfg
                break

        if launch_worker is None:
            print("FAIL: Component 3 — No configuration named 'Launch Worker' found")
        else:
            worker_type = launch_worker.get('type', '')
            worker_request = launch_worker.get('request', '')
            worker_program = launch_worker.get('program', '')

            expected_program = '${workspaceFolder}/worker/index.js'
            if worker_type == 'node' and worker_request == 'launch' and worker_program == expected_program:
                print(f"PASS: Component 3 — 'Launch Worker' config correct: type='{worker_type}', request='{worker_request}', program='{worker_program}' (0.35 pts)")
                total_score += 0.35
            else:
                details = []
                if worker_type != 'node':
                    details.append(f"type expected 'node', found '{worker_type}'")
                if worker_request != 'launch':
                    details.append(f"request expected 'launch', found '{worker_request}'")
                if worker_program != expected_program:
                    details.append(f"program expected '{expected_program}', found '{worker_program}'")
                print(f"FAIL: Component 3 — 'Launch Worker' config incorrect: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical task path
verify_task(LAUNCH_JSON_PATH)
