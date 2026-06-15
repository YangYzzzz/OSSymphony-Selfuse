"""
Reward Script: Configure Python extension PYTHONPATH with src/ and lib/ directories
Task ID: vscode_py_074
Domain: vscode
Scoring:
  Component 1 (0.4): .env file contains PYTHONPATH with both src and lib
  Component 2 (0.3): settings.json has python.envFile referencing .env
  Component 3 (0.3): settings.json has python.analysis.extraPaths with src and lib
"""

import os
import json
import re

WORKDIR = '/home/user'
WORKSPACE = os.path.join(WORKDIR, 'workspace')
TASK_ID = 'vscode_py_074'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    env_file = os.path.join(WORKSPACE, '.env')
    settings_file = os.path.join(WORKSPACE, '.vscode', 'settings.json')

    # Component 1: .env file contains PYTHONPATH with both src and lib (0.4 points)
    try:
        if not os.path.exists(env_file):
            print("FAIL: Component 1 — .env file does not exist")
        else:
            with open(env_file, 'r') as f:
                env_content = f.read()

            # Parse PYTHONPATH value from the .env file
            pythonpath_match = re.search(r'PYTHONPATH\s*=\s*(.+)', env_content)
            if pythonpath_match:
                pythonpath_value = pythonpath_match.group(1).strip()
                # Split by : (Unix path separator) to get individual paths
                paths = [p.strip() for p in pythonpath_value.split(':')]
                has_src = any(p in ('src', 'src/', './src', './src/') for p in paths)
                has_lib = any(p in ('lib', 'lib/', './lib', './lib/') for p in paths)
                if has_src and has_lib:
                    print(f"PASS: Component 1 — PYTHONPATH contains both src and lib: '{pythonpath_value}' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — PYTHONPATH missing paths. src={has_src}, lib={has_lib}. Value: '{pythonpath_value}'")
            else:
                print(f"FAIL: Component 1 — PYTHONPATH not found in .env file. Content: {repr(env_content[:200])}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: settings.json has python.envFile pointing to .env (0.3 points)
    try:
        if not os.path.exists(settings_file):
            print("FAIL: Component 2 — .vscode/settings.json does not exist")
        else:
            with open(settings_file, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            stripped = re.sub(r'/\*.*?\*/', '', stripped, flags=re.DOTALL)
            settings = json.loads(stripped)

            env_file_setting = settings.get('python.envFile', None)
            if env_file_setting is not None:
                # Accept common variants: ${workspaceFolder}/.env or .env or absolute path
                valid_values = [
                    '${workspaceFolder}/.env',
                    '${workspaceRoot}/.env',
                    '.env',
                ]
                if env_file_setting in valid_values or env_file_setting.endswith('/.env'):
                    print(f"PASS: Component 2 — python.envFile = '{env_file_setting}' (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — python.envFile has unexpected value: '{env_file_setting}'")
            else:
                print("FAIL: Component 2 — python.envFile not found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: settings.json has python.analysis.extraPaths with src and lib (0.3 points)
    try:
        if not os.path.exists(settings_file):
            print("FAIL: Component 3 — .vscode/settings.json does not exist")
        else:
            with open(settings_file, 'r') as f:
                content = f.read()
            stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            stripped = re.sub(r'/\*.*?\*/', '', stripped, flags=re.DOTALL)
            settings = json.loads(stripped)

            extra_paths = settings.get('python.analysis.extraPaths', None)
            if extra_paths is not None and isinstance(extra_paths, list):
                # Normalize paths for comparison
                normalized = [p.rstrip('/').lstrip('./') for p in extra_paths]
                has_src = 'src' in normalized
                has_lib = 'lib' in normalized
                if has_src and has_lib:
                    print(f"PASS: Component 3 — python.analysis.extraPaths contains src and lib: {extra_paths} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — extraPaths missing entries. src={has_src}, lib={has_lib}. Value: {extra_paths}")
            else:
                print(f"FAIL: Component 3 — python.analysis.extraPaths not found or not a list in settings.json")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
