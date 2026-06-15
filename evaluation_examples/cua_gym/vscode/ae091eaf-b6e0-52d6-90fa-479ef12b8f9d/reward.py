"""
Reward Script: Configure VSCode terminal profiles
Task ID: vscode_wf_026
Domain: vscode
Scoring:
  Component 1: Python REPL profile (0.2)
  Component 2: Node REPL profile (0.2)
  Component 3: Project Shell profile with cwd + env (0.3)
  Component 4: Default profile set to Project Shell (0.3)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
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

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Get the terminal profiles block
    profiles = settings.get("terminal.integrated.profiles.linux", {})
    if not isinstance(profiles, dict):
        profiles = {}

    # Component 1: Python REPL profile with path=python3 (0.2 points)
    try:
        python_profile = profiles.get("Python REPL", None)
        if python_profile and isinstance(python_profile, dict):
            python_path = python_profile.get("path", "")
            if python_path == "python3":
                print(f"PASS: Component 1 -- Python REPL profile with path=python3 (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 -- Python REPL path expected 'python3', found '{python_path}'")
        else:
            print(f"FAIL: Component 1 -- 'Python REPL' profile not found in terminal profiles")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Node REPL profile with path=node (0.2 points)
    try:
        node_profile = profiles.get("Node REPL", None)
        if node_profile and isinstance(node_profile, dict):
            node_path = node_profile.get("path", "")
            if node_path == "node":
                print(f"PASS: Component 2 -- Node REPL profile with path=node (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 -- Node REPL path expected 'node', found '{node_path}'")
        else:
            print(f"FAIL: Component 2 -- 'Node REPL' profile not found in terminal profiles")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Project Shell profile with bash, cwd ~/project, env PROJECT_ENV=development (0.3 points)
    try:
        shell_profile = profiles.get("Project Shell", None)
        if shell_profile and isinstance(shell_profile, dict):
            sub_score = 0.0
            shell_path = shell_profile.get("path", "")
            shell_cwd = shell_profile.get("cwd", "")
            shell_env = shell_profile.get("env", {})

            # Check path is bash
            if shell_path == "bash" or shell_path == "/bin/bash" or shell_path == "/usr/bin/bash":
                sub_score += 0.1
            else:
                print(f"FAIL: Component 3a -- Project Shell path expected 'bash', found '{shell_path}'")

            # Check cwd is ~/project (accept variants)
            valid_cwds = ["~/project", os.path.expanduser("~/project"), "/home/user/project"]
            if shell_cwd in valid_cwds:
                sub_score += 0.1
            else:
                print(f"FAIL: Component 3b -- Project Shell cwd expected '~/project', found '{shell_cwd}'")

            # Check env has PROJECT_ENV=development
            if isinstance(shell_env, dict) and shell_env.get("PROJECT_ENV") == "development":
                sub_score += 0.1
            else:
                print(f"FAIL: Component 3c -- Project Shell env expected PROJECT_ENV=development, found '{shell_env}'")

            if sub_score > 0:
                print(f"PASS: Component 3 -- Project Shell profile partially/fully correct ({sub_score} pts)")
                total_score += sub_score
        else:
            print(f"FAIL: Component 3 -- 'Project Shell' profile not found in terminal profiles")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Default terminal profile set to 'Project Shell' (0.3 points)
    try:
        default_profile = settings.get("terminal.integrated.defaultProfile.linux", "")
        if default_profile == "Project Shell":
            print(f"PASS: Component 4 -- Default profile is 'Project Shell' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 -- Default profile expected 'Project Shell', found '{default_profile}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
