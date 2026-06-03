"""
Reward Script: Configure VSCode terminal initial command
Task ID: vscode_rrt_087
Domain: vscode
Scoring:
  Component 1 (0.3): bash profile path is /bin/bash
  Component 2 (0.3): bash profile args list exists with correct structure
  Component 3 (0.4): args contain uname -a, echo Welcome!, and exec bash
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_087'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Navigate to the terminal profiles section
    profiles_linux = settings.get('terminal.integrated.profiles.linux', {})
    bash_profile = profiles_linux.get('bash', {}) if isinstance(profiles_linux, dict) else {}

    print(f"DEBUG: terminal.integrated.profiles.linux = {json.dumps(profiles_linux, indent=2)}")
    print(f"DEBUG: bash profile = {json.dumps(bash_profile, indent=2)}")

    # Component 1: bash profile path is set to /bin/bash (0.3 points)
    try:
        bash_path = bash_profile.get('path', None)
        if bash_path == '/bin/bash':
            print(f"PASS: Component 1 — bash profile path is '/bin/bash' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected path '/bin/bash', found: {bash_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: bash profile args is a non-empty list (0.3 points)
    try:
        bash_args = bash_profile.get('args', None)
        if isinstance(bash_args, list) and len(bash_args) > 0:
            print(f"PASS: Component 2 — bash profile args is a non-empty list: {bash_args} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected non-empty list for args, found: {bash_args}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: args contain the correct command with uname -a, echo Welcome!, exec bash (0.4 points)
    try:
        bash_args = bash_profile.get('args', [])
        if isinstance(bash_args, list):
            # Join all args into a single string for content checking
            args_str = ' '.join(str(a) for a in bash_args)
            has_uname = 'uname -a' in args_str
            has_welcome = "echo" in args_str.lower() and "welcome" in args_str.lower()
            has_exec_bash = 'exec bash' in args_str

            if has_uname and has_welcome and has_exec_bash:
                print(f"PASS: Component 3 — args contain uname -a, echo Welcome!, and exec bash (0.4 pts)")
                total_score += 0.4
            else:
                missing = []
                if not has_uname:
                    missing.append("'uname -a'")
                if not has_welcome:
                    missing.append("'echo Welcome!'")
                if not has_exec_bash:
                    missing.append("'exec bash'")
                print(f"FAIL: Component 3 — args missing: {', '.join(missing)}. Full args: {bash_args}")
        else:
            print(f"FAIL: Component 3 — args is not a list: {bash_args}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
