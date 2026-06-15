"""
Reward Script: Fix Python debug configuration to allow stepping into library code
Task ID: vscode_fix_070
Domain: vscode
Scoring:
  Component 1 (0.5): First config 'justMyCode' is false
  Component 2 (0.5): Second config 'justMyCode' is false
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_070'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'pyproject', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file that may contain // comments (JSONC format)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist and be parseable
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configurations = data.get('configurations', [])
    if not configurations:
        print("FAIL: No configurations found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # Find all Python/debugpy configurations and check justMyCode
    python_configs_checked = 0

    # Component 1: First Python config has justMyCode == false (0.5 points)
    try:
        config = configurations[0] if len(configurations) > 0 else None
        if config and config.get('type') in ('debugpy', 'python'):
            val = config.get('justMyCode')
            if val is False:
                print(f"PASS: Component 1 — Config '{config.get('name', 'unknown')}' has justMyCode=false (0.5 pts)")
                total_score += 0.5
                python_configs_checked += 1
            else:
                print(f"FAIL: Component 1 — Config '{config.get('name', 'unknown')}' has justMyCode={val}, expected false")
                python_configs_checked += 1
        else:
            print(f"FAIL: Component 1 — First configuration is not a Python/debugpy config")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Second Python config has justMyCode == false (0.5 points)
    try:
        config = configurations[1] if len(configurations) > 1 else None
        if config and config.get('type') in ('debugpy', 'python'):
            val = config.get('justMyCode')
            if val is False:
                print(f"PASS: Component 2 — Config '{config.get('name', 'unknown')}' has justMyCode=false (0.5 pts)")
                total_score += 0.5
                python_configs_checked += 1
            else:
                print(f"FAIL: Component 2 — Config '{config.get('name', 'unknown')}' has justMyCode={val}, expected false")
                python_configs_checked += 1
        else:
            # If there's only one config, check that at least one was verified
            if python_configs_checked == 0:
                print(f"FAIL: Component 2 — No second Python/debugpy config found")
            else:
                print(f"INFO: Component 2 — Only one Python config found, skipping")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # If no Python configs were found at all, also check all configs generically
    if python_configs_checked == 0:
        # Fallback: check ANY config with justMyCode
        for i, config in enumerate(configurations):
            if 'justMyCode' in config:
                val = config.get('justMyCode')
                if val is False:
                    weight = 1.0 / len([c for c in configurations if 'justMyCode' in c])
                    print(f"PASS: Fallback — Config {i} '{config.get('name', 'unknown')}' has justMyCode=false ({weight:.2f} pts)")
                    total_score += weight
                else:
                    print(f"FAIL: Fallback — Config {i} '{config.get('name', 'unknown')}' has justMyCode={val}, expected false")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
