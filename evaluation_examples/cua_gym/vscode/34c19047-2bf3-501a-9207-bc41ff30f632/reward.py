"""
Reward Script: Create .vscode/extensions.json with recommended extensions for Python web dev
Task ID: vscode_we_058
Domain: vscode
Scoring:
  - Component 1 (0.2): extensions.json exists, is valid JSON, has "recommendations" array
  - Component 2 (0.6): All 5 required extensions present (0.12 each)
  - Component 3 (0.2): No extra/unexpected extensions in recommendations
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_058'

# The exact extension IDs required by the task
REQUIRED_EXTENSIONS = [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "batisteo.vscode-django",
    "rangav.vscode-thunder-client",
]

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    file_path = os.path.join(WORKDIR, 'projects', 'django-api', '.vscode', 'extensions.json')

    # Component 1: File exists, is valid JSON, has "recommendations" array (0.2 points)
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 -- extensions.json does not exist at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        with open(file_path, 'r') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"FAIL: Component 1 -- extensions.json root is not a JSON object, got {type(data).__name__}")
            print("REWARD: 0.0")
            return 0.0

        recommendations = data.get("recommendations")
        if not isinstance(recommendations, list):
            print(f"FAIL: Component 1 -- 'recommendations' key missing or not an array, got {type(recommendations).__name__ if recommendations is not None else 'None'}")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 -- extensions.json exists with valid 'recommendations' array (0.2 pts)")
        total_score += 0.2

    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 -- extensions.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: All 5 required extensions present (0.6 points, 0.12 each)
    try:
        # Normalize to lowercase for case-insensitive comparison
        actual_lower = [ext.lower().strip() for ext in recommendations]
        found_count = 0
        for ext_id in REQUIRED_EXTENSIONS:
            if ext_id.lower() in actual_lower:
                print(f"PASS: Component 2 -- Found required extension '{ext_id}' (0.12 pts)")
                total_score += 0.12
                found_count += 1
            else:
                print(f"FAIL: Component 2 -- Missing required extension '{ext_id}'")
        print(f"  Component 2 summary: {found_count}/{len(REQUIRED_EXTENSIONS)} required extensions found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: No extra unexpected extensions (0.2 points)
    try:
        required_lower = set(ext.lower() for ext in REQUIRED_EXTENSIONS)
        extras = [ext for ext in recommendations if ext.lower().strip() not in required_lower]
        if len(extras) == 0:
            print(f"PASS: Component 3 -- No extra extensions in recommendations (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Found {len(extras)} unexpected extensions: {extras}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
