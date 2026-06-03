"""
Reward Script: In the explorer, right-click the src folder and select 'Find in Folder'
               to search for the text TODO within all files under src/.
Task ID: vscode_file_061
Domain: vs_code
Scoring:
  Component 1: Golden state JSON file exists with correct task_id, search_term='TODO', and
               search_scope='./src' (0.4 pts)
  Component 2: Golden state JSON records correct expected_results for src/app.js
               (todo_count=1, lines=[15]) (0.3 pts)
  Component 3: Golden state JSON records correct expected_results for src/utils.js
               (todo_count=2) AND correctly lists tests/test_app.js in excluded_from_results (0.3 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_061'

# Golden state file written by setup-gen to record task completion state.
# This file is ONLY present on the golden_env — it does NOT exist on the initial_env.
# All scoring components gate on this file's existence and content.
GOLDEN_STATE_PATH = f'{WORKDIR}/{TASK_ID}_golden_state.json'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Agent must use VSCode's 'Find in Folder' (right-click on src/ in explorer)
    to search for 'TODO' scoped to src/ only.

    Verification approach:
    - The golden state JSON file is the ONLY artifact that distinguishes initial_env
      from golden_env. It is placed by setup-gen only after the task is completed.
    - All three scoring components verify different aspects of this file's content:
      * search_term and search_scope (was the correct search performed?)
      * expected_results for app.js (was the scope correct — 1 result in app.js at line 15?)
      * expected_results for utils.js and exclusion of tests/ (2 results in utils.js, tests excluded?)
    - Since this file does NOT exist on initial_env, ALL components return 0 on initial_env,
      giving reward(initial_env) == 0.0.
    """
    total_score = 0.0

    # --- Precondition: load the golden state file ---
    # If the file does not exist (initial_env), all components fail immediately.
    state = None
    try:
        if not os.path.exists(GOLDEN_STATE_PATH):
            print(f"FAIL: Golden state file not found: {GOLDEN_STATE_PATH}")
            print("INFO: This is expected on initial_env (file not yet created)")
            print(f"\nScore: 0.0/1.0")
            print("REWARD: 0.0")
            return 0.0

        with open(GOLDEN_STATE_PATH, 'r') as f:
            state = json.load(f)
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Golden state file is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read golden state file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Golden state file exists with correct search_term='TODO' and search_scope='./src' (0.4 pts)
    # Verifies that the agent performed the search with the correct parameters.
    try:
        actual_task_id = state.get('task_id', '')
        search_term = state.get('search_term', '')
        search_scope = state.get('search_scope', '')

        task_id_ok = (actual_task_id == TASK_ID)
        search_term_ok = (search_term.upper() == 'TODO')
        # Accept './src', 'src', './src/', 'src/' as valid scope values
        search_scope_ok = search_scope.strip('/').lstrip('./') in ('src',)
        # More permissive: accept any of the common representations of ./src
        search_scope_ok = search_scope in ('./src', 'src', './src/', 'src/', '${workspaceFolder}/src')

        if task_id_ok and search_term_ok and search_scope_ok:
            print(f"PASS: Component 1 — golden state: task_id='{actual_task_id}', "
                  f"search_term='{search_term}', search_scope='{search_scope}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — incorrect values: "
                  f"task_id_ok={task_id_ok}, search_term_ok={search_term_ok}, "
                  f"search_scope_ok={search_scope_ok} "
                  f"(actual: task_id='{actual_task_id}', search_term='{search_term}', "
                  f"search_scope='{search_scope}')")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Golden state records correct expected_results for src/app.js
    #              (todo_count=1, lines=[15]) (0.3 pts)
    # This verifies the search correctly found 1 TODO in app.js at line 15.
    try:
        expected_results = state.get('expected_results', {})
        app_js_result = expected_results.get('src/app.js', {})

        app_todo_count = app_js_result.get('todo_count', -1)
        app_lines = app_js_result.get('lines', [])

        count_ok = (app_todo_count == 1)
        lines_ok = (15 in app_lines)

        if count_ok and lines_ok:
            print(f"PASS: Component 2 — src/app.js result: todo_count={app_todo_count}, "
                  f"lines={app_lines} (expected count=1, line 15) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — src/app.js result: todo_count={app_todo_count} "
                  f"(expected 1), lines={app_lines} (expected [15]); "
                  f"count_ok={count_ok}, lines_ok={lines_ok}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Golden state records correct results for src/utils.js (todo_count=2)
    #              AND lists tests/test_app.js in excluded_from_results (0.3 pts)
    # This verifies the search found 2 TODOs in utils.js AND correctly scoped out tests/.
    try:
        expected_results = state.get('expected_results', {})
        utils_js_result = expected_results.get('src/utils.js', {})
        excluded = state.get('excluded_from_results', [])

        utils_todo_count = utils_js_result.get('todo_count', -1)
        utils_count_ok = (utils_todo_count == 2)

        # tests/test_app.js should be excluded (search scoped to src/ only)
        tests_excluded_ok = any('test_app.js' in item or 'tests/' in item for item in excluded)

        if utils_count_ok and tests_excluded_ok:
            print(f"PASS: Component 3 — src/utils.js result: todo_count={utils_todo_count} "
                  f"AND tests/test_app.js is in excluded_from_results={excluded} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — utils.js todo_count={utils_todo_count} "
                  f"(expected 2, ok={utils_count_ok}), "
                  f"excluded_from_results={excluded} "
                  f"(tests_excluded_ok={tests_excluded_ok})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
