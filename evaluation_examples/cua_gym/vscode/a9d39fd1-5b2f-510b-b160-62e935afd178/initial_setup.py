"""
Initial Setup: Open VSCode with empty ~/projects/rust-hello folder
Task ID: vscode_gf4_005
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_005'
PROJECT_DIR = f'{WORKDIR}/projects/rust-hello'
CARGO_BIN = f'{WORKDIR}/.cargo/bin'

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

def run_cmd(cmd, **kwargs):
    """Run a command with cargo bin in PATH."""
    env = os.environ.copy()
    env["PATH"] = f'{CARGO_BIN}:{env.get("PATH", "")}'
    return subprocess.run(cmd, env=env, capture_output=True, text=True, **kwargs)

def create_initial():
    # Step 1: Install Rust if not already present
    cargo_path = os.path.join(CARGO_BIN, 'cargo')
    if not os.path.exists(cargo_path):
        print('Installing Rust toolchain...')
        result = subprocess.run(
            ['bash', '-c', 'curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y'],
            capture_output=True, text=True
        )
        print(f'Rustup install stdout: {result.stdout[-500:] if result.stdout else ""}')
        print(f'Rustup install stderr: {result.stderr[-500:] if result.stderr else ""}')

    # Verify rust and cargo
    result = run_cmd([cargo_path, '--version'])
    print(f'Cargo version: {result.stdout.strip()}')

    rustc_path = os.path.join(CARGO_BIN, 'rustc')
    result = run_cmd([rustc_path, '--version'])
    print(f'Rustc version: {result.stdout.strip()}')

    # Step 2: Add cargo to user's PATH permanently
    bashrc = os.path.join(WORKDIR, '.bashrc')
    cargo_env_line = 'export PATH="$HOME/.cargo/bin:$PATH"'
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            content = f.read()
        if '.cargo/bin' not in content:
            with open(bashrc, 'a') as f:
                f.write(f'\n# Rust toolchain\n{cargo_env_line}\n')
            print('Added cargo to .bashrc PATH')
    else:
        with open(bashrc, 'w') as f:
            f.write(f'# Rust toolchain\n{cargo_env_line}\n')
        print('Created .bashrc with cargo PATH')

    # Step 3: Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created empty project directory: {PROJECT_DIR}')

    # Step 4: Install rust-analyzer VSCode extension
    result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True)
    extensions = result.stdout.strip().lower()
    print(f'Installed extensions:\n{result.stdout.strip()}')
    if 'rust-lang.rust-analyzer' not in extensions:
        print('Installing rust-analyzer extension...')
        subprocess.run(['code', '--install-extension', 'rust-lang.rust-analyzer'],
                       capture_output=True, text=True)
        print('rust-analyzer extension installed')

    # Step 5: Open VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with empty rust-hello folder')

create_initial()
