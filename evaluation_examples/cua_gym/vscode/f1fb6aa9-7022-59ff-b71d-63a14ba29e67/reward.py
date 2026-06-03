"""
Reward Script: Database migration workflow in VSCode
Task ID: vscode_gf3_066
Domain: vscode
Scoring:
  C1 (0.20) - migrations directory with both SQL files present
  C2 (0.20) - 001_initial_schema.sql: CREATE users + sessions tables
  C3 (0.20) - 002_add_oauth.sql: CREATE oauth_providers with FK to users
  C4 (0.20) - migrate.js: schema_migrations tracking, transactions, ordered reads
  C5 (0.20) - VSCode task "Run Migrations" executing "node migrate.js"
"""

import os
import re
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_066'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'backend')
MIGRATIONS_DIR = os.path.join(PROJECT_DIR, 'migrations')
MIGRATE_JS = os.path.join(PROJECT_DIR, 'migrate.js')
TASKS_JSON = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: migrations directory exists with both SQL files (0.20 points)
    try:
        file_001 = os.path.join(MIGRATIONS_DIR, '001_initial_schema.sql')
        file_002 = os.path.join(MIGRATIONS_DIR, '002_add_oauth.sql')
        has_001 = os.path.isfile(file_001)
        has_002 = os.path.isfile(file_002)
        if has_001 and has_002:
            print(f"PASS: Component 1 — Both migration SQL files exist in migrations/ (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_001:
                missing.append('001_initial_schema.sql')
            if not has_002:
                missing.append('002_add_oauth.sql')
            print(f"FAIL: Component 1 — Missing files: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 001_initial_schema.sql contains CREATE for users and sessions tables (0.20 points)
    try:
        file_001 = os.path.join(MIGRATIONS_DIR, '001_initial_schema.sql')
        if os.path.isfile(file_001):
            with open(file_001, 'r') as f:
                content = f.read().lower()
            has_create_users = bool(re.search(r'create\s+table\s+(if\s+not\s+exists\s+)?users\b', content))
            has_create_sessions = bool(re.search(r'create\s+table\s+(if\s+not\s+exists\s+)?sessions\b', content))
            if has_create_users and has_create_sessions:
                print(f"PASS: Component 2 — 001_initial_schema.sql has CREATE TABLE for users and sessions (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — users={has_create_users}, sessions={has_create_sessions}")
        else:
            print(f"FAIL: Component 2 — 001_initial_schema.sql not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 002_add_oauth.sql contains oauth_providers table with FK to users (0.20 points)
    try:
        file_002 = os.path.join(MIGRATIONS_DIR, '002_add_oauth.sql')
        if os.path.isfile(file_002):
            with open(file_002, 'r') as f:
                content = f.read().lower()
            has_create_oauth = bool(re.search(r'create\s+table\s+(if\s+not\s+exists\s+)?oauth_providers\b', content))
            has_fk_users = bool(re.search(r'references\s+users', content))
            if has_create_oauth and has_fk_users:
                print(f"PASS: Component 3 — 002_add_oauth.sql has oauth_providers with FK to users (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — oauth_providers={has_create_oauth}, fk_to_users={has_fk_users}")
        else:
            print(f"FAIL: Component 3 — 002_add_oauth.sql not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: migrate.js has schema_migrations tracking, transactions, and ordered file reading (0.20 points)
    try:
        if os.path.isfile(MIGRATE_JS):
            with open(MIGRATE_JS, 'r') as f:
                content = f.read()
            content_lower = content.lower()

            # Check key migration runner concepts
            has_schema_migrations = 'schema_migrations' in content_lower
            has_transaction = ('begin' in content_lower and ('commit' in content_lower or 'rollback' in content_lower))
            has_sort = ('.sort' in content or 'sort(' in content)
            has_readdir = ('readdirsync' in content_lower or 'readdir' in content_lower or 'readdirSync' in content)
            has_read_files = has_readdir or ('readfilesync' in content_lower or 'readFileSync' in content)

            sub_score = 0
            checks = {
                'schema_migrations': has_schema_migrations,
                'transactions': has_transaction,
                'sort_order': has_sort,
                'reads_migration_files': has_read_files,
            }
            passed = sum(1 for v in checks.values() if v)

            if passed == 4:
                print(f"PASS: Component 4 — migrate.js has all required features: {checks} (0.20 pts)")
                total_score += 0.20
            elif passed >= 3:
                pts = 0.15
                print(f"PARTIAL: Component 4 — migrate.js has {passed}/4 features: {checks} ({pts} pts)")
                total_score += pts
            elif passed >= 2:
                pts = 0.10
                print(f"PARTIAL: Component 4 — migrate.js has {passed}/4 features: {checks} ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 4 — migrate.js missing key features: {checks}")
        else:
            print(f"FAIL: Component 4 — migrate.js not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: VSCode task "Run Migrations" configured with "node migrate.js" (0.20 points)
    try:
        if os.path.isfile(TASKS_JSON):
            with open(TASKS_JSON, 'r') as f:
                raw = f.read()
            # Handle JSONC (strip comments)
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            tasks_config = json.loads(cleaned)

            tasks = tasks_config.get('tasks', [])
            matching = [
                t for t in tasks
                if 'run migrations' in t.get('label', '').lower()
                and 'node' in t.get('command', '').lower()
                and 'migrate' in t.get('command', '').lower()
            ]

            if len(matching) > 0:
                print(f"PASS: Component 5 — VSCode task 'Run Migrations' with 'node migrate.js' found (0.20 pts)")
                total_score += 0.20
            else:
                labels = [t.get('label', '') for t in tasks]
                print(f"FAIL: Component 5 — No matching task found. Available labels: {labels}")
        else:
            print(f"FAIL: Component 5 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
