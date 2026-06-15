"""
Initial Setup: Configure a complete Kubernetes Helm chart deployment
Task ID: os_gff_094
Domain: os
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_gff_094'

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

def sudo_run(cmd_str):
    """Run a command with sudo, piping password via stdin."""
    proc = subprocess.Popen(
        f"echo 'password' | sudo -S {cmd_str}",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"sudo command failed: {cmd_str}\n{err.decode()}")

def create_initial():
    # Create the /opt/helm/ directory as a starting point
    # The user is expected to create the myapp chart structure inside it
    sudo_run('mkdir -p /opt/helm')

    # Ensure proper permissions so the user can write to it
    sudo_run('chmod -R 777 /opt/helm')

    # Create a README to indicate this is the helm charts directory
    with open('/opt/helm/README.md', 'w') as f:
        f.write("""# Helm Charts Directory

This directory is used to store Helm charts for Kubernetes deployments.

## Getting Started

Create your Helm chart in a subdirectory (e.g., /opt/helm/myapp/).

## Prerequisites

- Helm 3 installed
- kubectl configured with cluster access
- nginx ingress controller installed on cluster
- cert-manager installed on cluster
""")

    # Create the staging namespace marker file (simulating kubectl config)
    os.makedirs(f'{WORKDIR}/.kube', exist_ok=True)
    with open(f'{WORKDIR}/.kube/config', 'w') as f:
        f.write("""apiVersion: v1
kind: Config
clusters:
- cluster:
    server: https://127.0.0.1:6443
    certificate-authority-data: LS0tLS1CRUdJTi...
  name: local-cluster
contexts:
- context:
    cluster: local-cluster
    namespace: default
    user: admin
  name: local-context
current-context: local-context
users:
- name: admin
  user:
    token: dummy-token-for-development
""")

    print(f'Initial environment created')
    print(f'  /opt/helm/ directory ready')
    print(f'  No Helm chart exists yet - user must create it')

    # Open a terminal for the user to work in
    launch_gui('gnome-terminal', delay_sec=1.5)
    # Open file manager at /opt/helm so user can see the directory
    launch_gui('nautilus /opt/helm', delay_sec=1.5)
    print('GUI_READY: launched terminal and file manager with DISPLAY=:0')

create_initial()
