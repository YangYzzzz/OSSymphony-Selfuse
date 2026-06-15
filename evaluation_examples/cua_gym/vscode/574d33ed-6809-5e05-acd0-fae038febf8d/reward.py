"""
Reward Script: Configure SQLTools workspace with multiple database connections
Task ID: vscode_gf3_091
Domain: vscode
Scoring:
  - Component 1 (0.15): sqltools.connections exists with 3 entries
  - Component 2 (0.25): Analytics DB PostgreSQL connection (host, port, database, driver)
  - Component 3 (0.20): Analytics DB extra options (previewLimit=1000, defaultDatabase)
  - Component 4 (0.20): Cache DB Redis connection (host, port, driver)
  - Component 5 (0.20): Warehouse SQLite connection (driver, database path)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_091'
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'data-platform', '.vscode', 'settings.json')


def load_settings(path):
    """Load settings.json, handling possible JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_connection(connections, name):
    """Find a connection by name (case-insensitive)."""
    for conn in connections:
        if isinstance(conn, dict) and conn.get('name', '').strip().lower() == name.lower():
            return conn
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings file
    try:
        settings = load_settings(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load settings file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get connections list
    connections = settings.get('sqltools.connections', None)

    # Component 1: sqltools.connections exists with 3 entries (0.15 points)
    try:
        if connections is not None and isinstance(connections, list) and len(connections) == 3:
            print(f"PASS: Component 1 -- sqltools.connections has {len(connections)} entries (0.15 pts)")
            total_score += 0.15
        else:
            if connections is None:
                print("FAIL: Component 1 -- sqltools.connections key not found")
            elif not isinstance(connections, list):
                print(f"FAIL: Component 1 -- sqltools.connections is not a list: {type(connections)}")
            else:
                print(f"FAIL: Component 1 -- expected 3 connections, found {len(connections)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if not connections or not isinstance(connections, list):
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Analytics DB PostgreSQL connection (0.25 points)
    try:
        analytics = find_connection(connections, 'Analytics DB')
        if analytics is None:
            print("FAIL: Component 2 -- 'Analytics DB' connection not found")
        else:
            checks_passed = 0
            total_checks = 4

            driver = str(analytics.get('driver', '')).lower()
            if 'postgres' in driver:
                checks_passed += 1
            else:
                print(f"  DETAIL: driver expected PostgreSQL-like, found '{analytics.get('driver')}'")

            if analytics.get('server') == 'analytics-db.local':
                checks_passed += 1
            else:
                print(f"  DETAIL: server expected 'analytics-db.local', found '{analytics.get('server')}'")

            if analytics.get('port') == 5432:
                checks_passed += 1
            else:
                print(f"  DETAIL: port expected 5432, found '{analytics.get('port')}'")

            if analytics.get('database') == 'analytics':
                checks_passed += 1
            else:
                print(f"  DETAIL: database expected 'analytics', found '{analytics.get('database')}'")

            if checks_passed == total_checks:
                print(f"PASS: Component 2 -- Analytics DB connection correct ({checks_passed}/{total_checks} checks) (0.25 pts)")
                total_score += 0.25
            elif checks_passed > 0:
                partial = round(0.25 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 2 -- Analytics DB {checks_passed}/{total_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- Analytics DB 0/{total_checks} checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Analytics DB previewLimit and defaultDatabase (0.20 points)
    try:
        analytics = find_connection(connections, 'Analytics DB')
        if analytics is None:
            print("FAIL: Component 3 -- 'Analytics DB' connection not found")
        else:
            sub_score = 0.0

            if analytics.get('previewLimit') == 1000:
                sub_score += 0.10
                print("  DETAIL: previewLimit=1000 found")
            else:
                print(f"  DETAIL: previewLimit expected 1000, found '{analytics.get('previewLimit')}'")

            if analytics.get('defaultDatabase') == 'analytics':
                sub_score += 0.10
                print("  DETAIL: defaultDatabase='analytics' found")
            else:
                print(f"  DETAIL: defaultDatabase expected 'analytics', found '{analytics.get('defaultDatabase')}'")

            if sub_score >= 0.20:
                print(f"PASS: Component 3 -- Analytics DB extra options correct (0.20 pts)")
            elif sub_score > 0:
                print(f"PARTIAL: Component 3 -- Analytics DB extra options ({sub_score} pts)")
            else:
                print("FAIL: Component 3 -- Analytics DB extra options missing")
            total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Cache DB Redis connection (0.20 points)
    try:
        cache = find_connection(connections, 'Cache DB')
        if cache is None:
            print("FAIL: Component 4 -- 'Cache DB' connection not found")
        else:
            checks_passed = 0
            total_checks = 3

            driver = str(cache.get('driver', '')).lower()
            if 'redis' in driver:
                checks_passed += 1
            else:
                print(f"  DETAIL: driver expected Redis-like, found '{cache.get('driver')}'")

            server = cache.get('server', '')
            if server == 'localhost':
                checks_passed += 1
            else:
                print(f"  DETAIL: server expected 'localhost', found '{server}'")

            if cache.get('port') == 6379:
                checks_passed += 1
            else:
                print(f"  DETAIL: port expected 6379, found '{cache.get('port')}'")

            if checks_passed == total_checks:
                print(f"PASS: Component 4 -- Cache DB connection correct ({checks_passed}/{total_checks} checks) (0.20 pts)")
                total_score += 0.20
            elif checks_passed > 0:
                partial = round(0.20 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 4 -- Cache DB {checks_passed}/{total_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- Cache DB 0/{total_checks} checks passed")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Warehouse SQLite connection (0.20 points)
    try:
        warehouse = find_connection(connections, 'Warehouse')
        if warehouse is None:
            print("FAIL: Component 5 -- 'Warehouse' connection not found")
        else:
            checks_passed = 0
            total_checks = 2

            driver = str(warehouse.get('driver', '')).lower()
            if 'sqlite' in driver:
                checks_passed += 1
            else:
                print(f"  DETAIL: driver expected SQLite-like, found '{warehouse.get('driver')}'")

            db_path = warehouse.get('database', '')
            if db_path == './data/warehouse.db':
                checks_passed += 1
            else:
                print(f"  DETAIL: database expected './data/warehouse.db', found '{db_path}'")

            if checks_passed == total_checks:
                print(f"PASS: Component 5 -- Warehouse connection correct ({checks_passed}/{total_checks} checks) (0.20 pts)")
                total_score += 0.20
            elif checks_passed > 0:
                partial = round(0.20 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 5 -- Warehouse {checks_passed}/{total_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- Warehouse 0/{total_checks} checks passed")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SETTINGS_PATH)
