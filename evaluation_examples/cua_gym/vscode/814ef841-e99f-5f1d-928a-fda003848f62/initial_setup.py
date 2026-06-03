"""
Initial Setup: Resolve a merge conflict in config.json (vscode_git_027)
Task ID: vscode_git_027
Domain: vs_code

Creates a Git repository at /home/user/project with a real merge conflict in config.json.
Both 'main' and 'feature/new-settings' diverge from a common ancestor by modifying
the same 'timeout' line to different values (30 and 60 respectively).
The agent must resolve the conflict by keeping the feature branch value (60),
stage the file, and complete the merge commit.

Conflict creation strategy:
  - Base commit: config.json has "timeout": 0 (placeholder)
  - Branch from base: create 'feature/new-settings'
  - On main: change "timeout": 0 -> "timeout": 30
  - On feature: change "timeout": 0 -> "timeout": 60
  - Merge feature into main -> CONFLICT on the timeout line
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f'CMD: {cmd}')
        print(f'STDOUT: {result.stdout}')
        print(f'STDERR: {result.stderr}')
    return result


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
    # Remove old project dir if it exists (idempotent)
    if os.path.exists(PROJECT_DIR):
        subprocess.run(['rm', '-rf', PROJECT_DIR], check=True)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo, try to use 'main' as default branch
    init_result = run_cmd('git init -b main', cwd=PROJECT_DIR)
    if init_result.returncode != 0:
        # Older git: init creates 'master', rename to 'main'
        run_cmd('git init', cwd=PROJECT_DIR)
        run_cmd('git symbolic-ref HEAD refs/heads/main', cwd=PROJECT_DIR)

    run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Dev User"', cwd=PROJECT_DIR)

    # -------------------------------------------------------
    # BASE COMMIT: config.json with "timeout": 0 (placeholder)
    # This is the common ancestor from which both branches diverge
    # -------------------------------------------------------
    config_base = '''{
  "app": {
    "name": "MyWebApp",
    "version": "2.1.0",
    "environment": "production"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "timeout": 0,
    "max_connections": 100,
    "keep_alive": true
  },
  "database": {
    "host": "db.internal.example.com",
    "port": 5432,
    "name": "mywebapp_prod",
    "pool_size": 10,
    "ssl": true
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "output": "/var/log/mywebapp/app.log",
    "rotate": "daily"
  },
  "cache": {
    "backend": "redis",
    "host": "cache.internal.example.com",
    "port": 6379,
    "ttl": 3600
  }
}
'''

    readme_content = '''# MyWebApp

A production web application with configurable settings.

## Configuration

Edit `config.json` to change server settings, database connection, logging, and cache options.

## Getting Started

1. Clone the repository
2. Update `config.json` with your environment settings
3. Run `npm start` to launch the application

## Branches

- `main` — stable production configuration
- `feature/new-settings` — updated server timeout and performance settings
'''

    gitignore_content = '''node_modules/
*.log
.env
.DS_Store
dist/
build/
'''

    with open(f'{PROJECT_DIR}/config.json', 'w') as f:
        f.write(config_base)
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore_content)

    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial commit: add app configuration (timeout TBD)"', cwd=PROJECT_DIR)

    # -------------------------------------------------------
    # FEATURE BRANCH: change "timeout": 0 -> "timeout": 60
    # -------------------------------------------------------
    run_cmd('git checkout -b feature/new-settings', cwd=PROJECT_DIR)

    config_feature = '''{
  "app": {
    "name": "MyWebApp",
    "version": "2.1.0",
    "environment": "production"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "timeout": 60,
    "max_connections": 100,
    "keep_alive": true
  },
  "database": {
    "host": "db.internal.example.com",
    "port": 5432,
    "name": "mywebapp_prod",
    "pool_size": 10,
    "ssl": true
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "output": "/var/log/mywebapp/app.log",
    "rotate": "daily"
  },
  "cache": {
    "backend": "redis",
    "host": "cache.internal.example.com",
    "port": 6379,
    "ttl": 3600
  }
}
'''

    with open(f'{PROJECT_DIR}/config.json', 'w') as f:
        f.write(config_feature)

    run_cmd('git add config.json', cwd=PROJECT_DIR)
    run_cmd('git commit -m "feature/new-settings: set server timeout to 60s for performance"', cwd=PROJECT_DIR)

    # -------------------------------------------------------
    # MAIN BRANCH: change "timeout": 0 -> "timeout": 30
    # -------------------------------------------------------
    # Get the initial commit hash to reset main to the base
    base_hash = run_cmd('git log --format=%H --reverse | head -1', cwd=PROJECT_DIR).stdout.strip()

    # Checkout main branch
    run_cmd('git checkout main', cwd=PROJECT_DIR)

    # Verify we are at the base (timeout: 0)
    with open(f'{PROJECT_DIR}/config.json', 'r') as f:
        check = f.read()
    assert '"timeout": 0' in check, f'Expected base state with timeout:0, got: {check[:200]}'

    # Modify main: change "timeout": 0 -> "timeout": 30
    config_main = '''{
  "app": {
    "name": "MyWebApp",
    "version": "2.1.0",
    "environment": "production"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "timeout": 30,
    "max_connections": 100,
    "keep_alive": true
  },
  "database": {
    "host": "db.internal.example.com",
    "port": 5432,
    "name": "mywebapp_prod",
    "pool_size": 10,
    "ssl": true
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "output": "/var/log/mywebapp/app.log",
    "rotate": "daily"
  },
  "cache": {
    "backend": "redis",
    "host": "cache.internal.example.com",
    "port": 6379,
    "ttl": 3600
  }
}
'''

    with open(f'{PROJECT_DIR}/config.json', 'w') as f:
        f.write(config_main)

    run_cmd('git add config.json', cwd=PROJECT_DIR)
    run_cmd('git commit -m "main: set default server timeout to 30s"', cwd=PROJECT_DIR)

    # -------------------------------------------------------
    # TRIGGER MERGE CONFLICT: merge feature/new-settings into main
    # Both branches changed the same line -> conflict
    # -------------------------------------------------------
    result = run_cmd('git merge feature/new-settings', cwd=PROJECT_DIR)
    print(f'Merge result (expected conflict, rc=1): returncode={result.returncode}')
    print(f'Merge stdout: {result.stdout}')
    print(f'Merge stderr: {result.stderr}')

    # Verify conflict markers exist in config.json
    with open(f'{PROJECT_DIR}/config.json', 'r') as f:
        content = f.read()

    if '<<<<<<< HEAD' in content:
        print('SUCCESS: Conflict markers confirmed in config.json')
    else:
        print(f'ERROR: No conflict markers found!')
        print(f'config.json:\n{content}')

    # Print final git status
    status = run_cmd('git status', cwd=PROJECT_DIR)
    print(f'Git status:\n{status.stdout}')

    log = run_cmd('git log --oneline --all', cwd=PROJECT_DIR)
    print(f'Git log:\n{log.stdout}')

    print(f'Initial repository created: {PROJECT_DIR}')
    print(f'config.json has merge conflict. Agent must resolve by keeping timeout=60.')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
