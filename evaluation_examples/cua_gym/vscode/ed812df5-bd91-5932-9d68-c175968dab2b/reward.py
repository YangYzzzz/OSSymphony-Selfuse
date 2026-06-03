"""
Reward Script: Jupyter notebook environment with .env file and VSCode settings
Task ID: vscode_py_088
Domain: vscode
Scoring:
  Component 1: .env file contains API_KEY=xxx             (0.3 pts)
  Component 2: .env file contains BASE_URL=https://api.example.com (0.3 pts)
  Component 3: .vscode/settings.json has python.envFile    (0.4 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_088'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)


def verify_task(project_dir):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    env_file = os.path.join(project_dir, '.env')
    settings_file = os.path.join(project_dir, '.vscode', 'settings.json')

    # Component 1: .env file contains API_KEY=xxx (0.3 points)
    try:
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                env_content = f.read()
            # Check for API_KEY=xxx (the exact expected value)
            if re.search(r'^API_KEY\s*=\s*xxx\s*$', env_content, re.MULTILINE):
                print(f"PASS: Component 1 -- .env contains API_KEY=xxx (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 -- .env does not contain API_KEY=xxx. Content: {env_content!r}")
        else:
            print(f"FAIL: Component 1 -- .env file not found at {env_file}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: .env file contains BASE_URL=https://api.example.com (0.3 points)
    try:
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                env_content = f.read()
            if re.search(r'^BASE_URL\s*=\s*https://api\.example\.com\s*$', env_content, re.MULTILINE):
                print(f"PASS: Component 2 -- .env contains BASE_URL=https://api.example.com (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- .env does not contain BASE_URL=https://api.example.com. Content: {env_content!r}")
        else:
            print(f"FAIL: Component 2 -- .env file not found at {env_file}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: .vscode/settings.json contains python.envFile = ${workspaceFolder}/.env (0.4 points)
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                content = f.read()
            # Strip JSONC comments if present
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            settings = json.loads(cleaned)

            env_file_setting = settings.get("python.envFile", None)
            if env_file_setting == "${workspaceFolder}/.env":
                print(f"PASS: Component 3 -- settings.json has python.envFile = ${{workspaceFolder}}/.env (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 -- python.envFile is {env_file_setting!r}, expected '${{workspaceFolder}}/.env'")
        else:
            print(f"FAIL: Component 3 -- .vscode/settings.json not found at {settings_file}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
project_dir = PROJECT_DIR
if not os.path.exists(project_dir):
    print(f"Project directory not found: {project_dir}")
    print("REWARD: 0.0")
else:
    verify_task(project_dir)
