"""
Reward Script: Create .env and .env.example files in project root
Task ID: vscode_file_034
Domain: vs_code
Scoring:
  - Component 1: .env file exists in /home/user/api-server/           (0.3 pts)
  - Component 2: .env.example file exists in /home/user/api-server/   (0.3 pts)
  - Component 3: .env.example contains all required placeholder vars  (0.4 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_034'
PROJECT_ROOT = '/home/user/api-server'

# Required placeholder variables that must appear in .env.example
REQUIRED_VARS = ['DB_HOST=', 'DB_PORT=', 'DB_NAME=', 'API_KEY=']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Create both a .env file and a .env.example file in the project root.
    The .env.example should contain placeholder variables:
      DB_HOST=
      DB_PORT=
      DB_NAME=
      API_KEY=
    """
    total_score = 0.0

    env_path = os.path.join(PROJECT_ROOT, '.env')
    env_example_path = os.path.join(PROJECT_ROOT, '.env.example')

    # Component 1: .env file exists in the project root (0.3 points)
    # This FAILS on initial_env (no .env present) and PASSES on golden_env
    try:
        if os.path.isfile(env_path):
            print(f"PASS: Component 1 — .env file exists at {env_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — .env file not found at {env_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .env.example file exists in the project root (0.3 points)
    # This FAILS on initial_env (no .env.example present) and PASSES on golden_env
    try:
        if os.path.isfile(env_example_path):
            print(f"PASS: Component 2 — .env.example file exists at {env_example_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — .env.example file not found at {env_example_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .env.example contains all required placeholder variables (0.4 points)
    # Checks that each of DB_HOST=, DB_PORT=, DB_NAME=, API_KEY= appears in .env.example
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if os.path.isfile(env_example_path):
            with open(env_example_path, 'r') as f:
                content = f.read()

            # Check each required variable is present
            missing_vars = []
            for var in REQUIRED_VARS:
                if var not in content:
                    missing_vars.append(var)

            if not missing_vars:
                print(f"PASS: Component 3 — .env.example contains all required placeholder variables: {REQUIRED_VARS} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — .env.example is missing variables: {missing_vars}")
                print(f"      Found content: {repr(content)}")
        else:
            print(f"FAIL: Component 3 — .env.example not found, cannot check placeholder variables")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
