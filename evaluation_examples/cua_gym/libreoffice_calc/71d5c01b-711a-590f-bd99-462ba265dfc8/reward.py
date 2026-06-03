"""
Reward Script: Implement HashMap class methods and run tests
Task ID: osworld_multi_apps_misc_040
Domain: os (multi-app: LibreOffice Writer + Python file editing)
Scoring:
  Component 1: hashmap_result.txt exists on Desktop (0.3 pts)
  Component 2: hashmap_result.txt contains all 8 PASSED test results (0.4 pts)
  Component 3: hashmap.py has non-stub put/get/remove implementations (0.3 pts)
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_misc_040'

RESULT_FILE = os.path.join(WORKDIR, 'hashmap_result.txt')
HASHMAP_FILE = os.path.join(WORKDIR, 'hashmap.py')

# Expected test results — all 8 tests must appear as PASSED
EXPECTED_PASSED_TESTS = [
    "Test 1 PASSED",
    "Test 2 PASSED",
    "Test 3 PASSED",
    "Test 4 PASSED",
    "Test 5 PASSED",
    "Test 6 PASSED",
    "Test 7 PASSED",
    "Test 8 PASSED",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: hashmap_result.txt exists on the Desktop (0.3 pts)
    # This file only exists after the agent runs hashmap.py; it is absent in initial_env.
    try:
        if os.path.isfile(RESULT_FILE):
            print(f"PASS: Component 1 — hashmap_result.txt exists at {RESULT_FILE} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — hashmap_result.txt not found at {RESULT_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: hashmap_result.txt contains all 8 PASSED test results (0.4 pts)
    # In initial_env the file does not exist, so this check inherently fails there.
    try:
        if os.path.isfile(RESULT_FILE):
            with open(RESULT_FILE, 'r') as f:
                content = f.read()
            passed_count = sum(1 for test in EXPECTED_PASSED_TESTS if test in content)
            if passed_count == len(EXPECTED_PASSED_TESTS):
                print(f"PASS: Component 2 — All {len(EXPECTED_PASSED_TESTS)} tests PASSED in hashmap_result.txt (0.4 pts)")
                total_score += 0.4
            else:
                missing = [t for t in EXPECTED_PASSED_TESTS if t not in content]
                print(f"FAIL: Component 2 — Only {passed_count}/{len(EXPECTED_PASSED_TESTS)} tests PASSED. Missing: {missing}")
        else:
            print("FAIL: Component 2 — hashmap_result.txt does not exist, cannot verify test results")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: hashmap.py has non-stub put/get/remove implementations (0.3 pts)
    # In initial_env all three methods contain only 'pass' (stubs). In golden_env
    # they contain real linear-probing logic. We verify that all three methods
    # have actual implementation (more than just 'pass') using AST analysis.
    try:
        import ast

        if os.path.isfile(HASHMAP_FILE):
            with open(HASHMAP_FILE, 'r') as f:
                source = f.read()

            def method_is_implemented(src, method_name):
                """
                Returns True if the method body contains actual statements
                beyond just a docstring and/or a single 'pass' statement.
                Uses Python AST to reliably skip docstrings.
                """
                try:
                    tree = ast.parse(src)
                except SyntaxError:
                    return False

                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name == method_name:
                            body = node.body
                            # Skip leading docstring (Expr node with a Constant string)
                            non_doc_body = []
                            for i, stmt in enumerate(body):
                                if i == 0 and isinstance(stmt, ast.Expr) and isinstance(getattr(stmt, 'value', None), ast.Constant) and isinstance(stmt.value.value, str):
                                    continue  # skip docstring
                                non_doc_body.append(stmt)
                            # If only 'pass' remains (or nothing), it's a stub
                            if not non_doc_body:
                                return False
                            if len(non_doc_body) == 1 and isinstance(non_doc_body[0], ast.Pass):
                                return False
                            return True
                return False

            implemented_methods = []
            for method in ['put', 'get', 'remove']:
                if method_is_implemented(source, method):
                    implemented_methods.append(method)
                else:
                    print(f"FAIL: Component 3 — method '{method}' appears to be a stub (only 'pass')")

            if len(implemented_methods) == 3:
                print(f"PASS: Component 3 — put, get, remove all implemented in hashmap.py (0.3 pts)")
                total_score += 0.3
            else:
                not_impl = [m for m in ['put', 'get', 'remove'] if m not in implemented_methods]
                print(f"FAIL: Component 3 — methods not implemented: {not_impl}")
        else:
            print(f"FAIL: Component 3 — hashmap.py not found at {HASHMAP_FILE}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
