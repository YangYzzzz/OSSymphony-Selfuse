"""
Reward Script: Create a Python type stub file (.pyi) for legacy_api.py
Task ID: vscode_lp_034
Domain: vscode (python files)
Scoring:
  Component 1 (0.25): legacy_api.pyi exists, is valid Python, and contains all 3 function stubs
  Component 2 (0.25): get_users stub has parameter and return type annotations
  Component 3 (0.25): create_order stub has parameter and return type annotations
  Component 4 (0.25): process_payment stub has parameter and return type annotations
"""

import os
import ast

WORKDIR = '/home/user/python_project'
TASK_ID = 'vscode_lp_034'
PYI_PATH = os.path.join(WORKDIR, 'legacy_api.pyi')


def check_func_annotations(tree, func_name, expected_params):
    """
    Find a function in the AST and check that all expected params
    and the return type have annotations.
    Returns (param_annotated_count, total_params, has_return).
    Returns None if function not found.
    """
    target_func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            target_func = node
            break
    if target_func is None:
        return None

    annotated_params = 0
    for arg in target_func.args.args:
        if arg.arg in expected_params and arg.annotation is not None:
            annotated_params += 1

    return_annotated = target_func.returns is not None
    return (annotated_params, len(expected_params), return_annotated)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(PYI_PATH):
        print(f"CRITICAL: Type stub file not found: {PYI_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(PYI_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {PYI_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the AST once
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"CRITICAL: .pyi file has syntax errors: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect function names from the stub
    func_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_names.add(node.name)

    required = {'get_users', 'create_order', 'process_payment'}
    found = required.intersection(func_names)

    # Component 1: Valid .pyi with all 3 required function stubs (0.25 points)
    try:
        if len(found) == 3:
            print(f"PASS: Component 1 - Valid .pyi with all 3 function stubs: {sorted(found)} (0.25 pts)")
            total_score += 0.25
        elif len(found) > 0:
            partial = round(0.25 * len(found) / 3, 3)
            print(f"PARTIAL: Component 1 - Found {len(found)}/3 functions: {sorted(found)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No required function stubs found. Functions in file: {sorted(func_names)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: get_users stub has type annotations (0.25 points)
    try:
        result = check_func_annotations(tree, 'get_users', ['limit'])
        if result is None:
            print("FAIL: Component 2 - get_users function not found in stub")
        else:
            annotated_params, total_params, has_return = result
            # 1 param + 1 return = 2 sub-checks
            sub_score = (annotated_params + int(has_return)) / (total_params + 1)
            comp_score = round(0.25 * sub_score, 3)
            if comp_score >= 0.25:
                print(f"PASS: Component 2 - get_users has param and return annotations (0.25 pts)")
                total_score += 0.25
            elif comp_score > 0:
                print(f"PARTIAL: Component 2 - get_users: params={annotated_params}/{total_params}, return={has_return} ({comp_score} pts)")
                total_score += comp_score
            else:
                print(f"FAIL: Component 2 - get_users has no type annotations")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: create_order stub has type annotations (0.25 points)
    try:
        result = check_func_annotations(tree, 'create_order', ['user_id', 'items'])
        if result is None:
            print("FAIL: Component 3 - create_order function not found in stub")
        else:
            annotated_params, total_params, has_return = result
            sub_score = (annotated_params + int(has_return)) / (total_params + 1)
            comp_score = round(0.25 * sub_score, 3)
            if comp_score >= 0.25:
                print(f"PASS: Component 3 - create_order has all annotations (0.25 pts)")
                total_score += 0.25
            elif comp_score > 0:
                print(f"PARTIAL: Component 3 - create_order: params={annotated_params}/{total_params}, return={has_return} ({comp_score} pts)")
                total_score += comp_score
            else:
                print(f"FAIL: Component 3 - create_order has no type annotations")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: process_payment stub has type annotations (0.25 points)
    try:
        result = check_func_annotations(tree, 'process_payment', ['order_id', 'amount'])
        if result is None:
            print("FAIL: Component 4 - process_payment function not found in stub")
        else:
            annotated_params, total_params, has_return = result
            sub_score = (annotated_params + int(has_return)) / (total_params + 1)
            comp_score = round(0.25 * sub_score, 3)
            if comp_score >= 0.25:
                print(f"PASS: Component 4 - process_payment has all annotations (0.25 pts)")
                total_score += 0.25
            elif comp_score > 0:
                print(f"PARTIAL: Component 4 - process_payment: params={annotated_params}/{total_params}, return={has_return} ({comp_score} pts)")
                total_score += comp_score
            else:
                print(f"FAIL: Component 4 - process_payment has no type annotations")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
