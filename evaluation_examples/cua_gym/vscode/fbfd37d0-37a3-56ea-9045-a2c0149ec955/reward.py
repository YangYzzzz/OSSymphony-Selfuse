"""
Reward Script: VSCode APScheduler background task processing setup
Task ID: vscode_gf6_094
Domain: vscode
Scoring:
  Component 1 (0.10): Packages installed (apscheduler, sqlalchemy, pytest)
  Component 2 (0.20): src/scheduler/jobs.py with 3 job functions + structlog
  Component 3 (0.20): src/scheduler/setup.py with correct scheduler config
  Component 4 (0.10): src/scheduler/health.py with get_scheduler_status
  Component 5 (0.15): tests/test_scheduler.py with >= 4 test functions
  Component 6 (0.10): .vscode/tasks.json with task definitions
  Component 7 (0.15): pytest tests pass
"""

import os
import json
import ast
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-background-tasks')
VENV_BIN = os.path.join(PROJECT, 'venv', 'bin')
VENV_SITE = os.path.join(PROJECT, 'venv', 'lib')


def check_package_installed(package_name):
    """Check if a package is installed in the project venv by looking for dist-info."""
    # Walk the site-packages to find dist-info dirs
    for root, dirs, files in os.walk(VENV_SITE):
        for d in dirs:
            if d.lower().startswith(package_name.lower()) and '.dist-info' in d.lower():
                return True
        # Only check one level of site-packages
        if 'site-packages' in root:
            break
    return False


def parse_functions_from_file(filepath):
    """Parse a Python file and return list of top-level function names."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    except Exception:
        return []


def parse_imports_from_file(filepath):
    """Parse a Python file and return list of imported module names."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        # Simple regex to find import statements
        imports = re.findall(r'(?:from|import)\s+([\w.]+)', content)
        return imports
    except Exception:
        return []


