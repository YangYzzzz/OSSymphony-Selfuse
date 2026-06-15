"""
Initial Setup: VSCode automation script environment
Task ID: vscode_gf5_049
Domain: vscode

Creates the pre-task state:
- ~/projects/target-repo/ as a git repo with sample files
- ~/exports/ directory (empty)
- ~/config/allowed-extensions.txt with 10 extension IDs
- ~/projects/vscode-automation/ directory (empty, ready for script creation)
- Opens VSCode with the vscode-automation folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_049'

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
    # 1. Create ~/projects/target-repo as a git repository
    target_repo = os.path.join(WORKDIR, 'projects', 'target-repo')
    os.makedirs(target_repo, exist_ok=True)

    # Add some realistic project files
    with open(os.path.join(target_repo, 'README.md'), 'w') as f:
        f.write('# Target Repository\n\n'
                'A sample data processing pipeline for internal analytics.\n\n'
                '## Setup\n\n'
                '```bash\npip install -r requirements.txt\n```\n\n'
                '## Usage\n\n'
                '```bash\npython main.py --config config.yaml\n```\n')

    with open(os.path.join(target_repo, 'main.py'), 'w') as f:
        f.write('#!/usr/bin/env python3\n'
                '"""Main entry point for the analytics pipeline."""\n\n'
                'import argparse\n'
                'import yaml\n'
                'from pathlib import Path\n\n'
                'def load_config(config_path: str) -> dict:\n'
                '    with open(config_path, "r") as f:\n'
                '        return yaml.safe_load(f)\n\n'
                'def run_pipeline(config: dict):\n'
                '    print(f"Running pipeline with {len(config.get(\'stages\', []))} stages")\n'
                '    for stage in config.get("stages", []):\n'
                '        print(f"  Processing stage: {stage[\'name\']}")\n\n'
                'if __name__ == "__main__":\n'
                '    parser = argparse.ArgumentParser(description="Analytics Pipeline")\n'
                '    parser.add_argument("--config", default="config.yaml")\n'
                '    args = parser.parse_args()\n'
                '    config = load_config(args.config)\n'
                '    run_pipeline(config)\n')

    with open(os.path.join(target_repo, 'requirements.txt'), 'w') as f:
        f.write('pyyaml>=6.0\n'
                'pandas>=2.0\n'
                'numpy>=1.24\n'
                'requests>=2.28\n')

    with open(os.path.join(target_repo, 'config.yaml'), 'w') as f:
        f.write('pipeline:\n'
                '  name: analytics-v2\n'
                '  version: 1.3.0\n\n'
                'stages:\n'
                '  - name: extract\n'
                '    source: s3://data-lake/raw\n'
                '  - name: transform\n'
                '    operations: [normalize, deduplicate, enrich]\n'
                '  - name: load\n'
                '    target: postgres://analytics-db/warehouse\n')

    os.makedirs(os.path.join(target_repo, 'src'), exist_ok=True)
    with open(os.path.join(target_repo, 'src', '__init__.py'), 'w') as f:
        f.write('')

    with open(os.path.join(target_repo, 'src', 'transform.py'), 'w') as f:
        f.write('"""Data transformation utilities."""\n\n'
                'import pandas as pd\n\n'
                'def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:\n'
                '    for col in df.select_dtypes(include=["float64"]).columns:\n'
                '        df[col] = (df[col] - df[col].mean()) / df[col].std()\n'
                '    return df\n\n'
                'def deduplicate(df: pd.DataFrame, key_cols: list) -> pd.DataFrame:\n'
                '    return df.drop_duplicates(subset=key_cols, keep="last")\n')

    # Initialize git repo
    subprocess.run(['git', 'init', target_repo], capture_output=True)
    subprocess.run(['git', '-C', target_repo, 'add', '.'], capture_output=True)
    subprocess.run(
        ['git', '-C', target_repo, 'commit', '-m', 'Initial commit: analytics pipeline'],
        capture_output=True,
        env={**os.environ, 'GIT_AUTHOR_NAME': 'Dev Team', 'GIT_AUTHOR_EMAIL': 'dev@company.com',
             'GIT_COMMITTER_NAME': 'Dev Team', 'GIT_COMMITTER_EMAIL': 'dev@company.com'}
    )

    # 2. Create ~/exports/ directory
    exports_dir = os.path.join(WORKDIR, 'exports')
    os.makedirs(exports_dir, exist_ok=True)

    # 3. Create ~/config/allowed-extensions.txt with 10 extension IDs
    config_dir = os.path.join(WORKDIR, 'config')
    os.makedirs(config_dir, exist_ok=True)

    allowed_extensions = [
        'ms-python.python',
        'ms-python.vscode-pylance',
        'ms-toolsai.jupyter',
        'esbenp.prettier-vscode',
        'dbaeumer.vscode-eslint',
        'eamodio.gitlens',
        'ms-azuretools.vscode-docker',
        'redhat.vscode-yaml',
        'github.copilot',
        'ms-vscode.cpptools',
    ]

    with open(os.path.join(config_dir, 'allowed-extensions.txt'), 'w') as f:
        for ext_id in allowed_extensions:
            f.write(ext_id + '\n')

    # 4. Create ~/projects/vscode-automation/ directory (empty, for the agent to create the script)
    automation_dir = os.path.join(WORKDIR, 'projects', 'vscode-automation')
    os.makedirs(automation_dir, exist_ok=True)

    print(f'Initial environment created:')
    print(f'  target-repo: {target_repo}')
    print(f'  exports: {exports_dir}')
    print(f'  config: {config_dir}/allowed-extensions.txt')
    print(f'  automation dir: {automation_dir}')

    # 5. Open VSCode with the vscode-automation folder
    launch_gui(f'code "{automation_dir}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
