"""
Reward Script: Add 'timeout' parameter to fetch_data function and update call sites
Task ID: vscode_rrt_040
Domain: vscode
Scoring:
  Precondition: main.py call sites remain valid (gate - not scored)
  Component 1 (0.5): fetch_data signature includes timeout=30
  Component 2 (0.5): requests.get call uses timeout=timeout
"""

import os
import re
import ast

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_040'

FETCHER_PATH = os.path.join(WORKDIR, 'projects', 'api', 'fetcher.py')
MAIN_PATH = os.path.join(WORKDIR, 'projects', 'api', 'main.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: fetcher.py must exist
    if not os.path.exists(FETCHER_PATH):
        print(f"CRITICAL: File not found: {FETCHER_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(FETCHER_PATH, 'r') as f:
            fetcher_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {FETCHER_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: main.py call sites must still be valid (gate, not scored)
    try:
        if not os.path.exists(MAIN_PATH):
            print(f"CRITICAL: main.py not found at {MAIN_PATH}")
            print("REWARD: 0.0")
            return 0.0

        with open(MAIN_PATH, 'r') as f:
            main_content = f.read()

        main_tree = ast.parse(main_content)
        fetch_calls = []
        for node in ast.walk(main_tree):
            if isinstance(node, ast.Call):
                func = node.func
                if (isinstance(func, ast.Name) and func.id == 'fetch_data') or \
                   (isinstance(func, ast.Attribute) and func.attr == 'fetch_data'):
                    fetch_calls.append(node)

        if len(fetch_calls) < 2:
            print(f"PRECONDITION FAIL: Expected at least 2 fetch_data calls in main.py, found {len(fetch_calls)}")
            print("REWARD: 0.0")
            return 0.0
        else:
            print("PRECONDITION OK: main.py has at least 2 fetch_data calls")
    except Exception as e:
        print(f"PRECONDITION ERROR: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: fetch_data signature includes timeout=30 (0.5 points)
    try:
        tree = ast.parse(fetcher_content)
        func_found = False
        has_timeout_param = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'fetch_data':
                func_found = True
                # Check for 'timeout' in the function's arguments with default 30
                args = node.args
                # defaults align to the end of args list; kwonlyargs have kw_defaults
                # Check regular args with defaults
                all_arg_names = [a.arg for a in args.args]
                num_defaults = len(args.defaults)
                num_args = len(args.args)
                for i, default in enumerate(args.defaults):
                    arg_index = num_args - num_defaults + i
                    arg_name = all_arg_names[arg_index]
                    if arg_name == 'timeout':
                        # Check default value is 30
                        if isinstance(default, ast.Constant) and default.value == 30:
                            has_timeout_param = True
                            break
                        elif isinstance(default, ast.Num) and default.n == 30:
                            has_timeout_param = True
                            break

                # Also check keyword-only args
                if not has_timeout_param:
                    for kw_arg, kw_default in zip(args.kwonlyargs, args.kw_defaults):
                        if kw_arg.arg == 'timeout' and kw_default is not None:
                            if isinstance(kw_default, ast.Constant) and kw_default.value == 30:
                                has_timeout_param = True
                                break
                break

        if not func_found:
            print("FAIL: Component 1 - fetch_data function not found in fetcher.py")
        elif has_timeout_param:
            print(f"PASS: Component 1 - fetch_data has timeout=30 parameter (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - fetch_data does not have timeout=30 parameter")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: requests.get call includes timeout=timeout (0.5 points)
    try:
        tree = ast.parse(fetcher_content)
        timeout_in_get_call = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'fetch_data':
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        # Check if this is requests.get(...)
                        func = child.func
                        is_requests_get = False
                        if isinstance(func, ast.Attribute) and func.attr == 'get':
                            if isinstance(func.value, ast.Name) and func.value.id == 'requests':
                                is_requests_get = True
                            elif isinstance(func.value, ast.Attribute):
                                is_requests_get = True

                        if is_requests_get:
                            # Check for timeout keyword argument
                            for kw in child.keywords:
                                if kw.arg == 'timeout':
                                    # The value should reference the timeout parameter
                                    if isinstance(kw.value, ast.Name) and kw.value.id == 'timeout':
                                        timeout_in_get_call = True
                                    elif isinstance(kw.value, ast.Constant):
                                        # Also accept a literal 30
                                        timeout_in_get_call = True
                                    break
                break

        if timeout_in_get_call:
            print(f"PASS: Component 2 - requests.get call includes timeout argument (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - requests.get call does not include timeout argument")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
