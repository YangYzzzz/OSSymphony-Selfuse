"""
Initial Setup: Open VSCode with empty ~/projects/nextjs-blog folder.
Node.js 18 installed via nvm. VSCode extensions for TypeScript, Tailwind, ESLint.
Task ID: vscode_gf4_024
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_024'
PROJECT_DIR = f'{WORKDIR}/projects/nextjs-blog'
NVM_DIR = f'{WORKDIR}/.nvm'


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


def run_cmd(cmd, check=True, timeout=300):
    """Run a shell command and print output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(f"STDERR: {result.stderr.strip()}")
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {cmd}")
    return result


def run_with_nvm(cmd, check=True, timeout=300):
    """Run a command with nvm environment loaded."""
    nvm_cmd = f'bash -c \'export NVM_DIR="{NVM_DIR}" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && {cmd}\''
    return run_cmd(nvm_cmd, check=check, timeout=timeout)


def install_node():
    """Install Node.js 18 via nvm if not present."""
    # Check if node is already available
    node_check = subprocess.run("which node", shell=True, capture_output=True, text=True)
    if node_check.returncode == 0:
        print("Node.js already installed")
        run_cmd("node --version")
        return

    # Check if nvm is installed
    if not os.path.exists(f'{NVM_DIR}/nvm.sh'):
        print("Installing nvm...")
        run_cmd(
            'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash',
            timeout=120
        )

    # Install Node.js 18 via nvm
    print("Installing Node.js 18 via nvm...")
    run_with_nvm('nvm install 20', timeout=120)
    run_with_nvm('nvm alias default 20', timeout=30)

    # Create symlinks so node/npm/npx are available system-wide for this user
    nvm_node_bin = f'{NVM_DIR}/versions/node'
    result = run_with_nvm('which node', timeout=10)
    node_path = result.stdout.strip()
    node_bin_dir = os.path.dirname(node_path)
    print(f"Node bin dir: {node_bin_dir}")

    # Add to PATH by creating symlinks in /usr/local/bin or ~/bin
    user_bin = f'{WORKDIR}/.local/bin'
    os.makedirs(user_bin, exist_ok=True)
    for tool in ['node', 'npm', 'npx', 'corepack']:
        src = os.path.join(node_bin_dir, tool)
        dst = os.path.join(user_bin, tool)
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            os.symlink(src, dst)
            print(f"Symlinked {tool} -> {src}")

    # Update PATH for current process
    os.environ['PATH'] = f"{user_bin}:{node_bin_dir}:{os.environ.get('PATH', '')}"

    # Also add to bashrc so future shells pick it up
    bashrc = f'{WORKDIR}/.bashrc'
    path_line = f'\nexport PATH="{user_bin}:$PATH"\n'
    with open(bashrc, 'a') as f:
        f.write(path_line)

    run_cmd("node --version")
    run_cmd("npm --version")


def create_initial():
    # 1. Install Node.js 18
    install_node()

    # 2. Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"Created project directory: {PROJECT_DIR}")

    # 3. Install VSCode extensions for TypeScript, Tailwind, and ESLint
    extensions = [
        "bradlc.vscode-tailwindcss",
        "dbaeumer.vscode-eslint",
    ]
    for ext in extensions:
        try:
            run_cmd(f'code --install-extension {ext} --force', check=False, timeout=60)
        except Exception as e:
            print(f"Warning: Could not install extension {ext}: {e}")

    # 4. Open VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: VSCode opened with {PROJECT_DIR}')


create_initial()
