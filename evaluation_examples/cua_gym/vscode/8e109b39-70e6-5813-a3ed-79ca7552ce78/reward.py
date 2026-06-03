"""
Reward Script: Docker-based Python/Flask debugging configuration in VSCode
Task ID: vscode_gf6_040
Domain: vscode
Scoring:
  Component 1 (0.35): docker-compose.yml has 'debug' service with port 5678 and debugpy command
  Component 2 (0.35): .vscode/launch.json has 'Docker: Debug Flask' config with correct fields
  Component 3 (0.15): .vscode/tasks.json has 'Docker: Start Debug' shell task
  Component 4 (0.15): launch.json preLaunchTask links to 'Docker: Start Debug'
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'docker-python-debug')
TASK_ID = 'vscode_gf6_040'


def parse_yaml_simple(content):
    """Minimal YAML parser for docker-compose — extracts service names and their properties."""
    # We only need to detect service blocks and key properties
    return content


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: docker-compose.yml has 'debug' service (0.35 points)
    # Sub-checks: service exists, port 5678, debugpy command
    # =========================================================================
    try:
        dc_path = os.path.join(PROJECT, 'docker-compose.yml')
        with open(dc_path, 'r') as f:
            dc_content = f.read()

        comp1_score = 0.0

        # Check that a 'debug' service section exists
        # Pattern: "debug:" at service indentation level (2 spaces under services)
        if re.search(r'^\s{2}debug:', dc_content, re.MULTILINE):
            print("PASS: Component 1a — 'debug' service found in docker-compose.yml")
            comp1_score += 0.10
        else:
            print("FAIL: Component 1a — 'debug' service not found in docker-compose.yml")

        # Check that port 5678 is mapped
        # Look for 5678:5678 or "5678:5678" in the debug service section
        # Extract debug service block
        debug_match = re.search(r'^\s{2}debug:\s*\n((?:\s{4,}.*\n)*)', dc_content, re.MULTILINE)
        if debug_match:
            debug_block = debug_match.group(1)

            # Check port 5678
            if re.search(r'5678:5678', debug_block):
                print("PASS: Component 1b — Port 5678 mapped in debug service")
                comp1_score += 0.10
            else:
                print(f"FAIL: Component 1b — Port 5678 not mapped in debug service")

            # Check debugpy command
            if 'debugpy' in debug_block and '--wait-for-client' in debug_block and '--listen' in debug_block:
                print("PASS: Component 1c — debugpy command with --wait-for-client and --listen found")
                comp1_score += 0.10
            else:
                print(f"FAIL: Component 1c — debugpy command not properly configured")

            # Check 0.0.0.0:5678 listen address
            if '0.0.0.0:5678' in debug_block:
                print("PASS: Component 1d — debugpy listens on 0.0.0.0:5678")
                comp1_score += 0.05
            else:
                print("FAIL: Component 1d — debugpy not listening on 0.0.0.0:5678")
        else:
            print("FAIL: Component 1b-d — Could not parse debug service block")

        total_score += comp1_score
        print(f"  Component 1 total: {comp1_score}/0.35")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: .vscode/launch.json with correct config (0.35 points)
    # Sub-checks: file exists, name, type, request, connect host/port, pathMappings
    # =========================================================================
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print("FAIL: Component 2 — .vscode/launch.json does not exist")
        else:
            # Handle JSONC (strip comments)
            with open(launch_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch = json.loads(content_clean)

            configs = launch.get('configurations', [])
            comp2_score = 0.0

            # Find the 'Docker: Debug Flask' configuration
            debug_config = None
            for cfg in configs:
                if cfg.get('name') == 'Docker: Debug Flask':
                    debug_config = cfg
                    break

            if debug_config is None:
                print("FAIL: Component 2a — No 'Docker: Debug Flask' configuration found")
            else:
                print("PASS: Component 2a — 'Docker: Debug Flask' configuration found")
                comp2_score += 0.05

                # Check type == 'python' (or debugpy which is the newer name)
                cfg_type = debug_config.get('type', '')
                if cfg_type in ('python', 'debugpy'):
                    print(f"PASS: Component 2b — type is '{cfg_type}'")
                    comp2_score += 0.05
                else:
                    print(f"FAIL: Component 2b — type is '{cfg_type}', expected 'python'")

                # Check request == 'attach'
                if debug_config.get('request') == 'attach':
                    print("PASS: Component 2c — request is 'attach'")
                    comp2_score += 0.05
                else:
                    print(f"FAIL: Component 2c — request is '{debug_config.get('request')}', expected 'attach'")

                # Check connect.host == 'localhost' and connect.port == 5678
                connect = debug_config.get('connect', {})
                if connect.get('host') == 'localhost' and connect.get('port') == 5678:
                    print("PASS: Component 2d — connect: host=localhost, port=5678")
                    comp2_score += 0.10
                else:
                    print(f"FAIL: Component 2d — connect: {connect}, expected host=localhost, port=5678")

                # Check pathMappings
                mappings = debug_config.get('pathMappings', [])
                if len(mappings) > 0:
                    m = mappings[0]
                    local = m.get('localRoot', '')
                    remote = m.get('remoteRoot', '')
                    if '${workspaceFolder}' in local and '/app' in local and remote == '/app':
                        print(f"PASS: Component 2e — pathMappings: localRoot='{local}', remoteRoot='{remote}'")
                        comp2_score += 0.10
                    else:
                        print(f"FAIL: Component 2e — pathMappings localRoot='{local}', remoteRoot='{remote}', expected localRoot containing ${{workspaceFolder}}/app -> /app")
                else:
                    print("FAIL: Component 2e — No pathMappings found")

            total_score += comp2_score
            print(f"  Component 2 total: {comp2_score}/0.35")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: .vscode/tasks.json with 'Docker: Start Debug' task (0.15 points)
    # =========================================================================
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print("FAIL: Component 3 — .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_json = json.loads(content_clean)

            tasks = tasks_json.get('tasks', [])
            comp3_score = 0.0

            # Find 'Docker: Start Debug' task
            debug_task = None
            for t in tasks:
                if t.get('label') == 'Docker: Start Debug':
                    debug_task = t
                    break

            if debug_task is None:
                print("FAIL: Component 3a — No 'Docker: Start Debug' task found")
            else:
                print("PASS: Component 3a — 'Docker: Start Debug' task found")
                comp3_score += 0.05

                # Check command contains docker-compose up
                cmd = debug_task.get('command', '')
                if 'docker-compose' in cmd and 'up' in cmd and 'debug' in cmd:
                    print(f"PASS: Component 3b — command is '{cmd}'")
                    comp3_score += 0.10
                elif 'docker compose' in cmd and 'up' in cmd and 'debug' in cmd:
                    # Also accept docker compose (v2 syntax)
                    print(f"PASS: Component 3b — command is '{cmd}' (docker compose v2)")
                    comp3_score += 0.10
                else:
                    print(f"FAIL: Component 3b — command is '{cmd}', expected docker-compose up -d debug")

            total_score += comp3_score
            print(f"  Component 3 total: {comp3_score}/0.15")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: launch.json preLaunchTask references 'Docker: Start Debug' (0.15 points)
    # =========================================================================
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print("FAIL: Component 4 — launch.json does not exist (needed for preLaunchTask check)")
        else:
            with open(launch_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch = json.loads(content_clean)

            configs = launch.get('configurations', [])
            comp4_score = 0.0

            # Find the debug config and check preLaunchTask or dependsOn
            for cfg in configs:
                if cfg.get('name') == 'Docker: Debug Flask':
                    pre_task = cfg.get('preLaunchTask', '')
                    depends_on = cfg.get('dependsOn', '')
                    if pre_task == 'Docker: Start Debug':
                        print(f"PASS: Component 4 — preLaunchTask is 'Docker: Start Debug'")
                        comp4_score = 0.15
                    elif depends_on == 'Docker: Start Debug':
                        print(f"PASS: Component 4 — dependsOn is 'Docker: Start Debug'")
                        comp4_score = 0.15
                    else:
                        print(f"FAIL: Component 4 — preLaunchTask='{pre_task}', dependsOn='{depends_on}', expected 'Docker: Start Debug'")
                    break
            else:
                print("FAIL: Component 4 — 'Docker: Debug Flask' config not found")

            total_score += comp4_score
            print(f"  Component 4 total: {comp4_score}/0.15")

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Final score
    # =========================================================================
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
