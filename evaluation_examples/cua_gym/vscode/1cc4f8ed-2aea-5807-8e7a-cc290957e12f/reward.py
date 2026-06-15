"""
Reward Script: Docker development workflow configuration in VSCode
Task ID: vscode_wf_044
Domain: vscode
Scoring:
  Component 1: Docker extension installed (0.15)
  Component 2: Dockerfile with Python/Flask setup (0.20)
  Component 3: docker-compose.yml with app + postgres services (0.25)
  Component 4: tasks.json with docker build/up/down tasks (0.20)
  Component 5: launch.json with debugpy remote attach on port 5678 (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_044'


def check_docker_extension_installed():
    """Check if Docker extension is installed by scanning extensions directory."""
    ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    if not os.path.isdir(ext_dir):
        return False
    entries = os.listdir(ext_dir)
    for entry in entries:
        if entry.lower().startswith('ms-azuretools.vscode-docker'):
            return True
    return False


def verify_task():
    """
    Verify Docker development workflow task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Docker extension installed (0.15 points)
    # Checks the extensions directory for ms-azuretools.vscode-docker
    try:
        if check_docker_extension_installed():
            print("PASS: Component 1 - Docker extension 'ms-azuretools.vscode-docker' is installed (0.15 pts)")
            total_score += 0.15
        else:
            ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
            entries = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
            print(f"FAIL: Component 1 - Docker extension not found. Extensions dir contents: {entries}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Dockerfile exists with Python base image and pip install (0.20 points)
    try:
        dockerfile_path = os.path.join(PROJECT, 'Dockerfile')
        if not os.path.exists(dockerfile_path):
            print(f"FAIL: Component 2 - Dockerfile not found at {dockerfile_path}")
        else:
            with open(dockerfile_path, 'r') as f:
                content = f.read().lower()

            sub_score = 0.0
            # Check Python base image
            if 'from python' in content:
                sub_score += 0.07
                print("  PASS: Component 2a - Python base image found in Dockerfile")
            else:
                print("  FAIL: Component 2a - No Python base image in Dockerfile")

            # Check pip install
            if 'pip install' in content or 'pip3 install' in content:
                sub_score += 0.07
                print("  PASS: Component 2b - pip install found in Dockerfile")
            else:
                print("  FAIL: Component 2b - No pip install in Dockerfile")

            # Check app startup (CMD or ENTRYPOINT)
            if 'cmd' in content or 'entrypoint' in content:
                sub_score += 0.06
                print("  PASS: Component 2c - App startup command found in Dockerfile")
            else:
                print("  FAIL: Component 2c - No CMD/ENTRYPOINT in Dockerfile")

            if sub_score > 0:
                print(f"PASS: Component 2 - Dockerfile checks ({sub_score:.2f} pts)")
                total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: docker-compose.yml with app and postgres services (0.25 points)
    try:
        compose_path = os.path.join(PROJECT, 'docker-compose.yml')
        if not os.path.exists(compose_path):
            # Also check .yaml extension
            compose_path = os.path.join(PROJECT, 'docker-compose.yaml')

        if not os.path.exists(compose_path):
            print("FAIL: Component 3 - docker-compose.yml not found")
        else:
            with open(compose_path, 'r') as f:
                content = f.read()
            content_lower = content.lower()

            sub_score = 0.0

            # Check for 'app' service
            if re.search(r'^\s+app:', content, re.MULTILINE):
                sub_score += 0.08
                print("  PASS: Component 3a - 'app' service found in docker-compose.yml")
            else:
                print("  FAIL: Component 3a - 'app' service not found in docker-compose.yml")

            # Check for 'postgres' service
            if re.search(r'^\s+postgres:', content, re.MULTILINE):
                sub_score += 0.08
                print("  PASS: Component 3b - 'postgres' service found in docker-compose.yml")
            else:
                print("  FAIL: Component 3b - 'postgres' service not found in docker-compose.yml")

            # Check for port mappings (5678 for debugpy)
            if '5678' in content:
                sub_score += 0.05
                print("  PASS: Component 3c - Port 5678 mapping found in docker-compose.yml")
            else:
                print("  FAIL: Component 3c - Port 5678 mapping not found in docker-compose.yml")

            # Check for debugpy in command/entrypoint
            if 'debugpy' in content_lower:
                sub_score += 0.04
                print("  PASS: Component 3d - debugpy reference found in docker-compose.yml")
            else:
                print("  FAIL: Component 3d - debugpy not referenced in docker-compose.yml")

            if sub_score > 0:
                print(f"PASS: Component 3 - docker-compose.yml checks ({sub_score:.2f} pts)")
                total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: tasks.json with docker build, up, down tasks (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 4 - tasks.json not found at {tasks_path}")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_config = json.loads(cleaned)

            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '').lower() for t in tasks]

            sub_score = 0.0

            # Check for docker build task
            if any('docker' in label and 'build' in label for label in task_labels):
                sub_score += 0.07
                print("  PASS: Component 4a - 'docker build' task found")
            else:
                print(f"  FAIL: Component 4a - 'docker build' task not found. Labels: {task_labels}")

            # Check for docker up task
            if any('docker' in label and 'up' in label for label in task_labels):
                sub_score += 0.07
                print("  PASS: Component 4b - 'docker up' task found")
            else:
                print(f"  FAIL: Component 4b - 'docker up' task not found. Labels: {task_labels}")

            # Check for docker down task
            if any('docker' in label and 'down' in label for label in task_labels):
                sub_score += 0.06
                print("  PASS: Component 4c - 'docker down' task found")
            else:
                print(f"  FAIL: Component 4c - 'docker down' task not found. Labels: {task_labels}")

            if sub_score > 0:
                print(f"PASS: Component 4 - tasks.json checks ({sub_score:.2f} pts)")
                total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: launch.json with debugpy remote attach on port 5678 (0.20 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print(f"FAIL: Component 5 - launch.json not found at {launch_path}")
        else:
            with open(launch_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_config = json.loads(cleaned)

            configs = launch_config.get('configurations', [])
            sub_score = 0.0

            # Scan all configurations for debugpy/attach/port requirements
            has_debugpy_type = any(
                'debugpy' in str(cfg.get('type', '')).lower() or 'python' in str(cfg.get('type', '')).lower()
                for cfg in configs
            )
            has_attach_request = any(
                str(cfg.get('request', '')).lower() == 'attach'
                for cfg in configs
            )
            has_port_5678 = any(
                (isinstance(cfg.get('connect', {}), dict) and cfg.get('connect', {}).get('port') == 5678)
                or cfg.get('port') == 5678
                for cfg in configs
            )

            if has_debugpy_type:
                sub_score += 0.07
                print("  PASS: Component 5a - debugpy configuration type found")
            else:
                print("  FAIL: Component 5a - No debugpy configuration type found")

            if has_attach_request:
                sub_score += 0.07
                print("  PASS: Component 5b - 'attach' request type found")
            else:
                print("  FAIL: Component 5b - No 'attach' request type found")

            if has_port_5678:
                sub_score += 0.06
                print("  PASS: Component 5c - Port 5678 configured")
            else:
                print("  FAIL: Component 5c - Port 5678 not found in connect configuration")

            if sub_score > 0:
                print(f"PASS: Component 5 - launch.json checks ({sub_score:.2f} pts)")
                total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
