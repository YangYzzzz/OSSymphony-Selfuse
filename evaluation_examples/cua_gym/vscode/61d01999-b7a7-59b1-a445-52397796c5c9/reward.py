"""
Reward Script: Task Queue System with Celery, FastAPI, Docker
Task ID: vscode_gf4_041
Domain: vscode
Scoring:
  C1: venv with required packages (0.15)
  C2: tasks/email_tasks.py with send_email + send_bulk_email Celery tasks w/ retry (0.20)
  C3: tasks/report_tasks.py with generate_report + export_pdf tasks (0.15)
  C4: api/main.py FastAPI with POST /tasks/email and /tasks/report using async dispatch (0.20)
  C5: celeryconfig.py with broker_url and result_backend (0.10)
  C6: docker-compose.yml with redis service (0.10)
  C7: Tests using unittest.mock (0.10)
"""

import os
import re
import ast

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-task-queue')


def check_venv_packages(project_dir):
    """Component 1: venv exists with required packages (0.15 pts)"""
    score = 0.0
    venv_dir = os.path.join(project_dir, 'venv')
    if not os.path.isdir(venv_dir):
        print("FAIL: C1 — venv/ directory not found")
        return 0.0

    # Check site-packages for required packages
    required = ['celery', 'redis', 'fastapi', 'pydantic', 'pytest']
    found = []
    # Search for site-packages directory
    site_pkgs = None
    for root, dirs, files in os.walk(venv_dir):
        if root.endswith('site-packages'):
            site_pkgs = root
            break

    if not site_pkgs:
        print("FAIL: C1 — site-packages not found in venv")
        return 0.0

    pkg_dirs = os.listdir(site_pkgs)
    for pkg in required:
        # Check if package dir or dist-info exists
        pkg_found = any(
            d.lower().startswith(pkg.lower()) or
            d.lower().startswith(f"_{pkg.lower()}")
            for d in pkg_dirs
        )
        if pkg_found:
            found.append(pkg)

    if len(found) == len(required):
        score = 0.15
        print(f"PASS: C1 — venv has all required packages: {found} (0.15 pts)")
    else:
        missing = set(required) - set(found)
        print(f"FAIL: C1 — missing packages: {missing}, found: {found}")

    return score


def check_email_tasks(project_dir):
    """Component 2: tasks/email_tasks.py with Celery tasks + retry (0.20 pts)"""
    score = 0.0
    fpath = os.path.join(project_dir, 'tasks', 'email_tasks.py')
    if not os.path.isfile(fpath):
        print("FAIL: C2 — tasks/email_tasks.py not found")
        return 0.0

    try:
        with open(fpath, 'r') as f:
            content = f.read()

        has_send_email = bool(re.search(r'def\s+send_email\s*\(', content))
        has_send_bulk = bool(re.search(r'def\s+send_bulk_email\s*\(', content))
        has_retry = bool(re.search(r'max_retries\s*=\s*\d+', content))
        has_celery_task = bool(re.search(r'@\w+\.task', content))

        checks = {
            'send_email function': has_send_email,
            'send_bulk_email function': has_send_bulk,
            'retry logic (max_retries)': has_retry,
            'Celery @task decorator': has_celery_task,
        }

        passed = sum(v for v in checks.values())
        if passed == len(checks):
            score = 0.20
            print(f"PASS: C2 — email_tasks.py has all required elements (0.20 pts)")
        else:
            # Partial: proportional
            score = round(0.20 * (passed / len(checks)), 2)
            for name, ok in checks.items():
                status = "OK" if ok else "MISSING"
                print(f"  C2 sub-check: {name} — {status}")
            print(f"PARTIAL: C2 — {passed}/{len(checks)} checks passed ({score} pts)")

    except Exception as e:
        print(f"ERROR: C2 — {e}")

    return score


def check_report_tasks(project_dir):
    """Component 3: tasks/report_tasks.py with generate_report + export_pdf (0.15 pts)"""
    score = 0.0
    fpath = os.path.join(project_dir, 'tasks', 'report_tasks.py')
    if not os.path.isfile(fpath):
        print("FAIL: C3 — tasks/report_tasks.py not found")
        return 0.0

    try:
        with open(fpath, 'r') as f:
            content = f.read()

        has_generate_report = bool(re.search(r'def\s+generate_report\s*\(', content))
        has_export_pdf = bool(re.search(r'def\s+export_pdf\s*\(', content))
        has_celery_task = bool(re.search(r'@\w+\.task', content))

        checks = {
            'generate_report function': has_generate_report,
            'export_pdf function': has_export_pdf,
            'Celery @task decorator': has_celery_task,
        }

        passed = sum(v for v in checks.values())
        if passed == len(checks):
            score = 0.15
            print(f"PASS: C3 — report_tasks.py has all required elements (0.15 pts)")
        else:
            score = round(0.15 * (passed / len(checks)), 2)
            for name, ok in checks.items():
                status = "OK" if ok else "MISSING"
                print(f"  C3 sub-check: {name} — {status}")
            print(f"PARTIAL: C3 — {passed}/{len(checks)} checks passed ({score} pts)")

    except Exception as e:
        print(f"ERROR: C3 — {e}")

    return score


