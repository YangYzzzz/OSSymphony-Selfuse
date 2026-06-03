"""
Reward Script: Add a function breakpoint for 'processOrder' in VSCode
Task ID: vscode_dbg_045
Domain: vs_code
Scoring:
  - Component 1: A debug.breakpoint entry exists in any VSCode workspace storage (0.4 pts)
  - Component 2: The breakpoint targets function 'processOrder' (0.4 pts)
  - Component 3: The breakpoint is enabled (0.2 pts)
"""

import os
import json
import sqlite3
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_045'
VSCODE_WS_STORAGE = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage')


def find_all_breakpoints():
    """
    Search all VSCode workspace storage SQLite databases for the 'debug.breakpoint' key.
    Returns a list of all breakpoint entries found across all workspace databases.
    """
    all_breakpoints = []
    dbs = glob.glob(os.path.join(VSCODE_WS_STORAGE, '*', 'state.vscdb'))
    for db_path in dbs:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'debug.breakpoint'")
            row = cursor.fetchone()
            conn.close()
            if row:
                parsed = json.loads(row[0])
                if isinstance(parsed, list):
                    all_breakpoints.extend(parsed)
                    print(f"INFO: Found debug.breakpoint in {db_path}: {row[0][:200]}")
        except Exception as e:
            print(f"WARN: Could not read {db_path}: {e}")
    return all_breakpoints


def verify_task():
    """
    Verify that a VSCode function breakpoint for 'processOrder' has been added.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: debug.breakpoint key exists in any workspace storage (0.4 points)
    # This key is absent in the initial env and present only after the breakpoint is set.
    try:
        all_breakpoints = find_all_breakpoints()
        if len(all_breakpoints) > 0:
            print(f"PASS: Component 1 — debug.breakpoint entries found: {len(all_breakpoints)} (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — No debug.breakpoint entries found in any workspace storage")
            # No breakpoints at all; remaining components also fail
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: At least one breakpoint has functionName == 'processOrder' (0.4 points)
    # This verifies the correct function was targeted, not just any function breakpoint.
    try:
        func_bp_found = False
        for bp in all_breakpoints:
            if isinstance(bp, dict) and bp.get('functionName') == 'processOrder':
                func_bp_found = True
                print(f"PASS: Component 2 — Function breakpoint for 'processOrder' found: {bp} (0.4 pts)")
                total_score += 0.4
                break
        if not func_bp_found:
            func_names = [bp.get('functionName') for bp in all_breakpoints if isinstance(bp, dict)]
            print(f"FAIL: Component 2 — No function breakpoint for 'processOrder'. Found functionNames: {func_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The 'processOrder' breakpoint is enabled (0.2 points)
    # Ensures the breakpoint is active and will trigger when the function is entered.
    try:
        enabled_found = False
        for bp in all_breakpoints:
            if isinstance(bp, dict) and bp.get('functionName') == 'processOrder':
                if bp.get('enabled') is True:
                    enabled_found = True
                    print(f"PASS: Component 3 — processOrder breakpoint is enabled (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — processOrder breakpoint is not enabled. enabled={bp.get('enabled')}")
                break
        if not enabled_found and total_score >= 0.4:
            # We found the function name but not the enabled state — check already done above
            pass
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
