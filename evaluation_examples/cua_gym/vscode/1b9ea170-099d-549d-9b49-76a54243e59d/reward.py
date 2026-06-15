"""
Reward Script: Configure ESLint to enforce React Hooks rules
Task ID: vscode_web_073
Domain: vs_code
Scoring:
  Component 1: 'react-hooks' in plugins array (0.3 pts)
  Component 2: react-hooks/rules-of-hooks set to 'error' (0.35 pts)
  Component 3: react-hooks/exhaustive-deps set to 'warn' (0.35 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_073'
ESLINTRC_PATH = os.path.join(WORKDIR, 'projects', 'react-app', '.eslintrc.json')


def load_eslintrc(file_path):
    """Load .eslintrc.json, handling possible JSONC comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task(file_path):
    """
    Verify ESLint React Hooks configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        config = load_eslintrc(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: .eslintrc.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse .eslintrc.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'react-hooks' in plugins array (0.3 points)
    # Initial state has plugins: ["react"] only — no react-hooks
    # Golden state should have "react-hooks" in plugins
    try:
        plugins = config.get('plugins', [])
        if isinstance(plugins, list) and 'react-hooks' in plugins:
            print(f"PASS: Component 1 - 'react-hooks' found in plugins: {plugins} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - 'react-hooks' not in plugins: {plugins}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: react-hooks/rules-of-hooks set to 'error' (0.35 points)
    # Initial state has no react-hooks rules at all
    # Golden state should have "react-hooks/rules-of-hooks": "error"
    try:
        rules = config.get('rules', {})
        roh_value = rules.get('react-hooks/rules-of-hooks')
        if roh_value == 'error' or roh_value == 2:
            print(f"PASS: Component 2 - react-hooks/rules-of-hooks = '{roh_value}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 - react-hooks/rules-of-hooks = '{roh_value}', expected 'error' or 2")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: react-hooks/exhaustive-deps set to 'warn' (0.35 points)
    # Initial state has no react-hooks rules at all
    # Golden state should have "react-hooks/exhaustive-deps": "warn"
    try:
        rules = config.get('rules', {})
        ed_value = rules.get('react-hooks/exhaustive-deps')
        if ed_value == 'warn' or ed_value == 1:
            print(f"PASS: Component 3 - react-hooks/exhaustive-deps = '{ed_value}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 - react-hooks/exhaustive-deps = '{ed_value}', expected 'warn' or 1")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(ESLINTRC_PATH):
    print(f"File not found: {ESLINTRC_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(ESLINTRC_PATH)
