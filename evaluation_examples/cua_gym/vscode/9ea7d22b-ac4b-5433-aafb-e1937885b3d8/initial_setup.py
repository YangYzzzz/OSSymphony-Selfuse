"""
Initial Setup: Configure a remote development preparation workflow in ~/project
Task ID: vscode_wf_065
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_065'
PROJECT_DIR = f'{WORKDIR}/project'

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
    # 1. Create ~/project directory with some starter files
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Add a README so the project isn't empty
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write("""# Remote Development Project

This project is set up for remote development workflows.

## Getting Started

1. Configure SSH access to the development server
2. Install required VSCode extensions
3. Run the setup script on the remote machine

## Architecture

- `src/` - Application source code
- `tests/` - Test suite
- `docs/` - Documentation
""")

    # Create some source files
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(src_dir, 'main.py'), 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"Main application entry point.\"\"\"

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def initialize_app():
    \"\"\"Initialize the application configuration.\"\"\"
    config_path = Path.home() / '.config' / 'myapp' / 'settings.yaml'
    logger.info(f"Loading config from {config_path}")
    return {"status": "initialized", "version": "0.1.0"}

def main():
    logging.basicConfig(level=logging.INFO)
    app = initialize_app()
    logger.info(f"Application started: {app['version']}")

if __name__ == '__main__':
    main()
""")

    with open(os.path.join(src_dir, 'utils.py'), 'w') as f:
        f.write("""\"\"\"Utility functions for the project.\"\"\"

import hashlib
import json
from datetime import datetime

def generate_session_id(user_id: str) -> str:
    \"\"\"Generate a unique session identifier.\"\"\"
    timestamp = datetime.utcnow().isoformat()
    raw = f"{user_id}:{timestamp}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def load_json_config(path: str) -> dict:
    \"\"\"Load and validate a JSON configuration file.\"\"\"
    with open(path, 'r') as f:
        return json.load(f)
""")

    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    with open(os.path.join(tests_dir, 'test_main.py'), 'w') as f:
        f.write("""import unittest
from src.main import initialize_app

class TestMain(unittest.TestCase):
    def test_initialize_app(self):
        result = initialize_app()
        self.assertEqual(result['status'], 'initialized')
        self.assertIn('version', result)

if __name__ == '__main__':
    unittest.main()
""")

    # 2. Ensure ~/.ssh directory exists (but no devserver config)
    ssh_dir = os.path.join(WORKDIR, '.ssh')
    os.makedirs(ssh_dir, exist_ok=True)
    os.chmod(ssh_dir, 0o700)

    # Create a basic ssh config if it doesn't exist (no devserver entry)
    ssh_config = os.path.join(ssh_dir, 'config')
    if not os.path.exists(ssh_config):
        with open(ssh_config, 'w') as f:
            f.write("""# SSH Configuration
# Add your host entries below

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
""")
        os.chmod(ssh_config, 0o600)

    # Generate an SSH key pair if none exists
    id_key = os.path.join(ssh_dir, 'id_ed25519')
    if not os.path.exists(id_key):
        subprocess.run(
            ['ssh-keygen', '-t', 'ed25519', '-f', id_key, '-N', '', '-q'],
            check=False
        )

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'SSH directory ready: {ssh_dir}')

    # 3. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
