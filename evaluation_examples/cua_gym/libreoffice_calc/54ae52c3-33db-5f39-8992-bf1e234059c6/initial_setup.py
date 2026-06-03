"""
Initial Setup: Set up a complete Git server using Gitolite
Task ID: os_gf5_028
Domain: os

Initial state: Ubuntu 22.04, Git installed, Gitolite NOT installed.
SSH keys for alice and bob at /home/user/keys/. Admin SSH key at ~/.ssh/id_rsa.
Terminal open for the user to begin the task.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_gf5_028'

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

def run(cmd, check=False):
    """Run a command, printing output for debugging."""
    print(f"  CMD: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"  OUT: {result.stdout.strip()[:500]}")
    if result.stderr.strip():
        print(f"  ERR: {result.stderr.strip()[:500]}")
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed (rc={result.returncode}): {cmd}\n{result.stderr}")
    return result

def sudo(cmd, check=False):
    """Run a command with sudo using the known password."""
    return run(f"echo 'password' | sudo -S {cmd} 2>/dev/null", check=check)

def create_initial():
    # 1. Create SSH keys directory for alice and bob
    keys_dir = f"{WORKDIR}/keys"
    os.makedirs(keys_dir, exist_ok=True)

    # 2. Generate SSH keys for alice and bob (no passphrase)
    for user in ['alice', 'bob']:
        key_path = f"{keys_dir}/{user}"
        if not os.path.exists(key_path):
            run(f'ssh-keygen -t rsa -b 2048 -f {key_path} -N "" -C "{user}@example.com"')
        print(f"SSH key for {user}: {key_path}.pub")

    # 3. Generate SSH key for user (admin) if not present
    user_ssh_dir = f"{WORKDIR}/.ssh"
    os.makedirs(user_ssh_dir, exist_ok=True)
    user_key = f"{user_ssh_dir}/id_rsa"
    if not os.path.exists(user_key):
        run(f'ssh-keygen -t rsa -b 2048 -f {user_key} -N "" -C "admin@example.com"')
    print(f"Admin SSH key: {user_key}.pub")

    # 4. Ensure git is installed
    run("which git", check=True)

    # 5. Make sure gitolite is NOT installed (initial state requirement)
    sudo("apt-get remove -y gitolite3 2>/dev/null || true")
    run("rm -rf /home/user/.gitolite /home/user/.gitolite.rc /home/user/repositories /home/user/bin/gitolite 2>/dev/null || true")

    # 6. Ensure SSH server is running (needed for gitolite)
    sudo("apt-get install -y openssh-server 2>/dev/null || true")
    sudo("systemctl enable ssh || true")
    sudo("systemctl start ssh || true")

    # 7. Configure SSH to accept localhost connections without host key checking
    ssh_config = f"{user_ssh_dir}/config"
    Path(ssh_config).write_text(
        "Host localhost\n"
        "  StrictHostKeyChecking no\n"
        "  UserKnownHostsFile /dev/null\n"
        "  IdentityFile ~/.ssh/id_rsa\n"
    )
    os.chmod(ssh_config, 0o600)

    # 8. Authorize user's own key for SSH to localhost
    authorized_keys = f"{user_ssh_dir}/authorized_keys"
    pub_key = Path(f"{user_key}.pub").read_text().strip()
    if os.path.exists(authorized_keys):
        existing = Path(authorized_keys).read_text()
        if pub_key not in existing:
            with open(authorized_keys, "a") as f:
                f.write(f"\n{pub_key}\n")
    else:
        Path(authorized_keys).write_text(f"{pub_key}\n")
    os.chmod(authorized_keys, 0o600)
    os.chmod(user_ssh_dir, 0o700)

    # 9. Verify initial state
    print("\n--- Initial State Verification ---")
    run("ls -la /home/user/keys/")
    run("ls -la /home/user/.ssh/")
    run("which git")
    result = run("which gitolite")
    if result.returncode == 0:
        print("WARNING: gitolite still found in PATH")
    else:
        print("OK: gitolite not installed (as expected for initial state)")

    # 10. Launch terminal for the task
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched terminal with DISPLAY=:0')

create_initial()
