"""
Reward Script: Pipeline DSL with operator overloading in VSCode
Task ID: vscode_gf4_094
Domain: libreoffice_calc (actually vscode/python project)
Scoring:
  C1: Virtual environment with required packages (0.15)
  C2: stage.py - Stage class with __or__ pipe operator (0.15)
  C3: pipeline.py - Pipeline with branch/merge/run (0.15)
  C4: decorators.py - @stage decorator with retry/timeout (0.10)
  C5: visualization.py - Graphviz DOT rendering (0.10)
  C6: monitoring.py - Per-stage timing and success tracking (0.10)
  C7: 15+ tests that pass (0.25)
"""

import os
import ast
import sys
import importlib.util

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_094'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-pipeline-dsl')
SRC_DSL = os.path.join(PROJECT, 'src', 'dsl')
VENV = os.path.join(PROJECT, 'venv')


def check_venv_packages():
    """Check venv exists and has pydantic, rich, pytest, graphviz installed."""
    pip_path = os.path.join(VENV, 'bin', 'pip')
    if not os.path.isfile(pip_path):
        return False, "venv/bin/pip not found"

    # Check installed packages by looking at site-packages dist-info dirs
    site_pkgs = None
    lib_dir = os.path.join(VENV, 'lib')
    if os.path.isdir(lib_dir):
        for d in os.listdir(lib_dir):
            sp = os.path.join(lib_dir, d, 'site-packages')
            if os.path.isdir(sp):
                site_pkgs = sp
                break

    if not site_pkgs:
        return False, "site-packages not found in venv"

    required = ['pydantic', 'rich', 'pytest', 'graphviz']
    entries = os.listdir(site_pkgs)
    missing = []
    for pkg in required:
        # Look for dist-info directory matching the package name
        found = any(
            e.lower().startswith(pkg.lower()) and ('.dist-info' in e or e == pkg or e == pkg + '.py')
            for e in entries
        )
        if not found:
            # Also check if the package directory itself exists
            if not os.path.isdir(os.path.join(site_pkgs, pkg)):
                missing.append(pkg)

    if missing:
        return False, f"Missing packages: {missing}"
    return True, "All required packages found"


