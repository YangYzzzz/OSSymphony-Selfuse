"""
Initial Setup: Build a custom VSCode extension with Git branch status bar indicator
Task ID: vscode_gf5_029
Domain: vscode (extension development)

Creates:
- Empty ~/projects/branch-indicator/ directory
- A sample Git repository at ~/projects/sample-workspace/ so .git exists
- Opens VSCode with the empty branch-indicator directory
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_029'
PROJECT_DIR = f'{WORKDIR}/projects/branch-indicator'
SAMPLE_WORKSPACE = f'{WORKDIR}/projects/sample-workspace'


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
    # 1. Create empty project directory for the extension
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created empty extension directory: {PROJECT_DIR}')

    # 2. Create a sample workspace with a git repo so there's a .git folder
    #    This simulates a real dev environment where git is initialized
    git_dir = os.path.join(SAMPLE_WORKSPACE, '.git')
    if not os.path.isdir(git_dir):
        os.makedirs(SAMPLE_WORKSPACE, exist_ok=True)
        subprocess.run(['git', 'init', SAMPLE_WORKSPACE], check=True,
                       capture_output=True, text=True)
        # Create a sample file and initial commit so 'main' branch exists
        readme_path = os.path.join(SAMPLE_WORKSPACE, 'README.md')
        with open(readme_path, 'w') as f:
            f.write('# Sample Workspace\n\nThis is a sample project for testing the branch indicator extension.\n')
        subprocess.run(['git', '-C', SAMPLE_WORKSPACE, 'add', '.'], check=True,
                       capture_output=True, text=True)
        subprocess.run(['git', '-C', SAMPLE_WORKSPACE, '-c', 'user.email=dev@example.com',
                       '-c', 'user.name=Developer', 'commit', '-m', 'Initial commit'],
                       check=True, capture_output=True, text=True)
        # Rename default branch to main if needed
        subprocess.run(['git', '-C', SAMPLE_WORKSPACE, 'branch', '-M', 'main'],
                       capture_output=True, text=True)
    print(f'Created sample git workspace: {SAMPLE_WORKSPACE}')

    # 3. Check Node.js availability (non-critical)
    try:
        node_result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if node_result.returncode == 0:
            print(f'Node.js version: {node_result.stdout.strip()}')
        else:
            print('Node.js not found on this VM (non-critical for initial setup)')
    except FileNotFoundError:
        print('Node.js binary not found on this VM (non-critical for initial setup)')

    try:
        npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if npm_result.returncode == 0:
            print(f'npm version: {npm_result.stdout.strip()}')
        else:
            print('npm not found on this VM (non-critical for initial setup)')
    except FileNotFoundError:
        print('npm binary not found on this VM (non-critical for initial setup)')

    # 4. Open VSCode with the empty branch-indicator directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
