"""
Reward Script: Create extensions.json with Python and Pylint extension recommendations
Task ID: vscode_file_023
Domain: vs_code
Scoring:
  Component 1: extensions.json exists and is valid JSON (0.30 pts)
  Component 2: recommendations array contains ms-python.python (0.35 pts)
  Component 3: recommendations array contains ms-python.pylint (0.35 pts)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user/data-project'
TASK_ID = 'vscode_file_023'
EXTENSIONS_JSON_PATH = os.path.join(WORKDIR, '.vscode', 'extensions.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires creating a .vscode/extensions.json file with:
      - A 'recommendations' array containing 'ms-python.python' and 'ms-python.pylint'
      - Valid JSON format
    """
    total_score = 0.0

    # Component 1: extensions.json exists and is valid parseable JSON (0.30 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 — extensions.json does not exist at {file_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        data = None
        try:
            data = json.loads(content)
        except json.JSONDecodeError as parse_err:
            print(f"FAIL: Component 1 — extensions.json exists but is not valid JSON: {parse_err}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        if data is not None:
            print(f"PASS: Component 1 — extensions.json exists and is valid JSON (0.30 pts)")
            total_score += 0.30

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: recommendations array contains 'ms-python.python' (0.35 points)
    # This FAILS on initial_env (no extensions.json) and PASSES on golden_env.
    try:
        recommendations = data.get('recommendations')
        if not isinstance(recommendations, list):
            print(f"FAIL: Component 2 — 'recommendations' key is missing or not a list (found: {type(recommendations).__name__})")
        elif 'ms-python.python' in recommendations:
            print(f"PASS: Component 2 — 'recommendations' contains 'ms-python.python' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — 'ms-python.python' not found in recommendations: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: recommendations array contains 'ms-python.pylint' (0.35 points)
    # This FAILS on initial_env (no extensions.json) and PASSES on golden_env.
    try:
        recommendations = data.get('recommendations')
        if not isinstance(recommendations, list):
            print(f"FAIL: Component 3 — 'recommendations' key is missing or not a list (found: {type(recommendations).__name__})")
        elif 'ms-python.pylint' in recommendations:
            print(f"PASS: Component 3 — 'recommendations' contains 'ms-python.pylint' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — 'ms-python.pylint' not found in recommendations: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against the canonical artifact path
if not os.path.isfile(EXTENSIONS_JSON_PATH):
    # File does not exist — score 0.0 immediately
    print(f"File not found: {EXTENSIONS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(EXTENSIONS_JSON_PATH)
