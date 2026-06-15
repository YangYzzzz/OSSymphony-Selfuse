"""
Initial Setup: Docker Swarm mode single-node cluster setup
Task ID: os_adm_048
Domain: os (Docker administration)

Initial state: Ubuntu 22.04 with Docker Engine installed.
Docker is NOT in Swarm mode. Terminal open for user.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_adm_048'
SUDO_PASS = 'password'


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


def run_cmd(command: str, check: bool = True, sudo: bool = False):
    """Run a shell command and return result."""
    if sudo:
        command = f"echo '{SUDO_PASS}' | sudo -S bash -c '{command}'"
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"WARN: Command failed: {command}")
        print(f"  stdout: {result.stdout.strip()}")
        print(f"  stderr: {result.stderr.strip()}")
    else:
        print(f"OK: {command[:80]}")
    return result


def install_docker():
    """Install Docker Engine if not already installed."""
    result = run_cmd("which docker", check=False)
    if result.returncode == 0:
        print("Docker already installed")
        return

    print("Installing Docker Engine...")
    # Install prerequisites
    run_cmd("apt-get update -y", check=True, sudo=True)
    run_cmd("apt-get install -y ca-certificates curl gnupg lsb-release", check=True, sudo=True)

    # Add Docker's official GPG key
    run_cmd("install -m 0755 -d /etc/apt/keyrings", check=True, sudo=True)
    run_cmd("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes", check=True, sudo=True)
    run_cmd("chmod a+r /etc/apt/keyrings/docker.gpg", check=True, sudo=True)

    # Set up repository
    run_cmd(
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] '
        'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | '
        'tee /etc/apt/sources.list.d/docker.list > /dev/null',
        check=True, sudo=True
    )

    # Install Docker Engine
    run_cmd("apt-get update -y", check=True, sudo=True)
    run_cmd("apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin", check=True, sudo=True)

    # Start Docker service
    run_cmd("systemctl start docker", check=True, sudo=True)
    run_cmd("systemctl enable docker", check=True, sudo=True)

    # Add user to docker group for non-sudo access
    run_cmd("usermod -aG docker user", check=False, sudo=True)

    # Make docker accessible without re-login by using newgrp trick
    print("Docker installed successfully")


def create_initial():
    # Install Docker if not present
    install_docker()

    # Verify docker is installed and running
    result = run_cmd("docker --version", sudo=True)
    print(f"Docker version: {result.stdout.strip()}")

    # Ensure Docker is NOT in swarm mode (leave if active)
    run_cmd("docker swarm leave --force 2>/dev/null", check=False, sudo=True)

    # Remove any existing nginx service (cleanup)
    run_cmd("docker service rm nginx 2>/dev/null", check=False, sudo=True)

    # Remove app-overlay network if it exists
    run_cmd("docker network rm app-overlay 2>/dev/null", check=False, sudo=True)

    # Pull nginx image to ensure it is available
    print("Pulling nginx image...")
    run_cmd("docker pull nginx:latest", check=True, sudo=True)

    # Verify swarm is inactive
    result = run_cmd("docker info --format '{{.Swarm.LocalNodeState}}'", check=False, sudo=True)
    print(f"Swarm state: {result.stdout.strip()}")

    # Set up passwordless sudo for docker commands so user can run docker without issues
    run_cmd('echo "user ALL=(ALL) NOPASSWD: /usr/bin/docker, /usr/bin/docker-compose" > /etc/sudoers.d/docker-user', sudo=True)

    print("Initial state ready: Docker installed, swarm mode inactive")

    # Open a terminal for the user
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
