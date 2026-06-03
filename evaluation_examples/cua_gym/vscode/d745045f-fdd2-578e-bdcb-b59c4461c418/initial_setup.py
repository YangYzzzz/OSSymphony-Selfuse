"""
Initial Setup: Set up sqlc for type-safe SQL in a Go project
Task ID: vscode_gf6_059
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_059'
PROJECT_DIR = f'{WORKDIR}/projects/go-sqlc'
GO_ROOT = f'{WORKDIR}/go-sdk'
GO_BIN = f'{GO_ROOT}/bin'
GOPATH = f'{WORKDIR}/go'
GOPATH_BIN = f'{GOPATH}/bin'
ENV = {
    **os.environ,
    'HOME': WORKDIR,
    'GOROOT': GO_ROOT,
    'GOPATH': GOPATH,
    'PATH': f'{GOPATH_BIN}:{GO_BIN}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin',
    'DISPLAY': ':0',
}


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=ENV,
    )
    time.sleep(delay_sec)


def install_go():
    """Download and install Go 1.21 if not present."""
    if os.path.exists(f'{GO_BIN}/go'):
        print("Go already installed")
        return
    print("Installing Go 1.21...")
    cmds = [
        'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz',
        f'rm -rf {GO_ROOT}',
        'tar -C /tmp -xzf /tmp/go.tar.gz',
        f'mv /tmp/go {GO_ROOT}',
        'rm -f /tmp/go.tar.gz',
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=ENV)
        if r.returncode != 0:
            print(f"WARN: {cmd} -> {r.stderr}")
    r = subprocess.run(f'{GO_BIN}/go version', shell=True, capture_output=True, text=True, env=ENV)
    print(f"Go installed: {r.stdout.strip()}")


def create_initial():
    # Install Go first (needed for the task)
    install_go()
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/sql/schema', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/sql/queries', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/internal', exist_ok=True)

    # Create go.mod
    go_mod_content = """module github.com/user/go-sqlc

go 1.21

require github.com/lib/pq v1.10.9
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod_content)

    # Run go mod tidy to generate correct go.sum
    subprocess.run(f'{GO_BIN}/go mod tidy', shell=True, cwd=PROJECT_DIR,
                   capture_output=True, text=True, env=ENV)
    print('Generated go.sum via go mod tidy')

    # Create a basic main.go so the project has something
    os.makedirs(f'{PROJECT_DIR}/cmd/server', exist_ok=True)
    main_go = """package main

import (
\t"fmt"
\t"log"
\t"net/http"
)

func main() {
\tfmt.Println("go-sqlc server starting...")
\tlog.Fatal(http.ListenAndServe(":8080", nil))
}
"""
    with open(f'{PROJECT_DIR}/cmd/server/main.go', 'w') as f:
        f.write(main_go)

    print(f'Initial project created at: {PROJECT_DIR}')

    # Add Go to user's PATH in bashrc so agent can use go commands in terminal
    bashrc_path = f'{WORKDIR}/.bashrc'
    go_path_line = f'\nexport GOROOT={GO_ROOT}\nexport GOPATH={GOPATH}\nexport PATH=$GOPATH/bin:$GOROOT/bin:$PATH\n'
    with open(bashrc_path, 'a') as f:
        f.write(go_path_line)
    print('Added Go to PATH in .bashrc')

    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
