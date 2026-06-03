"""
Reward Script: Verify 'Extract Method' refactoring — validate_input extracted from run_pipeline
Task ID: vscode_py_018
Domain: vscode (Python file)
Scoring:
  Component 1 (0.4): validate_input function exists as a top-level def
  Component 2 (0.3): run_pipeline calls validate_input
  Component 3 (0.3): validate_input contains key validation logic (type/id/value checks)
"""

import ast
import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_018'
TARGET_FILE = os.path.join(WORKDIR, 'data_pipeline.py')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load and parse the file
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get all top-level function definitions
    top_level_funcs = {}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            top_level_funcs[node.name] = node

    # Component 1: validate_input function exists as a top-level def (0.4 points)
    try:
        if 'validate_input' in top_level_funcs:
            print(f"PASS: Component 1 — 'validate_input' exists as top-level function (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — 'validate_input' not found as top-level function. "
                  f"Top-level functions: {list(top_level_funcs.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: run_pipeline calls validate_input (0.3 points)
    try:
        run_pipeline_node = top_level_funcs.get('run_pipeline')
        if run_pipeline_node is None:
            print(f"FAIL: Component 2 — 'run_pipeline' function not found")
        else:
            # Walk the AST of run_pipeline to find calls to validate_input
            call_names = [
                node.func.id
                for node in ast.walk(run_pipeline_node)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            ]
            if 'validate_input' in call_names:
                print(f"PASS: Component 2 — 'run_pipeline' calls 'validate_input' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — 'run_pipeline' does not call 'validate_input'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: validate_input contains key validation logic (0.3 points)
    # Check that the extracted function body contains isinstance checks and 'id' field checks
    try:
        vi_node = top_level_funcs.get('validate_input')
        if vi_node is None:
            print(f"FAIL: Component 3 — 'validate_input' not found, cannot check body")
        else:
            body_source = ast.get_source_segment(source, vi_node)
            if body_source is None:
                # Fallback: unparse the AST node
                body_source = ast.unparse(vi_node)

            # Check for key validation patterns:
            # 1. isinstance check (type validation)
            # 2. 'id' field check
            # 3. 'value' type check (int, float)
            has_isinstance = 'isinstance' in body_source
            has_id_check = "'id'" in body_source or '"id"' in body_source
            has_value_check = "'value'" in body_source or '"value"' in body_source

            checks_passed = sum([has_isinstance, has_id_check, has_value_check])

            if checks_passed >= 3:
                print(f"PASS: Component 3 — validate_input contains all key validation logic "
                      f"(isinstance, id check, value check) (0.3 pts)")
                total_score += 0.3
            elif checks_passed >= 2:
                print(f"PARTIAL: Component 3 — validate_input has {checks_passed}/3 key checks "
                      f"(isinstance={has_isinstance}, id={has_id_check}, value={has_value_check}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — validate_input missing key validation logic. "
                      f"isinstance={has_isinstance}, id={has_id_check}, value={has_value_check}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
