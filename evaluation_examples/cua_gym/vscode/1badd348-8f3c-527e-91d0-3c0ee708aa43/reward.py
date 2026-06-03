"""
Reward Script: Build a minimal Python ORM framework with fields, model, connection pool, query builder, and 15+ tests.
Task ID: vscode_gf4_046
Domain: vscode
Scoring:
  Component 1: venv/ exists with pytest installed             (0.10)
  Component 2: fields.py has 5 field types with validation    (0.20)
  Component 3: model.py has Model with CRUD methods           (0.20)
  Component 4: connection.py has ConnectionPool + ctx mgr     (0.10)
  Component 5: query.py has QueryBuilder fluent interface      (0.10)
  Component 6: 15+ test functions exist                        (0.10)
  Component 7: All pytest tests pass                           (0.20)
"""

import os
import ast
import sys
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-orm-framework')
SRC_ORM = os.path.join(PROJECT, 'src', 'orm')


def count_test_functions(test_dir):
    """Count test functions (def test_*) and test methods in test classes across all .py files."""
    count = 0
    if not os.path.isdir(test_dir):
        return 0
    for fname in os.listdir(test_dir):
        if not fname.endswith('.py') or fname == '__init__.py':
            continue
        fpath = os.path.join(test_dir, fname)
        try:
            with open(fpath, 'r') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                # Top-level test functions
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    count += 1
                # Test methods inside classes
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name.startswith('test_'):
                            count += 1
        except Exception:
            continue
    return count


def check_file_has_classes(filepath, required_classes):
    """Check that a file defines the given class names. Returns set of found classes."""
    found = set()
    if not os.path.isfile(filepath):
        return found
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in required_classes:
                found.add(node.name)
    except Exception:
        pass
    return found


def check_file_has_methods(filepath, class_name, required_methods):
    """Check that a class in a file defines the given method names. Returns set of found methods."""
    found = set()
    if not os.path.isfile(filepath):
        return found
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name in required_methods:
                        found.add(item.name)
    except Exception:
        pass
    return found


