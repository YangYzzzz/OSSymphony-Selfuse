"""
Reward Script: Set up a Python project with type checking tools and config
Task ID: vscode_wf_025
Domain: vscode
Scoring:
  Component 1 - mypy installed via pip (0.25)
  Component 2 - pyright installed via pip (0.25)
  Component 3 - VSCode settings contain python.analysis.typeCheckingMode = basic (0.25)
  Component 4 - ~/project/mypy.ini has [mypy] strict=True, disallow_untyped_defs=True (0.25)
"""

import os
import json
import re
import configparser

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
MYPY_INI_PATH = os.path.join(HOME, 'project', 'mypy.ini')


def check_pip_package(package_name):
    """Check if a package is installed by scanning pip's installed packages metadata."""
    import importlib.metadata
    try:
        importlib.metadata.distribution(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


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
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: mypy is installed (0.25 points)
    try:
        if check_pip_package('mypy'):
            print("PASS: Component 1 -- mypy is installed (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 1 -- mypy is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: pyright is installed (0.25 points)
    try:
        if check_pip_package('pyright'):
            print("PASS: Component 2 -- pyright is installed (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 2 -- pyright is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: VSCode settings contain python.analysis.typeCheckingMode = "basic" (0.25 points)
    try:
        settings = load_settings()
        if settings is not None:
            type_check_mode = settings.get('python.analysis.typeCheckingMode')
            if type_check_mode == 'basic':
                print(f"PASS: Component 3 -- python.analysis.typeCheckingMode = 'basic' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- python.analysis.typeCheckingMode = {type_check_mode!r}, expected 'basic'")
        else:
            print("FAIL: Component 3 -- settings.json could not be loaded")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: ~/project/mypy.ini exists with [mypy] strict=True, disallow_untyped_defs=True (0.25 points)
    try:
        if not os.path.exists(MYPY_INI_PATH):
            print(f"FAIL: Component 4 -- {MYPY_INI_PATH} does not exist")
        else:
            config = configparser.ConfigParser()
            config.read(MYPY_INI_PATH)
            if not config.has_section('mypy'):
                print("FAIL: Component 4 -- mypy.ini missing [mypy] section")
            else:
                strict_val = config.get('mypy', 'strict', fallback=None)
                disallow_val = config.get('mypy', 'disallow_untyped_defs', fallback=None)

                strict_ok = strict_val is not None and strict_val.strip().lower() == 'true'
                disallow_ok = disallow_val is not None and disallow_val.strip().lower() == 'true'

                if strict_ok and disallow_ok:
                    print(f"PASS: Component 4 -- mypy.ini has strict=True and disallow_untyped_defs=True (0.25 pts)")
                    total_score += 0.25
                else:
                    details = []
                    if not strict_ok:
                        details.append(f"strict={strict_val!r} (expected 'True')")
                    if not disallow_ok:
                        details.append(f"disallow_untyped_defs={disallow_val!r} (expected 'True')")
                    print(f"FAIL: Component 4 -- {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
