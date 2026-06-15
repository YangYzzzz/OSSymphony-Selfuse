"""
Reward Script: Sphinx documentation setup for python-sphinx-docs project
Task ID: vscode_gf6_083
Domain: vscode
Scoring:
  C1 (0.15): Sphinx packages installed in venv
  C2 (0.20): docs/conf.py has 5 required extensions
  C3 (0.10): docs/conf.py has html_theme='furo' and autodoc_default_options
  C4 (0.15): docs/api/index.rst has automodule directives for both modules
  C5 (0.15): All 8 public functions have Google-style docstrings
  C6 (0.10): docs/_build/html/index.html exists (successful sphinx build)
  C7 (0.15): .vscode/tasks.json has 'Docs: Build' and 'Docs: Serve' tasks
"""

import os
import ast
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-sphinx-docs')

REQUIRED_EXTENSIONS = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'myst_parser',
]

CORE_FUNCTIONS = ['calculate_statistics', 'transform_records', 'filter_by_threshold', 'merge_datasets', 'generate_report']
UTILS_FUNCTIONS = ['validate_email', 'format_timestamp', 'batch_process']


def check_packages_installed():
    """Check that sphinx, sphinx-autodoc-typehints, furo, myst-parser are installed in venv."""
    venv_lib = os.path.join(PROJECT, 'venv', 'lib')
    if not os.path.isdir(venv_lib):
        return False
    # Find the python site-packages dir
    site_packages = None
    for pydir in os.listdir(venv_lib):
        candidate = os.path.join(venv_lib, pydir, 'site-packages')
        if os.path.isdir(candidate):
            site_packages = candidate
            break
    if not site_packages:
        return False

    # Check for key package directories/dist-info
    required_markers = {
        'sphinx': False,
        'furo': False,
        'myst_parser': False,
        'sphinx_autodoc_typehints': False,
    }
    entries = os.listdir(site_packages)
    for entry in entries:
        entry_lower = entry.lower()
        if entry_lower.startswith('sphinx-') and 'dist-info' in entry_lower and 'autodoc' not in entry_lower:
            required_markers['sphinx'] = True
        elif entry_lower.startswith('furo'):
            required_markers['furo'] = True
        elif entry_lower == 'myst_parser' or (entry_lower.startswith('myst_parser') and 'dist-info' in entry_lower):
            required_markers['myst_parser'] = True
        elif entry_lower == 'sphinx_autodoc_typehints' or (entry_lower.startswith('sphinx_autodoc_typehints') and 'dist-info' in entry_lower):
            required_markers['sphinx_autodoc_typehints'] = True

    return all(required_markers.values())


def parse_conf_py(conf_path):
    """Parse conf.py and extract extensions list, html_theme, and autodoc_default_options."""
    if not os.path.isfile(conf_path):
        return None, None, None
    with open(conf_path, 'r') as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None, None, None

    extensions = None
    html_theme = None
    autodoc_opts = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == 'extensions' and isinstance(node.value, ast.List):
                        extensions = []
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                extensions.append(elt.value)
                    elif target.id == 'html_theme' and isinstance(node.value, ast.Constant):
                        html_theme = node.value.value
                    elif target.id == 'autodoc_default_options' and isinstance(node.value, ast.Dict):
                        autodoc_opts = {}
                        for k, v in zip(node.value.keys, node.value.values):
                            if isinstance(k, ast.Constant):
                                if isinstance(v, ast.Constant):
                                    autodoc_opts[k.value] = v.value
                                else:
                                    autodoc_opts[k.value] = True  # e.g. True

    return extensions, html_theme, autodoc_opts


def check_api_index_rst(rst_path):
    """Check docs/api/index.rst for automodule directives for core and utils."""
    if not os.path.isfile(rst_path):
        return False, False
    with open(rst_path, 'r') as f:
        content = f.read()
    has_core = bool(re.search(r'automodule::\s*mypackage\.core', content))
    has_utils = bool(re.search(r'automodule::\s*mypackage\.utils', content))
    return has_core, has_utils


def check_docstrings(file_path, expected_funcs):
    """Check that all expected public functions have docstrings."""
    if not os.path.isfile(file_path):
        return 0, len(expected_funcs)
    with open(file_path, 'r') as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return 0, len(expected_funcs)

    count_with_docstring = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in expected_funcs:
            ds = ast.get_docstring(node)
            if ds and len(ds.strip()) > 10:
                count_with_docstring += 1
    return count_with_docstring, len(expected_funcs)


