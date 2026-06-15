"""
Reward Script: Create .vscode/extensions.json with recommended and unwanted extensions
Task ID: vscode_ext_030
Domain: vs_code
Scoring:
  Component 1 (0.5): 'recommendations' array contains all 4 required extension IDs
  Component 2 (0.3): 'unwantedRecommendations' array contains all 2 required extension IDs
  Component 3 (0.2): Exact match — recommendations has exactly the 4 specified IDs,
                      unwantedRecommendations has exactly the 2 specified IDs (correct set, no extras)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_030'

EXTENSIONS_JSON_PATH = '/home/user/projects/fullstack/.vscode/extensions.json'

REQUIRED_RECOMMENDATIONS = [
    'ms-python.python',
    'dbaeumer.vscode-eslint',
    'esbenp.prettier-vscode',
    'ms-azuretools.vscode-docker',
]

REQUIRED_UNWANTED = [
    'hookyqr.beautify',
    'coenraads.bracket-pair-colorizer',
]


def load_extensions_json(file_path):
    """Load and parse extensions.json, stripping JSONC comments if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip JSONC comments (VSCode supports JSON with Comments)
    content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content_clean)


def verify_task(file_path):
    """
    Verify that .vscode/extensions.json contains both recommendations
    and unwantedRecommendations with the expected extension IDs.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: File must exist and be valid JSON
    if not os.path.exists(file_path):
        print(f"FAIL: extensions.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ext_config = load_extensions_json(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse extensions.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'recommendations' array contains all 4 required extensions (0.5 points)
    # This FAILS on initial_env (no file) and PASSES on golden_env (file with correct content)
    try:
        recommendations = ext_config.get('recommendations', None)
        if recommendations is None:
            print("FAIL: Component 1 — 'recommendations' key is missing from extensions.json")
        elif not isinstance(recommendations, list):
            print(f"FAIL: Component 1 — 'recommendations' is not a list, got: {type(recommendations).__name__}")
        else:
            # Normalize to lowercase for case-insensitive comparison
            recommendations_lower = [r.lower() for r in recommendations]
            missing_recs = [ext for ext in REQUIRED_RECOMMENDATIONS if ext.lower() not in recommendations_lower]
            if not missing_recs:
                print(f"PASS: Component 1 — All 4 required recommendations present: {recommendations}")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — Missing recommendations: {missing_recs}")
                print(f"      Found: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'unwantedRecommendations' array contains all 2 required entries (0.3 points)
    # This FAILS on initial_env (no file) and PASSES on golden_env (file with correct content)
    try:
        unwanted = ext_config.get('unwantedRecommendations', None)
        if unwanted is None:
            print("FAIL: Component 2 — 'unwantedRecommendations' key is missing from extensions.json")
        elif not isinstance(unwanted, list):
            print(f"FAIL: Component 2 — 'unwantedRecommendations' is not a list, got: {type(unwanted).__name__}")
        else:
            unwanted_lower = [u.lower() for u in unwanted]
            missing_unwanted = [ext for ext in REQUIRED_UNWANTED if ext.lower() not in unwanted_lower]
            if not missing_unwanted:
                print(f"PASS: Component 2 — All 2 required unwantedRecommendations present: {unwanted}")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Missing unwantedRecommendations: {missing_unwanted}")
                print(f"      Found: {unwanted}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The extension lists are exactly correct (no extra unwanted entries)
    # Verifies both arrays contain exactly the specified IDs (set equality), not just containment.
    # This FAILS on initial_env (no file) and PASSES on golden_env (exact match).
    try:
        recommendations = ext_config.get('recommendations', [])
        unwanted = ext_config.get('unwantedRecommendations', [])

        rec_set = set(r.lower() for r in recommendations)
        req_rec_set = set(r.lower() for r in REQUIRED_RECOMMENDATIONS)
        unwanted_set = set(u.lower() for u in unwanted)
        req_unwanted_set = set(u.lower() for u in REQUIRED_UNWANTED)

        rec_exact = (rec_set == req_rec_set)
        unwanted_exact = (unwanted_set == req_unwanted_set)

        if rec_exact and unwanted_exact:
            print(f"PASS: Component 3 — Both arrays are exact matches (no extra or missing entries)")
            total_score += 0.2
        else:
            if not rec_exact:
                extra_rec = rec_set - req_rec_set
                missing_rec = req_rec_set - rec_set
                if extra_rec:
                    print(f"FAIL: Component 3 — Extra recommendations not in spec: {extra_rec}")
                if missing_rec:
                    print(f"FAIL: Component 3 — Missing recommendations from spec: {missing_rec}")
            if not unwanted_exact:
                extra_unwanted = unwanted_set - req_unwanted_set
                missing_unwanted = req_unwanted_set - unwanted_set
                if extra_unwanted:
                    print(f"FAIL: Component 3 — Extra unwanted not in spec: {extra_unwanted}")
                if missing_unwanted:
                    print(f"FAIL: Component 3 — Missing unwanted from spec: {missing_unwanted}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = EXTENSIONS_JSON_PATH
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