def check_module_ast(filepath, required_classes=None, required_functions=None, required_methods=None):
    """Parse a Python file AST and check for required classes, functions, methods."""
    if not os.path.isfile(filepath):
        return False, f"File not found: {filepath}"

    try:
        with open(filepath, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        return False, f"Cannot parse {filepath}: {e}"

    # Collect class names and their methods
    classes = {}
    functions = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = set()
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.add(item.name)
            classes[node.name] = methods
        if isinstance(node, ast.FunctionDef) and not isinstance(getattr(node, '_parent', None), ast.ClassDef):
            functions.add(node.name)

    # Also collect top-level functions more carefully
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            functions.add(node.name)

    issues = []
    if required_classes:
        for cls_name in required_classes:
            if cls_name not in classes:
                issues.append(f"Missing class: {cls_name}")

    if required_functions:
        for fn_name in required_functions:
            if fn_name not in functions:
                issues.append(f"Missing function: {fn_name}")

    if required_methods:
        for cls_name, method_name in required_methods:
            if cls_name not in classes:
                issues.append(f"Missing class {cls_name} (needed for method {method_name})")
            elif method_name not in classes[cls_name]:
                issues.append(f"Missing method {cls_name}.{method_name}")

    if issues:
        return False, "; ".join(issues)
    return True, "All required elements found"


def count_and_run_tests():
    """Count test functions and attempt to run them via pytest."""
    tests_dir = os.path.join(PROJECT, 'tests')
    if not os.path.isdir(tests_dir):
        return 0, False, "tests/ directory not found"

    # Count test functions by parsing AST of test files
    test_count = 0
    test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]
    for tf in test_files:
        tf_path = os.path.join(tests_dir, tf)
        try:
            with open(tf_path, 'r') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_count += 1
        except Exception:
            pass

    # Try running pytest programmatically (no subprocess)
    pytest_passed = False
    venv_site = None
    lib_dir = os.path.join(VENV, 'lib')
    if os.path.isdir(lib_dir):
        for d in os.listdir(lib_dir):
            sp = os.path.join(lib_dir, d, 'site-packages')
            if os.path.isdir(sp):
                venv_site = sp
                break

    if not venv_site:
        return test_count, False, "venv site-packages not found"

    # Add venv site-packages and project src to sys.path for imports
    original_path = sys.path.copy()
    if venv_site not in sys.path:
        sys.path.insert(0, venv_site)
    src_path = os.path.join(PROJECT, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    if PROJECT not in sys.path:
        sys.path.insert(0, PROJECT)

    try:
        import pytest as _pytest
        original_cwd = os.getcwd()
        os.chdir(PROJECT)
        rc = _pytest.main([tests_dir, '-v', '--tb=short', '-q'])
        os.chdir(original_cwd)
        pytest_passed = (rc == 0)
        if not pytest_passed:
            return test_count, False, f"pytest failed (rc={rc})"
    except Exception as e:
        return test_count, False, f"pytest execution error: {e}"
    finally:
        sys.path[:] = original_path

    return test_count, pytest_passed, f"{test_count} tests found, pytest passed"


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: Virtual environment with required packages (0.15 points)
    try:
        passed, detail = check_venv_packages()
        if passed:
            print(f"PASS: Component 1 - Venv with required packages ({detail}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Venv packages: {detail}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: stage.py with Stage class and __or__ operator (0.15 points)
    try:
        stage_path = os.path.join(SRC_DSL, 'stage.py')
        passed, detail = check_module_ast(
            stage_path,
            required_classes=['Stage'],
            required_methods=[('Stage', '__or__'), ('Stage', '__init__')]
        )
        if passed:
            print(f"PASS: Component 2 - stage.py has Stage with __or__ (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - stage.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: pipeline.py with Pipeline class having branch/merge/run (0.15 points)
    try:
        pipeline_path = os.path.join(SRC_DSL, 'pipeline.py')
        passed, detail = check_module_ast(
            pipeline_path,
            required_classes=['Pipeline'],
            required_methods=[
                ('Pipeline', 'branch'),
                ('Pipeline', 'merge'),
                ('Pipeline', 'run')
            ]
        )
        if passed:
            print(f"PASS: Component 3 - pipeline.py has Pipeline with branch/merge/run (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - pipeline.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: decorators.py with @stage decorator (0.10 points)
    try:
        dec_path = os.path.join(SRC_DSL, 'decorators.py')
        passed, detail = check_module_ast(
            dec_path,
            required_functions=['stage']
        )
        if passed:
            # Also verify it's a decorator factory (takes name param, returns decorator)
            with open(dec_path, 'r') as f:
                src = f.read()
            # Check that 'retry' and 'timeout' appear as parameters
            if 'retry' in src and 'timeout' in src:
                print(f"PASS: Component 4 - decorators.py has @stage with retry/timeout (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 - decorators.py missing retry/timeout params")
        else:
            print(f"FAIL: Component 4 - decorators.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: visualization.py with DOT format rendering (0.10 points)
    try:
        viz_path = os.path.join(SRC_DSL, 'visualization.py')
        if not os.path.isfile(viz_path):
            print(f"FAIL: Component 5 - visualization.py not found")
        else:
            with open(viz_path, 'r') as f:
                src = f.read()
            # Must contain graphviz DOT format markers
            has_digraph = 'digraph' in src.lower() or 'dot' in src.lower()
            has_arrow = '->' in src
            tree = ast.parse(src)
            has_function = any(
                isinstance(n, ast.FunctionDef) for n in ast.walk(tree)
            )
            if has_function and (has_digraph or has_arrow):
                print(f"PASS: Component 5 - visualization.py renders DOT format (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 - visualization.py missing DOT format content (digraph={has_digraph}, arrow={has_arrow}, func={has_function})")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: monitoring.py with per-stage timing and success tracking (0.10 points)
    try:
        mon_path = os.path.join(SRC_DSL, 'monitoring.py')
        if not os.path.isfile(mon_path):
            print(f"FAIL: Component 6 - monitoring.py not found")
        else:
            with open(mon_path, 'r') as f:
                src = f.read()
            tree = ast.parse(src)
            class_names = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            # Must have at least one class and track time/success
            has_class = len(class_names) > 0
            has_time_tracking = any(w in src for w in ['time', 'elapsed', 'timing', 'total_time'])
            has_success_tracking = any(w in src for w in ['success', 'failure', 'success_count', 'success_rate'])
            if has_class and has_time_tracking and has_success_tracking:
                print(f"PASS: Component 6 - monitoring.py tracks timing and success (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 - monitoring.py incomplete (class={has_class}, time={has_time_tracking}, success={has_success_tracking})")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: 15+ tests that pass (0.25 points)
    try:
        test_count, pytest_passed, detail = count_and_run_tests()
        if test_count >= 15 and pytest_passed:
            print(f"PASS: Component 7 - {test_count} tests, all passing (0.25 pts)")
            total_score += 0.25
        elif test_count >= 15 and not pytest_passed:
            # Partial: tests exist but some fail
            print(f"PARTIAL: Component 7 - {test_count} tests found but pytest failed: {detail} (0.10 pts)")
            total_score += 0.10
        elif test_count > 0 and pytest_passed:
            # Partial: fewer than 15 tests but they pass
            partial = round(0.25 * (test_count / 15.0), 2)
            partial = min(partial, 0.20)  # cap at 0.20 if under 15
            print(f"PARTIAL: Component 7 - only {test_count}/15 tests, but passing ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 7 - {test_count} tests, passed={pytest_passed}: {detail}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()
