"""
Initial Setup: Rust game engine project with minimal Cargo.toml and main.rs
Task ID: vscode_gf4_049
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_049'
PROJECT_DIR = f'{WORKDIR}/projects/rust-game-engine'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # --- Cargo.toml: minimal, no dependencies ---
    cargo_toml = """\
[package]
name = "rust-game-engine"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)
    print(f'Created {PROJECT_DIR}/Cargo.toml')

    # --- src/main.rs: minimal stub ---
    main_rs = """\
fn main() {
}
"""
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(main_rs)
    print(f'Created {PROJECT_DIR}/src/main.rs')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
