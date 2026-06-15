"""
Reward Script: Multi-environment VSCode configuration system
Task ID: vscode_gf3_095
Domain: vscode
Scoring:
  - Component 1 (0.15): launch.json exists and is valid JSON with version field
  - Component 2 (0.30): Three named launch configurations exist
  - Component 3 (0.20): Each configuration has correct envFile property
  - Component 4 (0.20): tasks.json has 'Validate Env' task running node script
  - Component 5 (0.15): All launch configs have preLaunchTask = 'Validate Env'
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_095'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'fullstack')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
LAUNCH_PATH = os.path.join(VSCODE_DIR, 'launch.json')
TASKS_PATH = os.path.join(VSCODE_DIR, 'tasks.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Load launch.json ----
    launch_data = None
    try:
        with open(LAUNCH_PATH, 'r') as f:
            launch_data = json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {LAUNCH_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: launch.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json exists and is valid JSON with version (0.15 points)
    try:
        if isinstance(launch_data, dict) and 'version' in launch_data and 'configurations' in launch_data:
            print(f"PASS: Component 1 — launch.json is valid with version={launch_data['version']} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — launch.json missing 'version' or 'configurations' key")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Three named launch configurations exist (0.30 points)
    # Expected names: 'Debug: Local', 'Debug: Staging (Remote Attach)', 'Debug: Production Read-Only'
    try:
        configs = launch_data.get('configurations', [])
        config_names = [c.get('name', '') for c in configs]
        expected_names = [
            'Debug: Local',
            'Debug: Staging (Remote Attach)',
            'Debug: Production Read-Only'
        ]
        found_count = sum(1 for name in expected_names if name in config_names)
        if found_count == 3:
            print(f"PASS: Component 2 — All 3 launch configurations found: {config_names} (0.30 pts)")
            total_score += 0.30
        elif found_count > 0:
            partial = round(0.30 * found_count / 3, 2)
            print(f"PARTIAL: Component 2 — {found_count}/3 configs found: {config_names} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — None of the expected configs found. Got: {config_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each configuration has the correct envFile property (0.20 points)
    try:
        configs = launch_data.get('configurations', [])
        config_by_name = {c.get('name', ''): c for c in configs}

        expected_envfiles = {
            'Debug: Local': '.env.local',
            'Debug: Staging (Remote Attach)': '.env.staging',
            'Debug: Production Read-Only': '.env.production.readonly'
        }

        envfile_matches = 0
        for config_name, expected_file in expected_envfiles.items():
            cfg = config_by_name.get(config_name, {})
            env_file = cfg.get('envFile', '')
            # Accept both relative and ${workspaceFolder}-prefixed paths
            if env_file and (env_file.endswith(expected_file)):
                envfile_matches += 1
                print(f"  envFile OK: '{config_name}' -> '{env_file}'")
            else:
                print(f"  envFile MISMATCH: '{config_name}' -> expected '*{expected_file}', got '{env_file}'")

        if envfile_matches == 3:
            print(f"PASS: Component 3 — All 3 envFile properties correct (0.20 pts)")
            total_score += 0.20
        elif envfile_matches > 0:
            partial = round(0.20 * envfile_matches / 3, 2)
            print(f"PARTIAL: Component 3 — {envfile_matches}/3 envFile correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No envFile properties match expected values")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tasks.json has 'Validate Env' task running a node script (0.20 points)
    try:
        with open(TASKS_PATH, 'r') as f:
            tasks_data = json.load(f)

        tasks = tasks_data.get('tasks', [])
        validate_task = None
        for t in tasks:
            if t.get('label', '') == 'Validate Env':
                validate_task = t
                break

        if validate_task is None:
            print(f"FAIL: Component 4 — No task with label 'Validate Env' found in tasks.json")
        else:
            # Check it runs a node script
            command = validate_task.get('command', '')
            args = validate_task.get('args', [])
            task_type = validate_task.get('type', '')

            # Check it's a node-based command (shell type with 'node' command)
            uses_node = ('node' in command.lower())

            if uses_node:
                print(f"PASS: Component 4 — 'Validate Env' task found, command='{command}', type='{task_type}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — 'Validate Env' task exists but command is not node-based: command='{command}', type='{task_type}'")
    except FileNotFoundError:
        print(f"FAIL: Component 4 — tasks.json not found at {TASKS_PATH}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 4 — tasks.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All launch configs have preLaunchTask = 'Validate Env' (0.15 points)
    try:
        configs = launch_data.get('configurations', [])
        config_by_name = {c.get('name', ''): c for c in configs}

        expected_names = [
            'Debug: Local',
            'Debug: Staging (Remote Attach)',
            'Debug: Production Read-Only'
        ]

        prelaunch_matches = 0
        for config_name in expected_names:
            cfg = config_by_name.get(config_name, {})
            prelaunch = cfg.get('preLaunchTask', '')
            if prelaunch == 'Validate Env':
                prelaunch_matches += 1
                print(f"  preLaunchTask OK: '{config_name}' -> '{prelaunch}'")
            else:
                print(f"  preLaunchTask MISMATCH: '{config_name}' -> expected 'Validate Env', got '{prelaunch}'")

        if prelaunch_matches == 3:
            print(f"PASS: Component 5 — All 3 configs have preLaunchTask='Validate Env' (0.15 pts)")
            total_score += 0.15
        elif prelaunch_matches > 0:
            partial = round(0.15 * prelaunch_matches / 3, 2)
            print(f"PARTIAL: Component 5 — {prelaunch_matches}/3 preLaunchTask correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No configs have preLaunchTask='Validate Env'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
