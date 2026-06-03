"""
Initial Setup: Rust WebAssembly project in VSCode
Task ID: vscode_gf6_057
Domain: vscode

Creates ~/projects/rust-wasm with basic Cargo.toml (lib crate, no wasm deps)
and src/lib.rs (greet stub, no wasm_bindgen). Installs Rust toolchain.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_057'
PROJECT_DIR = f'{WORKDIR}/projects/rust-wasm'
SRC_DIR = f'{PROJECT_DIR}/src'

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

def run_cmd(cmd, timeout=300):
    """Run a shell command with timeout, print output."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(f"STDERR: {result.stderr.strip()}")
    return result

def create_initial():
    # Step 1: Install Rust toolchain
    print("Installing Rust toolchain...")
    run_cmd("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y", timeout=300)

    # Source cargo env
    cargo_env = os.path.expanduser("~/.cargo/env")
    if os.path.exists(cargo_env):
        # Export PATH to include cargo
        os.environ["PATH"] = os.path.expanduser("~/.cargo/bin") + ":" + os.environ.get("PATH", "")

    # Verify Rust is installed
    result = run_cmd("rustc --version")
    result2 = run_cmd("cargo --version")

    # Step 2: Install rust-analyzer extension for VSCode
    print("Installing rust-analyzer extension...")
    run_cmd("code --install-extension rust-lang.rust-analyzer", timeout=120)

    # Step 3: Create project directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    print(f"Created project directory: {PROJECT_DIR}")

    # Step 4: Create Cargo.toml - basic lib crate, NO wasm dependencies
    cargo_toml = """[package]
name = "rust-wasm"
version = "0.1.0"
edition = "2021"
description = "A Rust library project"

[lib]
# Standard lib crate
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)
    print("Created Cargo.toml (basic lib, no wasm deps)")

    # Step 5: Create src/lib.rs - basic greet stub, NO wasm_bindgen
    lib_rs = '''/// Returns a greeting message
pub fn greet() {
    println!("Hello from rust-wasm!");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greet() {
        greet();
    }
}
'''
    with open(f'{SRC_DIR}/lib.rs', 'w') as f:
        f.write(lib_rs)
    print("Created src/lib.rs (greet stub, no wasm_bindgen)")

    # Step 6: Ensure NO .vscode, www, pkg directories exist
    # (They shouldn't since we just created the project, but be safe)
    for d in [f'{PROJECT_DIR}/.vscode', f'{PROJECT_DIR}/www', f'{PROJECT_DIR}/pkg']:
        if os.path.exists(d):
            import shutil
            shutil.rmtree(d)

    # Step 7: wasm-pack must NOT be installed
    # (It shouldn't be, but verify)
    result = run_cmd("which wasm-pack 2>/dev/null || echo 'wasm-pack not installed (correct)'")

    # Step 8: Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
print("Initial setup complete.")
