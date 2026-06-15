"""
Reward Script: Identify the branch that introduced the regression in parse_data()
Task ID: vscode_git_074
Domain: vs_code (git/branch analysis)
Scoring:
  - Component 1: Answer file exists with non-empty content at /home/user/vscode_git_074.txt (0.3 pts)
  - Component 2: Answer correctly identifies 'feature/v2-parser' as the branch with regression (0.7 pts)
Total: 1.0

Context:
  The parse_data() function's return type was changed from List[Dict[str, Any]] to Dict[str, Any]
  in the SECOND commit of feature/v2-parser (the "refactor parse_data() to return metadata dict"
  commit). This is the regression. The agent must identify 'feature/v2-parser' as the branch.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_074'

EXPECTED_BRANCH = 'feature/v2-parser'
ANSWER_FILE = os.path.join(WORKDIR, f'{TASK_ID}.txt')


def verify_task():
    """
    Verify that the agent correctly identified the branch that introduced
    the regression in parse_data(). The agent should write the branch name
    to /home/user/vscode_git_074.txt.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Answer file exists with non-empty content (0.3 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        file_exists = os.path.exists(ANSWER_FILE)
        file_non_empty = file_exists and os.path.getsize(ANSWER_FILE) > 0

        if file_exists and file_non_empty:
            print(f"PASS: Component 1 — answer file found at {ANSWER_FILE} (0.3 pts)")
            total_score += 0.3
        elif not file_exists:
            print(f"FAIL: Component 1 — answer file not found at {ANSWER_FILE}")
        else:
            print(f"FAIL: Component 1 — answer file exists but is empty: {ANSWER_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — could not check answer file: {e}")

    # Component 2: Answer correctly identifies 'feature/v2-parser' as the branch (0.7 points)
    # The regression was introduced in the second commit of feature/v2-parser:
    # "feature/v2-parser: refactor parse_data() to return metadata dict with records and count"
    # This commit changed the return type from List[Dict[str, Any]] to Dict[str, Any].
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        if not os.path.exists(ANSWER_FILE):
            print(f"FAIL: Component 2 — answer file not found, cannot verify branch name")
        else:
            with open(ANSWER_FILE, 'r', encoding='utf-8') as f:
                answer_raw = f.read()

            # Normalize the answer: strip whitespace and common surrounding punctuation
            answer = answer_raw.strip().strip('"\'').strip()

            # Check for exact match (branch names are case-sensitive in git)
            if answer == EXPECTED_BRANCH:
                print(f"PASS: Component 2 — correct branch identified: '{answer}' (0.7 pts)")
                total_score += 0.7
            elif answer.lower() == EXPECTED_BRANCH.lower():
                # Accept case-insensitive match with partial credit
                print(f"PASS: Component 2 — correct branch identified (case-insensitive): '{answer}' (0.7 pts)")
                total_score += 0.7
            else:
                print(f"FAIL: Component 2 — expected '{EXPECTED_BRANCH}', found '{answer}'")
    except Exception as e:
        print(f"ERROR: Component 2 — could not verify branch name: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
