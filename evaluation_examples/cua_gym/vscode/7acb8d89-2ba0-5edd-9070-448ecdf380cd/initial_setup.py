"""
Initial Setup: Rust CLI tool project with minimal Cargo.toml and empty main.rs
Task ID: vscode_gf4_022
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_022'
PROJECT_DIR = f'{WORKDIR}/projects/rust-cli-tool'

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
    # Ensure cargo is in PATH for the user's shell
    bashrc_path = f'{WORKDIR}/.bashrc'
    cargo_env_line = '. "$HOME/.cargo/env"'
    try:
        with open(bashrc_path, 'r') as f:
            bashrc_content = f.read()
        if cargo_env_line not in bashrc_content:
            with open(bashrc_path, 'a') as f:
                f.write(f'\n{cargo_env_line}\n')
    except FileNotFoundError:
        with open(bashrc_path, 'w') as f:
            f.write(f'{cargo_env_line}\n')

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # --- Cargo.toml: minimal, no dependencies ---
    cargo_toml = """\
[package]
name = "rust-cli"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)
    print(f'Created: {PROJECT_DIR}/Cargo.toml')

    # --- src/main.rs: empty main function only ---
    main_rs = """\
fn main() {
}
"""
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(main_rs)
    print(f'Created: {PROJECT_DIR}/src/main.rs')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    # Also open Cargo.toml in the editor
    launch_gui(f'code "{PROJECT_DIR}/Cargo.toml"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
