"""
Initial Setup: Git remote push setup task
Task ID: vscode_git_059
Domain: vs_code

Creates /home/user/project with 5 commits on main branch and no remotes configured.
The agent will need to:
  1. Create /tmp/shared-repo.git as a bare repository
  2. Add it as remote 'origin' to /home/user/project
  3. Push main to origin
  4. Create and push a 'develop' branch
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_059'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, check=True):
    """Run a shell command and return stdout."""
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = 'Dev User'
    env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    env['GIT_COMMITTER_NAME'] = 'Dev User'
    env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'
    result = subprocess.run(
        shlex.split(cmd),
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        print(f'ERROR running: {cmd}')
        print(f'STDOUT: {result.stdout}')
        print(f'STDERR: {result.stderr}')
        raise RuntimeError(f'Command failed: {cmd}')
    return result.stdout.strip()


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Remove any existing project directory to ensure a clean state
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    # Remove any pre-existing bare repo from a previous run
    if os.path.exists('/tmp/shared-repo.git'):
        import shutil
        shutil.rmtree('/tmp/shared-repo.git')

    # Create project directory and initialize git repo
    os.makedirs(PROJECT_DIR, exist_ok=True)
    run('git init', cwd=PROJECT_DIR)
    run('git checkout -b main', cwd=PROJECT_DIR, check=False)

    # Create 5 meaningful commits with realistic content
    # Commit 1: Initial project structure
    readme_content = """# Analytics Dashboard

A web-based analytics dashboard for tracking business KPIs.

## Features
- Real-time data visualization
- Customizable widgets
- Export to CSV/PDF
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)
    run('git add README.md', cwd=PROJECT_DIR)
    run('git commit -m "Initial project setup with README"', cwd=PROJECT_DIR)

    # Commit 2: Add source directory and main entry point
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    main_py = """#!/usr/bin/env python3
\"\"\"
Analytics Dashboard - Main Entry Point
\"\"\"

import sys
from dashboard import App


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    sys.exit(main())
"""
    with open(os.path.join(src_dir, 'main.py'), 'w') as f:
        f.write(main_py)
    run('git add src/', cwd=PROJECT_DIR)
    run('git commit -m "Add main entry point and src directory"', cwd=PROJECT_DIR)

    # Commit 3: Add dashboard module
    dashboard_py = """\"\"\"Dashboard application core module.\"\"\"

import json
import os


class App:
    def __init__(self):
        self.config = self._load_config()
        self.widgets = []

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        if os.path.exists(config_path):
            with open(config_path) as f:
                return json.load(f)
        return {'title': 'Dashboard', 'refresh_interval': 30}

    def add_widget(self, widget):
        self.widgets.append(widget)

    def run(self):
        print(f"Starting {self.config['title']}")
        for w in self.widgets:
            w.render()
"""
    with open(os.path.join(src_dir, 'dashboard.py'), 'w') as f:
        f.write(dashboard_py)
    run('git add src/', cwd=PROJECT_DIR)
    run('git commit -m "Add dashboard core module with widget support"', cwd=PROJECT_DIR)

    # Commit 4: Add configuration file
    config_data = {
        "title": "Analytics Dashboard",
        "refresh_interval": 60,
        "theme": "dark",
        "data_sources": [
            {"name": "sales", "endpoint": "/api/v1/sales", "type": "time_series"},
            {"name": "users", "endpoint": "/api/v1/users", "type": "gauge"},
            {"name": "revenue", "endpoint": "/api/v1/revenue", "type": "bar_chart"}
        ],
        "widgets": [
            {"id": "w1", "type": "line_chart", "data_source": "sales", "position": {"x": 0, "y": 0}},
            {"id": "w2", "type": "gauge", "data_source": "users", "position": {"x": 1, "y": 0}},
            {"id": "w3", "type": "bar_chart", "data_source": "revenue", "position": {"x": 0, "y": 1}}
        ]
    }
    import json
    with open(os.path.join(PROJECT_DIR, 'config.json'), 'w') as f:
        json.dump(config_data, f, indent=2)
    run('git add config.json', cwd=PROJECT_DIR)
    run('git commit -m "Add dashboard configuration with data sources and widgets"', cwd=PROJECT_DIR)

    # Commit 5: Add tests directory
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    test_py = """\"\"\"Unit tests for the Analytics Dashboard.\"\"\"

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from dashboard import App


class TestApp(unittest.TestCase):
    def test_default_config_loaded(self):
        app = App()
        self.assertIn('title', app.config)

    def test_add_widget(self):
        app = App()
        dummy = object()
        app.add_widget(dummy)
        self.assertEqual(len(app.widgets), 1)

    def test_widget_list_empty_on_init(self):
        app = App()
        self.assertEqual(len(app.widgets), 0)


if __name__ == '__main__':
    unittest.main()
"""
    with open(os.path.join(tests_dir, 'test_dashboard.py'), 'w') as f:
        f.write(test_py)
    # Add .gitignore
    gitignore = """__pycache__/
*.pyc
*.pyo
.pytest_cache/
.venv/
dist/
build/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)
    run('git add tests/ .gitignore', cwd=PROJECT_DIR)
    run('git commit -m "Add unit tests and .gitignore"', cwd=PROJECT_DIR)

    # Verify 5 commits on main, no remotes
    log_output = run('git log --oneline', cwd=PROJECT_DIR)
    commit_count = len(log_output.strip().splitlines())
    print(f'Commits on main: {commit_count}')

    remotes = run('git remote -v', cwd=PROJECT_DIR, check=False)
    print(f'Remotes: "{remotes}" (should be empty)')

    branch_output = run('git branch', cwd=PROJECT_DIR)
    print(f'Branches: {branch_output}')

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Git log:\n{log_output}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project directory, DISPLAY=:0')


create_initial()
