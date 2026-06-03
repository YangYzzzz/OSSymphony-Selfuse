"""
Initial Setup: Git advanced operations workspace with multiple branches
Task ID: vscode_gf6_018
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_018'
PROJECT_DIR = f'{WORKDIR}/projects/git-advanced-ops'


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


def run(cmd, cwd=None):
    """Run a shell command, raising on failure."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result


def create_repo():
    """Create the git-advanced-ops repository with the required branch topology."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize repo with 'main' as default branch
    run('git init -b main', cwd=PROJECT_DIR)
    run('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run('git config user.name "Developer"', cwd=PROJECT_DIR)

    # Create initial file on main
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write('# Git Advanced Ops\n\nA sample project for practicing advanced git operations.\n')
    run('git add README.md', cwd=PROJECT_DIR)
    run('git commit -m "Initial commit: add README"', cwd=PROJECT_DIR)

    # --- Build commit history on main (commits 2-5) ---
    # Commit 2: add src directory
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'main.py'), 'w') as f:
        f.write('"""Main application module."""\n\ndef main():\n    print("Hello, world!")\n\nif __name__ == "__main__":\n    main()\n')
    run('git add src/main.py', cwd=PROJECT_DIR)
    run('git commit -m "Add main application entry point"', cwd=PROJECT_DIR)

    # Commit 3: add config
    with open(os.path.join(PROJECT_DIR, 'config.yaml'), 'w') as f:
        f.write('app:\n  name: git-advanced-ops\n  version: 1.0.0\n  debug: false\n')
    run('git add config.yaml', cwd=PROJECT_DIR)
    run('git commit -m "Add application configuration"', cwd=PROJECT_DIR)

    # Commit 4: add utils
    with open(os.path.join(src_dir, 'utils.py'), 'w') as f:
        f.write('"""Utility functions."""\n\nimport os\n\ndef get_project_root():\n    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n')
    run('git add src/utils.py', cwd=PROJECT_DIR)
    run('git commit -m "Add utility module"', cwd=PROJECT_DIR)

    # Commit 5: add tests directory
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')
    with open(os.path.join(tests_dir, 'test_main.py'), 'w') as f:
        f.write('"""Tests for main module."""\n\ndef test_main_exists():\n    from src.main import main\n    assert callable(main)\n')
    run('git add tests/', cwd=PROJECT_DIR)
    run('git commit -m "Add test framework scaffolding"', cwd=PROJECT_DIR)

    # Now we have 5 commits on main. We'll create branches that merge at specific points.

    # --- Create feature/completed-api branch (will merge 5 commits before HEAD) ---
    # Branch from current main, add some commits, then merge
    run('git checkout -b feature/completed-api', cwd=PROJECT_DIR)
    with open(os.path.join(src_dir, 'api.py'), 'w') as f:
        f.write('"""API module for handling HTTP requests."""\n\nimport json\n\ndef handle_request(method, path, body=None):\n    return {"status": 200, "method": method, "path": path}\n\ndef parse_json(raw):\n    return json.loads(raw)\n')
    run('git add src/api.py', cwd=PROJECT_DIR)
    run('git commit -m "Implement API request handler"', cwd=PROJECT_DIR)

    with open(os.path.join(tests_dir, 'test_api.py'), 'w') as f:
        f.write('"""Tests for API module."""\n\ndef test_handle_request():\n    from src.api import handle_request\n    result = handle_request("GET", "/users")\n    assert result["status"] == 200\n')
    run('git add tests/test_api.py', cwd=PROJECT_DIR)
    run('git commit -m "Add API unit tests"', cwd=PROJECT_DIR)

    # Switch to main and merge feature/completed-api
    run('git checkout main', cwd=PROJECT_DIR)
    run('git merge --no-ff feature/completed-api -m "Merge feature/completed-api into main"', cwd=PROJECT_DIR)
    # main now has commit 6 (merge of completed-api)

    # Commit 7 on main
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write('__pycache__/\n*.pyc\n.env\n*.egg-info/\ndist/\nbuild/\n')
    run('git add .gitignore', cwd=PROJECT_DIR)
    run('git commit -m "Add .gitignore for Python artifacts"', cwd=PROJECT_DIR)

    # --- Create feature/old-ui branch (will merge 2 commits before HEAD) ---
    run('git checkout -b feature/old-ui', cwd=PROJECT_DIR)
    templates_dir = os.path.join(PROJECT_DIR, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head><title>Git Advanced Ops</title></head>\n<body>\n  <h1>Dashboard</h1>\n  <div id="app"></div>\n</body>\n</html>\n')
    run('git add templates/', cwd=PROJECT_DIR)
    run('git commit -m "Add UI dashboard template"', cwd=PROJECT_DIR)

    with open(os.path.join(templates_dir, 'style.css'), 'w') as f:
        f.write('body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }\nh1 { color: #333; }\n#app { border: 1px solid #ddd; padding: 15px; }\n')
    run('git add templates/style.css', cwd=PROJECT_DIR)
    run('git commit -m "Add UI styles"', cwd=PROJECT_DIR)

    # Switch to main and merge feature/old-ui
    run('git checkout main', cwd=PROJECT_DIR)
    run('git merge --no-ff feature/old-ui -m "Merge feature/old-ui into main"', cwd=PROJECT_DIR)
    # main now has commit 8 (merge of old-ui)

    # Commit 9 on main: documentation update
    with open(readme_path, 'a') as f:
        f.write('\n## Setup\n\n1. Clone the repository\n2. Install dependencies\n3. Run `python src/main.py`\n')
    run('git add README.md', cwd=PROJECT_DIR)
    run('git commit -m "Update README with setup instructions"', cwd=PROJECT_DIR)

    # --- Create hotfix/minor-fix branch (will merge as last commit = commit 10) ---
    run('git checkout -b hotfix/minor-fix', cwd=PROJECT_DIR)
    with open(os.path.join(PROJECT_DIR, 'config.yaml'), 'a') as f:
        f.write('logging:\n  level: INFO\n  file: app.log\n')
    run('git add config.yaml', cwd=PROJECT_DIR)
    run('git commit -m "Fix: add missing logging configuration"', cwd=PROJECT_DIR)

    # Switch to main and merge hotfix/minor-fix
    run('git checkout main', cwd=PROJECT_DIR)
    run('git merge --no-ff hotfix/minor-fix -m "Merge hotfix/minor-fix into main"', cwd=PROJECT_DIR)
    # main now has commit 10 (merge of minor-fix)

    # --- Create feature/in-progress branch (NOT merged, 3 commits ahead) ---
    run('git checkout -b feature/in-progress', cwd=PROJECT_DIR)

    with open(os.path.join(src_dir, 'database.py'), 'w') as f:
        f.write('"""Database connection module (work in progress)."""\n\nclass DatabaseConnection:\n    def __init__(self, host, port, dbname):\n        self.host = host\n        self.port = port\n        self.dbname = dbname\n        self._conn = None\n\n    def connect(self):\n        # TODO: implement actual connection\n        pass\n')
    run('git add src/database.py', cwd=PROJECT_DIR)
    run('git commit -m "WIP: add database connection skeleton"', cwd=PROJECT_DIR)

    with open(os.path.join(src_dir, 'models.py'), 'w') as f:
        f.write('"""Data models (work in progress)."""\n\nclass User:\n    def __init__(self, user_id, name, email):\n        self.user_id = user_id\n        self.name = name\n        self.email = email\n\nclass Project:\n    def __init__(self, project_id, title, owner):\n        self.project_id = project_id\n        self.title = title\n        self.owner = owner\n')
    run('git add src/models.py', cwd=PROJECT_DIR)
    run('git commit -m "WIP: add User and Project models"', cwd=PROJECT_DIR)

    with open(os.path.join(src_dir, 'database.py'), 'a') as f:
        f.write('\n    def execute(self, query, params=None):\n        # TODO: implement query execution\n        pass\n\n    def close(self):\n        if self._conn:\n            self._conn = None\n')
    run('git add src/database.py', cwd=PROJECT_DIR)
    run('git commit -m "WIP: add execute and close methods to DatabaseConnection"', cwd=PROJECT_DIR)

    # Switch back to main for the initial state
    run('git checkout main', cwd=PROJECT_DIR)

    # Verify branch setup
    result = run('git branch', cwd=PROJECT_DIR)
    print(f"Local branches:\n{result.stdout}")

    result = run('git log --graph --all --oneline', cwd=PROJECT_DIR)
    print(f"Commit graph:\n{result.stdout}")

    print(f"Repository created at {PROJECT_DIR}")


def main():
    create_repo()

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
