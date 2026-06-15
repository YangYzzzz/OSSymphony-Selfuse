"""
Reward Script: VSCode Dev Container Configuration
Task ID: vscode_gf6_025
Domain: vscode
Scoring:
  Component 1: devcontainer.json exists and is valid JSON (0.10)
  Component 2: devcontainer.json has correct name and workspaceFolder (0.10)
  Component 3: dockerComposeFile and service fields correct (0.15)
  Component 4: postCreateCommand is 'npm install' (0.10)
  Component 5: extensions list contains all 3 required extensions (0.15)
  Component 6: remoteEnv contains DATABASE_URL pointing to postgres (0.10)
  Component 7: docker-compose.yml exists and is valid YAML with 'app' service (0.10)
  Component 8: docker-compose.yml 'app' service uses node:18 image and has volume mount (0.10)
  Component 9: docker-compose.yml has 'postgres' service using postgres:15 (0.10)
"""

import os
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'devcontainer-node')
DEVCONTAINER_DIR = os.path.join(PROJECT_DIR, '.devcontainer')
DEVCONTAINER_JSON = os.path.join(DEVCONTAINER_DIR, 'devcontainer.json')
COMPOSE_FILE = os.path.join(DEVCONTAINER_DIR, 'docker-compose.yml')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =====================================================
    # Component 1: devcontainer.json exists and is valid JSON (0.10 points)
    # =====================================================
    dc_config = None
    try:
        if os.path.isfile(DEVCONTAINER_JSON):
            with open(DEVCONTAINER_JSON, 'r') as f:
                dc_config = json.load(f)
            if isinstance(dc_config, dict) and len(dc_config) > 0:
                print(f"PASS: Component 1 - devcontainer.json exists and is valid JSON (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 - devcontainer.json is empty or not a dict")
        else:
            print(f"FAIL: Component 1 - devcontainer.json not found at {DEVCONTAINER_JSON}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if dc_config is None:
        # Cannot proceed without devcontainer.json
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # =====================================================
    # Component 2: name and workspaceFolder correct (0.10 points)
    # =====================================================
    try:
        name_ok = dc_config.get('name') == 'Node.js Dev Container'
        workspace_ok = dc_config.get('workspaceFolder') == '/workspace'
        if name_ok and workspace_ok:
            print(f"PASS: Component 2 - name='{dc_config.get('name')}', workspaceFolder='{dc_config.get('workspaceFolder')}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 - name={dc_config.get('name')} (expected 'Node.js Dev Container'), workspaceFolder={dc_config.get('workspaceFolder')} (expected '/workspace')")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # =====================================================
    # Component 3: dockerComposeFile and service fields (0.15 points)
    # =====================================================
    try:
        compose_ref = dc_config.get('dockerComposeFile', '')
        service = dc_config.get('service', '')
        # Accept both 'docker-compose.yml' and '.devcontainer/docker-compose.yml' variants
        compose_ok = compose_ref in ('docker-compose.yml', '.devcontainer/docker-compose.yml', './docker-compose.yml')
        service_ok = service == 'app'
        if compose_ok and service_ok:
            print(f"PASS: Component 3 - dockerComposeFile='{compose_ref}', service='{service}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - dockerComposeFile='{compose_ref}' (expected 'docker-compose.yml'), service='{service}' (expected 'app')")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # =====================================================
    # Component 4: postCreateCommand is 'npm install' (0.10 points)
    # =====================================================
    try:
        post_cmd = dc_config.get('postCreateCommand', '')
        if post_cmd == 'npm install':
            print(f"PASS: Component 4 - postCreateCommand='{post_cmd}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - postCreateCommand='{post_cmd}' (expected 'npm install')")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # =====================================================
    # Component 5: extensions list contains all 3 required (0.15 points)
    # =====================================================
    try:
        required_extensions = {
            'dbaeumer.vscode-eslint',
            'esbenp.prettier-vscode',
            'ms-vscode.vscode-typescript-next'
        }
        # Extensions can be at top-level or nested under customizations.vscode.extensions
        extensions = dc_config.get('extensions', [])
        if not extensions:
            customizations = dc_config.get('customizations', {})
            vscode_custom = customizations.get('vscode', {})
            extensions = vscode_custom.get('extensions', [])

        # Normalize to lowercase for comparison
        actual_ext_set = {e.lower() for e in extensions} if extensions else set()
        required_lower = {e.lower() for e in required_extensions}

        if required_lower.issubset(actual_ext_set):
            print(f"PASS: Component 5 - All 3 required extensions found: {extensions} (0.15 pts)")
            total_score += 0.15
        else:
            missing = required_lower - actual_ext_set
            print(f"FAIL: Component 5 - Missing extensions: {missing}. Found: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # =====================================================
    # Component 6: remoteEnv has DATABASE_URL pointing to postgres (0.10 points)
    # =====================================================
    try:
        remote_env = dc_config.get('remoteEnv', {})
        db_url = remote_env.get('DATABASE_URL', '')
        if db_url and 'postgres' in db_url.lower():
            print(f"PASS: Component 6 - remoteEnv.DATABASE_URL='{db_url}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 - remoteEnv.DATABASE_URL='{db_url}' (expected to contain 'postgres')")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # =====================================================
    # Component 7: docker-compose.yml exists with 'app' service (0.10 points)
    # =====================================================
    compose_data = None
    try:
        if os.path.isfile(COMPOSE_FILE):
            # Parse YAML manually without pyyaml - just check for key strings
            with open(COMPOSE_FILE, 'r') as f:
                compose_content = f.read()

            # Check for 'app' service definition
            if 'services:' in compose_content and 'app:' in compose_content:
                print(f"PASS: Component 7 - docker-compose.yml exists with 'app' service (0.10 pts)")
                total_score += 0.10
                compose_data = compose_content
            else:
                print(f"FAIL: Component 7 - docker-compose.yml missing 'services:' or 'app:' section")
        else:
            print(f"FAIL: Component 7 - docker-compose.yml not found at {COMPOSE_FILE}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    # =====================================================
    # Component 8: app service uses node:18 image and has volume mount (0.10 points)
    # =====================================================
    try:
        if compose_data:
            has_node18 = 'mcr.microsoft.com/devcontainers/node:18' in compose_data
            # Check for a volume mount that maps to workspace
            has_volume = ('/workspace' in compose_data) and ('volumes:' in compose_data)
            if has_node18 and has_volume:
                print(f"PASS: Component 8 - app service has node:18 image and workspace volume mount (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 8 - node:18 image: {has_node18}, volume mount: {has_volume}")
        else:
            print(f"FAIL: Component 8 - No compose data to check")
    except Exception as e:
        print(f"ERROR: Component 8 - {e}")

    # =====================================================
    # Component 9: postgres service using postgres:15 (0.10 points)
    # =====================================================
    try:
        if compose_data:
            has_postgres_service = 'postgres:' in compose_data
            has_postgres15 = 'postgres:15' in compose_data
            if has_postgres_service and has_postgres15:
                print(f"PASS: Component 9 - postgres service with postgres:15 image found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 9 - postgres service: {has_postgres_service}, postgres:15 image: {has_postgres15}")
        else:
            print(f"FAIL: Component 9 - No compose data to check")
    except Exception as e:
        print(f"ERROR: Component 9 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
