"""
Reward Script: SQL stored procedure and pgTAP testing workflow in VSCode
Task ID: vscode_gf3_082
Domain: vscode
Scoring:
  Component 1 (0.20): calculate_order_total.sql exists and defines a CREATE FUNCTION
  Component 2 (0.25): Function signature — name, INTEGER param, RETURNS NUMERIC(10,2), plpgsql
  Component 3 (0.20): Function body references order_line_items, promotions, and tax logic
  Component 4 (0.15): test_order_total.sql exists with pgTAP test structure
  Component 5 (0.20): .vscode/tasks.json with pg_prove task
"""

import os
import re
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_082'

PROC_PATH = os.path.join(WORKDIR, 'projects', 'backend', 'db', 'procedures', 'calculate_order_total.sql')
TEST_PATH = os.path.join(WORKDIR, 'projects', 'backend', 'db', 'tests', 'test_order_total.sql')
TASKS_PATH = os.path.join(WORKDIR, 'projects', 'backend', '.vscode', 'tasks.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ----------------------------------------------------------------
    # Component 1: calculate_order_total.sql exists and contains CREATE FUNCTION (0.20 pts)
    # ----------------------------------------------------------------
    proc_content = None
    try:
        if os.path.isfile(PROC_PATH):
            with open(PROC_PATH, 'r') as f:
                proc_content = f.read()
            if re.search(r'CREATE\s+(OR\s+REPLACE\s+)?FUNCTION', proc_content, re.IGNORECASE):
                print(f"PASS: Component 1 — {PROC_PATH} exists and contains CREATE FUNCTION (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — file exists but no CREATE FUNCTION statement found")
        else:
            print(f"FAIL: Component 1 — {PROC_PATH} does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Function signature correctness (0.25 pts)
    #   - function named calculate_order_total
    #   - takes INTEGER parameter
    #   - returns NUMERIC(10,2)
    #   - language plpgsql
    # ----------------------------------------------------------------
    try:
        if proc_content:
            sub_score = 0.0
            checks_passed = 0
            total_checks = 4

            # Check function name
            if re.search(r'FUNCTION\s+calculate_order_total', proc_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 2a — function name 'calculate_order_total' not found")

            # Check INTEGER parameter
            if re.search(r'calculate_order_total\s*\([^)]*INTEGER', proc_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 2b — INTEGER parameter not found in function signature")

            # Check RETURNS NUMERIC(10,2)
            if re.search(r'RETURNS\s+NUMERIC\s*\(\s*10\s*,\s*2\s*\)', proc_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 2c — RETURNS NUMERIC(10,2) not found")

            # Check LANGUAGE plpgsql
            if re.search(r'LANGUAGE\s+plpgsql', proc_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 2d — LANGUAGE plpgsql not found")

            if checks_passed == total_checks:
                total_score += 0.25
                print(f"PASS: Component 2 — all 4 signature checks passed (0.25 pts)")
            elif checks_passed > 0:
                partial = round(0.25 * checks_passed / total_checks, 2)
                total_score += partial
                print(f"PARTIAL: Component 2 — {checks_passed}/{total_checks} signature checks passed ({partial} pts)")
        else:
            print(f"FAIL: Component 2 — no procedure file to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Function body references key tables and logic (0.20 pts)
    #   - references order_line_items table
    #   - references promotions table
    #   - has tax/discount logic (mentions discount and tax)
    # ----------------------------------------------------------------
    try:
        if proc_content:
            checks_passed = 0
            total_checks = 3

            # Check order_line_items reference
            if re.search(r'order_line_items', proc_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 3a — no reference to order_line_items table")

            # Check promotions reference
            if re.search(r'promotions', proc_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 3b — no reference to promotions table")

            # Check tax/discount logic
            if re.search(r'(tax|discount)', proc_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 3c — no tax/discount logic found")

            if checks_passed == total_checks:
                total_score += 0.20
                print(f"PASS: Component 3 — all 3 body checks passed (0.20 pts)")
            elif checks_passed > 0:
                partial = round(0.20 * checks_passed / total_checks, 2)
                total_score += partial
                print(f"PARTIAL: Component 3 — {checks_passed}/{total_checks} body checks passed ({partial} pts)")
        else:
            print(f"FAIL: Component 3 — no procedure file to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: test_order_total.sql with pgTAP structure (0.15 pts)
    #   - file exists
    #   - uses pgTAP functions (plan, has_function or is)
    #   - calls calculate_order_total
    # ----------------------------------------------------------------
    try:
        if os.path.isfile(TEST_PATH):
            with open(TEST_PATH, 'r') as f:
                test_content = f.read()

            checks_passed = 0
            total_checks = 3

            # Check pgTAP plan()
            if re.search(r'SELECT\s+plan\s*\(', test_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 4a — no SELECT plan() found (pgTAP)")

            # Check pgTAP assertion functions (is, has_function, ok, etc.)
            if re.search(r'SELECT\s+(is|has_function|ok|isnt|matches)\s*\(', test_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 4b — no pgTAP assertion functions found")

            # Check that it calls calculate_order_total
            if re.search(r'calculate_order_total', test_content, re.IGNORECASE):
                checks_passed += 1
            else:
                print(f"FAIL: Component 4c — does not call calculate_order_total")

            if checks_passed == total_checks:
                total_score += 0.15
                print(f"PASS: Component 4 — all 3 test file checks passed (0.15 pts)")
            elif checks_passed > 0:
                partial = round(0.15 * checks_passed / total_checks, 2)
                total_score += partial
                print(f"PARTIAL: Component 4 — {checks_passed}/{total_checks} test checks passed ({partial} pts)")
        else:
            print(f"FAIL: Component 4 — {TEST_PATH} does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: .vscode/tasks.json with pg_prove task (0.20 pts)
    #   - file exists and is valid JSON
    #   - has a task with pg_prove command
    # ----------------------------------------------------------------
    try:
        if os.path.isfile(TASKS_PATH):
            with open(TASKS_PATH, 'r') as f:
                tasks_data = json.load(f)

            checks_passed = 0
            total_checks = 2

            # Check tasks array exists
            tasks_list = tasks_data.get('tasks', [])
            if isinstance(tasks_list, list) and len(tasks_list) > 0:
                checks_passed += 1
            else:
                print(f"FAIL: Component 5a — tasks.json has no tasks array or it is empty")

            # Check at least one task references pg_prove (in command or args)
            found_pgprove = False
            for task in tasks_list:
                task_str = json.dumps(task).lower()
                if 'pg_prove' in task_str or 'pgprove' in task_str:
                    found_pgprove = True
                    break
            if found_pgprove:
                checks_passed += 1
            else:
                print(f"FAIL: Component 5b — no task references pg_prove")

            if checks_passed == total_checks:
                total_score += 0.20
                print(f"PASS: Component 5 — tasks.json valid with pg_prove task (0.20 pts)")
            elif checks_passed > 0:
                partial = round(0.20 * checks_passed / total_checks, 2)
                total_score += partial
                print(f"PARTIAL: Component 5 — {checks_passed}/{total_checks} tasks.json checks passed ({partial} pts)")
        else:
            print(f"FAIL: Component 5 — {TASKS_PATH} does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
