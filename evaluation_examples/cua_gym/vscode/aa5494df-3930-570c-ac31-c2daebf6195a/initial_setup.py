"""
Initial Setup: React Dashboard project initialization in VSCode
Task ID: vscode_gf4_020
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_020'
PROJECT_DIR = f'{WORKDIR}/projects/react-dashboard'
NODE_DIR = f'{WORKDIR}/.local/nodejs'


def run_cmd(cmd, cwd=None, timeout=300, env=None):
    """Run a shell command, print output, raise on failure."""
    print(f'Running: {cmd}')
    run_env = env or get_env()
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True, timeout=timeout,
        env=run_env
    )
    if result.stdout:
        print(result.stdout[-2000:])
    if result.stderr:
        print(f'STDERR: {result.stderr[-1000:]}')
    if result.returncode != 0:
        raise RuntimeError(f'Command failed (rc={result.returncode}): {cmd}')
    return result


def get_env():
    """Return environment with Node.js in PATH."""
    env = os.environ.copy()
    node_bin = f'{NODE_DIR}/bin'
    if os.path.isdir(node_bin):
        env['PATH'] = f'{node_bin}:{env.get("PATH", "")}'
    return env


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = get_env()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def install_node():
    """Install Node.js 18 via binary tarball to user-local dir."""
    env = get_env()
    try:
        result = subprocess.run('node --version', shell=True, capture_output=True, text=True, env=env)
        if result.returncode == 0 and result.stdout.strip().startswith('v'):
            print(f'Node.js already installed: {result.stdout.strip()}')
            return
    except Exception:
        pass

    print('Installing Node.js 18 via binary tarball...')
    node_ver = 'v18.20.8'
    tarball = f'node-{node_ver}-linux-x64.tar.xz'
    url = f'https://nodejs.org/dist/{node_ver}/{tarball}'

    os.makedirs(NODE_DIR, exist_ok=True)
    run_cmd(f'curl -fsSL {url} -o /tmp/{tarball}', timeout=120)
    run_cmd(f'tar -xJf /tmp/{tarball} -C /tmp/', timeout=60)
    # Move extracted contents into NODE_DIR
    run_cmd(f'rm -rf {NODE_DIR}/*', timeout=10)
    run_cmd(f'mv /tmp/node-{node_ver}-linux-x64/* {NODE_DIR}/', timeout=10)
    run_cmd(f'rm -rf /tmp/node-{node_ver}-linux-x64 /tmp/{tarball}', timeout=10)

    # Also add to .bashrc so terminal sessions pick it up
    bashrc = os.path.join(WORKDIR, '.bashrc')
    export_line = f'export PATH="{NODE_DIR}/bin:$PATH"'
    with open(bashrc, 'r') as f:
        content = f.read()
    if NODE_DIR not in content:
        with open(bashrc, 'a') as f:
            f.write(f'\n# Node.js\n{export_line}\n')

    run_cmd('node --version')
    run_cmd('npm --version')


def create_initial():
    # Install Node.js 18 (task context says it should be available)
    install_node()

    # Install create-react-app globally (task says it's available globally)
    run_cmd(f'npm install -g create-react-app', timeout=120)

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Launch VSCode with the empty project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
