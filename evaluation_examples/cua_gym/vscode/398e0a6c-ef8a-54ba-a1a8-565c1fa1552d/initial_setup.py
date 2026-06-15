"""
Initial Setup: Go chi router REST API project skeleton
Task ID: vscode_gf6_073
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_073'
PROJECT_DIR = f'{WORKDIR}/projects/go-chi-api'


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


def install_go():
    """Install Go 1.21 if not already present."""
    import shutil as _shutil
    if _shutil.which('go') or os.path.exists('/usr/local/go/bin/go'):
        print('Go already installed, skipping.')
        return
    print('Installing Go 1.21...')
    subprocess.run(
        ['bash', '-c',
         'cd /tmp && '
         'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz && '
         'echo "password" | sudo -S tar -C /usr/local -xzf go1.21.13.linux-amd64.tar.gz && '
         'echo "password" | sudo -S ln -sf /usr/local/go/bin/go /usr/local/bin/go && '
         'echo "password" | sudo -S ln -sf /usr/local/go/bin/gofmt /usr/local/bin/gofmt && '
         'rm -f go1.21.13.linux-amd64.tar.gz'],
        check=True, timeout=120,
    )
    print('Go 1.21 installed successfully.')


def create_initial():
    install_go()

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/cmd/server', exist_ok=True)

    # go.mod - basic module without chi dependency
    go_mod_content = """module github.com/user/go-chi-api

go 1.21
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod_content)

    # cmd/server/main.go - empty main function
    main_go_content = """package main

import "fmt"

func main() {
\tfmt.Println("go-chi-api server")
}
"""
    with open(f'{PROJECT_DIR}/cmd/server/main.go', 'w') as f:
        f.write(main_go_content)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  go.mod: {PROJECT_DIR}/go.mod')
    print(f'  main.go: {PROJECT_DIR}/cmd/server/main.go')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
