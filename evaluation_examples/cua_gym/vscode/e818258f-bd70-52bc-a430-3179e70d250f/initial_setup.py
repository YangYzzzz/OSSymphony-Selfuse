"""
Initial Setup: Configure Remote - SSH extension settings and SSH config
Task ID: vscode_rrt_013
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
SSH_DIR = os.path.join(HOME, ".ssh")
SSH_CONFIG_PATH = os.path.join(SSH_DIR, "config")


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # 1. Set VSCode setting: remote.SSH.showLoginTerminal = false
    update_settings({
        "remote.SSH.showLoginTerminal": False,
    })
    print(f"VSCode settings updated: remote.SSH.showLoginTerminal = false")

    # 2. Create SSH config with git-server host (NO ForwardAgent)
    os.makedirs(SSH_DIR, exist_ok=True)

    ssh_config_content = """\
Host git-server
    HostName git.internal.co
    User gitadmin
    IdentityFile ~/.ssh/id_rsa
    Port 22

Host staging-box
    HostName staging.internal.co
    User deploy
    Port 2222

Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
"""
    with open(SSH_CONFIG_PATH, "w") as f:
        f.write(ssh_config_content)
    os.chmod(SSH_CONFIG_PATH, 0o600)
    print(f"SSH config created: {SSH_CONFIG_PATH}")

    # 3. Launch VSCode
    launch_gui('code "/home/user"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
