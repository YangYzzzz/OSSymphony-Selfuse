"""
Reward Script: VSCode sqlc setup for type-safe SQL in Go project
Task ID: vscode_gf6_059
Domain: vscode
Scoring:
  1. sqlc.yaml with correct config (0.15)
  2. sql/schema/001_users.sql with users+posts tables (0.15)
  3. sql/queries/users.sql with 5 named queries (0.15)
  4. internal/db/ generated Go files exist (0.20)
  5. cmd/migrate/main.go exists with migration logic (0.10)
  6. Makefile has sqlc-generate target (0.10)
  7. .vscode/tasks.json has 'SQLC: Generate' task (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-sqlc')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: sqlc.yaml exists with correct configuration (0.15 points)
    try:
        sqlc_path = os.path.join(PROJECT, 'sqlc.yaml')
        if os.path.isfile(sqlc_path):
            with open(sqlc_path, 'r') as f:
                content = f.read()
            # Check key configuration elements
            has_version_2 = bool(re.search(r'version:\s*["\']?2["\']?', content))
            has_postgresql = 'postgresql' in content
            has_queries_path = 'queries' in content and 'sql' in content
            has_schema_path = 'schema' in content
            has_gen_go = 'go:' in content or 'go :' in content
            has_out_db = 'internal/db' in content
            has_package_db = 'package:' in content and 'db' in content

            if has_version_2 and has_postgresql and has_queries_path and has_schema_path and has_gen_go and has_out_db and has_package_db:
                print(f"PASS: Component 1 — sqlc.yaml has correct config (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_version_2: missing.append('version:2')
                if not has_postgresql: missing.append('postgresql')
                if not has_queries_path: missing.append('queries path')
                if not has_schema_path: missing.append('schema path')
                if not has_gen_go: missing.append('gen.go')
                if not has_out_db: missing.append('internal/db out')
                if not has_package_db: missing.append('package:db')
                print(f"FAIL: Component 1 — sqlc.yaml missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 1 — sqlc.yaml not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: sql/schema/001_users.sql with users and posts CREATE TABLE (0.15 points)
    try:
        schema_path = os.path.join(PROJECT, 'sql', 'schema', '001_users.sql')
        if os.path.isfile(schema_path):
            with open(schema_path, 'r') as f:
                content = f.read().lower()
            has_create_users = bool(re.search(r'create\s+table\s+users', content))
            has_create_posts = bool(re.search(r'create\s+table\s+posts', content))
            # Check key columns for users table
            has_user_cols = all(col in content for col in ['email', 'username', 'created_at', 'updated_at'])
            # Check key columns for posts table
            has_post_cols = all(col in content for col in ['user_id', 'title', 'content', 'published_at'])

            if has_create_users and has_create_posts and has_user_cols and has_post_cols:
                print(f"PASS: Component 2 — 001_users.sql has users+posts tables with correct columns (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_create_users: missing.append('CREATE TABLE users')
                if not has_create_posts: missing.append('CREATE TABLE posts')
                if not has_user_cols: missing.append('user columns')
                if not has_post_cols: missing.append('post columns')
                print(f"FAIL: Component 2 — 001_users.sql missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 2 — sql/schema/001_users.sql not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: sql/queries/users.sql with 5 named queries (0.15 points)
    try:
        queries_path = os.path.join(PROJECT, 'sql', 'queries', 'users.sql')
        if os.path.isfile(queries_path):
            with open(queries_path, 'r') as f:
                content = f.read()
            required_queries = ['GetUser', 'ListUsers', 'CreateUser', 'UpdateUser', 'DeleteUser']
            found_queries = [q for q in required_queries if re.search(rf'--\s*name:\s*{q}\b', content)]

            if len(found_queries) == 5:
                print(f"PASS: Component 3 — users.sql has all 5 named queries (0.15 pts)")
                total_score += 0.15
            else:
                missing = [q for q in required_queries if q not in found_queries]
                print(f"FAIL: Component 3 — users.sql missing queries: {', '.join(missing)} (found {len(found_queries)}/5)")
        else:
            print(f"FAIL: Component 3 — sql/queries/users.sql not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: internal/db/ contains generated Go files (0.20 points)
    try:
        db_dir = os.path.join(PROJECT, 'internal', 'db')
        if os.path.isdir(db_dir):
            go_files = [f for f in os.listdir(db_dir) if f.endswith('.go')]
            has_db_go = 'db.go' in go_files
            has_models_go = 'models.go' in go_files
            has_users_sql_go = 'users.sql.go' in go_files

            score_4 = 0.0
            if has_db_go:
                score_4 += 0.07
            if has_models_go:
                score_4 += 0.07
            if has_users_sql_go:
                score_4 += 0.06

            if score_4 > 0:
                # Verify they contain generated code markers
                db_go_path = os.path.join(db_dir, 'db.go')
                if has_db_go and os.path.isfile(db_go_path):
                    with open(db_go_path, 'r') as f:
                        db_content = f.read()
                    if 'package db' in db_content and 'sqlc' in db_content.lower():
                        print(f"PASS: Component 4 — internal/db/ has generated Go files ({score_4:.2f} pts)")
                        total_score += score_4
                    else:
                        print(f"FAIL: Component 4 — db.go exists but doesn't appear to be sqlc-generated")
                else:
                    print(f"PARTIAL: Component 4 — some generated files present ({score_4:.2f} pts)")
                    total_score += score_4
            else:
                print(f"FAIL: Component 4 — internal/db/ has no expected Go files (found: {go_files})")
        else:
            print(f"FAIL: Component 4 — internal/db/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: cmd/migrate/main.go exists with migration logic (0.10 points)
    try:
        migrate_path = os.path.join(PROJECT, 'cmd', 'migrate', 'main.go')
        if os.path.isfile(migrate_path):
            with open(migrate_path, 'r') as f:
                content = f.read()
            has_package_main = 'package main' in content
            has_sql_import = 'database/sql' in content
            has_migration_logic = 'sql/schema' in content or 'migration' in content.lower()

            if has_package_main and has_sql_import and has_migration_logic:
                print(f"PASS: Component 5 — cmd/migrate/main.go has migration logic (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — cmd/migrate/main.go exists but missing key elements")
        else:
            print(f"FAIL: Component 5 — cmd/migrate/main.go not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Makefile has sqlc generate target (0.10 points)
    try:
        makefile_path = os.path.join(PROJECT, 'Makefile')
        if os.path.isfile(makefile_path):
            with open(makefile_path, 'r') as f:
                content = f.read()
            # Check for a target that runs sqlc generate
            has_sqlc_target = bool(re.search(r'sqlc[\s_-]*generate', content, re.IGNORECASE))

            if has_sqlc_target:
                print(f"PASS: Component 6 — Makefile has sqlc generate target (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — Makefile missing sqlc generate target")
        else:
            print(f"FAIL: Component 6 — Makefile not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: .vscode/tasks.json has 'SQLC: Generate' task (0.15 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                # Handle JSONC (strip comments)
                raw = f.read()
                cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
                tasks_config = json.loads(cleaned)

            tasks = tasks_config.get('tasks', [])
            sqlc_task_found = False
            for task in tasks:
                label = task.get('label', '')
                command = task.get('command', '')
                if 'sqlc' in label.lower() and 'generate' in label.lower():
                    if 'sqlc' in command.lower() and 'generate' in command.lower():
                        sqlc_task_found = True
                        break

            if sqlc_task_found:
                print(f"PASS: Component 7 — .vscode/tasks.json has 'SQLC: Generate' task (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 — .vscode/tasks.json missing 'SQLC: Generate' task (found labels: {[t.get('label','') for t in tasks]})")
        else:
            print(f"FAIL: Component 7 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
