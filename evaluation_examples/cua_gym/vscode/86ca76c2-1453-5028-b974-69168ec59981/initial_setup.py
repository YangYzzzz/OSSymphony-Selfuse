"""
Initial Setup: Rust scripting engine project - pre-task state
Task ID: vscode_gf4_093
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_093'
PROJECT_DIR = f'{WORKDIR}/projects/rust-scripting-engine'

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

def run_cmd(cmd, cwd=None, timeout=600):
    """Run a shell command, printing output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True, timeout=timeout
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print(f"STDERR: {result.stderr.strip()}")
    return result

def create_initial():
    # Step 1: Install Rust if not present
    rust_check = subprocess.run("which cargo", shell=True, capture_output=True)
    if rust_check.returncode != 0:
        print("Installing Rust...")
        run_cmd("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y", timeout=300)
        # Source cargo env
        os.environ["PATH"] = f"{WORKDIR}/.cargo/bin:" + os.environ.get("PATH", "")

    # Verify rust is available
    run_cmd(f"{WORKDIR}/.cargo/bin/rustc --version || rustc --version")
    run_cmd(f"{WORKDIR}/.cargo/bin/cargo --version || cargo --version")

    # Step 2: Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Step 3: Create Cargo.toml - basic, no scripting dependencies
    cargo_toml = '''[package]
name = "rust-scripting"
version = "0.1.0"
edition = "2021"

[dependencies]
'''
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)
    print(f'Created {PROJECT_DIR}/Cargo.toml')

    # Step 4: Create src/main.rs - simple starter
    main_rs = '''fn main() {
    println!("Rust Scripting Engine - v0.1.0");
    println!("TODO: Implement Lua scripting integration");
}
'''
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(main_rs)
    print(f'Created {PROJECT_DIR}/src/main.rs')

    # Step 5: Install rust-analyzer extension for VSCode
    run_cmd("code --install-extension rust-lang.rust-analyzer", timeout=120)

    # Step 6: Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
