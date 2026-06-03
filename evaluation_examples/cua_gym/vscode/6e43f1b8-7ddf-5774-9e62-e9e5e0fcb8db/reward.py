"""
Reward Script: Install Jest Runner extension and configure its settings in VSCode
Task ID: vscode_gf3_039
Domain: vscode
Scoring:
  Component 1: Jest Runner extension installed (0.4 points)
  Component 2: jestrunner.jestCommand set to 'npx jest' (0.3 points)
  Component 3: jestrunner.runOptions includes '--forceExit' (0.3 points)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_039'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return {}


def get_installed_extension_ids():
    """Get set of installed VSCode extension IDs by scanning extension directories and metadata."""
    extensions = set()

    # Scan the extensions directory directly
    ext_dirs = [
        os.path.join(WORKDIR, '.vscode', 'extensions'),
        os.path.join(WORKDIR, '.vscode-server', 'extensions'),
    ]
    for ext_dir in ext_dirs:
        if os.path.isdir(ext_dir):
            for name in os.listdir(ext_dir):
                # Extension dirs are like "publisher.name-version"
                parts = name.rsplit('-', 1)
                if parts:
                    extensions.add(parts[0].lower())

    # Also check extensions.json metadata file
    ext_json_paths = [
        os.path.join(WORKDIR, '.vscode', 'extensions', 'extensions.json'),
    ]
    for ejp in ext_json_paths:
        if os.path.exists(ejp):
            try:
                with open(ejp, 'r') as f:
                    ext_list = json.load(f)
                for ext in ext_list:
                    eid = ext.get('identifier', {}).get('id', '')
                    if eid:
                        extensions.add(eid.lower())
            except Exception:
                pass

    return extensions


def check_extension_via_marker():
    """Check if Jest Runner extension is installed by looking for its files."""
    # Look in common extension directories
    search_dirs = [
        os.path.join(WORKDIR, '.vscode', 'extensions'),
        os.path.join(WORKDIR, '.vscode-server', 'extensions'),
        '/usr/share/code/resources/app/extensions',
    ]

    for search_dir in search_dirs:
        if not os.path.isdir(search_dir):
            continue
        for entry in os.listdir(search_dir):
            if 'jest-runner' in entry.lower() or 'vscode-jest-runner' in entry.lower():
                return True

    # Also check snap-installed code extensions
    snap_ext = os.path.join(WORKDIR, 'snap', 'code', 'current', '.vscode', 'extensions')
    if os.path.isdir(snap_ext):
        for entry in os.listdir(snap_ext):
            if 'jest-runner' in entry.lower() or 'vscode-jest-runner' in entry.lower():
                return True

    # Check the dotnet directory presence as indirect evidence (Jest Runner uses .NET?)
    # Not reliable, skip

    # Check extensions.json in .vscode/extensions
    ext_json = os.path.join(WORKDIR, '.vscode', 'extensions', 'extensions.json')
    if os.path.exists(ext_json):
        try:
            with open(ext_json, 'r') as f:
                data = json.load(f)
            for ext in data:
                eid = ext.get('identifier', {}).get('id', '').lower()
                if 'jest-runner' in eid or 'vscode-jest-runner' in eid:
                    return True
        except Exception:
            pass

    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: test file exists
    test_file = os.path.join(WORKDIR, 'projects', 'node-api', 'src', '__tests__', 'userService.test.js')
    if not os.path.exists(test_file):
        print(f"PRECONDITION FAIL: Test file not found at {test_file}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Jest Runner extension is installed (0.4 points)
    try:
        # Check via directory scanning for extension folders
        is_installed = check_extension_via_marker()

        # Fallback: also check via extensions.json metadata
        if not is_installed:
            all_ext_ids = get_installed_extension_ids()
            matching = [eid for eid in all_ext_ids
                        if 'jest-runner' in eid or 'vscode-jest-runner' in eid]
            is_installed = len(matching) > 0

        if is_installed:
            print(f"PASS: Component 1 - Jest Runner extension is installed (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - Jest Runner extension not found in any extension directory")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: jestrunner.jestCommand set to 'npx jest' (0.3 points)
    try:
        settings = load_settings()
        jest_command = settings.get('jestrunner.jestCommand', None)
        if jest_command is not None and jest_command.strip() == 'npx jest':
            print(f"PASS: Component 2 - jestrunner.jestCommand = '{jest_command}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - Expected jestrunner.jestCommand='npx jest', found: {jest_command!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: jestrunner.runOptions includes '--forceExit' (0.3 points)
    try:
        settings = load_settings()
        run_options = settings.get('jestrunner.runOptions', None)
        if run_options is not None and isinstance(run_options, list) and '--forceExit' in run_options:
            print(f"PASS: Component 3 - jestrunner.runOptions contains '--forceExit' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 - Expected jestrunner.runOptions to contain '--forceExit', found: {run_options!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point display issues
    final_score = round(final_score, 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
