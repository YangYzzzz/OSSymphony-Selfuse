"""
Reward Script: Plugin architecture implementation in VSCode
Task ID: vscode_gf4_043
Domain: vscode
Scoring:
  Component 1 (0.10): venv with pydantic, importlib-metadata, pytest
  Component 2 (0.15): plugin_base.py - abstract BasePlugin + PluginMetadata
  Component 3 (0.15): plugin_registry.py - PluginRegistry with importlib discovery
  Component 4 (0.15): csv_plugin.py - concrete BasePlugin implementation
  Component 5 (0.10): json_plugin.py - concrete BasePlugin implementation
  Component 6 (0.15): pipeline.py - Pipeline chaining plugins
  Component 7 (0.10): examples/transform_pipeline.py demonstrates the system
  Component 8 (0.10): pytest passes >= 8 tests
"""

import os
import sys
import ast
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-plugin-system')


def check_venv_packages():
    """Check venv exists and has required packages installed."""
    venv_dir = os.path.join(PROJECT, 'venv')
    if not os.path.isdir(venv_dir):
        return False
    # Check site-packages for required libraries
    site_pkg = None
    lib_dir = os.path.join(venv_dir, 'lib')
    if os.path.isdir(lib_dir):
        for d in os.listdir(lib_dir):
            sp = os.path.join(lib_dir, d, 'site-packages')
            if os.path.isdir(sp):
                site_pkg = sp
                break
    if not site_pkg:
        return False

    pkg_dirs = os.listdir(site_pkg)
    pkg_dirs_lower = [p.lower() for p in pkg_dirs]
    # Check pydantic
    has_pydantic = any('pydantic' in p and 'dist-info' in p for p in pkg_dirs_lower)
    # Check importlib-metadata
    has_importlib = any('importlib_metadata' in p and 'dist-info' in p for p in pkg_dirs_lower)
    # Check pytest
    has_pytest = any('pytest' in p and 'dist-info' in p for p in pkg_dirs_lower)

    return has_pydantic and has_importlib and has_pytest


def check_plugin_base():
    """Check plugin_base.py has abstract BasePlugin with required methods and PluginMetadata."""
    path = os.path.join(PROJECT, 'src', 'core', 'plugin_base.py')
    if not os.path.isfile(path):
        return False, "file not found"
    with open(path) as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False, "syntax error"

    classes = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}

    # Check PluginMetadata exists and uses BaseModel (Pydantic)
    if 'PluginMetadata' not in classes:
        return False, "PluginMetadata class not found"
    pm_class = classes['PluginMetadata']
    pm_bases = [getattr(b, 'id', getattr(b, 'attr', '')) for b in pm_class.bases]
    if 'BaseModel' not in pm_bases:
        return False, "PluginMetadata does not inherit BaseModel"

    # Check BasePlugin exists and is abstract
    if 'BasePlugin' not in classes:
        return False, "BasePlugin class not found"
    bp_class = classes['BasePlugin']
    bp_bases = [getattr(b, 'id', getattr(b, 'attr', '')) for b in bp_class.bases]
    if 'ABC' not in bp_bases and 'ABCMeta' not in bp_bases:
        return False, "BasePlugin does not inherit ABC"

    # Check required methods
    methods = set()
    for node in ast.walk(bp_class):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.add(node.name)
    required = {'register', 'execute', 'teardown', 'metadata'}
    missing = required - methods
    if missing:
        return False, f"missing methods: {missing}"

    # Check execute takes 'context' parameter
    if 'execute' in methods:
        for node in ast.walk(bp_class):
            if isinstance(node, ast.FunctionDef) and node.name == 'execute':
                arg_names = [a.arg for a in node.args.args]
                if 'context' not in arg_names:
                    return False, "execute missing 'context' parameter"

    return True, "OK"


def check_plugin_registry():
    """Check plugin_registry.py has PluginRegistry with required methods using importlib."""
    path = os.path.join(PROJECT, 'src', 'core', 'plugin_registry.py')
    if not os.path.isfile(path):
        return False, "file not found"
    with open(path) as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False, "syntax error"

    classes = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    if 'PluginRegistry' not in classes:
        return False, "PluginRegistry class not found"

    pr_class = classes['PluginRegistry']
    methods = set()
    for node in ast.walk(pr_class):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.add(node.name)

    required = {'discover_plugins', 'register', 'get', 'list_all'}
    missing = required - methods
    if missing:
        return False, f"missing methods: {missing}"

    # Check importlib usage
    if 'importlib' not in content:
        return False, "importlib not used"

    return True, "OK"