def check_api_main(project_dir):
    """Component 4: api/main.py with FastAPI + POST endpoints using async dispatch (0.20 pts)"""
    score = 0.0
    fpath = os.path.join(project_dir, 'api', 'main.py')
    if not os.path.isfile(fpath):
        print("FAIL: C4 — api/main.py not found")
        return 0.0

    try:
        with open(fpath, 'r') as f:
            content = f.read()

        has_fastapi = bool(re.search(r'FastAPI\s*\(', content))
        has_post_email = bool(re.search(r'@\w+\.post\s*\(\s*["\']\/tasks\/email["\']', content))
        has_post_report = bool(re.search(r'@\w+\.post\s*\(\s*["\']\/tasks\/report["\']', content))
        has_async_dispatch = bool(re.search(r'\.(delay|apply_async)\s*\(', content))

        checks = {
            'FastAPI() instantiation': has_fastapi,
            'POST /tasks/email endpoint': has_post_email,
            'POST /tasks/report endpoint': has_post_report,
            'async dispatch (.delay or .apply_async)': has_async_dispatch,
        }

        passed = sum(v for v in checks.values())
        if passed == len(checks):
            score = 0.20
            print(f"PASS: C4 — api/main.py has all required elements (0.20 pts)")
        else:
            score = round(0.20 * (passed / len(checks)), 2)
            for name, ok in checks.items():
                status = "OK" if ok else "MISSING"
                print(f"  C4 sub-check: {name} — {status}")
            print(f"PARTIAL: C4 — {passed}/{len(checks)} checks passed ({score} pts)")

    except Exception as e:
        print(f"ERROR: C4 — {e}")

    return score


def check_celeryconfig(project_dir):
    """Component 5: celeryconfig.py with broker_url and result_backend (0.10 pts)"""
    score = 0.0
    fpath = os.path.join(project_dir, 'celeryconfig.py')
    if not os.path.isfile(fpath):
        print("FAIL: C5 — celeryconfig.py not found")
        return 0.0

    try:
        with open(fpath, 'r') as f:
            content = f.read()

        has_broker = bool(re.search(r'broker_url\s*=', content))
        has_backend = bool(re.search(r'result_backend\s*=', content))

        if has_broker and has_backend:
            score = 0.10
            print(f"PASS: C5 — celeryconfig.py has broker_url and result_backend (0.10 pts)")
        else:
            if has_broker:
                score = 0.05
            if has_backend:
                score += 0.05
            print(f"PARTIAL: C5 — broker_url={has_broker}, result_backend={has_backend} ({score} pts)")

    except Exception as e:
        print(f"ERROR: C5 — {e}")

    return score


def check_docker_compose(project_dir):
    """Component 6: docker-compose.yml with redis service (0.10 pts)"""
    score = 0.0
    fpath = os.path.join(project_dir, 'docker-compose.yml')
    if not os.path.isfile(fpath):
        # Also check docker-compose.yaml
        fpath = os.path.join(project_dir, 'docker-compose.yaml')
        if not os.path.isfile(fpath):
            print("FAIL: C6 — docker-compose.yml not found")
            return 0.0

    try:
        with open(fpath, 'r') as f:
            content = f.read()

        has_services = bool(re.search(r'services\s*:', content))
        has_redis = bool(re.search(r'redis\s*:', content))
        has_redis_image = bool(re.search(r'image\s*:\s*.*redis', content))

        if has_services and has_redis and has_redis_image:
            score = 0.10
            print(f"PASS: C6 — docker-compose.yml defines redis service (0.10 pts)")
        elif has_services and has_redis:
            score = 0.07
            print(f"PARTIAL: C6 — redis service defined but no redis image ({score} pts)")
        else:
            print(f"FAIL: C6 — services={has_services}, redis={has_redis}, redis_image={has_redis_image}")

    except Exception as e:
        print(f"ERROR: C6 — {e}")

    return score


def check_tests(project_dir):
    """Component 7: Tests using unittest.mock exist (0.10 pts)"""
    score = 0.0

    # Look for test files in tests/ directory or project root
    test_files = []
    tests_dir = os.path.join(project_dir, 'tests')
    if os.path.isdir(tests_dir):
        for f in os.listdir(tests_dir):
            if f.startswith('test_') and f.endswith('.py'):
                test_files.append(os.path.join(tests_dir, f))

    # Also check project root
    for f in os.listdir(project_dir):
        if f.startswith('test_') and f.endswith('.py'):
            test_files.append(os.path.join(project_dir, f))

    if not test_files:
        print("FAIL: C7 — no test files found")
        return 0.0

    try:
        mock_count = 0
        test_func_count = 0
        for tf in test_files:
            with open(tf, 'r') as f:
                content = f.read()
            mock_count += len(re.findall(r'(from\s+unittest\.mock\s+import|from\s+unittest\s+import\s+mock|@patch|MagicMock|Mock\b)', content))
            test_func_count += len(re.findall(r'(def\s+test_|class\s+Test)', content))

        if mock_count > 0 and test_func_count > 0:
            score = 0.10
            print(f"PASS: C7 — test files found with unittest.mock usage (0.10 pts)")
        elif test_func_count > 0:
            score = 0.05
            print(f"PARTIAL: C7 — tests exist but no mock usage found ({score} pts)")
        else:
            print(f"FAIL: C7 — test files found but no test functions/classes")

    except Exception as e:
        print(f"ERROR: C7 — {e}")

    return score


def verify_task():
    """Main verification function."""
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT):
        print(f"CRITICAL: Project directory not found: {PROJECT}")
        print("REWARD: 0.0")
        return 0.0

    # Run all component checks
    checks = [
        ("C1: venv packages", check_venv_packages),
        ("C2: email tasks", check_email_tasks),
        ("C3: report tasks", check_report_tasks),
        ("C4: API main", check_api_main),
        ("C5: celeryconfig", check_celeryconfig),
        ("C6: docker-compose", check_docker_compose),
        ("C7: tests with mock", check_tests),
    ]
    for name, check_fn in checks:
        try:
            component_score = check_fn(PROJECT)
            if component_score > 0:
                total_score += component_score
        except Exception as e:
            print(f"ERROR: {name} — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
