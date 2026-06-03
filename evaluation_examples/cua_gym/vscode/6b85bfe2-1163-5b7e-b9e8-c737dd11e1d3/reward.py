"""
Reward Script: VSCode custom terminal profile 'Python REPL'
Task ID: vscode_gf5_042
Domain: vscode
Scoring:
  - Component 1 (0.3): 'Python REPL' profile exists in terminal.integrated.profiles.linux
  - Component 2 (0.3): Profile path is 'python3' (the command to run)
  - Component 3 (0.4): Profile env has PYTHONSTARTUP set to '~/python-startup.py'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_042'

SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, stripping JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that a 'Python REPL' terminal profile has been added to VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Get terminal profiles for linux
    profiles = settings.get('terminal.integrated.profiles.linux', {})

    # Component 1: 'Python REPL' profile exists (0.3 points)
    try:
        python_repl = profiles.get('Python REPL')
        if python_repl is not None and isinstance(python_repl, dict):
            print(f"PASS: Component 1 — 'Python REPL' profile exists in terminal.integrated.profiles.linux (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — 'Python REPL' profile not found. Available profiles: {list(profiles.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Profile path/command is 'python3' (0.3 points)
    try:
        if python_repl and isinstance(python_repl, dict):
            # The command can be under 'path' or 'command' key
            cmd = python_repl.get('path') or python_repl.get('command', '')
            # Normalize: could be 'python3', '/usr/bin/python3', etc.
            if isinstance(cmd, str) and 'python3' in cmd:
                print(f"PASS: Component 2 — Profile command is '{cmd}' (contains python3) (0.3 pts)")
                total_score += 0.3
            elif isinstance(cmd, list) and any('python3' in str(c) for c in cmd):
                print(f"PASS: Component 2 — Profile command list contains python3: {cmd} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Profile command is '{cmd}', expected 'python3'")
        else:
            print(f"FAIL: Component 2 — Cannot check command, 'Python REPL' profile not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Profile env has PYTHONSTARTUP pointing to python-startup.py (0.4 points)
    try:
        if python_repl and isinstance(python_repl, dict):
            env_vars = python_repl.get('env', {})
            pythonstartup = env_vars.get('PYTHONSTARTUP', '')
            # Accept ~/python-startup.py or /home/user/python-startup.py or similar
            if isinstance(pythonstartup, str) and 'python-startup.py' in pythonstartup:
                print(f"PASS: Component 3 — PYTHONSTARTUP env set to '{pythonstartup}' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — PYTHONSTARTUP is '{pythonstartup}', expected path containing 'python-startup.py'")
        else:
            print(f"FAIL: Component 3 — Cannot check env, 'Python REPL' profile not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
