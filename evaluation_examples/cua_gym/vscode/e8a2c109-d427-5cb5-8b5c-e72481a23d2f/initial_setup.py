"""
Initial Setup: Go testing project with calculator package
Task ID: vscode_gf6_010
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_010'
PROJECT_DIR = f'{WORKDIR}/projects/go-testing'
PKG_DIR = f'{PROJECT_DIR}/pkg/calculator'

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
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result

def create_initial():
    # Step 1: Install Go 1.21 in user home if not present
    go_root = f'{WORKDIR}/go-sdk'
    go_bin = f'{go_root}/bin/go'
    if not os.path.exists(go_bin):
        print("Installing Go 1.21...")
        run_cmd("wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz")
        os.makedirs(go_root, exist_ok=True)
        run_cmd(f"tar -C {WORKDIR} -xzf /tmp/go.tar.gz")
        # tar extracts to /home/user/go, rename to go-sdk
        if os.path.exists(f'{WORKDIR}/go') and not os.path.exists(go_root):
            os.rename(f'{WORKDIR}/go', go_root)
        elif os.path.exists(f'{WORKDIR}/go') and os.path.exists(go_root):
            # Already exists from makedirs, remove empty and rename
            os.rmdir(go_root)
            os.rename(f'{WORKDIR}/go', go_root)
        run_cmd("rm -f /tmp/go.tar.gz")

    # Set up PATH for Go
    go_env = os.environ.copy()
    go_env['PATH'] = f'{go_root}/bin:{go_env.get("PATH", "")}'
    go_env['GOPATH'] = f'{WORKDIR}/gopath'
    go_env['GOROOT'] = go_root
    go_env['HOME'] = WORKDIR

    # Add Go to profile so it persists
    profile_line = f'export GOROOT={go_root}\nexport PATH={go_root}/bin:$PATH\nexport GOPATH=$HOME/gopath\n'
    with open(f'{WORKDIR}/.profile', 'a') as f:
        f.write(profile_line)
    with open(f'{WORKDIR}/.bashrc', 'a') as f:
        f.write(profile_line)

    # Verify Go
    result = run_cmd(f'{go_bin} version', env=go_env)
    print(f"Go installed: {result.returncode == 0}")

    # Step 2: Create project directory structure
    os.makedirs(PKG_DIR, exist_ok=True)

    # Step 3: Create go.mod
    go_mod_content = """module github.com/user/go-testing

go 1.21
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod_content)

    # Step 4: Create calculator.go with Add, Subtract, Multiply, Divide, Sqrt
    calculator_go = '''package calculator

import (
\t"errors"
\t"math"
)

// Add returns the sum of two float64 numbers.
func Add(a, b float64) float64 {
\treturn a + b
}

// Subtract returns the difference of two float64 numbers.
func Subtract(a, b float64) float64 {
\treturn a - b
}

// Multiply returns the product of two float64 numbers.
func Multiply(a, b float64) float64 {
\treturn a * b
}

// Divide returns the quotient of two float64 numbers.
// Returns an error if the divisor is zero.
func Divide(a, b float64) (float64, error) {
\tif b == 0 {
\t\treturn 0, errors.New("division by zero")
\t}
\treturn a / b, nil
}

// Sqrt returns the square root of a float64 number.
// Returns an error if the input is negative.
func Sqrt(x float64) (float64, error) {
\tif x < 0 {
\t\treturn 0, errors.New("cannot compute square root of negative number")
\t}
\treturn math.Sqrt(x), nil
}
'''
    with open(f'{PKG_DIR}/calculator.go', 'w') as f:
        f.write(calculator_go)

    print(f'Initial project created at: {PROJECT_DIR}')

    # Step 5: Verify Go can parse the module
    run_cmd(f'{go_bin} vet ./...', cwd=PROJECT_DIR, env=go_env)

    # Step 6: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
