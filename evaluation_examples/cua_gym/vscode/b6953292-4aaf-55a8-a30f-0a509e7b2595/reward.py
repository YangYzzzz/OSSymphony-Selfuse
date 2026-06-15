"""
Reward Script: Create workspace recommendations file with 4 required extensions
Task ID: vscode_ext_021
Domain: vs_code
Scoring:
  Component 1: .vscode/extensions.json file exists at correct path (0.3 pts)
  Component 2: File contains valid JSON with a 'recommendations' key (0.3 pts)
  Component 3: All 4 required extension IDs are present in recommendations (0.4 pts)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_021'

EXTENSIONS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'react-app', '.vscode', 'extensions.json')

REQUIRED_EXTENSIONS = [
    "dsznajder.es7-react-js-snippets",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "formulahendry.auto-close-tag",
]


def verify_task(file_path: str) -> float:
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: extensions.json file exists at the correct path (0.3 points)
    # This FAILS on initial (no .vscode dir) and PASSES on golden
    try:
        if os.path.isfile(file_path):
            print(f"PASS: Component 1 — extensions.json exists at {file_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — extensions.json not found at {file_path}")
            # Without the file, nothing else can be verified
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File contains valid JSON with a 'recommendations' key (0.3 points)
    # This FAILS on initial (file doesn't exist) and PASSES on golden
    recommendations = None
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict) and 'recommendations' in data and isinstance(data['recommendations'], list):
            recommendations = data['recommendations']
            total_score += 0.3  # PASS: valid JSON with recommendations list
            print(f"PASS: Component 2 — File is valid JSON with 'recommendations' list ({len(recommendations)} entries) (0.3 pts)")
        else:
            keys_found = list(data.keys()) if isinstance(data, dict) else 'not a dict'
            print(f"FAIL: Component 2 — JSON lacks 'recommendations' list. Keys found: {keys_found}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — File is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if recommendations is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: All 4 required extension IDs are present in recommendations (0.4 points)
    # Each missing extension deducts 0.1 from this component
    # This FAILS on initial (file doesn't exist) and PASSES on golden
    try:
        # Normalize to lowercase for comparison (extension IDs are case-insensitive)
        recommendations_lower = [ext.lower() for ext in recommendations]
        found = []
        missing = []
        for ext_id in REQUIRED_EXTENSIONS:
            if ext_id.lower() in recommendations_lower:
                found.append(ext_id)
            else:
                missing.append(ext_id)

        if len(missing) == 0:
            print(f"PASS: Component 3 — All 4 required extensions found in recommendations (0.4 pts)")
            print(f"  Found: {found}")
            total_score += 0.4
        else:
            partial = len(found) * 0.1
            print(f"FAIL: Component 3 — {len(missing)} extension(s) missing from recommendations")
            print(f"  Found: {found}")
            print(f"  Missing: {missing}")
            if partial > 0:
                print(f"  Partial credit: {partial:.1f} pts ({len(found)}/4 extensions found)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isdir(os.path.dirname(EXTENSIONS_JSON_PATH)):
    # .vscode directory does not exist — definitely not completed
    print(f"PRECONDITION FAIL: .vscode directory not found at "
          f"{os.path.dirname(EXTENSIONS_JSON_PATH)}")
    print("REWARD: 0.0")
else:
    verify_task(EXTENSIONS_JSON_PATH)
