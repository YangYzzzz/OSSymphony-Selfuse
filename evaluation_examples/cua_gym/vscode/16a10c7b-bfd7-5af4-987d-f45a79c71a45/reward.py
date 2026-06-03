"""
Reward Script: Extract sorting/filtering logic into filterAndSortProducts function
Task ID: vscode_rrt_042
Domain: vscode
Scoring:
  - Component 1: filterAndSortProducts function exists (0.25)
  - Component 2: filterAndSortProducts has correct parameters (0.15)
  - Component 3: filterAndSortProducts contains filtering/sorting logic (0.25)
  - Component 4: get_catalog calls filterAndSortProducts (0.20)
  - Component 5: Behavioral equivalence test (0.15)
"""

import os
import ast
import re
import sys
import importlib.util
import uuid

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_042'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'shop', 'catalog.py')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse AST
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"CRITICAL: File has syntax errors: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract top-level function definitions
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = node

    # Component 1: filterAndSortProducts function exists as a top-level def (0.25 pts)
    try:
        if 'filterAndSortProducts' in functions:
            print(f"PASS: Component 1 — filterAndSortProducts function exists (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — filterAndSortProducts function not found. Found functions: {list(functions.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: filterAndSortProducts has correct parameters (products, category, min_price) (0.15 pts)
    try:
        if 'filterAndSortProducts' in functions:
            func_node = functions['filterAndSortProducts']
            param_names = [arg.arg for arg in func_node.args.args]
            expected_params = ['products', 'category', 'min_price']
            if param_names == expected_params:
                print(f"PASS: Component 2 — filterAndSortProducts has correct parameters {param_names} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Expected parameters {expected_params}, found {param_names}")
        else:
            print(f"FAIL: Component 2 — filterAndSortProducts not found, cannot check parameters")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: filterAndSortProducts contains filtering/sorting logic (0.25 pts)
    try:
        if 'filterAndSortProducts' in functions:
            func_node = functions['filterAndSortProducts']
            # Get source lines for this function
            func_source = ast.get_source_segment(content, func_node)
            if func_source is None:
                # Fallback: extract by line numbers
                lines = content.split('\n')
                func_source = '\n'.join(lines[func_node.lineno - 1:func_node.end_lineno])

            has_filter = 'category' in func_source and ('for' in func_source or 'if' in func_source or 'filter' in func_source.lower())
            has_sort = '.sort(' in func_source or 'sorted(' in func_source
            has_price = 'price' in func_source or 'min_price' in func_source
            has_return = 'return' in func_source

            checks_passed = sum([has_filter, has_sort, has_price, has_return])

            if checks_passed >= 3:
                print(f"PASS: Component 3 — filterAndSortProducts contains filtering/sorting logic (filter={has_filter}, sort={has_sort}, price={has_price}, return={has_return}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — filterAndSortProducts missing key logic (filter={has_filter}, sort={has_sort}, price={has_price}, return={has_return}). Only {checks_passed}/4 checks passed.")
        else:
            print(f"FAIL: Component 3 — filterAndSortProducts not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: get_catalog calls filterAndSortProducts (0.20 pts)
    try:
        if 'get_catalog' in functions:
            gc_node = functions['get_catalog']
            gc_source = ast.get_source_segment(content, gc_node)
            if gc_source is None:
                lines = content.split('\n')
                gc_source = '\n'.join(lines[gc_node.lineno - 1:gc_node.end_lineno])

            if 'filterAndSortProducts' in gc_source:
                print(f"PASS: Component 4 — get_catalog calls filterAndSortProducts (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — get_catalog does not call filterAndSortProducts. Source: {gc_source[:200]}")
        else:
            print(f"FAIL: Component 4 — get_catalog function not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Behavioral equivalence after refactoring (0.15 pts)
    # This component is gated on filterAndSortProducts existing AND get_catalog calling it,
    # ensuring it only awards points when the refactoring was actually done.
    try:
        if 'filterAndSortProducts' not in functions:
            print(f"FAIL: Component 5 — filterAndSortProducts not found, cannot test behavioral equivalence")
        else:
            # Verify get_catalog calls filterAndSortProducts before testing behavior
            gc_node = functions.get('get_catalog')
            gc_source_check = ''
            if gc_node:
                gc_source_check = ast.get_source_segment(content, gc_node) or ''
            if 'filterAndSortProducts' not in gc_source_check:
                print(f"FAIL: Component 5 — get_catalog does not call filterAndSortProducts, cannot verify equivalence")
            else:
                # Dynamically import the module and test it
                module_name = f"catalog_test_{uuid.uuid4().hex[:8]}"
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Test data
                test_products = [
                    {"name": "Widget A", "category": "tools", "price": 25.99},
                    {"name": "Widget B", "category": "tools", "price": 15.50},
                    {"name": "Gadget C", "category": "electronics", "price": 99.99},
                    {"name": "Widget D", "category": "tools", "price": 5.00},
                ]

                # Test get_catalog still works after refactoring
                result = module.get_catalog(test_products, "tools", 10.0)

                # Expected: Widget B ($15.50) and Widget A ($25.99) sorted by price, D excluded (price < 10)
                if isinstance(result, list) and len(result) == 2:
                    names = [r["name"] for r in result]
                    if names == ["Widget B", "Widget A"]:
                        print(f"PASS: Component 5 — Behavioral equivalence verified after refactoring. get_catalog returns correct results: {result} (0.15 pts)")
                        total_score += 0.15
                    else:
                        print(f"FAIL: Component 5 — get_catalog returned items in wrong order or wrong items. Got names: {names}, expected ['Widget B', 'Widget A']")
                else:
                    print(f"FAIL: Component 5 — get_catalog returned unexpected result: {result}")

                # Cleanup
                if module_name in sys.modules:
                    del sys.modules[module_name]
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
