"""
Reward Script: Configure structured logging with structlog in a FastAPI project
Task ID: vscode_gf6_072
Domain: libreoffice_calc (actually vscode/python project)
Scoring:
  Component 1: Packages installed (structlog, rich, orjson) — 0.15
  Component 2: src/logging_setup.py with correct structlog config — 0.20
  Component 3: src/middleware/structlog_middleware.py with request_id — 0.15
  Component 4: src/api/users.py uses structlog instead of print — 0.20
  Component 5: tests/test_logging.py with capture_logs tests — 0.15
  Component 6: .vscode/launch.json with APP_ENV=development — 0.15
"""

import os
import json
import re
import ast

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-structlog')
VENV_SITE = os.path.join(PROJECT, 'venv', 'lib')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Packages installed — structlog, rich, orjson (0.15 points)
    try:
        installed_count = 0
        # Walk venv site-packages to check for dist-info directories
        site_packages = None
        for root, dirs, files in os.walk(VENV_SITE):
            if 'site-packages' in root:
                site_packages = root
                break
        if site_packages is None:
            # Try common path
            site_packages = os.path.join(PROJECT, 'venv', 'lib', 'python3.10', 'site-packages')

        if os.path.isdir(site_packages):
            pkg_dirs = os.listdir(site_packages)
            pkg_names_lower = [d.lower() for d in pkg_dirs]
            for pkg in ['structlog', 'rich', 'orjson']:
                # Check for package directory or dist-info
                if any(p.startswith(pkg) for p in pkg_names_lower):
                    installed_count += 1

        if installed_count == 3:
            print(f"PASS: Component 1 — All 3 packages installed (structlog, rich, orjson) (0.15 pts)")
            total_score += 0.15
        elif installed_count > 0:
            partial = round(0.15 * installed_count / 3, 3)
            print(f"PARTIAL: Component 1 — {installed_count}/3 packages installed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No required packages found in venv")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: src/logging_setup.py exists and configures structlog properly (0.20 points)
    try:
        logging_setup_path = os.path.join(PROJECT, 'src', 'logging_setup.py')
        if not os.path.exists(logging_setup_path):
            print(f"FAIL: Component 2 — src/logging_setup.py does not exist")
        else:
            with open(logging_setup_path, 'r') as f:
                content = f.read()

            checks_passed = 0
            total_checks = 5

            # Check 2a: imports structlog
            if 'import structlog' in content:
                checks_passed += 1

            # Check 2b: JSON renderer for production (APP_ENV=production)
            if 'JSONRenderer' in content and 'production' in content:
                checks_passed += 1

            # Check 2c: ConsoleRenderer with colors for development
            if 'ConsoleRenderer' in content and 'colors' in content:
                checks_passed += 1

            # Check 2d: timestamp processor, callsite info, and log level
            has_timestamp = 'TimeStamper' in content
            has_callsite = 'CallsiteParameterAdder' in content or 'CallsiteParameter' in content
            has_loglevel = 'add_log_level' in content
            if has_timestamp and has_callsite and has_loglevel:
                checks_passed += 1

            # Check 2e: request_id context var processor using contextvars.ContextVar
            if 'contextvars' in content and 'request_id' in content and 'ContextVar' in content:
                checks_passed += 1

            score_2 = round(0.20 * checks_passed / total_checks, 3)
            if checks_passed == total_checks:
                print(f"PASS: Component 2 — logging_setup.py has all required elements ({score_2} pts)")
            else:
                print(f"PARTIAL: Component 2 — {checks_passed}/{total_checks} checks passed ({score_2} pts)")
            total_score += score_2
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/middleware/structlog_middleware.py with request_id binding (0.15 points)
    try:
        middleware_path = os.path.join(PROJECT, 'src', 'middleware', 'structlog_middleware.py')
        if not os.path.exists(middleware_path):
            print(f"FAIL: Component 3 — src/middleware/structlog_middleware.py does not exist")
        else:
            with open(middleware_path, 'r') as f:
                content = f.read()

            checks_passed = 0
            total_checks = 3

            # Check 3a: imports structlog and uuid
            if 'import structlog' in content and 'import uuid' in content:
                checks_passed += 1

            # Check 3b: binds request_id (UUID) to structlog context
            if 'uuid' in content.lower() and 'request_id' in content:
                checks_passed += 1

            # Check 3c: is middleware class or function (dispatch/middleware pattern)
            if 'Middleware' in content or 'dispatch' in content or 'middleware' in content.lower():
                checks_passed += 1

            score_3 = round(0.15 * checks_passed / total_checks, 3)
            if checks_passed == total_checks:
                print(f"PASS: Component 3 — structlog_middleware.py has all required elements ({score_3} pts)")
            else:
                print(f"PARTIAL: Component 3 — {checks_passed}/{total_checks} checks passed ({score_3} pts)")
            total_score += score_3
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: src/api/users.py uses structlog instead of print (0.20 points)
    try:
        users_path = os.path.join(PROJECT, 'src', 'api', 'users.py')
        if not os.path.exists(users_path):
            print(f"FAIL: Component 4 — src/api/users.py does not exist")
        else:
            with open(users_path, 'r') as f:
                content = f.read()

            checks_passed = 0
            total_checks = 3

            # Check 4a: imports structlog
            if 'import structlog' in content:
                checks_passed += 1

            # Check 4b: uses structlog.get_logger() or structlog.get_logger
            if 'structlog.get_logger' in content or 'get_logger()' in content:
                checks_passed += 1

            # Check 4c: No print() calls used for logging (the key change!)
            # Count print() calls in function bodies (not in docstrings)
            # Parse AST to find print calls
            try:
                tree = ast.parse(content)
                print_calls = 0
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'print':
                            print_calls += 1
                if print_calls == 0:
                    checks_passed += 1
                else:
                    print(f"  Detail: Found {print_calls} print() calls still in users.py")
            except SyntaxError:
                # Fallback: regex
                print_matches = re.findall(r'^\s+print\(', content, re.MULTILINE)
                if len(print_matches) == 0:
                    checks_passed += 1

            score_4 = round(0.20 * checks_passed / total_checks, 3)
            if checks_passed == total_checks:
                print(f"PASS: Component 4 — users.py uses structlog, no print() calls ({score_4} pts)")
            else:
                print(f"PARTIAL: Component 4 — {checks_passed}/{total_checks} checks passed ({score_4} pts)")
            total_score += score_4
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tests/test_logging.py with capture_logs tests (0.15 points)
    try:
        test_path = os.path.join(PROJECT, 'tests', 'test_logging.py')
        if not os.path.exists(test_path):
            print(f"FAIL: Component 5 — tests/test_logging.py does not exist")
        else:
            with open(test_path, 'r') as f:
                content = f.read()

            checks_passed = 0
            total_checks = 3

            # Check 5a: uses structlog.testing.capture_logs
            if 'capture_logs' in content:
                checks_passed += 1

            # Check 5b: has at least 2 test functions
            test_funcs = re.findall(r'def (test_\w+)', content)
            if len(test_funcs) >= 2:
                checks_passed += 1

            # Check 5c: imports structlog
            if 'import structlog' in content:
                checks_passed += 1

            score_5 = round(0.15 * checks_passed / total_checks, 3)
            if checks_passed == total_checks:
                print(f"PASS: Component 5 — test_logging.py has capture_logs and {len(test_funcs)} tests ({score_5} pts)")
            else:
                print(f"PARTIAL: Component 5 — {checks_passed}/{total_checks} checks passed ({score_5} pts)")
            total_score += score_5
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/launch.json with APP_ENV=development (0.15 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print(f"FAIL: Component 6 — .vscode/launch.json does not exist")
        else:
            with open(launch_path, 'r') as f:
                # Handle JSONC (strip comments)
                raw = f.read()
                cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
                launch_config = json.loads(cleaned)

            checks_passed = 0
            total_checks = 2

            # Check 6a: has configurations array
            configs = launch_config.get('configurations', [])
            if len(configs) > 0:
                checks_passed += 1

            # Check 6b: at least one config has env.APP_ENV = "development"
            has_app_env = False
            for config in configs:
                env = config.get('env', {})
                if env.get('APP_ENV') == 'development':
                    has_app_env = True
                    break
            if has_app_env:
                checks_passed += 1

            score_6 = round(0.15 * checks_passed / total_checks, 3)
            if checks_passed == total_checks:
                print(f"PASS: Component 6 — launch.json has APP_ENV=development ({score_6} pts)")
            else:
                print(f"PARTIAL: Component 6 — {checks_passed}/{total_checks} checks passed ({score_6} pts)")
            total_score += score_6
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
