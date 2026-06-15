"""
Reward Script: SQL Query Optimizer project in VSCode
Task ID: vscode_gf4_091
Domain: vscode
Scoring:
  Component 1 (0.15): venv with sqlparse, networkx, pytest, pydantic
  Component 2 (0.15): parser.py with LogicalPlan and SQLParser classes
  Component 3 (0.20): rules.py with 4 optimization rule classes
  Component 4 (0.15): planner.py with PhysicalPlanner and cost estimation
  Component 5 (0.10): executor.py with Executor class (SQLite execution)
  Component 6 (0.25): 12+ tests passing via pytest
"""

import os
import ast
import sys
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-query-optimizer')
SRC_OPT = os.path.join(PROJECT, 'src', 'optimizer')


def get_classes_and_funcs(filepath):
    """Parse a Python file and return sets of class names and function names."""
    with open(filepath) as f:
        tree = ast.parse(f.read())
    classes = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
    funcs = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    return classes, funcs


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: venv exists with required packages (0.15 points)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        if not os.path.isdir(venv_dir):
            print("FAIL: Component 1 — venv/ directory does not exist")
        else:
            # Check installed packages by looking at site-packages dist-info dirs
            site_packages = None
            for root, dirs, files in os.walk(os.path.join(venv_dir, 'lib')):
                if 'site-packages' in dirs:
                    site_packages = os.path.join(root, 'site-packages')
                    break
            if site_packages is None:
                print("FAIL: Component 1 — venv site-packages not found")
            else:
                pkg_dirs = os.listdir(site_packages)
                required = ['sqlparse', 'networkx', 'pytest', 'pydantic']
                found = []
                for pkg in required:
                    # Check for dist-info directory containing package name
                    if any(d.lower().startswith(pkg) and '.dist-info' in d for d in pkg_dirs):
                        found.append(pkg)
                    elif any(d.lower() == pkg for d in pkg_dirs):
                        found.append(pkg)

                if len(found) == 4:
                    print(f"PASS: Component 1 — venv has all 4 packages: {found} (0.15 pts)")
                    total_score += 0.15
                else:
                    missing = set(required) - set(found)
                    print(f"FAIL: Component 1 — missing packages: {missing} (found: {found})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: parser.py with LogicalPlan and SQLParser (0.15 points)
    try:
        parser_path = os.path.join(SRC_OPT, 'parser.py')
        if not os.path.isfile(parser_path):
            print("FAIL: Component 2 — src/optimizer/parser.py does not exist")
        else:
            classes, funcs = get_classes_and_funcs(parser_path)
            has_logical_plan = any('logicalplan' in c.lower() or 'logical_plan' in c.lower() for c in classes)
            has_parser = any('parser' in c.lower() for c in classes)
            has_parse_func = any('parse' in f.lower() for f in funcs)

            if has_logical_plan and (has_parser or has_parse_func):
                print(f"PASS: Component 2 — parser.py has LogicalPlan and parser classes={classes} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — parser.py missing key classes. Found classes={classes}, funcs={funcs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: rules.py with 4 optimization rules (0.20 points)
    try:
        rules_path = os.path.join(SRC_OPT, 'rules.py')
        if not os.path.isfile(rules_path):
            print("FAIL: Component 3 — src/optimizer/rules.py does not exist")
        else:
            classes, funcs = get_classes_and_funcs(rules_path)
            required_rules = {
                'PredicatePushdown': False,
                'ProjectionPushdown': False,
                'JoinReordering': False,
                'ConstantFolding': False,
            }
            for cls_name in classes:
                lower = cls_name.lower()
                if 'predicatepush' in lower or 'predicate_push' in lower:
                    required_rules['PredicatePushdown'] = True
                if 'projectionpush' in lower or 'projection_push' in lower:
                    required_rules['ProjectionPushdown'] = True
                if 'joinreorder' in lower or 'join_reorder' in lower:
                    required_rules['JoinReordering'] = True
                if 'constantfold' in lower or 'constant_fold' in lower:
                    required_rules['ConstantFolding'] = True

            found_count = sum(required_rules.values())
            if found_count == 4:
                print(f"PASS: Component 3 — rules.py has all 4 optimization rules (0.20 pts)")
                total_score += 0.20
            elif found_count >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 3 — rules.py has {found_count}/4 rules ({partial} pts). Missing: {[k for k,v in required_rules.items() if not v]}")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — rules.py has {found_count}/4 rules. Missing: {[k for k,v in required_rules.items() if not v]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: planner.py with PhysicalPlanner and cost estimation (0.15 points)
    try:
        planner_path = os.path.join(SRC_OPT, 'planner.py')
        if not os.path.isfile(planner_path):
            print("FAIL: Component 4 — src/optimizer/planner.py does not exist")
        else:
            classes, funcs = get_classes_and_funcs(planner_path)
            with open(planner_path) as f:
                content = f.read().lower()

            has_physical_planner = any('physicalplanner' in c.lower() or 'physical_planner' in c.lower() for c in classes)
            has_physical_plan = any('physicalplan' in c.lower() or 'physical_plan' in c.lower() for c in classes)
            has_cost = 'cost' in content

            if has_physical_planner and has_cost:
                print(f"PASS: Component 4 — planner.py has PhysicalPlanner with cost estimation (0.15 pts)")
                total_score += 0.15
            elif has_physical_plan and has_cost:
                print(f"PASS: Component 4 — planner.py has PhysicalPlan with cost estimation (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — planner.py missing PhysicalPlanner or cost. classes={classes}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: executor.py with Executor class using SQLite (0.10 points)
    try:
        executor_path = os.path.join(SRC_OPT, 'executor.py')
        if not os.path.isfile(executor_path):
            print("FAIL: Component 5 — src/optimizer/executor.py does not exist")
        else:
            classes, funcs = get_classes_and_funcs(executor_path)
            with open(executor_path) as f:
                content = f.read()

            has_executor = any('executor' in c.lower() for c in classes)
            has_sqlite = 'sqlite' in content.lower()

            if has_executor and has_sqlite:
                print(f"PASS: Component 5 — executor.py has Executor with SQLite support (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — executor.py missing Executor or SQLite. classes={classes}, sqlite_ref={has_sqlite}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 12+ tests defined and passing (0.25 points)
    try:
        # Find test files in tests/ dir and project root
        tests_dir = os.path.join(PROJECT, 'tests')
        test_files = []
        if os.path.isdir(tests_dir):
            for f in os.listdir(tests_dir):
                if f.startswith('test_') and f.endswith('.py'):
                    test_files.append(os.path.join(tests_dir, f))
        for f in os.listdir(PROJECT):
            fpath = os.path.join(PROJECT, f)
            if f.startswith('test_') and f.endswith('.py') and fpath not in test_files:
                test_files.append(fpath)

        if not test_files:
            print("FAIL: Component 6 — no test files found")
        else:
            # Count test functions/methods via AST
            total_test_funcs = 0
            for tf in test_files:
                try:
                    with open(tf) as fh:
                        tree = ast.parse(fh.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                            total_test_funcs += 1
                except Exception:
                    pass

            # Try running tests via pytest Python API (no subprocess)
            passed_count = 0
            try:
                # Add venv site-packages to path so imports work
                venv_sp = None
                venv_lib = os.path.join(PROJECT, 'venv', 'lib')
                if os.path.isdir(venv_lib):
                    for d in os.listdir(venv_lib):
                        sp = os.path.join(venv_lib, d, 'site-packages')
                        if os.path.isdir(sp):
                            venv_sp = sp
                            break
                if venv_sp and venv_sp not in sys.path:
                    sys.path.insert(0, venv_sp)
                # Add project root to path for src imports
                if PROJECT not in sys.path:
                    sys.path.insert(0, PROJECT)

                import pytest as _pytest
                orig_cwd = os.getcwd()
                os.chdir(PROJECT)
                exit_code = _pytest.main(['--tb=no', '-q', '--no-header'] + test_files)
                os.chdir(orig_cwd)
                # exit_code 0 means all passed; we need the count
                # Re-count by collecting: use pytest's collection API
                if exit_code == 0:
                    passed_count = total_test_funcs  # all passed
                    print(f"  pytest exit_code=0 (all tests passed)")
                else:
                    print(f"  pytest exit_code={exit_code} (some tests failed)")
            except Exception as pe:
                print(f"  pytest import/run error: {pe}")

            if passed_count >= 12:
                print(f"PASS: Component 6 — {passed_count} tests passed (>= 12 required) (0.25 pts)")
                total_score += 0.25
            elif total_test_funcs >= 12 and passed_count == 0:
                # Tests exist but couldn't run pytest - partial credit for having 12+ test functions
                print(f"PARTIAL: Component 6 — {total_test_funcs} test functions found, pytest unavailable (0.10 pts)")
                total_score += 0.10
            elif passed_count >= 8:
                print(f"PARTIAL: Component 6 — {passed_count} tests passed (< 12 required) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — test_files={len(test_files)}, test_funcs={total_test_funcs}, passed={passed_count}")

    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
