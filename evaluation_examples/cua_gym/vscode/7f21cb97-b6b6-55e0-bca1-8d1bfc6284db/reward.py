"""
Reward Script: Verify workspace-level recommended extensions (extensions.json)
Task ID: vscode_web_038
Domain: vscode
Scoring:
  Component 1: extensions.json exists and is valid JSON (0.1 pts)
  Component 2: recommendations array has all 4 required extensions (0.5 pts)
  Component 3: unwantedRecommendations contains hookyqr.beautify (0.2 pts)
  Component 4: No extraneous entries in recommendations or unwantedRecommendations (0.2 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_038'
EXTENSIONS_PATH = os.path.join(WORKDIR, 'projects', 'react-app', '.vscode', 'extensions.json')

REQUIRED_RECOMMENDATIONS = [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "dsznajder.es7-react-js-snippets",
]

REQUIRED_UNWANTED = [
    "hookyqr.beautify",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: extensions.json exists and is valid JSON (0.1 points)
    try:
        if not os.path.isfile(EXTENSIONS_PATH):
            print(f"FAIL: Component 1 -- extensions.json not found at {EXTENSIONS_PATH}")
            print("REWARD: 0.0")
            return 0.0

        with open(EXTENSIONS_PATH, 'r') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"FAIL: Component 1 -- extensions.json is not a JSON object, got {type(data).__name__}")
            print("REWARD: 0.0")
            return 0.0

        if isinstance(data, dict):
            print(f"PASS: Component 1 -- extensions.json exists and is valid JSON (0.1 pts)")
            total_score += 0.1
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 -- extensions.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: recommendations array contains all 4 required extensions (0.5 points)
    # Each extension is worth 0.125 points
    try:
        recommendations = data.get("recommendations", [])
        if not isinstance(recommendations, list):
            print(f"FAIL: Component 2 -- 'recommendations' is not a list, got {type(recommendations).__name__}")
        else:
            # Normalize to lowercase for case-insensitive comparison
            recs_lower = [r.lower() for r in recommendations if isinstance(r, str)]
            found_count = 0
            for ext in REQUIRED_RECOMMENDATIONS:
                if ext.lower() in recs_lower:
                    print(f"PASS: Component 2 -- Found recommended extension: {ext} (0.125 pts)")
                    total_score += 0.125
                    found_count += 1
                else:
                    print(f"FAIL: Component 2 -- Missing recommended extension: {ext}")
            print(f"Component 2 summary: {found_count}/{len(REQUIRED_RECOMMENDATIONS)} recommended extensions found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: unwantedRecommendations contains hookyqr.beautify (0.2 points)
    try:
        unwanted = data.get("unwantedRecommendations", [])
        if not isinstance(unwanted, list):
            print(f"FAIL: Component 3 -- 'unwantedRecommendations' is not a list, got {type(unwanted).__name__}")
        else:
            unwanted_lower = [u.lower() for u in unwanted if isinstance(u, str)]
            if "hookyqr.beautify" in unwanted_lower:
                print(f"PASS: Component 3 -- hookyqr.beautify is in unwantedRecommendations (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 -- hookyqr.beautify not found in unwantedRecommendations: {unwanted}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: No extraneous entries (0.2 points)
    # recommendations should only contain the 4 required ones; unwantedRecommendations should only contain hookyqr.beautify
    try:
        recommendations = data.get("recommendations", [])
        unwanted = data.get("unwantedRecommendations", [])
        extra_score = 0.0

        if isinstance(recommendations, list):
            recs_lower = set(r.lower() for r in recommendations if isinstance(r, str))
            expected_recs = set(r.lower() for r in REQUIRED_RECOMMENDATIONS)
            extra_recs = recs_lower - expected_recs
            if not extra_recs:
                extra_score += 0.1
                print(f"PASS: Component 4a -- No extra recommendations (0.1 pts)")
            else:
                print(f"FAIL: Component 4a -- Extra recommendations found: {extra_recs}")

        if isinstance(unwanted, list):
            unwanted_lower = set(u.lower() for u in unwanted if isinstance(u, str))
            expected_unwanted = set(u.lower() for u in REQUIRED_UNWANTED)
            extra_unwanted = unwanted_lower - expected_unwanted
            if not extra_unwanted:
                extra_score += 0.1
                print(f"PASS: Component 4b -- No extra unwanted recommendations (0.1 pts)")
            else:
                print(f"FAIL: Component 4b -- Extra unwanted recommendations found: {extra_unwanted}")

        if extra_score > 0:
            total_score += extra_score
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
