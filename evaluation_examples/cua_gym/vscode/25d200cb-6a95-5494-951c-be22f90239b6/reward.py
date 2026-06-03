"""
Reward Script: Verify .vscode/extensions.json with Python data science extension recommendations
Task ID: vscode_lp_085
Domain: vscode
Scoring:
  - Component 1 (0.20): .vscode/extensions.json exists and is valid JSON with "recommendations" list
  - Component 2 (0.20): Contains ms-python.python
  - Component 3 (0.20): Contains ms-toolsai.jupyter
  - Component 4 (0.20): Contains ms-python.vscode-pylance
  - Component 5 (0.20): Contains ms-python.data-wrangler
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_085'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
EXTENSIONS_FILE = os.path.join(PROJECT_DIR, '.vscode', 'extensions.json')

# Required extension IDs (case-insensitive matching)
REQUIRED_EXTENSIONS = [
    "ms-python.python",
    "ms-toolsai.jupyter",
    "ms-python.vscode-pylance",
    "ms-python.data-wrangler",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/extensions.json exists and is valid JSON with "recommendations" list (0.20 pts)
    recommendations = None
    try:
        if not os.path.isfile(EXTENSIONS_FILE):
            print(f"FAIL: Component 1 — {EXTENSIONS_FILE} does not exist")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(EXTENSIONS_FILE, 'r') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"FAIL: Component 1 — JSON root is not an object, got {type(data).__name__}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        recs = data.get("recommendations")
        if not isinstance(recs, list):
            print(f"FAIL: Component 1 — 'recommendations' key missing or not a list, got {type(recs).__name__}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        recommendations = [str(r).lower().strip() for r in recs]
        print(f"PASS: Component 1 — extensions.json exists with {len(recommendations)} recommendations (0.20 pts)")
        total_score += 0.20
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — extensions.json is not valid JSON: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Components 2-5: Check each required extension (0.20 pts each)
    for i, ext_id in enumerate(REQUIRED_EXTENSIONS, start=2):
        try:
            if ext_id.lower() in recommendations:
                print(f"PASS: Component {i} — '{ext_id}' found in recommendations (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component {i} — '{ext_id}' NOT found in recommendations. Present: {recommendations}")
        except Exception as e:
            print(f"ERROR: Component {i} — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
