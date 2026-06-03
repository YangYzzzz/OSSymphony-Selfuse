"""
Reward Script: DDD structure for e-commerce domain in VSCode
Task ID: vscode_gf6_078
Domain: vscode
Scoring:
  C1: src/domain/shared/base.py with Entity + AggregateRoot (0.10)
  C2: src/domain/user/entity.py with User, Email, UserId (0.15)
  C3: src/domain/user/repository.py with AbstractUserRepository (abc.ABC) (0.10)
  C4: src/domain/user/events.py with >= 2 event classes (0.10)
  C5: src/application/user/commands.py with handler classes (0.10)
  C6: src/application/user/queries.py with handler classes (0.10)
  C7: src/infrastructure/db/user_repository.py implementing AbstractUserRepository (0.10)
  C8: tests/domain/test_user.py exists with >= 5 test functions (0.10)
  C9: pytest tests/domain/ passes all tests (0.10)
  C10: .vscode/tasks.json distinguishes unit and integration test tasks (0.05)
"""

import os
import ast
import json

WORKDIR = '/home/user/projects/python-ddd'
TASK_ID = 'vscode_gf6_078'


def _count_classes_with_base(filepath, base_name):
    """Count classes that inherit from base_name in a Python file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    name = None
                    if isinstance(base, ast.Name):
                        name = base.id
                    elif isinstance(base, ast.Attribute):
                        name = base.attr
                    if name == base_name:
                        count += 1
        return count
    except Exception:
        return 0


def _get_class_names(filepath):
    """Get all class names defined in a Python file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    except Exception:
        return []


def _get_function_names(filepath):
    """Get all function/method names defined in a Python file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        funcs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                funcs.append(node.name)
        return funcs
    except Exception:
        return []


def _file_has_import(filepath, module_name):
    """Check if a file imports from a given module (substring match in import statements)."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and module_name in node.module:
                return True
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if module_name in alias.name:
                        return True
        return False
    except Exception:
        return False


def _file_contains_string(filepath, target):
    """Check if file source contains a target string."""
    try:
        with open(filepath, 'r') as f:
            return target in f.read()
    except Exception:
        return False


