"""
Initial Setup: Go Wire DI project scaffold
Task ID: vscode_gf6_077
Domain: vscode

Creates ~/projects/go-wire-di with:
  - go.mod (no wire dependency)
  - empty internal/{db,repository,service,handler} directories
  - cmd/server/main.go (basic, no InitializeApp)
  - Opens VSCode with the project folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_077'
PROJECT_DIR = f'{WORKDIR}/projects/go-wire-di'


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
    # Create project directory structure
    dirs = [
        f'{PROJECT_DIR}/internal/db',
        f'{PROJECT_DIR}/internal/repository',
        f'{PROJECT_DIR}/internal/service',
        f'{PROJECT_DIR}/internal/handler',
        f'{PROJECT_DIR}/cmd/server',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # go.mod - basic module, NO wire dependency
    go_mod = """module github.com/user/go-wire-di

go 1.21
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod)

    # cmd/server/main.go - basic main without InitializeApp
    main_go = """package main

import (
\t"fmt"
\t"log"
\t"net/http"
)

func main() {
\tfmt.Println("Starting server...")

\thttp.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
\t\tw.WriteHeader(http.StatusOK)
\t\tw.Write([]byte("OK"))
\t})

\tlog.Println("Server listening on :8080")
\tif err := http.ListenAndServe(":8080", nil); err != nil {
\t\tlog.Fatal(err)
\t}
}
"""
    with open(f'{PROJECT_DIR}/cmd/server/main.go', 'w') as f:
        f.write(main_go)

    # Add .gitkeep files to empty directories so they exist
    for subdir in ['db', 'repository', 'service', 'handler']:
        gitkeep = f'{PROJECT_DIR}/internal/{subdir}/.gitkeep'
        with open(gitkeep, 'w') as f:
            f.write('')

    print(f'Initial project created: {PROJECT_DIR}')

    # Install Go if not present (agent needs Go to install wire and build)
    env = os.environ.copy()
    go_local = f'{WORKDIR}/go-sdk'
    env['PATH'] = f'{go_local}/bin:{WORKDIR}/go/bin:' + env.get('PATH', '')
    env['GOPATH'] = f'{WORKDIR}/go'
    env['GOROOT'] = go_local

    go_check = subprocess.run('go version', shell=True, capture_output=True, text=True, env=env)
    if go_check.returncode != 0:
        print('Go not found, installing to ~/go-sdk...')
        subprocess.run('wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz',
                       shell=True, check=True)
        subprocess.run(
            f'rm -rf {go_local} && mkdir -p /tmp/go-extract && tar -C /tmp/go-extract -xzf /tmp/go.tar.gz && mv /tmp/go-extract/go {go_local} && rm -rf /tmp/go-extract /tmp/go.tar.gz',
            shell=True, check=True)
        print(f'Go installed to {go_local}')

    # Verify go works
    result = subprocess.run('go version', shell=True, capture_output=True, text=True, env=env)
    print(f'Go version: {result.stdout.strip()}')

    # Add Go to user's PATH via .bashrc
    bashrc_path = f'{WORKDIR}/.bashrc'
    path_line = f'export GOROOT="{go_local}"\nexport PATH="{go_local}/bin:$HOME/go/bin:$PATH"'
    try:
        with open(bashrc_path, 'r') as f:
            bashrc = f.read()
        if go_local not in bashrc:
            with open(bashrc_path, 'a') as f:
                f.write(f'\n{path_line}\n')
    except FileNotFoundError:
        with open(bashrc_path, 'w') as f:
            f.write(f'{path_line}\n')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
