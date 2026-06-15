"""
Reward Script: Create launch.json for debugging Python with integratedTerminal console
Task ID: vscode_td_085
Domain: vscode
Scoring:
  - Component 1 (0.2): launch.json exists, valid JSON, has configurations array
  - Component 2 (0.2): type == "debugpy" and request == "launch"
  - Component 3 (0.3): program == "${workspaceFolder}/src/quiz.py"
  - Component 4 (0.3): console == "integratedTerminal"
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_085'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'interactive-app', '.vscode', 'launch.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists, is valid JSON, and has a configurations array (0.2 points)
    config = None
    try:
        if not os.path.isfile(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        with open(LAUNCH_JSON_PATH, 'r') as f:
            content = f.read()

        # Strip JSONC comments (VSCode allows // comments)
        import re
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        data = json.loads(stripped)

        configs = data.get('configurations', None)
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 — launch.json is valid JSON with {len(configs)} configuration(s) (0.2 pts)")
            total_score += 0.2
            # Find a Python debug config (look for one with type debugpy or python)
            for c in configs:
                if c.get('type') in ('debugpy', 'python'):
                    config = c
                    break
            if config is None:
                # Fall back to first config
                config = configs[0]
        else:
            print(f"FAIL: Component 1 — launch.json missing or empty 'configurations' array")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — launch.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if config is None:
        print(f"FAIL: No configuration found to evaluate further")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: type == "debugpy" and request == "launch" (0.2 points)
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if cfg_type == 'debugpy' and cfg_request == 'launch':
            print(f"PASS: Component 2 — type='{cfg_type}', request='{cfg_request}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected type='debugpy' and request='launch', found type='{cfg_type}', request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: program == "${workspaceFolder}/src/quiz.py" (0.3 points)
    try:
        cfg_program = config.get('program', '')
        expected_program = '${workspaceFolder}/src/quiz.py'
        if cfg_program == expected_program:
            print(f"PASS: Component 3 — program='{cfg_program}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — expected program='{expected_program}', found '{cfg_program}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: console == "integratedTerminal" (0.3 points)
    try:
        cfg_console = config.get('console', '')
        if cfg_console == 'integratedTerminal':
            print(f"PASS: Component 4 — console='{cfg_console}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — expected console='integratedTerminal', found '{cfg_console}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
