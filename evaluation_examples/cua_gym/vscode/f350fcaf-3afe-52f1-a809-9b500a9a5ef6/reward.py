"""
Reward Script: Swap route decorator parameters in routes.py
Task ID: vscode_edit_048
Domain: vs_code
Scoring:
  Component 1: At least one decorator has swapped parameters (methods first) — 0.3 pts
  Component 2: All 5 route decorators have swapped parameter order — 0.5 pts
  Component 3: Original path strings are preserved without corruption — 0.2 pts
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_048'

FILE_PATH = f'{WORKDIR}/Desktop/routes.py'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    The task: swap '@app.route("/path", methods=[...])' to '@app.route(methods=[...], "/path")'
    for all 5 route decorators in routes.py.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Regex patterns to find route decorators
    # Initial format: @app.route("path", methods=[...])
    # Golden format:  @app.route(methods=[...], "path")
    #
    # A swapped decorator: @app.route(methods=..., "path")
    # An original decorator: @app.route("path", methods=...)

    pattern_original = re.compile(r'@app\.route\(\s*["\'].*?["\'],\s*methods=')
    pattern_swapped = re.compile(r'@app\.route\(\s*methods=.*?,\s*["\'].*?["\']')

    original_matches = pattern_original.findall(content)
    swapped_matches = pattern_swapped.findall(content)

    print(f"INFO: Original-format decorators found: {len(original_matches)}")
    print(f"INFO: Swapped-format decorators found: {len(swapped_matches)}")

    # Component 1: At least one decorator has the swapped order (methods first) — 0.3 pts
    # This FAILS on initial (all decorators have original format) and PASSES on golden
    try:
        if len(swapped_matches) >= 1:
            print(f"PASS: Component 1 — at least 1 decorator has swapped parameter order (found {len(swapped_matches)}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — no decorators with swapped parameter order found (expected methods= first)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ALL 5 route decorators have swapped parameter order — 0.5 pts
    # This FAILS on initial (0 swapped, 5 original) and PASSES on golden (5 swapped, 0 original)
    try:
        # The expected routes are:
        # /api/tasks (GET), /api/tasks/<int:task_id> (POST),
        # /api/tasks/<int:task_id>/update (PUT), /api/tasks/<int:task_id>/delete (DELETE),
        # /api/users/register (POST) — 5 total
        total_decorators_swapped = len(swapped_matches)
        total_decorators_original = len(original_matches)

        if total_decorators_swapped == 5 and total_decorators_original == 0:
            print(f"PASS: Component 2 — all 5 route decorators have swapped parameter order (0.5 pts)")
            total_score += 0.5
        elif total_decorators_swapped > 0 and total_decorators_original == 0:
            print(f"FAIL: Component 2 — {total_decorators_swapped}/5 decorators swapped, but expected exactly 5")
        elif total_decorators_swapped == 5 and total_decorators_original > 0:
            print(f"FAIL: Component 2 — found 5 swapped but also {total_decorators_original} un-swapped (expected 0 un-swapped)")
        else:
            print(f"FAIL: Component 2 — only {total_decorators_swapped}/5 decorators have swapped order; {total_decorators_original} still in original format")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Original path strings are preserved — 0.2 pts
    # Check that all 5 expected paths are still present in the file (no data loss)
    # This checks swapped decorators still contain correct paths.
    # Note: this ALONE would pass on initial too (paths exist), so we gate it on Component 2.
    try:
        expected_paths = [
            '"/api/tasks"',
            '"/api/tasks/<int:task_id>"',
            '"/api/tasks/<int:task_id>/update"',
            '"/api/tasks/<int:task_id>/delete"',
            '"/api/users/register"',
        ]
        paths_present = all(path in content for path in expected_paths)

        # Gate: only award if decorators are swapped (task was actually attempted)
        # Verify paths appear in the context of swapped decorators
        if len(swapped_matches) >= 1 and paths_present:
            # Further check: count how many paths appear in swapped decorator context
            paths_in_swapped_count = sum(
                1 for path in expected_paths
                if re.search(
                    r'@app\.route\(\s*methods=.*?' + re.escape(path),
                    content,
                    re.DOTALL
                )
            )
            missing_count = len(expected_paths) - paths_in_swapped_count
            if missing_count > 0:
                print(f"FAIL: Component 3 — {missing_count} path(s) missing from swapped-format decorators")
            if missing_count == 0:
                print(f"PASS: Component 3 — all 5 original path strings present in swapped decorators (0.2 pts)")
                total_score += 0.2
        elif not paths_present:
            print(f"FAIL: Component 3 — some expected path strings are missing from the file")
        else:
            print(f"FAIL: Component 3 — no swapped decorators found, paths exist but task not completed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
