"""
Initial Setup: Docker Swarm cluster preparation
Task ID: os_gff_064
Domain: os (Docker)

Creates the pre-task state:
- Docker Engine installed and running
- Docker is NOT in swarm mode
- /opt/swarm/ does NOT exist (no stack.yml)
- Terminal open showing system readiness
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_gff_064'
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


def run(cmd, check=True):
    """Run a shell command, print output, optionally check."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {cmd}")
    return result


def sudo(cmd, check=True):
    """Run a command with sudo, providing password via stdin."""
    return run(f"echo '{SUDO_PASS}' | sudo -S {cmd}", check=check)


def install_docker():
    """Install Docker Engine on Ubuntu 22.04."""
    sudo("apt-get update -y")
    sudo("apt-get install -y ca-certificates curl gnupg lsb-release")

    sudo("mkdir -p /etc/apt/keyrings")
    run(f"curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -S gpg --batch --dearmor -o /etc/apt/keyrings/docker.gpg <<< '{SUDO_PASS}'", check=False)
    # Alternative approach if the above fails
    run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /tmp/docker.gpg")
    sudo("gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg /tmp/docker.gpg", check=False)
    sudo("chmod a+r /etc/apt/keyrings/docker.gpg")

    result = run("lsb_release -cs")
    codename = result.stdout.strip()
    repo_line = f"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu {codename} stable"
    run(f"echo '{repo_line}' | sudo -S tee /etc/apt/sources.list.d/docker.list > /dev/null <<< '{SUDO_PASS}'", check=False)
    sudo(f"bash -c \"echo '{repo_line}' > /etc/apt/sources.list.d/docker.list\"")

    sudo("apt-get update -y")
    sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")

    sudo("systemctl start docker")
    sudo("systemctl enable docker")
    sudo("usermod -aG docker user", check=False)

    # Allow current user to use docker without re-login
    sudo("chmod 666 /var/run/docker.sock", check=False)

    run("docker --version")
    print("Docker installed and running.")


def ensure_no_swarm():
    """Make sure Docker is NOT in swarm mode."""
    result = run("docker info --format '{{.Swarm.LocalNodeState}}'", check=False)
    if 'active' in result.stdout:
        run("docker swarm leave --force", check=False)
    print("Docker is not in swarm mode (as required for initial state).")


def ensure_no_stack_dir():
    """Make sure /opt/swarm/ does NOT exist."""
    sudo("rm -rf /opt/swarm", check=False)
    print("/opt/swarm does not exist (as required for initial state).")


def create_initial():
    # Step 1: Install Docker
    install_docker()

    # Step 2: Ensure not in swarm mode
    ensure_no_swarm()

    # Step 3: Ensure no stack.yml
    ensure_no_stack_dir()

    # Step 4: Open terminal showing system is ready
    launch_gui('gnome-terminal -- bash -c "echo Docker is installed and ready; docker --version; echo; echo Docker Swarm status:; docker info --format \'Swarm: {{.Swarm.LocalNodeState}}\'; echo; exec bash"', delay_sec=2.0)
    print("GUI_READY: launched terminal with DISPLAY=:0")


create_initial()
