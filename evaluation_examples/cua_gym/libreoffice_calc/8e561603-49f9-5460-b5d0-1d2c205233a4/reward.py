"""
Reward Script: DI Container project verification
Task ID: vscode_gf4_053
Domain: vscode (Python project)
Scoring:
  1. venv with pytest installed (0.10)
  2. src/container.py with Container class having register/resolve/inject (0.15)
  3. src/providers.py with SingletonProvider and TransientProvider (0.10)
  4. src/decorators.py with @service, @repository, @component (0.10)
  5. examples/app.py with three-layer architecture (0.10)
  6. Container uses inspect module for type-annotation-based resolution (0.10)
  7. 12+ test functions exist (0.10)
  8. Tests pass via pytest (0.25)
"""

import os
import ast
import re
import sys

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-dependency-injection')
TASK_ID = 'vscode_gf4_053'


def count_test_functions(tests_dir):
    """Count test functions (def test_*) across all test files."""
    count = 0
    if not os.path.isdir(tests_dir):
        return 0
    for fname in os.listdir(tests_dir):
        if fname.startswith('test_') and fname.endswith('.py'):
            fpath = os.path.join(tests_dir, fname)
            try:
                with open(fpath, 'r') as f:
                    content = f.read()
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name.startswith('test_'):
                            count += 1
            except Exception:
                pass
    return count


def check_class_has_methods(filepath, class_name, method_names):
    """Check if a file contains a class with the given methods."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                found_methods = set()
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        found_methods.add(item.name)
                return all(m in found_methods for m in method_names)
    except Exception:
        return False
    return False


def check_file_has_classes(filepath, class_names):
    """Check if a file defines all listed class names."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        tree = ast.parse(content)
        defined = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                defined.add(node.name)
        return all(cn in defined for cn in class_names)
    except Exception:
        return False


def check_file_has_functions(filepath, func_names):
    """Check if a file defines all listed top-level function names."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        tree = ast.parse(content)
        defined = set()
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined.add(node.name)
        return all(fn in defined for fn in func_names)
    except Exception:
        return False


def check_file_imports(filepath, module_name):
    """Check if file imports a given module."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return module_name in content
    except Exception:
        return False


