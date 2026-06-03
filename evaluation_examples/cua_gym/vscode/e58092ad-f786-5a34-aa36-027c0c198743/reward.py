"""
Reward Script: Property-based testing with Hypothesis for sorting and string utils
Task ID: vscode_gf6_069
Domain: vscode
Scoring:
  Component 1: hypothesis installed in venv (0.15)
  Component 2: test_sorting_properties.py exists with @given decorators and 3+ tests (0.25)
  Component 3: Sorting tests cover required properties (match sorted, length, sortedness) (0.15)
  Component 4: parse_date round-trip property test exists (0.10)
  Component 5: pytest.ini or pyproject.toml has hypothesis config (0.10)
  Component 6: .vscode/tasks.json has Property Tests task (0.15)
  Component 7: Property tests actually pass when run (0.10)
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-hypothesis')
TASK_ID = 'vscode_gf6_069'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: hypothesis is installed in venv (0.15 points)
    # This FAILS on initial (no hypothesis), PASSES on golden
    try:
        hypothesis_dir = os.path.join(PROJECT, 'venv', 'lib')
        hypothesis_found = False
        if os.path.isdir(hypothesis_dir):
            for pyver in os.listdir(hypothesis_dir):
                sp = os.path.join(hypothesis_dir, pyver, 'site-packages', 'hypothesis')
                if os.path.isdir(sp):
                    hypothesis_found = True
                    break
        if hypothesis_found:
            print(f"PASS: Component 1 - hypothesis is installed in venv (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - hypothesis not found in venv/lib/*/site-packages/")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: tests/test_sorting_properties.py exists with @given decorators
    # and at least 3 test functions (0.25 points)
    # FAILS on initial (no tests/ dir), PASSES on golden
    test_sorting_path = os.path.join(PROJECT, 'tests', 'test_sorting_properties.py')
    sorting_test_content = None
    try:
        if os.path.isfile(test_sorting_path):
            with open(test_sorting_path, 'r') as f:
                sorting_test_content = f.read()

            # Count @given decorators
            given_count = len(re.findall(r'@given\(', sorting_test_content))
            # Count test functions
            test_func_count = len(re.findall(r'def test_\w+', sorting_test_content))
            # Check for st.lists(st.integers())
            has_strategy = bool(re.search(r'st\.lists\s*\(\s*st\.integers\s*\(\s*\)', sorting_test_content))

            if given_count >= 3 and test_func_count >= 3 and has_strategy:
                print(f"PASS: Component 2 - test_sorting_properties.py has {given_count} @given decorators, "
                      f"{test_func_count} test functions, uses st.lists(st.integers()) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - @given count={given_count} (need>=3), "
                      f"test funcs={test_func_count} (need>=3), strategy={has_strategy}")
        else:
            print(f"FAIL: Component 2 - tests/test_sorting_properties.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Sorting tests cover required properties:
    # (a) match sorted(), (b) length check, (c) sortedness check (0.15 points)
    # FAILS on initial (file doesn't exist), PASSES on golden
    try:
        if sorting_test_content:
            checks_found = 0

            # (a) Comparison with Python's sorted()
            if re.search(r'sorted\s*\(', sorting_test_content):
                checks_found += 1

            # (b) Length equality check
            if re.search(r'len\s*\(', sorting_test_content):
                checks_found += 1

            # (c) Sortedness check (element <= next element pattern)
            if (re.search(r'result\[i\]\s*<=\s*result\[i\s*\+\s*1\]', sorting_test_content) or
                re.search(r'is_sorted|each element.*<=.*next|output is sorted', sorting_test_content, re.IGNORECASE)):
                checks_found += 1

            if checks_found >= 3:
                print(f"PASS: Component 3 - All 3 property types verified: sorted() comparison, "
                      f"length check, sortedness check (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 - Only {checks_found}/3 property types found")
        else:
            print(f"FAIL: Component 3 - No sorting test content to analyze")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: parse_date round-trip property test exists (0.10 points)
    # FAILS on initial (no test files), PASSES on golden
    try:
        round_trip_found = False
        # Check in test_sorting_properties.py or a separate file
        test_dir = os.path.join(PROJECT, 'tests')
        if os.path.isdir(test_dir):
            for fname in os.listdir(test_dir):
                if fname.endswith('.py') and fname.startswith('test_'):
                    fpath = os.path.join(test_dir, fname)
                    with open(fpath, 'r') as f:
                        content = f.read()
                    # Check for parse_date and format_date round-trip test
                    if ('parse_date' in content and 'format_date' in content and
                            '@given' in content):
                        round_trip_found = True
                        break

        if round_trip_found:
            print(f"PASS: Component 4 - parse_date/format_date round-trip property test found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - No parse_date round-trip property test found in tests/")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: pytest.ini or pyproject.toml has hypothesis settings (0.10 points)
    # FAILS on initial (no pytest.ini), PASSES on golden
    try:
        config_found = False

        # Check pytest.ini
        pytest_ini = os.path.join(PROJECT, 'pytest.ini')
        if os.path.isfile(pytest_ini):
            with open(pytest_ini, 'r') as f:
                ini_content = f.read()
            if 'hypothesis' in ini_content.lower():
                config_found = True

        # Check pyproject.toml
        if not config_found:
            pyproject = os.path.join(PROJECT, 'pyproject.toml')
            if os.path.isfile(pyproject):
                with open(pyproject, 'r') as f:
                    toml_content = f.read()
                if 'hypothesis' in toml_content.lower():
                    config_found = True

        # Check setup.cfg
        if not config_found:
            setup_cfg = os.path.join(PROJECT, 'setup.cfg')
            if os.path.isfile(setup_cfg):
                with open(setup_cfg, 'r') as f:
                    cfg_content = f.read()
                if 'hypothesis' in cfg_content.lower():
                    config_found = True

        if config_found:
            print(f"PASS: Component 5 - Hypothesis configuration found in project config (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - No hypothesis settings in pytest.ini/pyproject.toml/setup.cfg")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: .vscode/tasks.json has a 'Property Tests' task (0.15 points)
    # FAILS on initial (no .vscode/tasks.json), PASSES on golden
    try:
        tasks_json_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_json_path):
            with open(tasks_json_path, 'r') as f:
                tasks_data = json.load(f)

            property_task_found = False
            tasks_list = tasks_data.get('tasks', [])
            for task in tasks_list:
                label = task.get('label', '')
                if 'property' in label.lower() and 'test' in label.lower():
                    property_task_found = True
                    break

            if property_task_found:
                print(f"PASS: Component 6 - .vscode/tasks.json has 'Property Tests' task (0.15 pts)")
                total_score += 0.15
            else:
                labels = [t.get('label', '') for t in tasks_list]
                print(f"FAIL: Component 6 - No 'Property Tests' task found. Labels: {labels}")
        else:
            print(f"FAIL: Component 6 - .vscode/tasks.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: Property tests actually pass (0.10 points)
    # FAILS on initial (no test files and no hypothesis), PASSES on golden
    try:
        import sys
        venv_python = os.path.join(PROJECT, 'venv', 'bin', 'python')
        if os.path.isfile(venv_python) and os.path.isfile(test_sorting_path):
            # Run pytest using the venv python
            import io
            exit_code = os.system(
                f'cd {PROJECT} && {venv_python} -m pytest tests/ -x -q --tb=short '
                f'--hypothesis-seed=0 -p no:cacheprovider 2>&1 | tail -5'
            )
            # os.system returns wait status; exit code is shifted
            actual_exit = exit_code >> 8 if os.name != 'nt' else exit_code
            if actual_exit == 0:
                print(f"PASS: Component 7 - pytest tests/ passed (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 - pytest tests/ failed with exit code {actual_exit}")
        else:
            print(f"FAIL: Component 7 - venv python or test file not found, cannot run tests")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
