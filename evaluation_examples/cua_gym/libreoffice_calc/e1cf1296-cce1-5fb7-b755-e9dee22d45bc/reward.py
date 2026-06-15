"""
Reward Script: Celery async task processing setup in VSCode
Task ID: vscode_gf6_060
Domain: vscode (python project setup)
Scoring:
  Component 1: venv with required packages (0.15)
  Component 2: celery_app.py configuration (0.20)
  Component 3: email_tasks.py with 3 tasks + group() (0.20)
  Component 4: data_tasks.py with periodic task + beat_schedule (0.15)
  Component 5: test_tasks.py with ALWAYS_EAGER + >=2 tests (0.15)
  Component 6: .vscode/launch.json with Celery worker config (0.15)
"""

import os
import json
import re
import ast

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-celery')


def verify_task():
    """Verify Celery project setup with progressive scoring."""
    total_score = 0.0

    # Component 1: venv exists with celery, redis, flower, pytest-celery (0.15 points)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        if os.path.isdir(venv_dir):
            # Check installed packages by looking at site-packages
            site_packages = None
            lib_dir = os.path.join(venv_dir, 'lib')
            if os.path.isdir(lib_dir):
                for d in os.listdir(lib_dir):
                    sp = os.path.join(lib_dir, d, 'site-packages')
                    if os.path.isdir(sp):
                        site_packages = sp
                        break

            if site_packages:
                pkg_dirs = os.listdir(site_packages)
                pkg_names_lower = [p.lower().replace('-', '_') for p in pkg_dirs]
                required = ['celery', 'redis', 'flower', 'pytest_celery']
                found = []
                for req in required:
                    # Check if any directory starts with the package name
                    if any(p.startswith(req) for p in pkg_names_lower):
                        found.append(req)

                if len(found) == len(required):
                    print(f"PASS: Component 1 — venv has all required packages: {found} (0.15 pts)")
                    total_score += 0.15
                else:
                    missing = set(required) - set(found)
                    print(f"FAIL: Component 1 — missing packages: {missing}")
            else:
                print("FAIL: Component 1 — venv exists but no site-packages found")
        else:
            print("FAIL: Component 1 — venv/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: celery_app.py with correct broker, backend, serializer, timezone (0.20 points)
    try:
        celery_app_path = os.path.join(PROJECT, 'src', 'celery_app.py')
        if os.path.isfile(celery_app_path):
            with open(celery_app_path, 'r') as f:
                content = f.read()

            checks_passed = 0
            # Check broker URL
            if 'redis://localhost:6379/0' in content and ('broker' in content.lower()):
                checks_passed += 1
            # Check result backend
            if 'result_backend' in content or 'CELERY_RESULT_BACKEND' in content:
                if 'redis://localhost:6379/0' in content:
                    checks_passed += 1
            # Check task_serializer = json
            if ('task_serializer' in content or 'CELERY_TASK_SERIALIZER' in content) and "'json'" in content:
                checks_passed += 1
            # Check timezone = UTC
            if ('timezone' in content or 'CELERY_TIMEZONE' in content) and "'UTC'" in content:
                checks_passed += 1

            if checks_passed == 4:
                print(f"PASS: Component 2 — celery_app.py has all 4 config items (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — celery_app.py has {checks_passed}/4 config items")
        else:
            print("FAIL: Component 2 — src/celery_app.py not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: email_tasks.py with 3 tasks + group() usage (0.20 points)
    try:
        email_path = os.path.join(PROJECT, 'src', 'tasks', 'email_tasks.py')
        if os.path.isfile(email_path):
            with open(email_path, 'r') as f:
                content = f.read()

            comp3_score = 0.0

            # Check for 3 task functions: send_welcome_email, send_password_reset, batch_send_newsletter
            task_funcs = ['send_welcome_email', 'send_password_reset', 'batch_send_newsletter']
            found_funcs = [fn for fn in task_funcs if re.search(rf'def\s+{fn}\s*\(', content)]

            # Check that tasks are decorated with @shared_task or @app.task
            has_task_decorator = bool(re.search(r'@(shared_task|app\.task)', content))

            if len(found_funcs) == 3 and has_task_decorator:
                comp3_score += 0.12
                print(f"  Component 3a: All 3 task functions found with decorator")
            else:
                print(f"  Component 3a FAIL: Found {len(found_funcs)}/3 functions, decorator={has_task_decorator}")

            # Check batch_send_newsletter uses group()
            # Look for group import and usage
            has_group_import = bool(re.search(r'from\s+celery\s+import.*group|from\s+celery\.canvas\s+import.*group', content))
            has_group_usage = 'group(' in content

            if has_group_import and has_group_usage:
                comp3_score += 0.08
                print(f"  Component 3b: group() import and usage found")
            else:
                print(f"  Component 3b FAIL: group import={has_group_import}, group usage={has_group_usage}")

            if comp3_score > 0:
                print(f"PASS: Component 3 — email_tasks.py ({comp3_score} pts)")
                total_score += comp3_score
            else:
                print(f"FAIL: Component 3 — email_tasks.py checks failed")
        else:
            print("FAIL: Component 3 — src/tasks/email_tasks.py not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: data_tasks.py with periodic task + beat_schedule (0.15 points)
    try:
        data_path = os.path.join(PROJECT, 'src', 'tasks', 'data_tasks.py')
        if os.path.isfile(data_path):
            with open(data_path, 'r') as f:
                content = f.read()

            comp4_score = 0.0

            # Check for @shared_task decorated function
            has_shared_task = bool(re.search(r'@shared_task', content))
            has_def = bool(re.search(r'def\s+\w+\s*\(', content))

            if has_shared_task and has_def:
                comp4_score += 0.07
                print(f"  Component 4a: Periodic task with @shared_task found")
            else:
                print(f"  Component 4a FAIL: shared_task={has_shared_task}, def={has_def}")

            # Check for beat_schedule configuration
            has_beat_schedule = 'beat_schedule' in content
            has_schedule_entry = bool(re.search(r"'schedule'\s*:", content) or re.search(r'"schedule"\s*:', content))

            if has_beat_schedule and has_schedule_entry:
                comp4_score += 0.08
                print(f"  Component 4b: beat_schedule configuration found")
            else:
                print(f"  Component 4b FAIL: beat_schedule={has_beat_schedule}, schedule_entry={has_schedule_entry}")

            if comp4_score > 0:
                print(f"PASS: Component 4 — data_tasks.py ({comp4_score} pts)")
                total_score += comp4_score
            else:
                print(f"FAIL: Component 4 — data_tasks.py checks failed")
        else:
            print("FAIL: Component 4 — src/tasks/data_tasks.py not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: test_tasks.py with ALWAYS_EAGER and tests >=2 tasks (0.15 points)
    try:
        test_path = os.path.join(PROJECT, 'tests', 'test_tasks.py')
        if os.path.isfile(test_path):
            with open(test_path, 'r') as f:
                content = f.read()

            comp5_score = 0.0

            # Check for CELERY_TASK_ALWAYS_EAGER or task_always_eager setting
            has_eager = bool(
                re.search(r'CELERY_TASK_ALWAYS_EAGER', content) or
                re.search(r'task_always_eager\s*=\s*True', content)
            )

            if has_eager:
                comp5_score += 0.07
                print(f"  Component 5a: CELERY_TASK_ALWAYS_EAGER setting found")
            else:
                print(f"  Component 5a FAIL: No ALWAYS_EAGER setting found")

            # Check for at least 2 test functions
            test_functions = re.findall(r'def\s+(test_\w+)\s*\(', content)
            if len(test_functions) >= 2:
                comp5_score += 0.08
                print(f"  Component 5b: {len(test_functions)} test functions found: {test_functions[:5]}")
            else:
                print(f"  Component 5b FAIL: Only {len(test_functions)} test function(s) found")

            if comp5_score > 0:
                print(f"PASS: Component 5 — test_tasks.py ({comp5_score} pts)")
                total_score += comp5_score
            else:
                print(f"FAIL: Component 5 — test_tasks.py checks failed")
        else:
            print("FAIL: Component 5 — tests/test_tasks.py not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/launch.json with Celery worker debug config (0.15 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                # Handle JSONC (strip comments)
                raw = f.read()
                cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
                launch_config = json.loads(cleaned)

            configurations = launch_config.get('configurations', [])

            # Find a configuration that launches a Celery worker
            celery_configs = [
                cfg for cfg in configurations
                if 'celery' in json.dumps(cfg).lower()
                and ('worker' in json.dumps(cfg).lower() or 'module' in cfg.get('type', ''))
            ]

            if len(celery_configs) > 0:
                print(f"PASS: Component 6 — launch.json has Celery worker config (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — No Celery worker configuration found in launch.json")
        else:
            print("FAIL: Component 6 — .vscode/launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
