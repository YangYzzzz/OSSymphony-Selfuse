"""
Reward Script: Enable JavaScript type checking via jsconfig.json
Task ID: vscode_lp_006
Domain: vscode
Scoring:
  Component 1 (0.3 pts): jsconfig.json exists and is valid JSON with compilerOptions
  Component 2 (0.4 pts): checkJs is set to boolean true
  Component 3 (0.3 pts): target is set to "ES2020"
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_006'
JSCONFIG_PATH = os.path.join(WORKDIR, 'projects', 'js-app', 'jsconfig.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist
    if not os.path.exists(JSCONFIG_PATH):
        print(f"CRITICAL: jsconfig.json not found at {JSCONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: file must be valid JSON
    try:
        with open(JSCONFIG_PATH, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"CRITICAL: jsconfig.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: jsconfig.json has compilerOptions key (0.3 points)
    # This checks that the file was created with the correct top-level structure.
    # Fails on initial_env because the file does not exist at all (gate catches it).
    try:
        compiler_options = data.get('compilerOptions')
        if isinstance(compiler_options, dict):
            print(f"PASS: Component 1 - compilerOptions exists and is a dict (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - compilerOptions missing or not a dict, found: {compiler_options}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: checkJs is set to boolean true (0.4 points)
    # This is the core requirement - enabling JS type checking.
    try:
        compiler_options = data.get('compilerOptions', {})
        check_js = compiler_options.get('checkJs')
        if check_js is True:
            print(f"PASS: Component 2 - checkJs is true (boolean) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - checkJs expected true (bool), found: {check_js!r} (type: {type(check_js).__name__})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: target is set to "ES2020" (0.3 points)
    try:
        compiler_options = data.get('compilerOptions', {})
        target = compiler_options.get('target')
        if isinstance(target, str) and target.upper() == 'ES2020':
            print(f"PASS: Component 3 - target is '{target}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 - target expected 'ES2020', found: {target!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
