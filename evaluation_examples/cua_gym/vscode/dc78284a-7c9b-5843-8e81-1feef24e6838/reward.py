"""
Reward Script: Code review improvements for endpoints.py
Task ID: vscode_gf6_029
Domain: vscode
Scoring:
  C1 (0.20) - src/db/queries.py exists with named SQL constants
  C2 (0.15) - src/utils/pagination.py exists with Paginator class
  C3 (0.15) - endpoints.py imports from src.db.queries
  C4 (0.10) - endpoints.py imports from src.utils.pagination
  C5 (0.15) - No bare except: clauses, uses specific exception types
  C6 (0.10) - All 6 functions have type hints in signatures
  C7 (0.05) - All public functions have docstrings
  C8 (0.10) - code_review_notes.md exists with 5 improvement categories
"""

import os
import re
import ast

WORKDIR = '/home/user/projects/code-review-python'
TASK_ID = 'vscode_gf6_029'

# The 6 function names that must be present in endpoints.py
EXPECTED_FUNCTIONS = ['get_users', 'get_user', 'create_user', 'update_user', 'delete_user', 'list_orders']

# Minimum SQL constant names expected in queries.py
EXPECTED_QUERY_CONSTANTS = ['GET_USER', 'CREATE_USER', 'DELETE_USER', 'GET_ORDERS', 'GET_USERS']


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    endpoints_path = os.path.join(WORKDIR, 'src', 'api', 'endpoints.py')
    queries_path = os.path.join(WORKDIR, 'src', 'db', 'queries.py')
    pagination_path = os.path.join(WORKDIR, 'src', 'utils', 'pagination.py')
    notes_path = os.path.join(WORKDIR, 'code_review_notes.md')

    # Load endpoints.py content (needed for multiple checks)
    try:
        with open(endpoints_path, 'r') as f:
            endpoints_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read endpoints.py: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ----------------------------------------------------------------
    # Component 1: src/db/queries.py exists with named SQL constants (0.20 points)
    # This file does NOT exist in initial_env, only in golden_env
    # ----------------------------------------------------------------
    try:
        if os.path.isfile(queries_path):
            with open(queries_path, 'r') as f:
                queries_content = f.read()
            # Check for named SQL constant assignments
            found_constants = []
            for const_name in EXPECTED_QUERY_CONSTANTS:
                if re.search(rf'^{const_name}\s*=', queries_content, re.MULTILINE):
                    found_constants.append(const_name)
            if len(found_constants) >= 4:
                print(f"PASS: Component 1 -- queries.py has {len(found_constants)} SQL constants: {found_constants} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 -- queries.py found only {len(found_constants)} constants (need >=4): {found_constants}")
        else:
            print(f"FAIL: Component 1 -- queries.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ----------------------------------------------------------------
    # Component 2: src/utils/pagination.py exists with Paginator class (0.15 points)
    # This file does NOT exist in initial_env, only in golden_env
    # ----------------------------------------------------------------
    try:
        if os.path.isfile(pagination_path):
            with open(pagination_path, 'r') as f:
                pagination_content = f.read()
            # Check for Paginator class definition
            if re.search(r'class\s+Paginator', pagination_content):
                # Check it has offset and limit properties/methods
                has_offset = 'offset' in pagination_content
                has_limit = 'limit' in pagination_content
                if has_offset and has_limit:
                    print(f"PASS: Component 2 -- pagination.py has Paginator class with offset/limit (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 -- Paginator class missing offset={has_offset} or limit={has_limit}")
            else:
                print(f"FAIL: Component 2 -- pagination.py exists but no Paginator class found")
        else:
            print(f"FAIL: Component 2 -- pagination.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ----------------------------------------------------------------
    # Component 3: endpoints.py imports from src.db.queries (0.15 points)
    # Initial endpoints.py has inline SQL, no such import
    # ----------------------------------------------------------------
    try:
        has_queries_import = bool(re.search(
            r'from\s+src\.db\.queries\s+import|import\s+src\.db\.queries',
            endpoints_content
        ))
        # Also check that inline SQL strings are gone (no raw SELECT/INSERT/UPDATE/DELETE strings)
        inline_sql_patterns = re.findall(
            r'(?:db\.execute|cursor\.execute)\s*\(\s*["\'](?:SELECT|INSERT|UPDATE|DELETE)',
            endpoints_content,
            re.IGNORECASE
        )
        if has_queries_import and len(inline_sql_patterns) == 0:
            print(f"PASS: Component 3 -- endpoints.py imports from queries and no inline SQL found (0.15 pts)")
            total_score += 0.15
        elif has_queries_import:
            # Partial: has import but still has some inline SQL
            print(f"PARTIAL: Component 3 -- has queries import but {len(inline_sql_patterns)} inline SQL remain (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 3 -- endpoints.py does not import from src.db.queries")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ----------------------------------------------------------------
    # Component 4: endpoints.py imports from src.utils.pagination (0.10 points)
    # Initial endpoints.py has manual skip/limit, no such import
    # ----------------------------------------------------------------
    try:
        has_pagination_import = bool(re.search(
            r'from\s+src\.utils\.pagination\s+import|import\s+src\.utils\.pagination',
            endpoints_content
        ))
        # Check usage of Paginator in the code
        uses_paginator = bool(re.search(r'Paginator\s*\(', endpoints_content))
        if has_pagination_import and uses_paginator:
            print(f"PASS: Component 4 -- endpoints.py imports and uses Paginator (0.10 pts)")
            total_score += 0.10
        elif has_pagination_import:
            print(f"PARTIAL: Component 4 -- imports pagination but doesn't use Paginator (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 -- endpoints.py does not import from src.utils.pagination")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # ----------------------------------------------------------------
    # Component 5: No bare except: clauses, uses specific exceptions (0.15 points)
    # Initial endpoints.py has bare except: in all 6 functions
    # ----------------------------------------------------------------
    try:
        # Parse the AST to find exception handlers
        tree = ast.parse(endpoints_content)
        bare_excepts = 0
        specific_excepts = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    bare_excepts += 1
                else:
                    specific_excepts += 1

        if bare_excepts == 0 and specific_excepts > 0:
            print(f"PASS: Component 5 -- no bare except: clauses, {specific_excepts} specific handlers (0.15 pts)")
            total_score += 0.15
        elif bare_excepts > 0:
            print(f"FAIL: Component 5 -- found {bare_excepts} bare except: clauses (need 0)")
        else:
            print(f"FAIL: Component 5 -- no exception handlers found at all")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # ----------------------------------------------------------------
    # Component 6: All 6 functions have type hints (0.10 points)
    # Initial endpoints.py has no type hints on function signatures
    # ----------------------------------------------------------------
    try:
        tree = ast.parse(endpoints_content)
        functions_with_hints = 0
        functions_checked = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in EXPECTED_FUNCTIONS:
                functions_checked += 1
                has_return_annotation = node.returns is not None
                has_param_annotations = any(
                    arg.annotation is not None
                    for arg in node.args.args
                    if arg.arg != 'self'
                )
                if has_return_annotation and has_param_annotations:
                    functions_with_hints += 1

        if functions_checked >= 6 and functions_with_hints >= 6:
            print(f"PASS: Component 6 -- all {functions_with_hints}/{functions_checked} functions have type hints (0.10 pts)")
            total_score += 0.10
        elif functions_with_hints >= 4:
            partial = round(0.10 * functions_with_hints / 6, 2)
            print(f"PARTIAL: Component 6 -- {functions_with_hints}/{functions_checked} functions have type hints ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 -- only {functions_with_hints}/{functions_checked} functions have type hints")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # ----------------------------------------------------------------
    # Component 7: All public functions have docstrings (0.05 points)
    # Initial endpoints.py has no docstrings
    # ----------------------------------------------------------------
    try:
        tree = ast.parse(endpoints_content)
        functions_with_docstrings = 0
        functions_checked = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in EXPECTED_FUNCTIONS:
                functions_checked += 1
                if (node.body and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, (ast.Constant, ast.Str))):
                    functions_with_docstrings += 1

        if functions_checked >= 6 and functions_with_docstrings >= 6:
            print(f"PASS: Component 7 -- all {functions_with_docstrings} functions have docstrings (0.05 pts)")
            total_score += 0.05
        elif functions_with_docstrings >= 3:
            partial = round(0.05 * functions_with_docstrings / 6, 3)
            print(f"PARTIAL: Component 7 -- {functions_with_docstrings}/{functions_checked} have docstrings ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 7 -- only {functions_with_docstrings}/{functions_checked} functions have docstrings")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # ----------------------------------------------------------------
    # Component 8: code_review_notes.md exists with 5 categories (0.10 points)
    # This file does NOT exist in initial_env
    # ----------------------------------------------------------------
    try:
        if os.path.isfile(notes_path):
            with open(notes_path, 'r') as f:
                notes_content = f.read().lower()
            # Check for mention of all 5 improvement categories
            categories_found = 0
            category_checks = [
                ('sql' in notes_content and 'quer' in notes_content, 'SQL query extraction'),
                ('except' in notes_content and ('bare' in notes_content or 'specific' in notes_content), 'exception handling'),
                ('type hint' in notes_content or 'type annotation' in notes_content or 'typing' in notes_content, 'type hints'),
                ('paginat' in notes_content, 'pagination'),
                ('docstring' in notes_content, 'docstrings'),
            ]
            for check_result, name in category_checks:
                if check_result:
                    categories_found += 1

            if categories_found >= 4:
                print(f"PASS: Component 8 -- code_review_notes.md has {categories_found}/5 categories (0.10 pts)")
                total_score += 0.10
            elif categories_found >= 2:
                partial = round(0.10 * categories_found / 5, 2)
                print(f"PARTIAL: Component 8 -- code_review_notes.md has {categories_found}/5 categories ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 8 -- code_review_notes.md has only {categories_found}/5 categories")
        else:
            print(f"FAIL: Component 8 -- code_review_notes.md does not exist")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
