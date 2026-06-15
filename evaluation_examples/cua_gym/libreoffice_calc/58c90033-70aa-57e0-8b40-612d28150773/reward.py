"""
Reward Script: Create .vscode/extensions.json with recommendations and unwanted extensions
Task ID: vscode_we_059
Domain: vs-code (file-based)
Scoring:
  Component 1 (0.15): File exists and is valid JSON with correct top-level keys
  Component 2 (0.40): recommendations array contains all 4 required extensions
  Component 3 (0.30): unwantedRecommendations array contains all 2 required extensions
  Component 4 (0.15): No extra/unexpected entries in either array (exact match)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_059'
TARGET_FILE = os.path.join(WORKDIR, 'projects', 'react-ts', '.vscode', 'extensions.json')

EXPECTED_RECOMMENDATIONS = [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "dsznajder.es7-react-js-snippets",
]

EXPECTED_UNWANTED = [
    "hookyqr.beautify",
    "ms-vscode.vscode-typescript-tslint-plugin",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(TARGET_FILE):
        print(f"CRITICAL: File not found: {TARGET_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be valid JSON
    try:
        with open(TARGET_FILE, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse JSON from {TARGET_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(data, dict):
        print(f"CRITICAL: Expected JSON object, got {type(data).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has both required top-level keys (0.15 points)
    # This is task-introduced: initial_env has no .vscode dir at all
    try:
        has_recommendations = "recommendations" in data
        has_unwanted = "unwantedRecommendations" in data
        if has_recommendations and has_unwanted:
            print(f"PASS: Component 1 -- Both 'recommendations' and 'unwantedRecommendations' keys present (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_recommendations:
                missing.append("recommendations")
            if not has_unwanted:
                missing.append("unwantedRecommendations")
            print(f"FAIL: Component 1 -- Missing keys: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: recommendations array contains all 4 required extensions (0.40 points)
    # Partial credit: 0.10 per extension found
    try:
        recs = data.get("recommendations", [])
        if not isinstance(recs, list):
            print(f"FAIL: Component 2 -- 'recommendations' is not a list, got {type(recs).__name__}")
        else:
            # Case-insensitive comparison for extension IDs
            recs_lower = [r.lower().strip() for r in recs if isinstance(r, str)]
            found_count = 0
            for ext in EXPECTED_RECOMMENDATIONS:
                if ext.lower() in recs_lower:
                    found_count += 1
                    print(f"  FOUND recommendation: {ext}")
                else:
                    print(f"  MISSING recommendation: {ext}")
            comp2_score = found_count * 0.10
            if comp2_score > 0:
                total_score += comp2_score
            if found_count == len(EXPECTED_RECOMMENDATIONS):
                print(f"PASS: Component 2 -- All {found_count} recommendations found ({comp2_score} pts)")
            else:
                print(f"PARTIAL: Component 2 -- {found_count}/{len(EXPECTED_RECOMMENDATIONS)} recommendations found ({comp2_score} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: unwantedRecommendations array contains all 2 required extensions (0.30 points)
    # Partial credit: 0.15 per extension found
    try:
        unwanted = data.get("unwantedRecommendations", [])
        if not isinstance(unwanted, list):
            print(f"FAIL: Component 3 -- 'unwantedRecommendations' is not a list, got {type(unwanted).__name__}")
        else:
            unwanted_lower = [u.lower().strip() for u in unwanted if isinstance(u, str)]
            found_count = 0
            for ext in EXPECTED_UNWANTED:
                if ext.lower() in unwanted_lower:
                    found_count += 1
                    print(f"  FOUND unwanted: {ext}")
                else:
                    print(f"  MISSING unwanted: {ext}")
            comp3_score = found_count * 0.15
            if comp3_score > 0:
                total_score += comp3_score
            if found_count == len(EXPECTED_UNWANTED):
                print(f"PASS: Component 3 -- All {found_count} unwanted recommendations found ({comp3_score} pts)")
            else:
                print(f"PARTIAL: Component 3 -- {found_count}/{len(EXPECTED_UNWANTED)} unwanted recommendations found ({comp3_score} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: No extra entries in either array (0.15 points)
    # Exact match on both arrays (order-independent)
    try:
        recs = data.get("recommendations", [])
        unwanted = data.get("unwantedRecommendations", [])
        recs_lower = set(r.lower().strip() for r in recs if isinstance(r, str))
        unwanted_lower = set(u.lower().strip() for u in unwanted if isinstance(u, str))
        expected_recs_lower = set(e.lower() for e in EXPECTED_RECOMMENDATIONS)
        expected_unwanted_lower = set(e.lower() for e in EXPECTED_UNWANTED)

        extra_recs = recs_lower - expected_recs_lower
        extra_unwanted = unwanted_lower - expected_unwanted_lower

        if not extra_recs and not extra_unwanted:
            print(f"PASS: Component 4 -- No extra entries in either array (0.15 pts)")
            total_score += 0.15
        else:
            if extra_recs:
                print(f"FAIL: Component 4 -- Extra recommendations: {extra_recs}")
            if extra_unwanted:
                print(f"FAIL: Component 4 -- Extra unwanted: {extra_unwanted}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