def check_tasks_json(tasks_path):
    """Check .vscode/tasks.json for 'Docs: Build' and 'Docs: Serve' tasks."""
    if not os.path.isfile(tasks_path):
        return False, False
    try:
        with open(tasks_path, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError):
        return False, False

    tasks = data.get('tasks', [])
    has_build = False
    has_serve = False
    for task in tasks:
        label = task.get('label', '')
        if 'build' in label.lower() and 'doc' in label.lower():
            has_build = True
        if 'serve' in label.lower() and 'doc' in label.lower():
            has_serve = True
    return has_build, has_serve


def verify_task():
    """Verify Sphinx documentation setup with progressive scoring."""
    total_score = 0.0

    # Component 1: Sphinx packages installed in venv (0.15 points)
    try:
        if check_packages_installed():
            print("PASS: Component 1 - Sphinx packages installed in venv (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 - Not all required Sphinx packages found in venv")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: docs/conf.py has 5 required extensions (0.20 points)
    conf_path = os.path.join(PROJECT, 'docs', 'conf.py')
    extensions = None
    html_theme = None
    autodoc_opts = None
    try:
        extensions, html_theme, autodoc_opts = parse_conf_py(conf_path)
        if extensions is not None:
            found = [ext for ext in REQUIRED_EXTENSIONS if ext in extensions]
            if len(found) == len(REQUIRED_EXTENSIONS):
                print(f"PASS: Component 2 - All 5 required extensions found in conf.py (0.20 pts)")
                total_score += 0.20
            else:
                missing = [ext for ext in REQUIRED_EXTENSIONS if ext not in extensions]
                print(f"FAIL: Component 2 - Missing extensions: {missing}")
        else:
            print(f"FAIL: Component 2 - Could not parse extensions from conf.py (file exists: {os.path.isfile(conf_path)})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: html_theme='furo' and autodoc_default_options with members+show-inheritance (0.10 points)
    try:
        theme_ok = (html_theme == 'furo')
        opts_ok = (autodoc_opts is not None and 'members' in autodoc_opts and 'show-inheritance' in autodoc_opts)
        if theme_ok and opts_ok:
            print(f"PASS: Component 3 - html_theme='furo' and autodoc_default_options correct (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 - theme='{html_theme}' (expect 'furo'), autodoc_opts={autodoc_opts}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: docs/api/index.rst has automodule directives for core and utils (0.15 points)
    rst_path = os.path.join(PROJECT, 'docs', 'api', 'index.rst')
    try:
        has_core, has_utils = check_api_index_rst(rst_path)
        if has_core and has_utils:
            print(f"PASS: Component 4 - api/index.rst has automodule for both core and utils (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - core={has_core}, utils={has_utils} in {rst_path}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: All 8 public functions have docstrings (0.15 points)
    try:
        core_path = os.path.join(PROJECT, 'src', 'mypackage', 'core.py')
        utils_path = os.path.join(PROJECT, 'src', 'mypackage', 'utils.py')
        core_count, core_total = check_docstrings(core_path, CORE_FUNCTIONS)
        utils_count, utils_total = check_docstrings(utils_path, UTILS_FUNCTIONS)
        total_funcs = core_total + utils_total
        total_with_ds = core_count + utils_count
        if total_with_ds == total_funcs:
            print(f"PASS: Component 5 - All {total_funcs} public functions have docstrings (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - {total_with_ds}/{total_funcs} functions have docstrings (core={core_count}/{core_total}, utils={utils_count}/{utils_total})")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: docs/_build/html/index.html exists (successful build) (0.10 points)
    build_html = os.path.join(PROJECT, 'docs', '_build', 'html', 'index.html')
    try:
        if os.path.isfile(build_html):
            size = os.path.getsize(build_html)
            if size > 100:
                print(f"PASS: Component 6 - docs/_build/html/index.html exists ({size} bytes) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 - index.html exists but too small ({size} bytes)")
        else:
            print(f"FAIL: Component 6 - docs/_build/html/index.html does not exist")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: .vscode/tasks.json has 'Docs: Build' and 'Docs: Serve' tasks (0.15 points)
    tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
    try:
        has_build, has_serve = check_tasks_json(tasks_path)
        if has_build and has_serve:
            print(f"PASS: Component 7 - tasks.json has Docs: Build and Docs: Serve tasks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 7 - build={has_build}, serve={has_serve} in {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
