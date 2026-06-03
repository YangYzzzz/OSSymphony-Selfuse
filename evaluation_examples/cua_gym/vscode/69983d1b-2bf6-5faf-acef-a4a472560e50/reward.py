"""
Reward Script: Add preLaunchTask to VSCode launch.json
Task ID: vscode_dbg_016
Domain: vs_code
Scoring:
  Component 1: preLaunchTask field exists in launch configuration (0.5 points)
  Component 2: preLaunchTask value is exactly "npm: build" (0.3 points)
  Component 3: preLaunchTask is in the correct Node.js config for dist/app.js, other properties intact (0.2 points)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_016'

LAUNCH_JSON_PATH = f'{WORKDIR}/projects/build-app/.vscode/launch.json'


def load_json_with_comments(file_path):
    """Load JSON file, stripping JSONC-style comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task(file_path):
    """
    Verify that the launch.json has a preLaunchTask of "npm: build"
    in the Node.js launch configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the launch.json file
    try:
        launch_config = load_json_with_comments(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Cannot parse launch.json as JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve configurations list
    configurations = launch_config.get('configurations', [])
    if not isinstance(configurations, list) or len(configurations) == 0:
        print("CRITICAL: No configurations found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: preLaunchTask field exists in any configuration (0.5 points)
    # This FAILS on initial (no preLaunchTask) -> PASSES on golden (preLaunchTask added)
    try:
        pre_launch_tasks = []
        for cfg in configurations:
            if 'preLaunchTask' in cfg:
                pre_launch_tasks.append(cfg['preLaunchTask'])

        if pre_launch_tasks:
            print(f"PASS: Component 1 — preLaunchTask field exists (found: {pre_launch_tasks}) (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — no preLaunchTask found in any configuration")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: preLaunchTask value is exactly "npm: build" (0.3 points)
    # This FAILS on initial -> PASSES on golden
    try:
        found_correct_value = False
        for cfg in configurations:
            if cfg.get('preLaunchTask') == 'npm: build':
                found_correct_value = True
                break

        if found_correct_value:
            print("PASS: Component 2 — preLaunchTask value is exactly \"npm: build\" (0.3 pts)")
            total_score += 0.3
        else:
            # Report actual values for debugging
            actual_values = [cfg.get('preLaunchTask') for cfg in configurations if 'preLaunchTask' in cfg]
            print(f"FAIL: Component 2 — preLaunchTask value is not \"npm: build\", found: {actual_values}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: preLaunchTask is in the correct Node.js launch config for dist/app.js
    #              AND the existing config properties are preserved (0.2 points)
    # This FAILS on initial -> PASSES on golden
    try:
        correct_config_found = False
        for cfg in configurations:
            is_node_config = (
                cfg.get('type') == 'node' and
                cfg.get('request') == 'launch' and
                '${workspaceFolder}/dist/app.js' in str(cfg.get('program', ''))
            )
            has_pre_launch = cfg.get('preLaunchTask') == 'npm: build'

            if is_node_config and has_pre_launch:
                # Verify key existing properties are preserved
                has_skip_files = 'skipFiles' in cfg and isinstance(cfg['skipFiles'], list)
                has_out_files = 'outFiles' in cfg and isinstance(cfg['outFiles'], list)
                if has_skip_files and has_out_files:
                    correct_config_found = True
                    break

        if correct_config_found:
            print("PASS: Component 3 — preLaunchTask in correct Node.js config for dist/app.js, properties intact (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 3 — preLaunchTask not found in the correct Node.js launch config for dist/app.js with all properties intact")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
