"""
Initial Setup: Configure Remote Development workspace for SSH in VSCode
Task ID: vscode_gf6_023
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_023'
PROJECT_DIR = f'{WORKDIR}/projects/remote-setup'
SSH_DIR = f'{WORKDIR}/.ssh'

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
    # 1. Create the project workspace directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a dist/ folder with some sample files (needed for the scp deploy task)
    dist_dir = os.path.join(PROJECT_DIR, 'dist')
    os.makedirs(dist_dir, exist_ok=True)
    with open(os.path.join(dist_dir, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head><title>Remote App</title></head>\n<body>\n<h1>Deployment Build</h1>\n</body>\n</html>\n')
    with open(os.path.join(dist_dir, 'app.js'), 'w') as f:
        f.write('// Compiled application bundle\nconsole.log("App initialized");\n')
    with open(os.path.join(dist_dir, 'style.css'), 'w') as f:
        f.write('body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }\n')

    # Create a simple README and source files in the project
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('# Remote Setup Project\n\nThis project is configured for remote development on dev-server.\n')

    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'main.py'), 'w') as f:
        f.write('"""Main application entry point."""\n\nimport os\nimport sys\n\ndef main():\n    print("Running remote application")\n    return 0\n\nif __name__ == "__main__":\n    sys.exit(main())\n')
    with open(os.path.join(src_dir, 'config.py'), 'w') as f:
        f.write('"""Configuration module."""\n\nDEBUG = False\nSERVER_HOST = "0.0.0.0"\nSERVER_PORT = 8080\nDB_URL = "postgresql://localhost:5432/appdb"\n')

    print(f'Project directory created: {PROJECT_DIR}')

    # 2. Set up SSH directory and key
    os.makedirs(SSH_DIR, exist_ok=True)
    os.chmod(SSH_DIR, 0o700)

    # Create the SSH key file (simulated)
    key_path = os.path.join(SSH_DIR, 'dev-key')
    if not os.path.exists(key_path):
        with open(key_path, 'w') as f:
            f.write('-----BEGIN OPENSSH PRIVATE KEY-----\n')
            f.write('b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\n')
            f.write('QyNTUxOQAAACBmYWtlLWtleS1mb3ItdGVzdGluZy1wdXJwb3Nlcy1vbmx5AAAAIAAAAA\n')
            f.write('-----END OPENSSH PRIVATE KEY-----\n')
        os.chmod(key_path, 0o600)
    print(f'SSH key exists: {key_path}')

    # 3. Create ~/.ssh/config with some existing entries but NO dev-server
    config_path = os.path.join(SSH_DIR, 'config')
    with open(config_path, 'w') as f:
        f.write('# SSH Configuration File\n')
        f.write('\n')
        f.write('Host github.com\n')
        f.write('    HostName github.com\n')
        f.write('    User git\n')
        f.write('    IdentityFile ~/.ssh/id_ed25519\n')
        f.write('\n')
        f.write('Host staging-server\n')
        f.write('    HostName 10.0.0.50\n')
        f.write('    User deploy\n')
        f.write('    Port 2222\n')
        f.write('    IdentityFile ~/.ssh/staging-key\n')
        f.write('\n')
    os.chmod(config_path, 0o644)
    print(f'SSH config created (no dev-server entry): {config_path}')

    # 4. Ensure NO .vscode/ directory exists in the workspace
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # 5. Ensure NO workspace file exists
    ws_file = os.path.join(PROJECT_DIR, 'remote-workspace.code-workspace')
    if os.path.exists(ws_file):
        os.remove(ws_file)

    print('Verified: no .vscode/ directory or workspace file exists')

    # 6. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
