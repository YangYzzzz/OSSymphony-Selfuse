"""
Reward Script: Migrate Python project from setup.py to Poetry
Task ID: vscode_gf6_056
Domain: vscode
Scoring:
  1. pyproject.toml with [tool.poetry] name=myapp, python>=3.11 (0.15)
  2. Main deps: fastapi, uvicorn, sqlalchemy (0.15)
  3. Dev deps: pytest, black, mypy, ruff (0.15)
  4. setup.py and requirements.txt removed (0.15)
  5. [tool.ruff] line-length=88 and [tool.pytest.ini_options] testpaths (0.15)
  6. poetry.lock exists (0.10)
  7. .vscode/settings.json has python.defaultInterpreterPath (0.10)
  8. .vscode/tasks.json has 3 Poetry tasks (0.05)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-poetry')
PYPROJECT = os.path.join(PROJECT, 'pyproject.toml')


def parse_toml_simple(path):
    """Minimal TOML parser sufficient for pyproject.toml verification.
    Returns dict of section -> raw text lines."""
    sections = {}
    current_section = None
    current_lines = []
    with open(path, 'r') as f:
        for line in f:
            line_s = line.strip()
            # Match section headers like [tool.poetry] or [tool.poetry.dependencies]
            m = re.match(r'^\[([^\]]+)\]$', line_s)
            if m:
                if current_section is not None:
                    sections[current_section] = current_lines
                current_section = m.group(1)
                current_lines = []
            else:
                if current_section is not None:
                    current_lines.append(line_s)
    if current_section is not None:
        sections[current_section] = current_lines
    return sections


def get_toml_values(lines):
    """Extract key=value pairs from TOML section lines."""
    result = {}
    for line in lines:
        if '=' in line and not line.startswith('#'):
            key, _, val = line.partition('=')
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def verify_task():
    total_score = 0.0

    # Precondition: pyproject.toml must exist
    if not os.path.exists(PYPROJECT):
        print(f"CRITICAL: pyproject.toml not found at {PYPROJECT}")
        print("REWARD: 0.0")
        return 0.0

    try:
        sections = parse_toml_simple(PYPROJECT)
    except Exception as e:
        print(f"CRITICAL: Cannot parse pyproject.toml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: [tool.poetry] has name=myapp and python>=3.11 (0.15 pts)
    try:
        poetry_section = sections.get('tool.poetry', [])
        poetry_vals = get_toml_values(poetry_section)

        deps_section = sections.get('tool.poetry.dependencies', [])
        deps_vals = get_toml_values(deps_section)

        name_ok = poetry_vals.get('name', '') == 'myapp'
        # Python version constraint: should contain >=3.11
        python_val = deps_vals.get('python', '')
        python_ok = '3.11' in python_val

        if name_ok and python_ok:
            print(f"PASS: Component 1 — name=myapp, python={python_val} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — name={'myapp' if name_ok else poetry_vals.get('name', 'MISSING')}, python={python_val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Main dependencies (fastapi, uvicorn, sqlalchemy) (0.15 pts)
    try:
        deps_section = sections.get('tool.poetry.dependencies', [])
        deps_vals = get_toml_values(deps_section)
        # Check keys (case-insensitive)
        dep_keys = [k.lower() for k in deps_vals.keys()]
        required_main = ['fastapi', 'uvicorn', 'sqlalchemy']
        found_main = [d for d in required_main if d in dep_keys]

        if len(found_main) == len(required_main):
            print(f"PASS: Component 2 — all main deps found: {found_main} (0.15 pts)")
            total_score += 0.15
        else:
            missing = [d for d in required_main if d not in dep_keys]
            print(f"FAIL: Component 2 — missing main deps: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Dev dependencies (pytest, black, mypy, ruff) (0.15 pts)
    try:
        dev_section = sections.get('tool.poetry.group.dev.dependencies', [])
        dev_vals = get_toml_values(dev_section)
        dev_keys = [k.lower() for k in dev_vals.keys()]
        required_dev = ['pytest', 'black', 'mypy', 'ruff']
        found_dev = [d for d in required_dev if d in dev_keys]

        if len(found_dev) == len(required_dev):
            print(f"PASS: Component 3 — all dev deps found: {found_dev} (0.15 pts)")
            total_score += 0.15
        else:
            missing = [d for d in required_dev if d not in dev_keys]
            print(f"FAIL: Component 3 — missing dev deps: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: setup.py and requirements.txt removed (0.15 pts)
    try:
        setup_gone = not os.path.exists(os.path.join(PROJECT, 'setup.py'))
        reqs_gone = not os.path.exists(os.path.join(PROJECT, 'requirements.txt'))

        if setup_gone and reqs_gone:
            print("PASS: Component 4 — setup.py and requirements.txt removed (0.15 pts)")
            total_score += 0.15
        else:
            still_present = []
            if not setup_gone:
                still_present.append('setup.py')
            if not reqs_gone:
                still_present.append('requirements.txt')
            print(f"FAIL: Component 4 — still present: {still_present}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: [tool.ruff] with line-length=88 and [tool.pytest.ini_options] with testpaths (0.15 pts)
    try:
        ruff_section = sections.get('tool.ruff', [])
        ruff_vals = get_toml_values(ruff_section)
        ruff_ok = ruff_vals.get('line-length', '') == '88'

        pytest_section = sections.get('tool.pytest.ini_options', [])
        pytest_vals = get_toml_values(pytest_section)
        # testpaths may be like ["tests"] — check raw text
        pytest_raw = '\n'.join(pytest_section)
        pytest_ok = 'testpaths' in pytest_raw and 'tests' in pytest_raw

        if ruff_ok and pytest_ok:
            print(f"PASS: Component 5 — [tool.ruff] line-length=88, [tool.pytest.ini_options] testpaths (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — ruff line-length={'88' if ruff_ok else ruff_vals.get('line-length', 'MISSING')}, pytest testpaths={'OK' if pytest_ok else 'MISSING'}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: poetry.lock exists (0.10 pts)
    # This is task-introduced (initial has no poetry.lock)
    try:
        lock_path = os.path.join(PROJECT, 'poetry.lock')
        if os.path.exists(lock_path) and os.path.getsize(lock_path) > 100:
            print(f"PASS: Component 6 — poetry.lock exists ({os.path.getsize(lock_path)} bytes) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — poetry.lock missing or empty")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: .vscode/settings.json has python.defaultInterpreterPath pointing to poetry venv (0.10 pts)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                # Handle JSONC (strip comments)
                content = f.read()
                content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                settings = json.loads(content_clean)

            interp = settings.get('python.defaultInterpreterPath', '')
            # Should point to a poetry virtualenv path
            if interp and ('pypoetry' in interp or 'poetry' in interp.lower()) and 'virtualenvs' in interp:
                print(f"PASS: Component 7 — python.defaultInterpreterPath = {interp} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — python.defaultInterpreterPath = '{interp}' (not a poetry venv)")
        else:
            print(f"FAIL: Component 7 — .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: .vscode/tasks.json has 3 Poetry tasks (Install, Test, Build) (0.05 pts)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                content = f.read()
                content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_data = json.loads(content_clean)

            task_labels = [t.get('label', '').lower() for t in tasks_data.get('tasks', [])]
            required_tasks = ['install', 'test', 'build']
            found_tasks = []
            for req in required_tasks:
                if any(req in label and 'poetry' in label for label in task_labels):
                    found_tasks.append(req)

            if len(found_tasks) == 3:
                print(f"PASS: Component 8 — all 3 Poetry tasks found: {found_tasks} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 8 — found {len(found_tasks)}/3 Poetry tasks. Labels: {task_labels}")
        else:
            print(f"FAIL: Component 8 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
