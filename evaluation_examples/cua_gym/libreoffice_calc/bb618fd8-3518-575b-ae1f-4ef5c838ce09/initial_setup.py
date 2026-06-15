"""
Initial Setup: pre-commit config edit task — flake8 hook only, no black hook
Task ID: osworld_multi_apps_vscode_config_edit_012
Domain: multi-apps (VSCode + Chrome)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_config_edit_012'
REPO_DIR = f'{WORKDIR}/Code/myrepo'
CONFIG_PATH = f'{REPO_DIR}/.pre-commit-config.yaml'


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
    # Create the repo directory
    os.makedirs(REPO_DIR, exist_ok=True)

    # Create a realistic .pre-commit-config.yaml with only flake8 hook
    # NOTE: No 'black' hook, no default_language_version for python3.12
    # These are what the agent needs to add
    content = """\
repos:
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]
"""
    with open(CONFIG_PATH, 'w') as f:
        f.write(content)

    print(f'Initial config created: {CONFIG_PATH}')
    print('Contents:')
    with open(CONFIG_PATH, 'r') as f:
        print(f.read())

    # GUI startup: open Chrome at pre-commit docs, then open VSCode with the file
    # First, launch Chrome with the pre-commit documentation URL
    launch_gui('google-chrome "https://pre-commit.com/"', delay_sec=3.0)

    # Then launch VSCode with the config file open
    launch_gui(f'code "{CONFIG_PATH}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome (pre-commit.com) and VSCode with DISPLAY=:0')


create_initial()
