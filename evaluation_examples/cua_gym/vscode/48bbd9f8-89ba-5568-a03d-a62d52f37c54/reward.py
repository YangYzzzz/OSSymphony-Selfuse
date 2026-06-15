"""
Reward Script: SQL Query Optimization Workflow
Task ID: vscode_gf3_058
Domain: vscode
Scoring:
  Component 1 (0.25): EXPLAIN ANALYZE statement present
  Component 2 (0.25): SELECT from orders JOIN customers
  Component 3 (0.25): WHERE clause filtering on customer status
  Component 4 (0.25): CREATE INDEX with composite index on customers
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_058'

FILE_PATH = os.path.join(WORKDIR, 'projects', 'backend', 'queries', 'slow-query.sql')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize content: strip SQL comments for analysis but keep original for reference
    # Remove single-line comments (-- ...) for cleaner matching
    content_lower = content.lower()
    # Strip comment-only lines for SQL analysis
    sql_lines = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped and not stripped.startswith('--'):
            sql_lines.append(line)
    sql_content = '\n'.join(sql_lines)
    sql_content_lower = sql_content.lower()

    # Component 1: EXPLAIN ANALYZE statement present (0.25 points)
    # This checks that the file contains an actual EXPLAIN ANALYZE SQL statement,
    # not just a comment mentioning it. The initial file only has TODO comments.
    try:
        # Look for EXPLAIN ANALYZE as a SQL statement (not inside a comment)
        if re.search(r'explain\s+analyze', sql_content_lower):
            print(f"PASS: Component 1 - EXPLAIN ANALYZE statement found in SQL (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - No EXPLAIN ANALYZE statement found in executable SQL")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: SELECT from orders JOIN customers (0.25 points)
    # The task requires querying the orders table joining customers
    try:
        has_select = 'select' in sql_content_lower
        has_orders = re.search(r'\bfrom\s+orders\b', sql_content_lower) is not None
        has_join_customers = re.search(r'\bjoin\s+customers\b', sql_content_lower) is not None

        if has_select and has_orders and has_join_customers:
            print(f"PASS: Component 2 - SELECT from orders JOIN customers found (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if not has_select:
                missing.append('SELECT')
            if not has_orders:
                missing.append('FROM orders')
            if not has_join_customers:
                missing.append('JOIN customers')
            print(f"FAIL: Component 2 - Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: WHERE clause filtering on customer status (0.25 points)
    # The task specifies filtering on customer status in the WHERE clause
    try:
        # Look for WHERE clause that references status (e.g., c.status, customers.status, status =)
        has_where_status = re.search(
            r'where\s+.*\bstatus\b', sql_content_lower, re.DOTALL
        ) is not None

        if has_where_status:
            print(f"PASS: Component 3 - WHERE clause with status filter found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - No WHERE clause filtering on status found in SQL")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: CREATE INDEX with composite index on customers (0.25 points)
    # The task asks to create a composite index to fix sequential scan
    try:
        has_create_index = re.search(r'create\s+index', sql_content_lower) is not None
        # Composite index: has at least two columns in parentheses on customers table
        has_composite_on_customers = re.search(
            r'create\s+index\s+\w+\s+on\s+customers\s*\(\s*\w+\s*,\s*\w+',
            sql_content_lower
        ) is not None

        if has_create_index and has_composite_on_customers:
            print(f"PASS: Component 4 - CREATE INDEX with composite index on customers found (0.25 pts)")
            total_score += 0.25
        elif has_create_index:
            # Partial: has CREATE INDEX but not a proper composite on customers
            print(f"FAIL: Component 4 - CREATE INDEX found but not a composite index on customers table")
        else:
            print(f"FAIL: Component 4 - No CREATE INDEX statement found in SQL")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
