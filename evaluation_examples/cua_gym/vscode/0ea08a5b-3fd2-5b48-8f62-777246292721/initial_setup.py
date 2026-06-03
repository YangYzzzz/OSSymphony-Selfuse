"""
Initial Setup: Rust async runtime project scaffold
Task ID: vscode_gf4_035
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_035'
PROJECT_DIR = f'{WORKDIR}/projects/rust-async-runtime'

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

def install_rust():
    """Install Rust toolchain if not present."""
    result = subprocess.run(['bash', '-c', 'source $HOME/.cargo/env 2>/dev/null && which cargo'],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print('Installing Rust toolchain...')
        subprocess.run(
            ['bash', '-c', 'curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y'],
            check=True
        )
        print('Rust installed successfully.')
    else:
        print('Rust already installed.')

def create_initial():
    # Install Rust toolchain
    install_rust()

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # --- Cargo.toml (minimal, no extra dependencies) ---
    cargo_toml = """\
[package]
name = "rust-async-runtime"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)
    print(f'Created: {PROJECT_DIR}/Cargo.toml')

    # --- src/main.rs (minimal) ---
    main_rs = """\
fn main() {}
"""
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(main_rs)
    print(f'Created: {PROJECT_DIR}/src/main.rs')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
