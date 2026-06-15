"""
Reward Script: Schema migration framework on top of Alembic
Task ID: vscode_gf4_074
Domain: vscode
Scoring:
  Component 1 (0.15): venv with required packages (sqlalchemy, alembic, pytest, click)
  Component 2 (0.20): manager.py with MigrationManager class and 5 required methods
  Component 3 (0.15): validator.py detects dangerous migration operations
  Component 4 (0.10): cli.py with Click CLI commands
  Component 5 (0.15): 3 sample migrations (CREATE TABLE, ALTER TABLE, ADD INDEX)
  Component 6 (0.25): 8+ test functions that exercise migration, rollback, and validation
"""

import os
import re
import sys
import ast

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_074'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-schema-migrations')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: venv with required packages (0.15 points)
    # Initial env has no venv at all, so this fails on initial.
    try:
        venv_dir = os.path.join(PROJECT_DIR, 'venv')
        if os.path.isdir(venv_dir):
            # Find the site-packages directory
            venv_site = None
            for pyver in ['python3.10', 'python3.11', 'python3.12', 'python3.9', 'python3.8']:
                candidate = os.path.join(venv_dir, 'lib', pyver, 'site-packages')
                if os.path.isdir(candidate):
                    venv_site = candidate
                    break

            if venv_site is None:
                # Walk to find it
                for root, dirs, files in os.walk(os.path.join(venv_dir, 'lib')):
                    if os.path.basename(root) == 'site-packages':
                        venv_site = root
                        break

            required_pkgs = ['sqlalchemy', 'alembic', 'pytest', 'click']
            found_pkgs = []

            if venv_site and os.path.isdir(venv_site):
                entries = os.listdir(venv_site)
                for pkg in required_pkgs:
                    # Check for package dir or dist-info
                    pkg_dir_exists = os.path.isdir(os.path.join(venv_site, pkg))
                    dist_info_exists = any(
                        e.lower().startswith(pkg.lower()) and e.endswith('.dist-info')
                        for e in entries
                    )
                    if pkg_dir_exists or dist_info_exists:
                        found_pkgs.append(pkg)

            if len(found_pkgs) == len(required_pkgs):
                print(f"PASS: Component 1 — venv with all required packages: {found_pkgs} (0.15 pts)")
                total_score += 0.15
            else:
                missing = set(required_pkgs) - set(found_pkgs)
                print(f"FAIL: Component 1 — venv missing packages: {missing} (found: {found_pkgs})")
        else:
            print(f"FAIL: Component 1 — venv directory not found at {venv_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: manager.py with MigrationManager class and 5 required methods (0.20 points)
    # Initial env has no src/ directory at all, so this fails on initial.
    try:
        manager_path = os.path.join(PROJECT_DIR, 'src', 'migrations', 'manager.py')
        if os.path.isfile(manager_path):
            with open(manager_path, 'r') as f:
                manager_src = f.read()

            tree = ast.parse(manager_src)

            # Find MigrationManager class
            mm_class = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == 'MigrationManager':
                    mm_class = node
                    break

            if mm_class:
                required_methods = ['create_migration', 'apply_migrations',
                                    'rollback_migration', 'migration_status', 'diff_schema']
                found_methods = set()
                for node in ast.walk(mm_class):
                    if isinstance(node, ast.FunctionDef) and node.name in required_methods:
                        found_methods.add(node.name)

                if found_methods == set(required_methods):
                    print(f"PASS: Component 2 — MigrationManager has all 5 methods: {sorted(found_methods)} (0.20 pts)")
                    total_score += 0.20
                else:
                    missing = set(required_methods) - found_methods
                    print(f"FAIL: Component 2 — MigrationManager missing methods: {missing}")
            else:
                print(f"FAIL: Component 2 — MigrationManager class not found in manager.py")
        else:
            print(f"FAIL: Component 2 — manager.py not found at {manager_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: validator.py detects dangerous operations (0.15 points)
    # Checks that validator.py has validation functions and detects drop_table and column type changes.
    # Initial env has no src/ directory.
    try:
        validator_path = os.path.join(PROJECT_DIR, 'src', 'migrations', 'validator.py')
        if os.path.isfile(validator_path):
            with open(validator_path, 'r') as f:
                validator_src = f.read()

            tree = ast.parse(validator_src)

            # Check for validation function definitions
            func_names = [node.name for node in ast.walk(tree)
                          if isinstance(node, ast.FunctionDef)]

            has_validate_func = any('validate' in fn.lower() or 'is_safe' in fn.lower()
                                    for fn in func_names)

            # Must detect dangerous operations (drop_table, column type changes)
            detects_drop = ('drop_table' in validator_src.lower() or
                            'drop table' in validator_src.lower())
            detects_type_change = ('type_' in validator_src or
                                   'alter_column' in validator_src or
                                   'column type' in validator_src.lower() or
                                   'type change' in validator_src.lower())

            if has_validate_func and detects_drop and detects_type_change:
                print(f"PASS: Component 3 — validator.py detects dangerous ops "
                      f"(functions: {[f for f in func_names if 'valid' in f.lower() or 'safe' in f.lower()]}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — validator incomplete: validate_func={has_validate_func}, "
                      f"detects_drop={detects_drop}, detects_type_change={detects_type_change}")
        else:
            print(f"FAIL: Component 3 — validator.py not found at {validator_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: cli.py with Click CLI commands (0.10 points)
    # Initial env has no src/ directory.
    try:
        cli_path = os.path.join(PROJECT_DIR, 'src', 'cli.py')
        if os.path.isfile(cli_path):
            with open(cli_path, 'r') as f:
                cli_src = f.read()

            has_click_import = 'import click' in cli_src
            has_click_group = ('@click.group' in cli_src or 'click.group' in cli_src)
            has_click_command = ('@cli.command' in cli_src or '@click.command' in cli_src)

            # Count migration-related CLI commands
            migration_commands = 0
            for cmd_name in ['create', 'apply', 'rollback', 'status', 'validate', 'diff',
                             'migrate', 'upgrade', 'downgrade']:
                if re.search(rf'def\s+{cmd_name}\s*\(', cli_src):
                    migration_commands += 1

            if has_click_import and has_click_group and has_click_command and migration_commands >= 3:
                print(f"PASS: Component 4 — cli.py has Click CLI with {migration_commands} commands (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — cli.py: click_import={has_click_import}, "
                      f"group={has_click_group}, command={has_click_command}, cmds={migration_commands}")
        else:
            print(f"FAIL: Component 4 — cli.py not found at {cli_path}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 3 sample migrations (CREATE TABLE, ALTER TABLE, ADD INDEX) (0.15 points)
    # Initial env has an empty alembic/ directory with no versions subdirectory.
    try:
        versions_dir = os.path.join(PROJECT_DIR, 'alembic', 'versions')
        if os.path.isdir(versions_dir):
            migration_files = [f for f in os.listdir(versions_dir)
                               if f.endswith('.py') and not f.startswith('__')]

            if len(migration_files) >= 3:
                # Read all migration files and check for the 3 operation types
                all_migration_src = ''
                for mf in migration_files:
                    with open(os.path.join(versions_dir, mf), 'r') as f:
                        all_migration_src += f.read() + '\n'

                has_create_table = 'create_table' in all_migration_src
                has_alter = ('add_column' in all_migration_src or
                             'alter_column' in all_migration_src or
                             'drop_column' in all_migration_src)
                has_index = 'create_index' in all_migration_src

                if has_create_table and has_alter and has_index:
                    print(f"PASS: Component 5 — {len(migration_files)} migrations with CREATE TABLE, "
                          f"ALTER TABLE, ADD INDEX (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 5 — Migration ops: create_table={has_create_table}, "
                          f"alter={has_alter}, index={has_index}")
            else:
                print(f"FAIL: Component 5 — Expected >= 3 migration files, found {len(migration_files)}")
        else:
            print(f"FAIL: Component 5 — versions directory not found at {versions_dir}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 8+ test functions covering migration, rollback, and validation (0.25 points)
    # Verifies tests exist with proper structure. Initial env has no tests/ directory.
    try:
        test_dir = os.path.join(PROJECT_DIR, 'tests')
        # Find test files
        test_files = []
        if os.path.isdir(test_dir):
            for root, dirs, files in os.walk(test_dir):
                for f in files:
                    if f.startswith('test_') and f.endswith('.py'):
                        test_files.append(os.path.join(root, f))

        if test_files:
            total_test_funcs = []
            has_migration_test = False
            has_rollback_test = False
            has_validation_test = False

            for tf in test_files:
                with open(tf, 'r') as f:
                    test_src = f.read()

                # Count test functions using AST
                try:
                    tree = ast.parse(test_src)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                            total_test_funcs.append(node.name)
                            name_lower = node.name.lower()
                            if 'apply' in name_lower or 'migrate' in name_lower or 'upgrade' in name_lower:
                                has_migration_test = True
                            if 'rollback' in name_lower or 'downgrade' in name_lower or 'revert' in name_lower:
                                has_rollback_test = True
                            if 'valid' in name_lower or 'safe' in name_lower or 'danger' in name_lower:
                                has_validation_test = True
                except SyntaxError:
                    pass

                # Also check by source content for coverage areas
                if 'apply_migration' in test_src or 'upgrade' in test_src:
                    has_migration_test = True
                if 'rollback' in test_src or 'downgrade' in test_src:
                    has_rollback_test = True
                if 'validate' in test_src or 'is_safe' in test_src or 'dangerous' in test_src:
                    has_validation_test = True

            num_tests = len(total_test_funcs)
            covers_key_areas = has_migration_test and has_rollback_test and has_validation_test

            if num_tests >= 8 and covers_key_areas:
                print(f"PASS: Component 6 — {num_tests} test functions covering migration, rollback, "
                      f"and validation (0.25 pts)")
                total_score += 0.25
            elif num_tests >= 8:
                # Has enough tests but missing coverage area
                print(f"PARTIAL: Component 6 — {num_tests} tests but incomplete coverage: "
                      f"migration={has_migration_test}, rollback={has_rollback_test}, "
                      f"validation={has_validation_test} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — Only {num_tests} test functions (need >= 8), "
                      f"coverage: migration={has_migration_test}, rollback={has_rollback_test}, "
                      f"validation={has_validation_test}")
        else:
            print(f"FAIL: Component 6 — No test files found in {test_dir}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
