"""
Initial Setup: Open pyproject.toml in VSCode with Chrome open at pytest docs
Task ID: osworld_multi_apps_vscode_config_edit_009
Domain: multi_apps (VSCode + Chrome + OS file)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_config_edit_009'
PROJECT_DIR = f'{WORKDIR}/Code/tests'
TOML_PATH = f'{PROJECT_DIR}/pyproject.toml'


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
    # Create directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create pyproject.toml with [tool.poetry] and [build-system] sections only
    # No pytest configuration (task is to add it)
    toml_content = """\
[tool.poetry]
name = "my-project"
version = "0.2.1"
description = "A Python project with automated testing"
authors = ["Alice Nguyen <alice.nguyen@example.com>"]
license = "MIT"
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31.0"
click = "^8.1.7"
pydantic = "^2.5.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.11.0"
ruff = "^0.1.6"
mypy = "^1.7.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

    with open(TOML_PATH, 'w') as f:
        f.write(toml_content)

    print(f'Initial file created: {TOML_PATH}')

    # Launch Chrome with pytest documentation
    launch_gui('google-chrome --new-window "https://docs.pytest.org/"', delay_sec=2.0)

    # Open VSCode with the pyproject.toml file
    launch_gui(f'code "{TOML_PATH}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome (pytest docs) and VSCode with pyproject.toml')


create_initial()
