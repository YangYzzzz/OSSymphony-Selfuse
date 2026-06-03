"""
Reward Script: VSCode FastAPI project setup
Task ID: vscode_gf4_012
Domain: vscode
Scoring:
  Component 1 (0.20): Virtual environment with required packages
  Component 2 (0.30): app/main.py with FastAPI app and 3 routes
  Component 3 (0.25): tests/test_main.py with async test functions
  Component 4 (0.15): .vscode/launch.json with uvicorn --reload
  Component 5 (0.10): pytest tests pass
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_012'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-fastapi')


def check_venv_packages():
    """Component 1: Virtual environment exists with required packages (0.20 points)"""
    venv_python = os.path.join(PROJECT_DIR, 'venv', 'bin', 'python')
    if not os.path.isfile(venv_python):
        print(f"FAIL: Component 1 — venv/bin/python not found at {venv_python}")
        return 0.0

    venv_lib = os.path.join(PROJECT_DIR, 'venv', 'lib')
    if not os.path.isdir(venv_lib):
        print(f"FAIL: Component 1 — venv/lib not found")
        return 0.0

    py_dirs = [d for d in os.listdir(venv_lib) if d.startswith('python')]
    if not py_dirs:
        print(f"FAIL: Component 1 — no python dir in venv/lib")
        return 0.0

    site_packages = os.path.join(venv_lib, py_dirs[0], 'site-packages')
    if not os.path.isdir(site_packages):
        print(f"FAIL: Component 1 — site-packages dir not found")
        return 0.0

    sp_contents = os.listdir(site_packages)
    sp_lower = [x.lower() for x in sp_contents]

    has_fastapi = any('fastapi' in x for x in sp_lower)
    has_uvicorn = any('uvicorn' in x for x in sp_lower)
    has_pytest_asyncio = any('pytest_asyncio' in x or 'pytest-asyncio' in x for x in sp_lower)
    has_httpx = any('httpx' in x for x in sp_lower)

    pkg_count = sum([has_fastapi, has_uvicorn, has_pytest_asyncio, has_httpx])
    if pkg_count == 4:
        print(f"PASS: Component 1 — venv exists with all 4 required packages (0.20 pts)")
        return 0.20
    elif pkg_count >= 2:
        print(f"PARTIAL: Component 1 — venv exists with {pkg_count}/4 packages (0.10 pts)")
        return 0.10
    else:
        print(f"FAIL: Component 1 — venv exists but only {pkg_count}/4 packages found")
        return 0.0


def check_main_py():
    """Component 2: app/main.py with FastAPI app and 3 routes (0.30 points)"""
    main_py_path = os.path.join(PROJECT_DIR, 'app', 'main.py')
    if not os.path.isfile(main_py_path):
        print(f"FAIL: Component 2 — app/main.py not found")
        return 0.0

    with open(main_py_path, 'r') as f:
        main_content = f.read()

    score = 0.0

    # Sub-check: FastAPI import and app instance
    if 'FastAPI' in main_content and re.search(r'app\s*=\s*FastAPI\(', main_content):
        score += 0.05
        print(f"  PASS: FastAPI app instance found")
    else:
        print(f"  FAIL: FastAPI app instance not found")

    # Sub-check: GET / route returning status ok
    if re.search(r'@app\.(get|route)\s*\(\s*["\']\/["\']\s*\)', main_content):
        if re.search(r'["\']status["\']\s*:\s*["\']ok["\']', main_content):
            score += 0.08
            print(f"  PASS: GET / route with status:ok found")
        else:
            score += 0.04
            print(f"  PARTIAL: GET / route found but status:ok not confirmed")
    else:
        print(f"  FAIL: GET / route not found")

    # Sub-check: GET /items route
    if re.search(r'@app\.get\s*\(\s*["\']\/items["\']\s*\)', main_content):
        score += 0.08
        print(f"  PASS: GET /items route found")
    else:
        print(f"  FAIL: GET /items route not found")

    # Sub-check: POST /items route with name and price
    if re.search(r'@app\.post\s*\(\s*["\']\/items["\']\s*\)', main_content):
        if 'name' in main_content and 'price' in main_content:
            score += 0.09
            print(f"  PASS: POST /items route with name/price found")
        else:
            score += 0.04
            print(f"  PARTIAL: POST /items route found but name/price fields not confirmed")
    else:
        print(f"  FAIL: POST /items route not found")

    if score > 0:
        print(f"PASS: Component 2 — app/main.py verified ({score:.2f} pts)")
    else:
        print(f"FAIL: Component 2 — app/main.py missing required routes")
    return score


def check_test_file():
    """Component 3: tests/test_main.py with async test functions (0.25 points)"""
    test_py_path = os.path.join(PROJECT_DIR, 'tests', 'test_main.py')
    if not os.path.isfile(test_py_path):
        print(f"FAIL: Component 3 — tests/test_main.py not found")
        return 0.0

    with open(test_py_path, 'r') as f:
        test_content = f.read()

    async_tests = re.findall(r'async\s+def\s+(test_\w+)', test_content)
    has_asyncio_marker = 'asyncio' in test_content
    has_async_client = 'AsyncClient' in test_content

    if len(async_tests) >= 3 and has_asyncio_marker and has_async_client:
        print(f"PASS: Component 3 — {len(async_tests)} async tests with AsyncClient (0.25 pts)")
        return 0.25
    elif len(async_tests) >= 2 and has_async_client:
        print(f"PARTIAL: Component 3 — {len(async_tests)} async tests with AsyncClient (0.15 pts)")
        return 0.15
    elif len(async_tests) >= 1:
        print(f"PARTIAL: Component 3 — {len(async_tests)} async tests found (0.08 pts)")
        return 0.08
    else:
        print(f"FAIL: Component 3 — no async test functions found")
        return 0.0


def check_launch_json():
    """Component 4: .vscode/launch.json with uvicorn --reload config (0.15 points)"""
    launch_json_path = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
    if not os.path.isfile(launch_json_path):
        print(f"FAIL: Component 4 — .vscode/launch.json not found")
        return 0.0

    with open(launch_json_path, 'r') as f:
        raw = f.read()

    # Strip JSONC comments before parsing
    cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
    launch_config = json.loads(cleaned)

    configurations = launch_config.get('configurations', [])
    if len(configurations) == 0:
        print(f"FAIL: Component 4 — launch.json has no configurations")
        return 0.0

    # Scan all configurations for uvicorn + --reload
    uvicorn_count = 0
    reload_count = 0
    for config in configurations:
        config_str = json.dumps(config).lower()
        if 'uvicorn' in config_str:
            uvicorn_count += 1
            args = config.get('args', [])
            if any('--reload' in str(a) for a in args):
                reload_count += 1

    if uvicorn_count > 0 and reload_count > 0:
        print(f"PASS: Component 4 — launch.json has uvicorn with --reload (0.15 pts)")
        return 0.15
    elif uvicorn_count > 0:
        print(f"PARTIAL: Component 4 — launch.json has uvicorn but no --reload (0.08 pts)")
        return 0.08
    else:
        print(f"FAIL: Component 4 — launch.json configurations don't reference uvicorn")
        return 0.0


def check_tests_pass():
    """Component 5: pytest tests pass (0.10 points)"""
    venv_pytest = os.path.join(PROJECT_DIR, 'venv', 'bin', 'pytest')
    if not os.path.isfile(venv_pytest):
        print(f"FAIL: Component 5 — venv pytest not found at {venv_pytest}")
        return 0.0

    # Need subprocess to invoke pytest in the venv — no other way to run tests
    import subprocess as sp
    env = os.environ.copy()
    env['PATH'] = os.path.join(PROJECT_DIR, 'venv', 'bin') + ':' + env.get('PATH', '')
    result = sp.run(
        [venv_pytest, 'tests/', '-v', '--tb=short'],
        capture_output=True, text=True, cwd=PROJECT_DIR,
        env=env, timeout=30
    )
    if result.returncode == 0:
        print(f"PASS: Component 5 — pytest tests pass (0.10 pts)")
        return 0.10
    else:
        print(f"FAIL: Component 5 — pytest returned non-zero: {result.returncode}")
        if result.stdout:
            print(f"  stdout (last 500): {result.stdout[-500:]}")
        if result.stderr:
            print(f"  stderr (last 500): {result.stderr[-500:]}")
        return 0.0


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Virtual environment with packages (0.20 pts)
    try:
        total_score += check_venv_packages()
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: app/main.py with routes (0.30 pts)
    try:
        total_score += check_main_py()
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: tests/test_main.py with async tests (0.25 pts)
    try:
        total_score += check_test_file()
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/launch.json (0.15 pts)
    try:
        total_score += check_launch_json()
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: pytest tests pass (0.10 pts)
    try:
        total_score += check_tests_pass()
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