def check_concrete_plugin(filename, expected_class_keyword=None):
    """Check a concrete plugin file implements BasePlugin."""
    path = os.path.join(PROJECT, 'src', 'plugins', filename)
    if not os.path.isfile(path):
        return False, "file not found"
    with open(path) as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False, "syntax error"

    # Find class that inherits from BasePlugin
    found_plugin = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [getattr(b, 'id', getattr(b, 'attr', '')) for b in node.bases]
            if 'BasePlugin' in bases:
                found_plugin = True
                # Check it implements required methods
                methods = set()
                for child in ast.walk(node):
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.add(child.name)
                required = {'register', 'execute', 'teardown', 'metadata'}
                missing = required - methods
                if missing:
                    return False, f"class {node.name} missing methods: {missing}"
                break

    if not found_plugin:
        return False, "no class inheriting BasePlugin found"

    return True, "OK"


def check_pipeline():
    """Check pipeline.py has Pipeline class that chains plugins."""
    path = os.path.join(PROJECT, 'src', 'core', 'pipeline.py')
    if not os.path.isfile(path):
        return False, "file not found"
    with open(path) as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False, "syntax error"

    classes = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    if 'Pipeline' not in classes:
        return False, "Pipeline class not found"

    pl_class = classes['Pipeline']
    methods = set()
    for node in ast.walk(pl_class):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.add(node.name)

    # Pipeline needs add/run methods at minimum
    if 'run' not in methods:
        return False, "Pipeline missing 'run' method"
    if 'add' not in methods and 'add_plugin' not in methods:
        return False, "Pipeline missing 'add' method"

    return True, "OK"


def check_example():
    """Check examples/transform_pipeline.py exists and demonstrates the system."""
    path = os.path.join(PROJECT, 'examples', 'transform_pipeline.py')
    if not os.path.isfile(path):
        return False, "file not found"
    with open(path) as f:
        content = f.read()

    # Check it imports from the project
    if 'pipeline' not in content.lower() and 'Pipeline' not in content:
        return False, "does not reference Pipeline"
    if 'registry' not in content.lower() and 'plugin' not in content.lower():
        return False, "does not reference plugin system"

    # Should have a main function or be runnable
    if 'def main' not in content and '__main__' not in content:
        return False, "no main function or __main__ block"

    return True, "OK"


def check_pytest():
    """Run pytest and check at least 8 tests pass."""
    import io
    import contextlib

    venv_pytest = os.path.join(PROJECT, 'venv', 'bin', 'pytest')
    if not os.path.isfile(venv_pytest):
        return False, 0, "pytest not found in venv"

    # Run pytest by reading its output from os.popen
    test_dir = os.path.join(PROJECT, 'tests')
    if not os.path.isdir(test_dir):
        return False, 0, "tests/ directory not found"

    # Use os.popen to run pytest
    cmd = f'cd {PROJECT} && {venv_pytest} tests/ -v 2>&1'
    stream = os.popen(cmd)
    output = stream.read()
    stream.close()

    # Count passed tests
    # Look for "X passed" in output
    match = re.search(r'(\d+)\s+passed', output)
    if match:
        passed = int(match.group(1))
        if passed >= 8:
            return True, passed, output
        else:
            return False, passed, output
    return False, 0, output


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: venv with pydantic, importlib-metadata, pytest (0.10 points)
    try:
        if check_venv_packages():
            print("PASS: Component 1 -- venv with required packages (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 1 -- venv missing or packages not installed")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: plugin_base.py (0.15 points)
    try:
        ok, detail = check_plugin_base()
        if ok:
            print(f"PASS: Component 2 -- plugin_base.py correct ({detail}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- plugin_base.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: plugin_registry.py (0.15 points)
    try:
        ok, detail = check_plugin_registry()
        if ok:
            print(f"PASS: Component 3 -- plugin_registry.py correct ({detail}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- plugin_registry.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: csv_plugin.py (0.15 points)
    try:
        ok, detail = check_concrete_plugin('csv_plugin.py')
        if ok:
            print(f"PASS: Component 4 -- csv_plugin.py correct ({detail}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- csv_plugin.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: json_plugin.py (0.10 points)
    try:
        ok, detail = check_concrete_plugin('json_plugin.py')
        if ok:
            print(f"PASS: Component 5 -- json_plugin.py correct ({detail}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- json_plugin.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: pipeline.py (0.15 points)
    try:
        ok, detail = check_pipeline()
        if ok:
            print(f"PASS: Component 6 -- pipeline.py correct ({detail}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 -- pipeline.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: examples/transform_pipeline.py (0.10 points)
    try:
        ok, detail = check_example()
        if ok:
            print(f"PASS: Component 7 -- examples/transform_pipeline.py correct ({detail}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 -- examples/transform_pipeline.py: {detail}")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: pytest passes >= 8 tests (0.10 points)
    try:
        ok, count, detail = check_pytest()
        if ok:
            print(f"PASS: Component 8 -- pytest: {count} tests passed (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 8 -- pytest: {count} tests passed (need >=8). Output: {detail[-200:]}")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()