def count_test_methods(filepath):
    """Count test methods (functions starting with test_) in a Python file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                count += 1
        return count
    except Exception:
        return 0


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: Packages installed (0.10 points)
    # apscheduler, sqlalchemy, and pytest must be in the venv
    try:
        pkg_results = {}
        for pkg in ['apscheduler', 'sqlalchemy', 'pytest']:
            pkg_results[pkg] = check_package_installed(pkg)

        all_installed = all(pkg_results.values())
        if all_installed:
            print(f"PASS: Component 1 -- All 3 packages installed: {pkg_results} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- Missing packages: {pkg_results}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: src/scheduler/jobs.py with 3 job functions + structlog (0.20 points)
    try:
        jobs_path = os.path.join(PROJECT, 'src', 'scheduler', 'jobs.py')
        if not os.path.isfile(jobs_path):
            print(f"FAIL: Component 2 -- src/scheduler/jobs.py does not exist")
        else:
            funcs = parse_functions_from_file(jobs_path)
            with open(jobs_path, 'r') as f:
                jobs_content = f.read()

            has_daily_report = 'daily_report' in funcs
            has_hourly_cleanup = 'hourly_cleanup' in funcs
            has_process_queue = 'process_queue' in funcs
            uses_structlog = 'structlog' in jobs_content

            sub_score = 0.0
            if has_daily_report and has_hourly_cleanup and has_process_queue:
                sub_score += 0.15
            if uses_structlog:
                sub_score += 0.05

            if sub_score >= 0.20:
                print(f"PASS: Component 2 -- jobs.py has all 3 functions + structlog (0.20 pts)")
                total_score += 0.20
            elif sub_score > 0:
                print(f"PARTIAL: Component 2 -- jobs.py partial: funcs={[has_daily_report, has_hourly_cleanup, has_process_queue]}, structlog={uses_structlog} ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 -- jobs.py missing functions or structlog")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: src/scheduler/setup.py with correct scheduler config (0.20 points)
    try:
        setup_path = os.path.join(PROJECT, 'src', 'scheduler', 'setup.py')
        if not os.path.isfile(setup_path):
            print(f"FAIL: Component 3 -- src/scheduler/setup.py does not exist")
        else:
            with open(setup_path, 'r') as f:
                setup_content = f.read()
            funcs = parse_functions_from_file(setup_path)

            has_create_scheduler = 'create_scheduler' in funcs
            has_asyncio_scheduler = 'AsyncIOScheduler' in setup_content
            has_sqlalchemy_store = 'SQLAlchemyJobStore' in setup_content
            has_threadpool = 'ThreadPoolExecutor' in setup_content
            has_cron_trigger = 'CronTrigger' in setup_content
            has_interval_trigger = 'IntervalTrigger' in setup_content
            has_max_workers_10 = 'max_workers=10' in setup_content or 'max_workers = 10' in setup_content

            checks = [has_create_scheduler, has_asyncio_scheduler, has_sqlalchemy_store,
                       has_threadpool, has_cron_trigger, has_interval_trigger]
            passed = sum(checks)

            if passed == 6:
                print(f"PASS: Component 3 -- setup.py has all required components (0.20 pts)")
                total_score += 0.20
            elif passed >= 3:
                partial = round(0.20 * (passed / 6), 2)
                print(f"PARTIAL: Component 3 -- setup.py has {passed}/6 checks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- setup.py missing key components ({passed}/6)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: src/scheduler/health.py with get_scheduler_status (0.10 points)
    try:
        health_path = os.path.join(PROJECT, 'src', 'scheduler', 'health.py')
        if not os.path.isfile(health_path):
            print(f"FAIL: Component 4 -- src/scheduler/health.py does not exist")
        else:
            funcs = parse_functions_from_file(health_path)
            with open(health_path, 'r') as f:
                health_content = f.read()

            has_get_status = 'get_scheduler_status' in funcs
            # Check it returns job-related info (names, next_run_time, state)
            has_job_metadata = ('name' in health_content and
                                ('next_run_time' in health_content or 'next_run' in health_content) and
                                'state' in health_content)

            if has_get_status and has_job_metadata:
                print(f"PASS: Component 4 -- health.py has get_scheduler_status with job metadata (0.10 pts)")
                total_score += 0.10
            elif has_get_status:
                print(f"PARTIAL: Component 4 -- health.py has function but missing metadata fields (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 4 -- health.py missing get_scheduler_status function")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: tests/test_scheduler.py with >= 4 test functions (0.15 points)
    try:
        test_path = os.path.join(PROJECT, 'tests', 'test_scheduler.py')
        if not os.path.isfile(test_path):
            print(f"FAIL: Component 5 -- tests/test_scheduler.py does not exist")
        else:
            test_count = count_test_methods(test_path)
            if test_count >= 4:
                print(f"PASS: Component 5 -- test_scheduler.py has {test_count} test functions (>= 4) (0.15 pts)")
                total_score += 0.15
            elif test_count >= 2:
                print(f"PARTIAL: Component 5 -- test_scheduler.py has {test_count} tests (< 4) (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 5 -- test_scheduler.py has {test_count} test functions (need >= 4)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: .vscode/tasks.json exists with task definitions (0.10 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.isfile(tasks_path):
            print(f"FAIL: Component 6 -- .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                tasks_data = json.load(f)

            has_version = 'version' in tasks_data
            has_tasks = 'tasks' in tasks_data and isinstance(tasks_data.get('tasks'), list)
            task_count = len(tasks_data.get('tasks', []))

            if has_tasks and task_count >= 1:
                print(f"PASS: Component 6 -- tasks.json has {task_count} task(s) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- tasks.json has no tasks or invalid format")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: pytest tests pass (0.15 points)
    try:
        test_path = os.path.join(PROJECT, 'tests', 'test_scheduler.py')
        pytest_bin = os.path.join(VENV_BIN, 'pytest')
        if not os.path.isfile(test_path):
            print(f"FAIL: Component 7 -- test file does not exist, cannot run tests")
        elif not os.path.isfile(pytest_bin):
            print(f"FAIL: Component 7 -- pytest not installed in venv")
        else:
            # Run pytest and check exit code
            import sys
            original_argv = sys.argv
            original_cwd = os.getcwd()
            try:
                os.chdir(PROJECT)
                # Use the venv's pytest module directly
                sys.path.insert(0, os.path.join(PROJECT, 'venv', 'lib', 'python3.10', 'site-packages'))
                sys.path.insert(0, PROJECT)

                import pytest as _pytest
                exit_code = _pytest.main([test_path, '-x', '--tb=short', '-q'])

                if exit_code == 0:
                    print(f"PASS: Component 7 -- All tests passed (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 7 -- Tests failed with exit code {exit_code}")
            except Exception as e2:
                print(f"ERROR: Component 7 -- Failed to run pytest: {e2}")
            finally:
                sys.argv = original_argv
                os.chdir(original_cwd)
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
