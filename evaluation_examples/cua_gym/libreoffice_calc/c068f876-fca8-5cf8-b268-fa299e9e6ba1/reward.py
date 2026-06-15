"""
Reward Script: Fix Python database migration script to check for column existence before ALTER TABLE
Task ID: osworld_multi_apps_vscode_debug_crash_010
Domain: multi_apps (VSCode + Python/SQLite)
Scoring:
  Component 1 (0.4 pts): migrate.py contains a column-existence check (PRAGMA table_info or equivalent)
  Component 2 (0.3 pts): run_migration guards the ALTER TABLE with the column-existence check
  Component 3 (0.3 pts): Running the migration twice does NOT raise OperationalError (idempotent)
"""

import os
import re
import sys
import sqlite3
import shutil
import tempfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_debug_crash_010'
MIGRATE_PY = os.path.join(WORKDIR, 'Desktop', 'db_migrate', 'migrate.py')
TEST_DB = os.path.join(WORKDIR, 'Desktop', 'test.db')


def has_column_existence_check(code):
    """
    Return True if migrate.py code contains a column-existence check.
    Accepted patterns:
      - PRAGMA table_info(<table>)
      - querying sqlite_master for column names
      - row['name'] == 'loyalty_tier' pattern
    """
    if re.search(r'PRAGMA\s+table_info\s*\(', code, re.IGNORECASE):
        return True
    if re.search(r'sqlite_master.*column|column.*sqlite_master', code, re.IGNORECASE):
        return True
    if re.search(r"row\[.name.\]\s*==\s*['\"]loyalty_tier['\"]", code):
        return True
    return False


def has_guarded_alter(code):
    """
    Return True if the ALTER TABLE (V2_ALTER) execution is guarded by
    a conditional check in the surrounding code.
    """
    lines = code.split('\n')
    alter_lines = [i for i, l in enumerate(lines) if 'V2_ALTER' in l or 'ADD COLUMN' in l.upper()]
    for alter_idx in alter_lines:
        context_start = max(0, alter_idx - 5)
        context = '\n'.join(lines[context_start:alter_idx + 1])
        if re.search(r'\bif\b', context):
            return True
    return False


def run_idempotency_test(project_dir, test_db_path):
    """
    Run the migration twice against a fresh DB copy.
    Returns (success: bool, message: str).
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_db = os.path.join(tmpdir, 'test_copy.db')
            shutil.copy2(test_db_path, tmp_db)

            # Add project directory to Python path for imports
            if project_dir not in sys.path:
                sys.path.insert(0, project_dir)

            # Force fresh import of migration modules
            for mod in ('migrate', 'schema', 'db'):
                if mod in sys.modules:
                    del sys.modules[mod]

            import migrate as migrate_mod

            # First run — get initial state
            migrate_mod.run_migration(tmp_db)
            print("  Idempotency: first run succeeded.")

            # Second run — must NOT raise OperationalError
            migrate_mod.run_migration(tmp_db)
            return True, "second run completed without OperationalError"

    except sqlite3.OperationalError as oe:
        return False, f"second run raised sqlite3.OperationalError: {oe}"
    except Exception as e:
        return False, f"unexpected error during idempotency test: {e}"


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: migrate.py must exist ---
    if not os.path.exists(MIGRATE_PY):
        print(f"CRITICAL: migrate.py not found at {MIGRATE_PY}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(MIGRATE_PY, 'r') as f:
            migrate_code = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read migrate.py: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: migrate.py contains a column-existence check using PRAGMA
    #              table_info or equivalent SQL introspection (0.4 points)
    # -----------------------------------------------------------------------
    try:
        check_present = has_column_existence_check(migrate_code)
        if check_present:
            print("PASS: Component 1 — column-existence check found in migrate.py "
                  "(PRAGMA table_info or equivalent) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — no column-existence check found in migrate.py")
            print("      Expected: PRAGMA table_info(...) or similar SQL column introspection")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: The ALTER TABLE statement is guarded by the column-existence
    #              check (not executed unconditionally) (0.3 points)
    # -----------------------------------------------------------------------
    try:
        alter_guarded = has_guarded_alter(migrate_code)
        if alter_guarded:
            print("PASS: Component 2 — ALTER TABLE execution is guarded by a conditional check (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 2 — ALTER TABLE is executed unconditionally (no 'if' guard near V2_ALTER)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Idempotency test — running the migration twice on the same
    #              database does NOT raise sqlite3.OperationalError (0.3 points)
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(TEST_DB):
            print(f"FAIL: Component 3 — test.db not found at {TEST_DB}")
        else:
            project_dir = os.path.join(WORKDIR, 'Desktop', 'db_migrate')
            success, message = run_idempotency_test(project_dir, TEST_DB)
            if success:
                print(f"PASS: Component 3 — {message} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — {message}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
