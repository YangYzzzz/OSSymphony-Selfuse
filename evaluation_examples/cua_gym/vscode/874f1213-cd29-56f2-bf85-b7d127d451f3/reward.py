"""
Reward Script: Configure workspace-level extension recommendations
Task ID: vscode_prod_017
Domain: vscode
Scoring:
  Component 1: extensions.json exists and is valid JSON with "recommendations" array (0.3 pts)
  Component 2: Contains ms-python.python in recommendations (0.25 pts)
  Component 3: Contains ms-python.pylint in recommendations (0.25 pts)
  Component 4: Contains ms-python.black-formatter in recommendations (0.2 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_017'
EXTENSIONS_PATH = os.path.join(WORKDIR, 'projects', 'python-api', '.vscode', 'extensions.json')

REQUIRED_EXTENSIONS = [
    'ms-python.python',
    'ms-python.pylint',
    'ms-python.black-formatter',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: extensions.json exists and is valid JSON with "recommendations" array (0.3 pts)
    # This component gates all subsequent checks -- if the file doesn't exist or isn't valid,
    # no further scoring is possible.
    recommendations = None
    try:
        with open(EXTENSIONS_PATH, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict) and 'recommendations' in data and isinstance(data['recommendations'], list):
            recommendations = [ext.lower().strip() for ext in data['recommendations'] if isinstance(ext, str)]
            print(f"PASS: Component 1 -- extensions.json exists with valid recommendations array ({len(recommendations)} items) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- extensions.json exists but missing or invalid 'recommendations' key. Data: {data}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 -- extensions.json not found at {EXTENSIONS_PATH}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 -- extensions.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if recommendations is None:
        # Cannot proceed without a valid recommendations list
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: ms-python.python in recommendations (0.25 pts)
    try:
        if 'ms-python.python' in recommendations:
            print(f"PASS: Component 2 -- 'ms-python.python' found in recommendations (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- 'ms-python.python' not found. Present: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: ms-python.pylint in recommendations (0.25 pts)
    try:
        if 'ms-python.pylint' in recommendations:
            print(f"PASS: Component 3 -- 'ms-python.pylint' found in recommendations (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- 'ms-python.pylint' not found. Present: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: ms-python.black-formatter in recommendations (0.2 pts)
    try:
        if 'ms-python.black-formatter' in recommendations:
            print(f"PASS: Component 4 -- 'ms-python.black-formatter' found in recommendations (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- 'ms-python.black-formatter' not found. Present: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
