"""
Initial Setup: Add multiple SSH host entries by editing SSH config file
Task ID: vscode_rrt_010
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_010'

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

    # Create empty SSH config file
    ssh_config_path = os.path.join(ssh_dir, 'config')
    with open(ssh_config_path, 'w') as f:
        f.write('')  # Empty config
    os.chmod(ssh_config_path, 0o644)

    # Create the identity file (prod_key) - a dummy private key placeholder
    prod_key_path = os.path.join(ssh_dir, 'prod_key')
    with open(prod_key_path, 'w') as f:
        f.write('-----BEGIN OPENSSH PRIVATE KEY-----\n')
        f.write('b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\n')
        f.write('QyNTUxOQAAACBmMzg5NjJhZTY1YjRiYTkxZmE3MDIzMTU2Yzg2YjRhMAAAAJh0ZXN0\n')
        f.write('a2V5dGVzdGtleQ==\n')
        f.write('-----END OPENSSH PRIVATE KEY-----\n')
    os.chmod(prod_key_path, 0o600)

    print(f'SSH config created (empty): {ssh_config_path}')
    print(f'Identity file created: {prod_key_path}')

    # Open VSCode with the SSH config file
    launch_gui(f'code "{ssh_config_path}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with SSH config file with DISPLAY=:0')

create_initial()
