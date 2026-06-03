"""
Initial Setup: Fix SSH config for Remote-SSH extension
Task ID: vscode_fix_048
Domain: vscode

Creates:
  - ~/.ssh/config with Host entry for 'devbox' (missing IdentityFile)
  - ~/.ssh/id_ed25519_work (dummy private key)
  - ~/.ssh/id_ed25519_work.pub (dummy public key)
  - Opens VSCode with the SSH config file
"""

import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
SSH_DIR = os.path.join(HOME, ".ssh")
SSH_CONFIG = os.path.join(SSH_DIR, "config")
KEY_PATH = os.path.join(SSH_DIR, "id_ed25519_work")
KEY_PUB_PATH = KEY_PATH + ".pub"


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
    # Ensure .ssh directory exists with correct permissions
    os.makedirs(SSH_DIR, exist_ok=True)
    os.chmod(SSH_DIR, 0o700)

    # Create SSH config with Host entry for 'devbox' but NO IdentityFile
    ssh_config_content = """\
# SSH Configuration File
# Last updated: 2025-11-20

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

Host devbox
    HostName 10.128.0.47
    User deploy
    Port 22
    ForwardAgent no
    StrictHostKeyChecking ask

Host staging-server
    HostName staging.internal.acmecorp.com
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_rsa_staging
    ForwardAgent yes

Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
"""
    with open(SSH_CONFIG, "w") as f:
        f.write(ssh_config_content)
    os.chmod(SSH_CONFIG, 0o644)

    # Create a dummy ed25519 private key file (realistic-looking but not real)
    dummy_private_key = """\
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBmVk3wR7qI5Ky6jTf0H8Z2GnJ3D9cXmLpKVqFw2H4xDAAAAJhBxKfEQc
SnxAAAAAtzc2gtZWQyNTUxOQAAACBmVk3wR7qI5Ky6jTf0H8Z2GnJ3D9cXmLpKVqFw2H
4xDAAAAQC7Nkp1vWz5bHj4Y6c8dX9qR2mF3gA5tB8nK7eP1wZVGGZWTfBHuojkrLqNN/
QfxnYacncP1xeYukpWoXDYfjEAAAAOZGVwbG95QGRldmJveAECAwQF
-----END OPENSSH PRIVATE KEY-----
"""
    with open(KEY_PATH, "w") as f:
        f.write(dummy_private_key)
    os.chmod(KEY_PATH, 0o600)

    # Create matching public key
    dummy_public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGZWTfBHuojkrLqNN/QfxnYacncP1xeYukpWoXDYfjEM deploy@devbox\n"
    with open(KEY_PUB_PATH, "w") as f:
        f.write(dummy_public_key)
    os.chmod(KEY_PUB_PATH, 0o644)

    # Also create a default ed25519 key (referenced by github.com entry)
    default_key = os.path.join(SSH_DIR, "id_ed25519")
    if not os.path.exists(default_key):
        with open(default_key, "w") as f:
            f.write("-----BEGIN OPENSSH PRIVATE KEY-----\n"
                    "b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAA\n"
                    "-----END OPENSSH PRIVATE KEY-----\n")
        os.chmod(default_key, 0o600)

    default_pub = default_key + ".pub"
    if not os.path.exists(default_pub):
        with open(default_pub, "w") as f:
            f.write("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIG1234567890abcdef user@localhost\n")
        os.chmod(default_pub, 0o644)

    # Ensure ssh-agent is NOT running (task requirement)
    subprocess.run(["pkill", "-u", os.getenv("USER", "user"), "ssh-agent"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"SSH config created: {SSH_CONFIG}")
    print(f"Work key created: {KEY_PATH}")

    # Open VSCode with the SSH config file
    launch_gui(f'code "{SSH_CONFIG}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