def check_file_contains_patterns(filepath, patterns):
    """Check that a file's source code contains certain string patterns. Returns dict of pattern->bool."""
    results = {}
    if not os.path.isfile(filepath):
        return {p: False for p in patterns}
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        for p in patterns:
            results[p] = p in content
    except Exception:
        return {p: False for p in patterns}
    return results


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # ============================================================
    # Component 1: venv/ exists with pytest installed (0.10 points)
    # ============================================================
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        # Check venv exists
        if not os.path.isdir(venv_dir):
            print("FAIL: Component 1 -- venv/ directory does not exist")
        else:
            # Check pytest is installed by looking for pytest executable or package
            pytest_found = False
            # Check for pytest binary
            for bindir in ['bin', 'Scripts']:
                pytest_bin = os.path.join(venv_dir, bindir, 'pytest')
                if os.path.isfile(pytest_bin):
                    pytest_found = True
                    break
            if not pytest_found:
                # Check for pytest in site-packages
                for root, dirs, files in os.walk(os.path.join(venv_dir, 'lib')):
                    for d in dirs:
                        if d.startswith('pytest') and '.dist-info' in d:
                            pytest_found = True
                            break
                    if pytest_found:
                        break
            if pytest_found:
                print("PASS: Component 1 -- venv/ exists with pytest installed (0.10 pts)")
                total_score += 0.10
            else:
                print("FAIL: Component 1 -- venv/ exists but pytest not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ============================================================
    # Component 2: fields.py has 5 field types with validation (0.20 points)
    # ============================================================
    try:
        fields_path = os.path.join(SRC_ORM, 'fields.py')
        if not os.path.isfile(fields_path):
            print("FAIL: Component 2 -- src/orm/fields.py does not exist")
        else:
            required_fields = {'IntegerField', 'StringField', 'BooleanField', 'FloatField', 'DateTimeField'}
            found_fields = check_file_has_classes(fields_path, required_fields)
            missing = required_fields - found_fields

            # Also check for validate method pattern (type validation)
            patterns = check_file_contains_patterns(fields_path, ['def validate', 'TypeError', 'isinstance'])
            has_validation = patterns.get('def validate', False) and (
                patterns.get('TypeError', False) or patterns.get('isinstance', False)
            )

            if len(found_fields) == 5 and has_validation:
                print(f"PASS: Component 2 -- fields.py has all 5 field types with validation (0.20 pts)")
                total_score += 0.20
            elif len(found_fields) >= 3 and has_validation:
                partial = 0.10
                print(f"PARTIAL: Component 2 -- fields.py has {len(found_fields)}/5 types (missing: {missing}) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- fields.py found {len(found_fields)}/5 types, validation={has_validation}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ============================================================
    # Component 3: model.py has Model with metaclass and CRUD (0.20 points)
    # ============================================================
    try:
        model_path = os.path.join(SRC_ORM, 'model.py')
        if not os.path.isfile(model_path):
            print("FAIL: Component 3 -- src/orm/model.py does not exist")
        else:
            # Check for Model class with key CRUD methods
            model_methods = check_file_has_methods(model_path, 'Model', {
                'save', 'find', 'find_all', 'delete', 'ddl', 'create_table'
            })
            # Check for metaclass (ModelMeta or __new__ that registers fields)
            model_classes = check_file_has_classes(model_path, {'ModelMeta', 'Model'})
            patterns = check_file_contains_patterns(model_path, ['metaclass', 'type.__new__', 'CREATE TABLE'])

            has_metaclass = 'ModelMeta' in model_classes or patterns.get('metaclass', False)
            has_ddl = 'ddl' in model_methods or patterns.get('CREATE TABLE', False)
            crud_methods = {'save', 'find', 'find_all', 'delete'}
            found_crud = crud_methods & model_methods
            has_all_crud = len(found_crud) == 4

            if 'Model' in model_classes and has_metaclass and has_ddl and has_all_crud:
                print(f"PASS: Component 3 -- model.py has Model metaclass with DDL + CRUD (0.20 pts)")
                total_score += 0.20
            elif 'Model' in model_classes and len(found_crud) >= 2:
                partial = 0.10
                missing_crud = crud_methods - found_crud
                print(f"PARTIAL: Component 3 -- Model found but incomplete: metaclass={has_metaclass}, ddl={has_ddl}, missing_crud={missing_crud} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- Model={('Model' in model_classes)}, metaclass={has_metaclass}, crud={found_crud}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ============================================================
    # Component 4: connection.py has ConnectionPool + context manager (0.10 points)
    # ============================================================
    try:
        conn_path = os.path.join(SRC_ORM, 'connection.py')
        if not os.path.isfile(conn_path):
            print("FAIL: Component 4 -- src/orm/connection.py does not exist")
        else:
            conn_classes = check_file_has_classes(conn_path, {'ConnectionPool'})
            conn_patterns = check_file_contains_patterns(conn_path, [
                'contextmanager', 'sqlite3', 'acquire', 'release'
            ])
            # Alternative: check for __enter__/__exit__ or @contextmanager
            has_ctx = conn_patterns.get('contextmanager', False)
            conn_methods = check_file_has_methods(conn_path, 'ConnectionPool', {'connection', 'acquire', 'release'})
            has_ctx = has_ctx or 'connection' in conn_methods

            if 'ConnectionPool' in conn_classes and has_ctx:
                print(f"PASS: Component 4 -- connection.py has ConnectionPool with context manager (0.10 pts)")
                total_score += 0.10
            elif 'ConnectionPool' in conn_classes:
                partial = 0.05
                print(f"PARTIAL: Component 4 -- ConnectionPool found but no context manager ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- ConnectionPool not found in connection.py")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # ============================================================
    # Component 5: query.py has QueryBuilder with fluent interface (0.10 points)
    # ============================================================
    try:
        query_path = os.path.join(SRC_ORM, 'query.py')
        if not os.path.isfile(query_path):
            print("FAIL: Component 5 -- src/orm/query.py does not exist")
        else:
            qb_classes = check_file_has_classes(query_path, {'QueryBuilder'})
            qb_methods = check_file_has_methods(query_path, 'QueryBuilder', {
                'select', 'where', 'order_by', 'limit', 'execute'
            })
            required_qb = {'select', 'where', 'order_by', 'limit', 'execute'}
            found_qb = required_qb & qb_methods

            if 'QueryBuilder' in qb_classes and len(found_qb) == 5:
                print(f"PASS: Component 5 -- query.py has QueryBuilder with full fluent API (0.10 pts)")
                total_score += 0.10
            elif 'QueryBuilder' in qb_classes and len(found_qb) >= 3:
                partial = 0.05
                print(f"PARTIAL: Component 5 -- QueryBuilder has {len(found_qb)}/5 methods ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- QueryBuilder={'QueryBuilder' in qb_classes}, methods={found_qb}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # ============================================================
    # Component 6: 15+ test functions exist (0.10 points)
    # ============================================================
    try:
        test_dir = os.path.join(PROJECT, 'tests')
        if not os.path.isdir(test_dir):
            print("FAIL: Component 6 -- tests/ directory does not exist")
        else:
            test_count = count_test_functions(test_dir)
            if test_count >= 15:
                print(f"PASS: Component 6 -- {test_count} test functions found (>= 15) (0.10 pts)")
                total_score += 0.10
            elif test_count >= 8:
                partial = 0.05
                print(f"PARTIAL: Component 6 -- {test_count} test functions found (>= 8 but < 15) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 -- only {test_count} test functions found (need >= 15)")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # ============================================================
    # Component 7: All pytest tests pass (0.20 points)
    # ============================================================
    try:
        # We need to actually run pytest on the project
        # Use the venv pytest if available, otherwise system pytest
        venv_pytest = os.path.join(PROJECT, 'venv', 'bin', 'pytest')
        test_dir = os.path.join(PROJECT, 'tests')

        if not os.path.isfile(venv_pytest):
            print("FAIL: Component 7 -- venv pytest not found, cannot run tests")
        elif not os.path.isdir(test_dir):
            print("FAIL: Component 7 -- tests/ directory not found")
        else:
            # Run pytest and capture result
            import json as _json
            exit_code = os.system(
                f'cd {PROJECT} && {venv_pytest} tests/ --tb=short -q > /tmp/pytest_output.txt 2>&1'
            )
            try:
                with open('/tmp/pytest_output.txt', 'r') as f:
                    pytest_output = f.read()
            except Exception:
                pytest_output = ''

            print(f"  pytest output: {pytest_output.strip()}")

            if exit_code == 0:
                # Parse number of passed tests from output
                match = re.search(r'(\d+) passed', pytest_output)
                if match:
                    passed = int(match.group(1))
                    print(f"PASS: Component 7 -- pytest: {passed} tests passed, exit code 0 (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"PASS: Component 7 -- pytest exited 0 (0.20 pts)")
                    total_score += 0.20
            else:
                # Check for partial pass
                match_passed = re.search(r'(\d+) passed', pytest_output)
                match_failed = re.search(r'(\d+) failed', pytest_output)
                passed = int(match_passed.group(1)) if match_passed else 0
                failed = int(match_failed.group(1)) if match_failed else 0
                total_tests = passed + failed
                if total_tests > 0 and passed / total_tests >= 0.7:
                    partial = 0.10
                    print(f"PARTIAL: Component 7 -- pytest: {passed}/{total_tests} passed ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 7 -- pytest failed: {passed} passed, {failed} failed")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
