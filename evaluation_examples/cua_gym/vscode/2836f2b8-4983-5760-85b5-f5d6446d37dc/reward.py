"""
Reward Script: Python package development workflow in VSCode
Task ID: vscode_wf_068
Domain: vscode
Scoring:
  - Component 1: Package structure (mypackage/__init__.py, core.py, utils.py) — 0.15
  - Component 2: setup.py with required metadata — 0.15
  - Component 3: MANIFEST.in exists with content — 0.10
  - Component 4: tox.ini configured for py39, py310, py311 — 0.15
  - Component 5: tests/ with test files importing mypackage — 0.15
  - Component 6: tasks.json with test, build-package, lint, type-check — 0.20
  - Component 7: launch.json with pytest debug config — 0.10
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_068'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Package structure (0.15 points)
    # mypackage/__init__.py, mypackage/core.py, mypackage/utils.py must exist
    try:
        pkg_dir = os.path.join(PROJECT, 'mypackage')
        required_files = ['__init__.py', 'core.py', 'utils.py']
        found_count = 0
        for f in required_files:
            fpath = os.path.join(pkg_dir, f)
            if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
                found_count += 1
            else:
                print(f"FAIL: Component 1 — missing or empty: mypackage/{f}")
        if found_count == len(required_files):
            print(f"PASS: Component 1 — package structure complete ({found_count}/{len(required_files)} files) (0.15 pts)")
            total_score += 0.15
        elif found_count > 0:
            partial = round(0.15 * found_count / len(required_files), 3)
            print(f"PARTIAL: Component 1 — {found_count}/{len(required_files)} files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — no package files found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: setup.py with required metadata (0.15 points)
    # Must contain name, version, author, install_requires
    try:
        setup_path = os.path.join(PROJECT, 'setup.py')
        if os.path.isfile(setup_path):
            with open(setup_path, 'r') as f:
                setup_content = f.read()
            checks = {
                'name=': bool(re.search(r'name\s*=', setup_content)),
                'version=': bool(re.search(r'version\s*=', setup_content)),
                'author=': bool(re.search(r'author\s*=', setup_content)),
                'install_requires=': bool(re.search(r'install_requires\s*=', setup_content)),
            }
            passed = sum(checks.values())
            if passed == len(checks):
                print(f"PASS: Component 2 — setup.py has all required metadata (0.15 pts)")
                total_score += 0.15
            else:
                missing = [k for k, v in checks.items() if not v]
                partial = round(0.15 * passed / len(checks), 3)
                print(f"PARTIAL: Component 2 — missing: {missing} ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 — setup.py not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: MANIFEST.in exists with content (0.10 points)
    try:
        manifest_path = os.path.join(PROJECT, 'MANIFEST.in')
        if os.path.isfile(manifest_path):
            with open(manifest_path, 'r') as f:
                manifest_content = f.read().strip()
            if len(manifest_content) > 5:
                print(f"PASS: Component 3 — MANIFEST.in exists with content (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — MANIFEST.in is too short/empty")
        else:
            print(f"FAIL: Component 3 — MANIFEST.in not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tox.ini with py39, py310, py311 (0.15 points)
    try:
        tox_path = os.path.join(PROJECT, 'tox.ini')
        if os.path.isfile(tox_path):
            with open(tox_path, 'r') as f:
                tox_content = f.read()
            # Check for envlist containing py39, py310, py311
            has_py39 = bool(re.search(r'py3[\.]*9', tox_content))
            has_py310 = bool(re.search(r'py3[\.]*10', tox_content))
            has_py311 = bool(re.search(r'py3[\.]*11', tox_content))
            versions_found = sum([has_py39, has_py310, has_py311])
            if versions_found == 3:
                print(f"PASS: Component 4 — tox.ini has py39, py310, py311 (0.15 pts)")
                total_score += 0.15
            else:
                partial = round(0.15 * versions_found / 3, 3)
                missing = []
                if not has_py39: missing.append('py39')
                if not has_py310: missing.append('py310')
                if not has_py311: missing.append('py311')
                print(f"PARTIAL: Component 4 — missing versions: {missing} ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 4 — tox.ini not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tests/ with test files importing mypackage (0.15 points)
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        if os.path.isdir(tests_dir):
            test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]
            if len(test_files) >= 1:
                # Check that at least one test file imports from mypackage
                import_count = sum(
                    1 for tf in test_files
                    if re.search(r'(from\s+mypackage|import\s+mypackage)',
                                 open(os.path.join(tests_dir, tf), 'r').read())
                )
                if import_count >= 1 and len(test_files) >= 2:
                    print(f"PASS: Component 5 — tests/ has {len(test_files)} test files importing mypackage (0.15 pts)")
                    total_score += 0.15
                elif import_count >= 1:
                    print(f"PARTIAL: Component 5 — {len(test_files)} test file(s) importing mypackage (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 5 — test files exist but none import mypackage")
            else:
                print(f"FAIL: Component 5 — no test_*.py files in tests/")
        else:
            print(f"FAIL: Component 5 — tests/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: tasks.json with test, build-package, lint, type-check tasks (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(content_clean)
            task_labels = set()
            if 'tasks' in tasks_data:
                for t in tasks_data['tasks']:
                    label = t.get('label', '').lower().strip()
                    task_labels.add(label)

            required_labels = ['test', 'build-package', 'lint', 'type-check']
            found_labels = []
            for rl in required_labels:
                if rl in task_labels:
                    found_labels.append(rl)

            if len(found_labels) == len(required_labels):
                # Also verify build-package command contains setup.py sdist bdist_wheel
                build_task = next(
                    (t for t in tasks_data['tasks']
                     if t.get('label', '').lower().strip() == 'build-package'),
                    None
                )
                cmd = build_task.get('command', '') if build_task else ''
                if 'setup.py' in cmd and 'sdist' in cmd and 'bdist_wheel' in cmd:
                    print(f"PASS: Component 6 — tasks.json has all 4 required tasks with correct build command (0.20 pts)")
                    total_score += 0.20
                elif len(found_labels) == len(required_labels):
                    print(f"PARTIAL: Component 6 — all 4 task labels found but build-package command incorrect (0.15 pts)")
                    total_score += 0.15
            else:
                missing = [rl for rl in required_labels if rl not in found_labels]
                partial = round(0.20 * len(found_labels) / len(required_labels), 3)
                print(f"PARTIAL: Component 6 — found {found_labels}, missing {missing} ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 6 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: launch.json with pytest debug config (0.10 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_data = json.loads(content_clean)
            configs = launch_data.get('configurations', [])
            pytest_configs = [
                cfg for cfg in configs
                if 'pytest' in cfg.get('module', '')
                or 'pytest' in cfg.get('program', '')
                or 'pytest' in ' '.join(str(a) for a in cfg.get('args', []))
            ]
            if len(pytest_configs) > 0:
                print(f"PASS: Component 7 — launch.json has pytest debug config (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — launch.json has no pytest debug configuration")
        else:
            print(f"FAIL: Component 7 — .vscode/launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
