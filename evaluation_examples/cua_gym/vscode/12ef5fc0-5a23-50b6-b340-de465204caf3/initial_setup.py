"""
Initial Setup: Set up dependency injection with Uber's fx framework in a Go project
Task ID: vscode_gf6_082
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_082'
PROJECT_DIR = f'{WORKDIR}/projects/go-fx-di'

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

def run_cmd(cmd, cwd=None, env=None):
    """Run a command and print output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print(f"STDERR: {result.stderr.strip()}")
    return result

GO_SDK = f'{WORKDIR}/go-sdk'
GO_BIN = f'{GO_SDK}/go/bin/go'

def install_go():
    """Install Go 1.21 to user home directory."""
    if os.path.exists(GO_BIN):
        print("Go 1.21 already installed")
        return

    print("Installing Go 1.21...")
    os.makedirs(GO_SDK, exist_ok=True)
    run_cmd(f"wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz")
    run_cmd(f"tar -C {GO_SDK} -xzf /tmp/go.tar.gz")
    run_cmd("rm -f /tmp/go.tar.gz")

    # Add to PATH in bashrc
    bashrc = os.path.join(WORKDIR, '.bashrc')
    go_path_line = f'export PATH=$PATH:{GO_SDK}/go/bin:$HOME/go/bin'
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            content = f.read()
        if GO_SDK not in content:
            with open(bashrc, 'a') as f:
                f.write(f'\n{go_path_line}\n')
    else:
        with open(bashrc, 'w') as f:
            f.write(f'{go_path_line}\n')

    print("Go 1.21 installed successfully")

def get_go_env():
    """Get environment with Go in PATH."""
    env = os.environ.copy()
    env["PATH"] = f"{GO_SDK}/go/bin:{WORKDIR}/go/bin:" + env.get("PATH", "")
    env["GOPATH"] = f"{WORKDIR}/go"
    env["HOME"] = WORKDIR
    return env

def create_project():
    """Create the initial Go project structure."""
    # Create project directories
    os.makedirs(f'{PROJECT_DIR}/internal', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/cmd', exist_ok=True)

    # Create go.mod with just the module declaration (NO fx/zap dependencies)
    go_mod = """module github.com/user/go-fx-di

go 1.21
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod)

    print(f"Project structure created at {PROJECT_DIR}")

def create_initial():
    install_go()
    create_project()

    # Verify Go is working
    env = get_go_env()
    run_cmd(f"{GO_BIN} version", env=env)

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
