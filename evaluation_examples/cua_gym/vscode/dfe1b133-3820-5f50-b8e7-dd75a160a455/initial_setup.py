"""
Initial Setup: Set up SSH config for Remote-SSH extension
Task ID: vscode_we_065
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_065'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

def create_initial():
    ssh_dir = os.path.join(WORKDIR, '.ssh')
    os.makedirs(ssh_dir, exist_ok=True)

    # Create empty SSH config file (no host entries)
    config_path = os.path.join(ssh_dir, 'config')
    with open(config_path, 'w') as f:
        f.write("")  # Empty file - no entries

    # Set proper permissions
    os.chmod(ssh_dir, 0o700)
    os.chmod(config_path, 0o600)

    # Create a realistic SSH identity file (dev_key) so it exists on the system
    dev_key_path = os.path.join(ssh_dir, 'dev_key')
    if not os.path.exists(dev_key_path):
        # Generate a real SSH key pair for realism
        subprocess.run(
            ['ssh-keygen', '-t', 'ed25519', '-f', dev_key_path, '-N', '', '-C', 'developer@dev.example.com'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # Also create a known_hosts file for realism
    known_hosts_path = os.path.join(ssh_dir, 'known_hosts')
    if not os.path.exists(known_hosts_path):
        with open(known_hosts_path, 'w') as f:
            f.write("")
        os.chmod(known_hosts_path, 0o644)

    # Ensure Remote-SSH extension is installed
    result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True)
    if 'ms-vscode-remote.remote-ssh' not in result.stdout:
        subprocess.run(
            ['code', '--install-extension', 'ms-vscode-remote.remote-ssh'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(3)

    print(f'Initial SSH config created (empty): {config_path}')
    print(f'SSH key created: {dev_key_path}')

    # Launch VSCode
    launch_gui('code "/home/user"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
