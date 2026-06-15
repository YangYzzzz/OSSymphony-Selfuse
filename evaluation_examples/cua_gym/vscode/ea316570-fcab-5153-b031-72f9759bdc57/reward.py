"""
Reward Script: Install SQLTools + SQLite driver, create connection, create users table
Task ID: vscode_gf3_028
Domain: vscode
Scoring:
  Component 1: SQLTools extension installed (0.2)
  Component 2: SQLTools SQLite driver extension installed (0.2)
  Component 3: SQLTools connection "App SQLite" configured for /home/user/projects/app/data/app.db (0.25)
  Component 4: users table exists with correct schema in app.db (0.35)
"""

import os
import json
import re
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_028'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
DB_PATH = os.path.join(WORKDIR, 'projects', 'app', 'data', 'app.db')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Cannot load settings.json: {e}")
        return {}


def get_installed_extensions():
    """Get list of installed extension IDs."""
    extensions_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    if not os.path.isdir(extensions_dir):
        return []
    exts = []
    for name in os.listdir(extensions_dir):
        # Extension dirs are like "publisher.name-version"
        # Extract publisher.name by removing the version suffix
        parts = name.rsplit('-', 1)
        if len(parts) == 2:
            exts.append(parts[0].lower())
        else:
            exts.append(name.lower())
    return exts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: SQLTools extension installed (0.2 points)
    try:
        extensions = get_installed_extensions()
        sqltools_found = any('mtxr.sqltools' == ext for ext in extensions)
        if sqltools_found:
            print(f"PASS: Component 1 — SQLTools extension installed (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — SQLTools extension not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: SQLTools SQLite driver extension installed (0.2 points)
    try:
        extensions = get_installed_extensions()
        sqlite_driver_found = any('mtxr.sqltools-driver-sqlite' == ext for ext in extensions)
        if sqlite_driver_found:
            print(f"PASS: Component 2 — SQLTools SQLite driver extension installed (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — SQLTools SQLite driver not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: SQLTools connection "App SQLite" configured (0.25 points)
    try:
        settings = load_settings()
        connections = settings.get('sqltools.connections', [])
        conn_found = False
        for conn in connections:
            name = conn.get('name', '')
            driver = conn.get('driver', '')
            database = conn.get('database', '')
            if (name == 'App SQLite' and
                driver.lower() == 'sqlite' and
                database == DB_PATH):
                conn_found = True
                break
        if conn_found:
            print(f"PASS: Component 3 — Connection 'App SQLite' configured correctly (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Connection 'App SQLite' not found or misconfigured. Connections: {connections}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: users table with correct schema (0.35 points)
    try:
        if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
            print(f"FAIL: Component 4 — Database file missing or empty at {DB_PATH}")
        else:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Check table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            table = cursor.fetchone()
            if not table:
                print(f"FAIL: Component 4 — 'users' table does not exist in database")
                conn.close()
            else:
                # Check columns via PRAGMA
                cursor.execute("PRAGMA table_info(users)")
                columns = cursor.fetchall()
                # columns: list of (cid, name, type, notnull, dflt_value, pk)
                col_map = {col[1].lower(): col for col in columns}

                checks_passed = 0
                total_checks = 4

                # 4a: id column - INTEGER PRIMARY KEY
                if 'id' in col_map:
                    c = col_map['id']
                    if c[2].upper() == 'INTEGER' and c[5] == 1:  # pk=1
                        checks_passed += 1
                        print(f"  PASS: 4a — 'id' is INTEGER PRIMARY KEY")
                    else:
                        print(f"  FAIL: 4a — 'id' type={c[2]} pk={c[5]}, expected INTEGER PK")
                else:
                    print(f"  FAIL: 4a — 'id' column not found")

                # 4b: name column - TEXT NOT NULL
                if 'name' in col_map:
                    c = col_map['name']
                    if c[2].upper() == 'TEXT' and c[3] == 1:  # notnull=1
                        checks_passed += 1
                        print(f"  PASS: 4b — 'name' is TEXT NOT NULL")
                    else:
                        print(f"  FAIL: 4b — 'name' type={c[2]} notnull={c[3]}, expected TEXT NOT NULL")
                else:
                    print(f"  FAIL: 4b — 'name' column not found")

                # 4c: email column - TEXT UNIQUE
                if 'email' in col_map:
                    c = col_map['email']
                    if c[2].upper() == 'TEXT':
                        # Check UNIQUE constraint via index_list
                        cursor.execute("PRAGMA index_list(users)")
                        indexes = cursor.fetchall()
                        email_unique = False
                        for idx in indexes:
                            idx_name = idx[1]
                            is_unique = idx[2]
                            if is_unique:
                                cursor.execute(f"PRAGMA index_info({idx_name})")
                                idx_cols = cursor.fetchall()
                                if any(ic[2].lower() == 'email' for ic in idx_cols):
                                    email_unique = True
                                    break
                        if email_unique:
                            checks_passed += 1
                            print(f"  PASS: 4c — 'email' is TEXT UNIQUE")
                        else:
                            print(f"  FAIL: 4c — 'email' is TEXT but UNIQUE constraint not found")
                    else:
                        print(f"  FAIL: 4c — 'email' type={c[2]}, expected TEXT")
                else:
                    print(f"  FAIL: 4c — 'email' column not found")

                # 4d: created_at column - DATETIME DEFAULT CURRENT_TIMESTAMP
                if 'created_at' in col_map:
                    c = col_map['created_at']
                    if c[2].upper() == 'DATETIME':
                        dflt = c[4]
                        if dflt and 'CURRENT_TIMESTAMP' in dflt.upper():
                            checks_passed += 1
                            print(f"  PASS: 4d — 'created_at' is DATETIME DEFAULT CURRENT_TIMESTAMP")
                        else:
                            print(f"  FAIL: 4d — 'created_at' default={dflt}, expected CURRENT_TIMESTAMP")
                    else:
                        print(f"  FAIL: 4d — 'created_at' type={c[2]}, expected DATETIME")
                else:
                    print(f"  FAIL: 4d — 'created_at' column not found")

                conn.close()

                # Award proportional points for schema correctness
                schema_score = (checks_passed / total_checks) * 0.35
                if checks_passed == total_checks:
                    print(f"PASS: Component 4 — All {total_checks} column checks passed (0.35 pts)")
                else:
                    print(f"PARTIAL: Component 4 — {checks_passed}/{total_checks} column checks passed ({schema_score:.2f} pts)")
                total_score += schema_score

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
