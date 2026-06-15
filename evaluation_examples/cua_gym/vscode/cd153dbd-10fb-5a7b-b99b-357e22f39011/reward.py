"""
Reward Script: Resolve merge conflict in app.py by accepting both changes
Task ID: vscode_stu_061
Domain: vscode
Scoring:
  Component 1 (0.30): No conflict markers remain in app.py
  Component 2 (0.30): create_task includes both 'description' and 'priority' fields (without conflict markers)
  Component 3 (0.20): update_task (PUT) route is present (without conflict markers)
  Component 4 (0.20): delete_task (DELETE) route is present (without conflict markers)

All components gate on conflict markers being absent first, ensuring initial_env scores 0.0.
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_061'
FILE_PATH = os.path.join(WORKDIR, 'workspace', 'app.py')

CONFLICT_MARKERS = ['<<<<<<< ', '>>>>>>> ']


def verify_task(file_path):
    """
    Verify merge conflict resolution with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Pre-check: are conflict markers present?
    has_conflict_markers = any(marker in content for marker in CONFLICT_MARKERS)

    # Component 1: No conflict markers remain (0.30 points)
    # In initial_env, conflict markers ARE present -> FAIL
    # In golden_env, conflict markers are removed -> PASS
    try:
        if not has_conflict_markers:
            print(f"PASS: Component 1 — no conflict markers found (0.30 pts)")
            total_score += 0.30
        else:
            found = [m.strip() for m in CONFLICT_MARKERS if m in content]
            print(f"FAIL: Component 1 — conflict markers still present: {found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: create_task has both 'description' AND 'priority' fields,
    # AND no conflict markers (0.30 points)
    # In initial_env: has conflict markers -> gated out -> FAIL
    # In golden_env: both fields present cleanly -> PASS
    try:
        if has_conflict_markers:
            print(f"FAIL: Component 2 — conflict markers present, cannot verify cleanly")
        else:
            has_description = bool(re.search(
                r'["\']description["\']\s*:\s*data\.get\(\s*["\']description["\']',
                content
            ))
            has_priority = bool(re.search(
                r'["\']priority["\']\s*:\s*data\.get\(\s*["\']priority["\']',
                content
            ))

            if has_description and has_priority:
                print(f"PASS: Component 2 — both 'description' and 'priority' fields present in create_task (0.30 pts)")
                total_score += 0.30
            else:
                missing = []
                if not has_description:
                    missing.append("description")
                if not has_priority:
                    missing.append("priority")
                print(f"FAIL: Component 2 — missing field(s) in create_task: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: update_task (PUT) route exists AND no conflict markers (0.20 points)
    # In initial_env: gated out by conflict markers -> FAIL
    # In golden_env: route present cleanly -> PASS
    try:
        if has_conflict_markers:
            print(f"FAIL: Component 3 — conflict markers present, cannot verify cleanly")
        else:
            has_update_route = bool(re.search(
                r'@app\.route\(\s*["\']/tasks/<int:task_id>["\']\s*,\s*methods=\[.*?["\']PUT["\'].*?\]\s*\)',
                content
            ))
            has_update_func = bool(re.search(
                r'def\s+update_task\s*\(\s*task_id\s*\)',
                content
            ))

            if has_update_route and has_update_func:
                print(f"PASS: Component 3 — update_task PUT route present (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — update_task PUT route missing (route={has_update_route}, func={has_update_func})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: delete_task (DELETE) route exists AND no conflict markers (0.20 points)
    # In initial_env: gated out by conflict markers -> FAIL
    # In golden_env: route present cleanly -> PASS
    try:
        if has_conflict_markers:
            print(f"FAIL: Component 4 — conflict markers present, cannot verify cleanly")
        else:
            has_delete_route = bool(re.search(
                r'@app\.route\(\s*["\']/tasks/<int:task_id>["\']\s*,\s*methods=\[.*?["\']DELETE["\'].*?\]\s*\)',
                content
            ))
            has_delete_func = bool(re.search(
                r'def\s+delete_task\s*\(\s*task_id\s*\)',
                content
            ))

            if has_delete_route and has_delete_func:
                print(f"PASS: Component 4 — delete_task DELETE route present (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — delete_task DELETE route missing (route={has_delete_route}, func={has_delete_func})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
