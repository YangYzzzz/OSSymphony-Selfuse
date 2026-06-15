"""
Reward Script: Scaffold a Python package 'datatools' with proper structure and configs
Task ID: vscode_gf6_001
Domain: vs_code
Scoring:
  Component 1: Package structure files exist (0.30)
  Component 2: Test files exist (0.10)
  Component 3: setup.py content correct (0.25)
  Component 4: .vscode/settings.json correct (0.20)
  Component 5: .editorconfig correct (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_001'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-scaffold')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Package structure files (0.30 points)
    # datatools/__init__.py, datatools/core.py, datatools/utils.py, datatools/cli.py
    try:
        pkg_files = [
            'datatools/__init__.py',
            'datatools/core.py',
            'datatools/utils.py',
            'datatools/cli.py',
        ]
        found_count = 0
        for f in pkg_files:
            fpath = os.path.join(PROJECT_DIR, f)
            if os.path.isfile(fpath):
                found_count += 1
                print(f"  OK: {f} exists")
            else:
                print(f"  MISSING: {f}")
        if found_count == len(pkg_files):
            print(f"PASS: Component 1 - All 4 package files exist (0.30 pts)")
            total_score += 0.30
        elif found_count > 0:
            partial = round(0.30 * found_count / len(pkg_files), 2)
            print(f"PARTIAL: Component 1 - {found_count}/{len(pkg_files)} package files exist ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No package files found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Test files exist (0.10 points)
    # tests/__init__.py, tests/test_core.py
    try:
        test_files = [
            'tests/__init__.py',
            'tests/test_core.py',
        ]
        found_count = 0
        for f in test_files:
            fpath = os.path.join(PROJECT_DIR, f)
            if os.path.isfile(fpath):
                found_count += 1
                print(f"  OK: {f} exists")
            else:
                print(f"  MISSING: {f}")
        if found_count == len(test_files):
            print(f"PASS: Component 2 - All test files exist (0.10 pts)")
            total_score += 0.10
        elif found_count > 0:
            partial = round(0.10 * found_count / len(test_files), 2)
            print(f"PARTIAL: Component 2 - {found_count}/{len(test_files)} test files exist ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No test files found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: setup.py content correct (0.25 points)
    # name='datatools', version='0.1.0', packages=['datatools'], install_requires=['click', 'rich']
    try:
        setup_path = os.path.join(PROJECT_DIR, 'setup.py')
        if not os.path.isfile(setup_path):
            print(f"FAIL: Component 3 - setup.py does not exist")
        else:
            with open(setup_path, 'r') as f:
                setup_content = f.read()

            sub_score = 0.0
            sub_total = 4  # 4 sub-checks

            # Check name='datatools'
            if re.search(r"""name\s*=\s*['"]datatools['"]""", setup_content):
                sub_score += 1
                print(f"  OK: name='datatools' found")
            else:
                print(f"  MISSING: name='datatools' not found in setup.py")

            # Check version='0.1.0'
            if re.search(r"""version\s*=\s*['"]0\.1\.0['"]""", setup_content):
                sub_score += 1
                print(f"  OK: version='0.1.0' found")
            else:
                print(f"  MISSING: version='0.1.0' not found in setup.py")

            # Check packages=['datatools'] (or find_packages that would include it)
            if re.search(r"""packages\s*=\s*\[['"]datatools['"]\]""", setup_content) or \
               'find_packages' in setup_content:
                sub_score += 1
                print(f"  OK: packages includes 'datatools'")
            else:
                print(f"  MISSING: packages=['datatools'] not found in setup.py")

            # Check install_requires includes 'click' and 'rich'
            if 'click' in setup_content and 'rich' in setup_content and 'install_requires' in setup_content:
                sub_score += 1
                print(f"  OK: install_requires includes 'click' and 'rich'")
            else:
                print(f"  MISSING: install_requires with 'click' and 'rich' not found")

            component_score = round(0.25 * sub_score / sub_total, 2)
            if sub_score == sub_total:
                print(f"PASS: Component 3 - setup.py fully correct (0.25 pts)")
                total_score += 0.25
            elif sub_score > 0:
                print(f"PARTIAL: Component 3 - setup.py {int(sub_score)}/{sub_total} checks ({component_score} pts)")
                total_score += component_score
            else:
                print(f"FAIL: Component 3 - setup.py content incorrect")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: .vscode/settings.json correct (0.20 points)
    # python.testing.pytestEnabled: true, editor.rulers: [88]
    try:
        vscode_settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        if not os.path.isfile(vscode_settings_path):
            print(f"FAIL: Component 4 - .vscode/settings.json does not exist")
        else:
            with open(vscode_settings_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            settings = json.loads(cleaned)

            sub_score = 0.0

            # Check pytestEnabled
            if settings.get('python.testing.pytestEnabled') is True:
                sub_score += 1
                print(f"  OK: python.testing.pytestEnabled is true")
            else:
                print(f"  MISSING: python.testing.pytestEnabled not true, got: {settings.get('python.testing.pytestEnabled')}")

            # Check editor.rulers contains 88
            rulers = settings.get('editor.rulers', [])
            if isinstance(rulers, list) and 88 in rulers:
                sub_score += 1
                print(f"  OK: editor.rulers contains 88")
            else:
                print(f"  MISSING: editor.rulers does not contain 88, got: {rulers}")

            if sub_score == 2:
                print(f"PASS: Component 4 - .vscode/settings.json correct (0.20 pts)")
                total_score += 0.20
            elif sub_score == 1:
                print(f"PARTIAL: Component 4 - 1/2 settings correct (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 - .vscode/settings.json incorrect")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: .editorconfig correct (0.15 points)
    # indent_style=space, indent_size=4 for Python files
    try:
        editorconfig_path = os.path.join(PROJECT_DIR, '.editorconfig')
        if not os.path.isfile(editorconfig_path):
            print(f"FAIL: Component 5 - .editorconfig does not exist")
        else:
            with open(editorconfig_path, 'r') as f:
                ec_content = f.read()

            sub_score = 0.0

            # Check for Python section [*.py]
            if re.search(r'\[\*\.py\]', ec_content):
                print(f"  OK: [*.py] section found")

                # Extract the Python section content
                py_section = re.search(r'\[\*\.py\](.*?)(?=\[|$)', ec_content, re.DOTALL)
                if py_section:
                    section_text = py_section.group(1)

                    # Check indent_style = space
                    if re.search(r'indent_style\s*=\s*space', section_text):
                        sub_score += 1
                        print(f"  OK: indent_style = space found")
                    else:
                        print(f"  MISSING: indent_style = space not found in [*.py] section")

                    # Check indent_size = 4
                    if re.search(r'indent_size\s*=\s*4', section_text):
                        sub_score += 1
                        print(f"  OK: indent_size = 4 found")
                    else:
                        print(f"  MISSING: indent_size = 4 not found in [*.py] section")
            else:
                print(f"  MISSING: [*.py] section not found in .editorconfig")

            if sub_score == 2:
                print(f"PASS: Component 5 - .editorconfig correct (0.15 pts)")
                total_score += 0.15
            elif sub_score == 1:
                print(f"PARTIAL: Component 5 - 1/2 editorconfig checks (0.075 pts)")
                total_score += 0.075
            else:
                print(f"FAIL: Component 5 - .editorconfig incorrect")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Also verify setup.py and README.md exist as top-level files (included in structural check)
    # README.md existence is implied by the task but not scored separately since the task
    # focuses on specific content requirements above.

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
