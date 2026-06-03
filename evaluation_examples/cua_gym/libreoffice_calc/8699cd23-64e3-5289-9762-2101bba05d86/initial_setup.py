"""
Initial Setup: Docker installed but docker-compose missing
Task ID: osworld_multi_apps_cli_path_fix_007
Domain: os

Sets up:
- A mock 'docker' binary in ~/.local/bin/ simulating Docker being installed
- ~/.bashrc without any docker-compose alias or PATH entry for docker-compose
- Terminal and Chrome browser open as per task context
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_007'
LOCAL_BIN = os.path.join(WORKDIR, '.local', 'bin')
BASHRC = os.path.join(WORKDIR, '.bashrc')


def launch_gui(command: str, delay_sec: float = 1.5):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def setup_initial():
    # Step 1: Ensure ~/.local/bin exists
    os.makedirs(LOCAL_BIN, exist_ok=True)
    print(f'Ensured {LOCAL_BIN} exists')

    # Step 2: Create a mock 'docker' binary simulating Docker being installed
    docker_bin = os.path.join(LOCAL_BIN, 'docker')
    docker_script = r"""#!/bin/bash
# Mock docker binary — simulates Docker being installed (without docker-compose)
ARGS="$@"

case "$1" in
    --version)
        echo "Docker version 24.0.7, build afdd53b"
        ;;
    version)
        echo "Docker version 24.0.7, build afdd53b"
        ;;
    info)
        echo "Client: Docker Engine - Community"
        echo " Version: 24.0.7"
        echo " Context: default"
        ;;
    compose)
        # docker compose (plugin) is available as 'docker compose'
        shift
        echo "docker compose $@"
        ;;
    ps)
        echo "CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES"
        ;;
    *)
        echo "docker: '$1' is not a docker command."
        echo "See 'docker --help'"
        exit 1
        ;;
esac
"""
    with open(docker_bin, 'w') as f:
        f.write(docker_script)
    os.chmod(docker_bin, 0o755)
    print(f'Created mock docker binary at {docker_bin}')

    # Step 3: Remove any existing docker-compose binary from user paths
    docker_compose_bin = os.path.join(LOCAL_BIN, 'docker-compose')
    if os.path.exists(docker_compose_bin):
        os.remove(docker_compose_bin)
        print(f'Removed existing docker-compose binary from {docker_compose_bin}')
    else:
        print(f'No docker-compose binary found in {docker_compose_bin} (good)')

    # Step 4: Ensure ~/.bashrc does NOT contain any docker-compose alias or PATH entry
    # Read current ~/.bashrc
    with open(BASHRC, 'r') as f:
        bashrc_content = f.read()

    # Remove any existing docker-compose related lines
    lines = bashrc_content.splitlines(keepends=True)
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip any docker-compose alias or PATH additions for docker-compose
        if 'docker-compose' in stripped or 'docker compose' in stripped.lower():
            print(f'Removing docker-compose line from .bashrc: {stripped}')
            continue
        filtered_lines.append(line)

    clean_bashrc = ''.join(filtered_lines)
    with open(BASHRC, 'w') as f:
        f.write(clean_bashrc)
    print(f'Cleaned ~/.bashrc of any docker-compose entries')

    # Step 5: Verify docker-compose is NOT available
    result = subprocess.run(
        ['bash', '-l', '-c', 'which docker-compose 2>/dev/null; echo rc=$?'],
        capture_output=True, text=True
    )
    if 'docker-compose' in result.stdout.split('\n')[0]:
        print(f'WARNING: docker-compose still found: {result.stdout}')
    else:
        print('Verified: docker-compose is NOT available (correct initial state)')

    # Step 6: Verify docker IS available
    result = subprocess.run(
        ['bash', '-l', '-c', 'which docker && docker --version'],
        capture_output=True, text=True
    )
    print(f'Docker status: {result.stdout.strip()}')

    # Step 7: Launch GUI - Terminal and Chrome browser
    # Open GNOME Terminal
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('Launched GNOME Terminal')

    # Open Chrome browser (for searching how to install docker-compose)
    launch_gui('google-chrome --new-window', delay_sec=2.0)
    print('Launched Chrome browser')

    print(f'\nInitial setup complete for task: {TASK_ID}')
    print('State: Docker installed (mock), docker-compose NOT available')
    print('GUI: Terminal and Chrome browser are open')
    print('GUI_READY: launched required app(s) with DISPLAY=:0')


setup_initial()