def verify_task():
    total_score = 0.0

    # Component 1: venv exists with pytest installed (0.10 points)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        # Check venv exists and has a python binary
        venv_python = None
        if os.path.isdir(venv_dir):
            for candidate in ['bin/python3', 'bin/python']:
                p = os.path.join(venv_dir, candidate)
                if os.path.exists(p):
                    venv_python = p
                    break

        if venv_python is None:
            print("FAIL: Component 1 -- venv directory not found or no python binary")
        else:
            # Check pytest is installed by looking for pytest in site-packages
            site_packages = None
            lib_dir = os.path.join(venv_dir, 'lib')
            if os.path.isdir(lib_dir):
                for d in os.listdir(lib_dir):
                    sp = os.path.join(lib_dir, d, 'site-packages')
                    if os.path.isdir(sp):
                        site_packages = sp
                        break
            pytest_found = (
                site_packages is not None
                and any(
                    entry.startswith('pytest') and ('dist-info' in entry or entry == 'pytest')
                    for entry in os.listdir(site_packages)
                )
            ) if site_packages else False
            if pytest_found:
                print("PASS: Component 1 -- venv exists with pytest installed (0.10 pts)")
                total_score += 0.10
            else:
                print("FAIL: Component 1 -- venv exists but pytest not found in site-packages")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: src/container.py with Container class having register, resolve, inject (0.15 points)
    try:
        container_path = os.path.join(PROJECT, 'src', 'container.py')
        if not os.path.isfile(container_path):
            print("FAIL: Component 2 -- src/container.py does not exist")
        elif check_class_has_methods(container_path, 'Container', ['register', 'resolve', 'inject']):
            print("PASS: Component 2 -- Container class with register/resolve/inject found (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 -- Container class missing register, resolve, or inject method")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: src/providers.py with SingletonProvider and TransientProvider (0.10 points)
    try:
        providers_path = os.path.join(PROJECT, 'src', 'providers.py')
        if not os.path.isfile(providers_path):
            print("FAIL: Component 3 -- src/providers.py does not exist")
        elif check_file_has_classes(providers_path, ['SingletonProvider', 'TransientProvider']):
            print("PASS: Component 3 -- SingletonProvider and TransientProvider found (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 3 -- Missing SingletonProvider or TransientProvider class")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: src/decorators.py with @service, @repository, @component (0.10 points)
    try:
        decorators_path = os.path.join(PROJECT, 'src', 'decorators.py')
        if not os.path.isfile(decorators_path):
            print("FAIL: Component 4 -- src/decorators.py does not exist")
        elif check_file_has_functions(decorators_path, ['service', 'repository', 'component']):
            print("PASS: Component 4 -- service, repository, component decorators found (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 4 -- Missing service, repository, or component function")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: examples/app.py with three-layer architecture (0.10 points)
    # Must have classes suggesting controller, service, repository layers
    try:
        app_path = os.path.join(PROJECT, 'examples', 'app.py')
        if not os.path.isfile(app_path):
            print("FAIL: Component 5 -- examples/app.py does not exist")
        else:
            with open(app_path, 'r') as f:
                app_content = f.read()
            tree = ast.parse(app_content)
            class_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_names.add(node.name.lower())

            # Check for three-layer pattern: must have classes with
            # controller/service/repository-like names
            has_controller = any('controller' in cn for cn in class_names)
            has_service = any('service' in cn for cn in class_names)
            has_repository = any('repo' in cn or 'repository' in cn for cn in class_names)

            if has_controller and has_service and has_repository:
                print("PASS: Component 5 -- three-layer architecture in examples/app.py (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 -- Missing layers. controller={has_controller}, "
                      f"service={has_service}, repository={has_repository}. Classes: {class_names}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Container uses inspect module for type-annotation-based resolution (0.10 points)
    try:
        container_path = os.path.join(PROJECT, 'src', 'container.py')
        if not os.path.isfile(container_path):
            print("FAIL: Component 6 -- src/container.py does not exist")
        else:
            uses_inspect = check_file_imports(container_path, 'inspect')
            if uses_inspect:
                # Also verify it references signature or parameters (actual type annotation resolution)
                with open(container_path, 'r') as f:
                    content = f.read()
                uses_signature = 'inspect.signature' in content or 'signature' in content
                uses_annotation = 'annotation' in content
                if uses_signature and uses_annotation:
                    print("PASS: Component 6 -- inspect module used for type-annotation resolution (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 6 -- imports inspect but missing signature/annotation usage. "
                          f"signature={uses_signature}, annotation={uses_annotation}")
            else:
                print("FAIL: Component 6 -- container.py does not import inspect module")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: 12+ test functions exist (0.10 points)
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        test_count = count_test_functions(tests_dir)
        if test_count >= 12:
            print(f"PASS: Component 7 -- {test_count} test functions found (>= 12) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 -- only {test_count} test functions found, need >= 12")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: Tests pass via pytest (0.25 points)
    try:
        # Run pytest programmatically
        venv_pytest = os.path.join(PROJECT, 'venv', 'bin', 'pytest')
        tests_dir = os.path.join(PROJECT, 'tests')

        if not os.path.isfile(venv_pytest):
            print("FAIL: Component 8 -- pytest binary not found in venv")
        elif not os.path.isdir(tests_dir):
            print("FAIL: Component 8 -- tests directory not found")
        else:
            # Use os.system to run pytest and capture exit code
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                tmp_path = tmp.name

            exit_code = os.system(
                f'cd {PROJECT} && {venv_pytest} tests/ -v > {tmp_path} 2>&1'
            )

            with open(tmp_path, 'r') as f:
                pytest_output = f.read()
            os.unlink(tmp_path)

            # Parse results
            passed_match = re.search(r'(\d+) passed', pytest_output)
            failed_match = re.search(r'(\d+) failed', pytest_output)
            passed_count = int(passed_match.group(1)) if passed_match else 0
            failed_count = int(failed_match.group(1)) if failed_match else 0

            if exit_code == 0 and passed_count >= 12 and failed_count == 0:
                print(f"PASS: Component 8 -- all {passed_count} tests passed (0.25 pts)")
                total_score += 0.25
            elif passed_count >= 12 and failed_count == 0:
                # Exit code might be non-zero for warnings etc.
                print(f"PASS: Component 8 -- {passed_count} tests passed, 0 failed (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 8 -- pytest: {passed_count} passed, {failed_count} failed, exit={exit_code}")
                print(f"  pytest output: {pytest_output[-500:]}")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
