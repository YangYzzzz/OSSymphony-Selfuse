"""
Reward Script: SQL migration files for users and posts tables
Task ID: vscode_gf3_040
Domain: vs_code
Scoring:
  C1: 001_create_users.sql exists with CREATE TABLE users      (0.15)
  C2: Users table has proper constraints (PK, NOT NULL, UNIQUE) (0.20)
  C3: Users table has indexes                                   (0.10)
  C4: 002_create_posts.sql exists with CREATE TABLE posts       (0.15)
  C5: Posts table has foreign key referencing users              (0.15)
  C6: Posts table has content TEXT column                        (0.10)
  C7: Posts table has published_at TIMESTAMP column             (0.05)
  C8: Partial index on published_at WHERE published_at IS NOT NULL (0.10)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_040'
MIGRATIONS_DIR = os.path.join(WORKDIR, 'projects', 'backend', 'src', 'database', 'migrations')

FILE1 = os.path.join(MIGRATIONS_DIR, '001_create_users.sql')
FILE2 = os.path.join(MIGRATIONS_DIR, '002_create_posts.sql')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Load file 1 ----
    sql1 = None
    try:
        with open(FILE1, 'r') as f:
            sql1 = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {FILE1}: {e}")

    # ---- Load file 2 ----
    sql2 = None
    try:
        with open(FILE2, 'r') as f:
            sql2 = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {FILE2}: {e}")

    # Component 1: 001_create_users.sql exists and contains CREATE TABLE users (0.15 pts)
    try:
        if sql1 and re.search(r'CREATE\s+TABLE\s+users\s*\(', sql1, re.IGNORECASE):
            print(f"PASS: Component 1 -- 001_create_users.sql has CREATE TABLE users (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- 001_create_users.sql missing or no CREATE TABLE users")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Users table has proper constraints (PK, NOT NULL, UNIQUE) (0.20 pts)
    try:
        if sql1:
            has_pk = bool(re.search(r'PRIMARY\s+KEY', sql1, re.IGNORECASE))
            has_not_null = bool(re.search(r'NOT\s+NULL', sql1, re.IGNORECASE))
            has_unique = bool(re.search(r'UNIQUE', sql1, re.IGNORECASE))

            constraints_met = sum([has_pk, has_not_null, has_unique])
            if constraints_met == 3:
                print(f"PASS: Component 2 -- Users table has PK, NOT NULL, UNIQUE (0.20 pts)")
                total_score += 0.20
            elif constraints_met >= 2:
                print(f"PARTIAL: Component 2 -- Users table has {constraints_met}/3 constraints (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 -- Users table has {constraints_met}/3 constraints (PK={has_pk}, NOT_NULL={has_not_null}, UNIQUE={has_unique})")
        else:
            print(f"FAIL: Component 2 -- File 1 not available")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Users table has indexes (0.10 pts)
    try:
        if sql1:
            index_matches = re.findall(r'CREATE\s+INDEX\s+\w+\s+ON\s+users', sql1, re.IGNORECASE)
            if len(index_matches) >= 1:
                print(f"PASS: Component 3 -- Users table has {len(index_matches)} index(es) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- No indexes found on users table")
        else:
            print(f"FAIL: Component 3 -- File 1 not available")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 002_create_posts.sql exists and contains CREATE TABLE posts (0.15 pts)
    try:
        if sql2 and re.search(r'CREATE\s+TABLE\s+posts\s*\(', sql2, re.IGNORECASE):
            print(f"PASS: Component 4 -- 002_create_posts.sql has CREATE TABLE posts (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- 002_create_posts.sql missing or no CREATE TABLE posts")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Posts table has foreign key referencing users (0.15 pts)
    try:
        if sql2:
            has_fk = bool(re.search(r'REFERENCES\s+users', sql2, re.IGNORECASE))
            if has_fk:
                print(f"PASS: Component 5 -- Posts table has FK to users (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- No REFERENCES users found in posts table")
        else:
            print(f"FAIL: Component 5 -- File 2 not available")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Posts table has content TEXT column (0.10 pts)
    try:
        if sql2:
            has_content_text = bool(re.search(r'content\s+TEXT', sql2, re.IGNORECASE))
            if has_content_text:
                print(f"PASS: Component 6 -- Posts table has content TEXT column (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- No 'content TEXT' column found in posts table")
        else:
            print(f"FAIL: Component 6 -- File 2 not available")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: Posts table has published_at TIMESTAMP column (0.05 pts)
    try:
        if sql2:
            has_published_at = bool(re.search(r'published_at\s+TIMESTAMP', sql2, re.IGNORECASE))
            if has_published_at:
                print(f"PASS: Component 7 -- Posts table has published_at TIMESTAMP (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 7 -- No 'published_at TIMESTAMP' column found")
        else:
            print(f"FAIL: Component 7 -- File 2 not available")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: Partial index on published_at WHERE published_at IS NOT NULL (0.10 pts)
    try:
        if sql2:
            has_partial_idx = bool(re.search(
                r'CREATE\s+INDEX\s+\w+\s+ON\s+posts\s*\(\s*published_at\s*\)\s*WHERE\s+published_at\s+IS\s+NOT\s+NULL',
                sql2, re.IGNORECASE
            ))
            if has_partial_idx:
                print(f"PASS: Component 8 -- Partial index on published_at WHERE IS NOT NULL (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 8 -- Partial index pattern not found")
        else:
            print(f"FAIL: Component 8 -- File 2 not available")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