def verify_task():
    total_score = 0.0

    # Component 1: src/domain/shared/base.py with Entity + AggregateRoot (0.10)
    try:
        base_path = os.path.join(WORKDIR, 'src', 'domain', 'shared', 'base.py')
        if not os.path.isfile(base_path):
            print("FAIL: C1 - src/domain/shared/base.py does not exist")
        else:
            classes = _get_class_names(base_path)
            has_entity = any('Entity' in c for c in classes)
            has_aggregate = any('AggregateRoot' in c or 'Aggregate' in c for c in classes)
            if has_entity and has_aggregate:
                print(f"PASS: C1 - base.py has Entity and AggregateRoot classes ({classes}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: C1 - Expected Entity and AggregateRoot classes, found: {classes}")
    except Exception as e:
        print(f"ERROR: C1 - {e}")

    # Component 2: src/domain/user/entity.py with User, Email, UserId (0.15)
    try:
        entity_path = os.path.join(WORKDIR, 'src', 'domain', 'user', 'entity.py')
        if not os.path.isfile(entity_path):
            print("FAIL: C2 - src/domain/user/entity.py does not exist")
        else:
            classes = _get_class_names(entity_path)
            class_lower = [c.lower() for c in classes]
            has_user = any('user' == c for c in class_lower)
            has_email = any('email' == c for c in class_lower)
            has_userid = any('userid' == c for c in class_lower)
            found = sum([has_user, has_email, has_userid])
            if found == 3:
                print(f"PASS: C2 - entity.py has User, Email, UserId ({classes}) (0.15 pts)")
                total_score += 0.15
            elif found >= 2:
                print(f"PARTIAL: C2 - entity.py has {found}/3 required classes ({classes}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: C2 - Expected User, Email, UserId; found: {classes}")
    except Exception as e:
        print(f"ERROR: C2 - {e}")

    # Component 3: src/domain/user/repository.py with AbstractUserRepository using abc.ABC (0.10)
    try:
        repo_path = os.path.join(WORKDIR, 'src', 'domain', 'user', 'repository.py')
        if not os.path.isfile(repo_path):
            print("FAIL: C3 - src/domain/user/repository.py does not exist")
        else:
            classes = _get_class_names(repo_path)
            has_abstract_repo = any('AbstractUserRepository' in c or 'UserRepository' in c for c in classes)
            uses_abc = _file_has_import(repo_path, 'abc')
            if has_abstract_repo and uses_abc:
                print(f"PASS: C3 - repository.py has abstract repo with abc ({classes}) (0.10 pts)")
                total_score += 0.10
            elif has_abstract_repo:
                print(f"PARTIAL: C3 - repository.py has repo class but no abc import (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C3 - Expected AbstractUserRepository class, found: {classes}")
    except Exception as e:
        print(f"ERROR: C3 - {e}")

    # Component 4: src/domain/user/events.py with >= 2 domain event classes (0.10)
    try:
        events_path = os.path.join(WORKDIR, 'src', 'domain', 'user', 'events.py')
        if not os.path.isfile(events_path):
            print("FAIL: C4 - src/domain/user/events.py does not exist")
        else:
            classes = _get_class_names(events_path)
            if len(classes) >= 2:
                print(f"PASS: C4 - events.py has {len(classes)} event classes ({classes}) (0.10 pts)")
                total_score += 0.10
            elif len(classes) == 1:
                print(f"PARTIAL: C4 - events.py has only 1 event class ({classes}) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C4 - Expected >= 2 event classes, found: {classes}")
    except Exception as e:
        print(f"ERROR: C4 - {e}")

    # Component 5: src/application/user/commands.py with handler classes (0.10)
    try:
        cmd_path = os.path.join(WORKDIR, 'src', 'application', 'user', 'commands.py')
        if not os.path.isfile(cmd_path):
            print("FAIL: C5 - src/application/user/commands.py does not exist")
        else:
            classes = _get_class_names(cmd_path)
            # Check for Register and Deactivate handlers (class names may vary)
            has_register = any('register' in c.lower() for c in classes)
            has_deactivate = any('deactivat' in c.lower() for c in classes)
            if has_register and has_deactivate:
                print(f"PASS: C5 - commands.py has register + deactivate handlers ({classes}) (0.10 pts)")
                total_score += 0.10
            elif has_register or has_deactivate:
                print(f"PARTIAL: C5 - commands.py has one handler ({classes}) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C5 - Expected register/deactivate handlers, found: {classes}")
    except Exception as e:
        print(f"ERROR: C5 - {e}")

    # Component 6: src/application/user/queries.py with handler classes (0.10)
    try:
        query_path = os.path.join(WORKDIR, 'src', 'application', 'user', 'queries.py')
        if not os.path.isfile(query_path):
            print("FAIL: C6 - src/application/user/queries.py does not exist")
        else:
            classes = _get_class_names(query_path)
            has_get_by_id = any('getuser' in c.lower() or 'get_user' in c.lower() for c in classes)
            has_list = any('list' in c.lower() for c in classes)
            if has_get_by_id and has_list:
                print(f"PASS: C6 - queries.py has GetUserById + ListUsers ({classes}) (0.10 pts)")
                total_score += 0.10
            elif has_get_by_id or has_list:
                print(f"PARTIAL: C6 - queries.py has one handler ({classes}) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C6 - Expected GetUserById/ListUsers handlers, found: {classes}")
    except Exception as e:
        print(f"ERROR: C6 - {e}")

    # Component 7: src/infrastructure/db/user_repository.py implementing AbstractUserRepository (0.10)
    try:
        infra_path = os.path.join(WORKDIR, 'src', 'infrastructure', 'db', 'user_repository.py')
        if not os.path.isfile(infra_path):
            print("FAIL: C7 - src/infrastructure/db/user_repository.py does not exist")
        else:
            classes = _get_class_names(infra_path)
            # Check it implements AbstractUserRepository (imports it)
            imports_repo = _file_has_import(infra_path, 'repository')
            has_impl_class = len(classes) >= 1
            uses_sqlalchemy = _file_has_import(infra_path, 'sqlalchemy')
            if has_impl_class and imports_repo:
                print(f"PASS: C7 - user_repository.py implements repo interface ({classes}) (0.10 pts)")
                total_score += 0.10
            elif has_impl_class:
                print(f"PARTIAL: C7 - user_repository.py has classes but may not implement interface (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C7 - Expected repository implementation, found: {classes}")
    except Exception as e:
        print(f"ERROR: C7 - {e}")

    # Component 8: tests/domain/test_user.py exists with >= 5 test functions (0.10)
    try:
        test_path = os.path.join(WORKDIR, 'tests', 'domain', 'test_user.py')
        if not os.path.isfile(test_path):
            print("FAIL: C8 - tests/domain/test_user.py does not exist")
        else:
            funcs = _get_function_names(test_path)
            test_funcs = [f for f in funcs if f.startswith('test_')]
            if len(test_funcs) >= 5:
                print(f"PASS: C8 - test_user.py has {len(test_funcs)} test functions (0.10 pts)")
                total_score += 0.10
            elif len(test_funcs) >= 3:
                print(f"PARTIAL: C8 - test_user.py has {len(test_funcs)} test functions (need >= 5) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: C8 - Expected >= 5 test functions, found {len(test_funcs)}: {test_funcs}")
    except Exception as e:
        print(f"ERROR: C8 - {e}")

    # Component 9: pytest tests/domain/ passes all tests (0.10)
    try:
        test_path = os.path.join(WORKDIR, 'tests', 'domain', 'test_user.py')
        if not os.path.isfile(test_path):
            print("FAIL: C9 - No test file to run")
        else:
            import sys
            import importlib.util
            # Run pytest programmatically
            venv_pytest = os.path.join(WORKDIR, 'venv', 'bin', 'pytest')
            if os.path.isfile(venv_pytest):
                # Use os.popen to capture pytest output (no subprocess)
                result = os.popen(f'cd {WORKDIR} && {venv_pytest} tests/domain/ -v --tb=short 2>&1').read()
                if 'passed' in result and 'failed' not in result and 'error' not in result.lower().split('passed')[0]:
                    print(f"PASS: C9 - All domain tests pass (0.10 pts)")
                    total_score += 0.10
                else:
                    # Check if some passed
                    if 'passed' in result:
                        print(f"PARTIAL: C9 - Some tests passed but not all (0.05 pts)")
                        total_score += 0.05
                    else:
                        print(f"FAIL: C9 - Tests did not pass")
                    print(f"  pytest output tail: {result[-300:]}")
            else:
                print("FAIL: C9 - pytest not found in venv")
    except Exception as e:
        print(f"ERROR: C9 - {e}")

    # Component 10: .vscode/tasks.json with unit and integration test tasks (0.05)
    try:
        tasks_path = os.path.join(WORKDIR, '.vscode', 'tasks.json')
        if not os.path.isfile(tasks_path):
            print("FAIL: C10 - .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            try:
                tasks_config = json.loads(content)
            except json.JSONDecodeError:
                # Try stripping JSONC comments
                import re
                cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_config = json.loads(cleaned)

            tasks = tasks_config.get('tasks', [])
            labels = [t.get('label', '').lower() for t in tasks]
            all_args = [' '.join(t.get('args', [])).lower() for t in tasks]
            all_cmds = [t.get('command', '').lower() for t in tasks]

            # Check for distinction between unit/domain and integration tests
            has_unit = any('unit' in l or 'domain' in l for l in labels) or \
                       any('tests/domain' in a or 'tests/unit' in a for a in all_args)
            has_integration = any('integration' in l for l in labels) or \
                              any('tests/integration' in a for a in all_args)

            if has_unit and has_integration:
                print(f"PASS: C10 - tasks.json distinguishes unit and integration tests (0.05 pts)")
                total_score += 0.05
            elif has_unit or has_integration:
                print(f"PARTIAL: C10 - tasks.json has one test type but not both (0.02 pts)")
                total_score += 0.02
            else:
                print(f"FAIL: C10 - tasks.json doesn't distinguish test layers. Labels: {labels}")
    except Exception as e:
        print(f"ERROR: C10 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
