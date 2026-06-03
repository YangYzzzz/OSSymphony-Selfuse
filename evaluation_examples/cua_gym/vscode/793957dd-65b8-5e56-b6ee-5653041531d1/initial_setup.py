"""
Initial Setup: Set up a multi-remote git configuration using local bare repositories
Task ID: vscode_git_071
Domain: vs_code

Creates /home/user/project as a git repository with:
- A main branch with realistic project content
- No remotes configured (agent must add them)
- No develop or experimental branches
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_071'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        shlex.split(cmd) if isinstance(cmd, str) else cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
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
    # Clean up existing project directory if present
    if os.path.exists(PROJECT_DIR):
        run_cmd(f'rm -rf {PROJECT_DIR}')

    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Set up git user config for commits
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Alice Thompson'
    git_env['GIT_AUTHOR_EMAIL'] = 'alice.thompson@devteam.io'
    git_env['GIT_COMMITTER_NAME'] = 'Alice Thompson'
    git_env['GIT_COMMITTER_EMAIL'] = 'alice.thompson@devteam.io'

    # Initialize git repo
    run_cmd('git init', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.name "Alice Thompson"', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.email "alice.thompson@devteam.io"', cwd=PROJECT_DIR, env=git_env)

    # Create README.md
    readme_content = """# Project Alpha

A collaborative software project for managing customer data pipelines.

## Overview

This project provides tools for ingesting, transforming, and exporting customer
transaction records from multiple data sources.

## Features

- Batch data ingestion from CSV and JSON sources
- Real-time stream processing via Kafka integration
- Configurable transformation pipeline
- Export to PostgreSQL and BigQuery

## Getting Started

```bash
pip install -r requirements.txt
python main.py --config config/default.yaml
```

## Project Structure

```
project/
├── src/
│   ├── ingestion/
│   ├── transform/
│   └── export/
├── config/
├── tests/
└── docs/
```

## Contributing

Please read CONTRIBUTING.md before submitting pull requests.
"""

    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Create requirements.txt
    requirements_content = """# Core dependencies
pandas==2.0.3
numpy==1.24.3
pyyaml==6.0
kafka-python==2.0.2
psycopg2-binary==2.9.6
google-cloud-bigquery==3.11.4
SQLAlchemy==2.0.19

# Development dependencies
pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
flake8==6.1.0
mypy==1.4.1
"""

    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # Create src directory structure
    os.makedirs(f'{PROJECT_DIR}/src/ingestion', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/transform', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/export', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # Create main.py
    main_content = '''#!/usr/bin/env python3
"""
Project Alpha - Main Entry Point
"""

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Project Alpha Data Pipeline")
    parser.add_argument("--config", type=str, default="config/default.yaml",
                        help="Path to configuration file")
    parser.add_argument("--mode", choices=["batch", "stream"], default="batch",
                        help="Processing mode")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate configuration without executing")
    return parser.parse_args()


def main():
    args = parse_args()
    logger.info(f"Starting pipeline in {args.mode} mode")
    logger.info(f"Config: {args.config}")

    if args.dry_run:
        logger.info("Dry run mode: configuration validated successfully")
        return 0

    # TODO: Initialize pipeline components
    logger.info("Pipeline execution complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(main_content)

    # Create config/default.yaml
    config_content = """# Default pipeline configuration
pipeline:
  name: "alpha-pipeline"
  version: "1.0.0"

ingestion:
  source_type: "csv"
  source_path: "/data/input"
  batch_size: 1000
  encoding: "utf-8"

transform:
  normalize_dates: true
  drop_duplicates: true
  fill_nulls: false

export:
  destination: "postgresql"
  host: "localhost"
  port: 5432
  database: "customer_data"
  table: "transactions"
"""

    with open(f'{PROJECT_DIR}/config/default.yaml', 'w') as f:
        f.write(config_content)

    # Create src/ingestion/__init__.py
    with open(f'{PROJECT_DIR}/src/ingestion/__init__.py', 'w') as f:
        f.write('"""Ingestion module for loading data from various sources."""\n')

    with open(f'{PROJECT_DIR}/src/transform/__init__.py', 'w') as f:
        f.write('"""Transform module for data cleaning and normalization."""\n')

    with open(f'{PROJECT_DIR}/src/export/__init__.py', 'w') as f:
        f.write('"""Export module for writing data to destinations."""\n')

    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg
*.egg-info/
dist/
build/
.eggs/
*.whl

# Virtual environments
venv/
.venv/
env/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Data files
*.csv
*.json
!config/*.json

# Logs
*.log
logs/
"""

    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore_content)

    # Stage and commit all files
    run_cmd('git add .', cwd=PROJECT_DIR, env=git_env)
    run_cmd(
        'git commit -m "Initial commit: project structure and core pipeline files"',
        cwd=PROJECT_DIR, env=git_env
    )

    # Add a second commit with a small update to make history more realistic
    with open(f'{PROJECT_DIR}/README.md', 'a') as f:
        f.write('\n## License\n\nMIT License. See LICENSE file for details.\n')

    run_cmd('git add README.md', cwd=PROJECT_DIR, env=git_env)
    run_cmd(
        'git commit -m "docs: add license section to README"',
        cwd=PROJECT_DIR, env=git_env
    )

    # Rename default branch to 'main' if needed
    result = run_cmd('git branch', cwd=PROJECT_DIR, env=git_env)
    branches = result.stdout.strip()
    if 'master' in branches and 'main' not in branches:
        run_cmd('git branch -m master main', cwd=PROJECT_DIR, env=git_env)

    # Verify: no remotes should be configured
    result = run_cmd('git remote -v', cwd=PROJECT_DIR, env=git_env)
    print(f'Remotes (should be empty): "{result.stdout.strip()}"')

    # Verify: only main branch
    result = run_cmd('git branch', cwd=PROJECT_DIR, env=git_env)
    print(f'Branches: {result.stdout.strip()}')

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder using DISPLAY=:0')


create_initial()
