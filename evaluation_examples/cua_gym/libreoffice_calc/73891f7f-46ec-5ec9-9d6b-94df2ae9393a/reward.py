"""
Reward Script: Complete matrix_multiply.py and capture result to result_matrix.txt
Task ID: osworld_multi_apps_vscode_run_capture_004
Domain: multi_apps / vscode / os
Scoring:
  Component 1 (0.40): result_matrix.txt exists and contains the correct matrix product
  Component 2 (0.35): matrix_multiply.py has a working multiply_matrices implementation (not just 'pass')
  Component 3 (0.25): multiply_matrices function correctly computes the matrix product when called
"""

import os
import ast

DESKTOP = '/home/user/Desktop'
SCRIPT_PATH = os.path.join(DESKTOP, 'matrix_multiply.py')
RESULT_PATH = os.path.join(DESKTOP, 'result_matrix.txt')
MATRIX_A_PATH = os.path.join(DESKTOP, 'matrix_a.txt')
MATRIX_B_PATH = os.path.join(DESKTOP, 'matrix_b.txt')

TASK_ID = 'osworld_multi_apps_vscode_run_capture_004'


def read_matrix_from_file(filepath):
    """Read a matrix from a comma-separated text file."""
    matrix = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                row = [int(x) for x in line.split(',')]
                matrix.append(row)
    return matrix


def expected_matrix_product(a, b):
    """Compute expected matrix product to verify result_matrix.txt."""
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])
    if cols_a != rows_b:
        return None
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    return result


def has_real_implementation(script_path):
    """
    Check if multiply_matrices in the given script has a real implementation.
    Returns (found: bool, implemented: bool)
    """
    with open(script_path, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'multiply_matrices':
            non_trivial = []
            for stmt in node.body:
                if isinstance(stmt, ast.Pass):
                    continue
                if isinstance(stmt, ast.Return) and (
                    stmt.value is None or
                    (isinstance(stmt.value, ast.Constant) and stmt.value.value is None)
                ):
                    continue
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                    # Docstring — skip
                    continue
                non_trivial.append(stmt)
            return (True, len(non_trivial) >= 2)
    return (False, False)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: check that matrix input files exist ---
    if not os.path.isfile(MATRIX_A_PATH) or not os.path.isfile(MATRIX_B_PATH):
        print("CRITICAL: Input matrix files missing; cannot verify task.")
        print("REWARD: 0.0")
        return 0.0

    # Compute expected result from input files
    try:
        mat_a = read_matrix_from_file(MATRIX_A_PATH)
        mat_b = read_matrix_from_file(MATRIX_B_PATH)
        expected = expected_matrix_product(mat_a, mat_b)
        if expected is None:
            print("CRITICAL: Matrix dimensions incompatible; cannot compute expected result.")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read input matrices: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: result_matrix.txt exists and has correct content (0.40 points) ---
    # This FAILS on initial_env (file absent) and PASSES on golden_env (file has correct values)
    try:
        if not os.path.isfile(RESULT_PATH):
            print("FAIL: Component 1 — result_matrix.txt does not exist on Desktop")
        else:
            actual_result = read_matrix_from_file(RESULT_PATH)
            if actual_result == expected:
                print(f"PASS: Component 1 — result_matrix.txt contains correct matrix product (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 — result_matrix.txt content incorrect. Expected {expected}, found {actual_result}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: multiply_matrices function in matrix_multiply.py is implemented (0.35 points) ---
    # This FAILS on initial_env (function is a stub with pass) and PASSES on golden_env (full implementation)
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print("FAIL: Component 2 — matrix_multiply.py does not exist on Desktop")
        else:
            func_found, func_implemented = has_real_implementation(SCRIPT_PATH)
            if not func_found:
                print("FAIL: Component 2 — multiply_matrices function not found in matrix_multiply.py")
            elif func_found and not func_implemented:
                print("FAIL: Component 2 — multiply_matrices function is still a stub (only pass/return None)")
            elif func_found and func_implemented:
                print(f"PASS: Component 2 — multiply_matrices has a real implementation (0.35 pts)")
                total_score += 0.35
    except SyntaxError as e:
        print(f"FAIL: Component 2 — matrix_multiply.py has syntax errors: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: multiply_matrices function computes correct matrix product (0.25 points) ---
    # This FAILS on initial_env (stub returns None) and PASSES on golden_env (correct result)
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print("FAIL: Component 3 — matrix_multiply.py does not exist on Desktop")
        else:
            import importlib.util
            spec = importlib.util.spec_from_file_location("matrix_multiply_test", SCRIPT_PATH)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            result = mod.multiply_matrices(mat_a, mat_b)
            if result is None:
                print("FAIL: Component 3 — multiply_matrices returned None (stub or dimension mismatch)")
            elif result == expected:
                print(f"PASS: Component 3 — multiply_matrices returns correct result {result} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — multiply_matrices returned {result}, expected {expected}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
