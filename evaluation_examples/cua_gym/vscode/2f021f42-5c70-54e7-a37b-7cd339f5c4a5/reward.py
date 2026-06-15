"""
Reward Script: VSCode env.d.ts type declaration for Node.js ProcessEnv
Task ID: vscode_web_074
Domain: vscode
Scoring:
  Component 1 (0.15): env.d.ts file exists at src/types/env.d.ts
  Component 2 (0.25): Contains 'declare namespace NodeJS' and 'interface ProcessEnv'
  Component 3 (0.60): All 4 env vars declared with correct types (0.15 each)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_074'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'api-server')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # The expected env.d.ts file path
    env_dts_path = os.path.join(PROJECT_DIR, 'src', 'types', 'env.d.ts')

    # Component 1: env.d.ts file exists (0.15 points)
    try:
        if os.path.isfile(env_dts_path):
            print(f"PASS: Component 1 — env.d.ts exists at {env_dts_path} (0.15 pts)")
            total_score += 0.15
        else:
            # Also check alternative locations
            alt_paths = [
                os.path.join(PROJECT_DIR, 'src', 'env.d.ts'),
                os.path.join(PROJECT_DIR, 'types', 'env.d.ts'),
                os.path.join(PROJECT_DIR, 'env.d.ts'),
                os.path.join(PROJECT_DIR, 'src', 'typings', 'env.d.ts'),
            ]
            env_dts_path = next((alt for alt in alt_paths if os.path.isfile(alt)), None)
            if env_dts_path is not None:
                print(f"PASS: Component 1 — env.d.ts found at alternate location {env_dts_path} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — env.d.ts not found at expected path or alternatives")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read the file content
    try:
        with open(env_dts_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read {env_dts_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Contains namespace NodeJS and interface ProcessEnv (0.25 points)
    try:
        # Check for 'declare namespace NodeJS' or 'namespace NodeJS'
        has_namespace = bool(re.search(r'(declare\s+)?namespace\s+NodeJS', content))
        # Check for 'interface ProcessEnv'
        has_interface = bool(re.search(r'interface\s+ProcessEnv', content))

        if has_namespace and has_interface:
            print(f"PASS: Component 2 — namespace NodeJS with interface ProcessEnv found (0.25 pts)")
            total_score += 0.25
        elif has_namespace:
            print(f"PARTIAL: Component 2 — namespace NodeJS found but interface ProcessEnv missing (0.1 pts)")
            total_score += 0.1
        elif has_interface:
            print(f"PARTIAL: Component 2 — interface ProcessEnv found but namespace NodeJS missing (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — neither namespace NodeJS nor interface ProcessEnv found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 4 env vars with correct types (0.60 points, 0.15 each)
    env_vars = {
        'DATABASE_URL': r'DATABASE_URL\s*:\s*string',
        'API_KEY': r'API_KEY\s*:\s*string',
        'NODE_ENV': r"NODE_ENV\s*:\s*['\"]development['\"]\s*\|\s*['\"]production['\"]\s*\|\s*['\"]test['\"]",
        'PORT': r'PORT\s*:\s*string',
    }

    try:
        for var_name, pattern in env_vars.items():
            if re.search(pattern, content):
                print(f"PASS: Component 3 — {var_name} declared with correct type (0.15 pts)")
                total_score += 0.15
            else:
                # Check if the variable is at least present (partial)
                if re.search(rf'{var_name}\s*:', content):
                    print(f"PARTIAL: Component 3 — {var_name} present but type may be wrong (0.05 pts)")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 3 — {var_name} not found in env.d.ts")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
