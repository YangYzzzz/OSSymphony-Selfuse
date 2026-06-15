"""
Initial Setup: Python Schema Migration Framework project scaffold
Task ID: vscode_gf4_074
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_074'
PROJECT_DIR = f'{WORKDIR}/projects/python-schema-migrations'


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/alembic', exist_ok=True)

    # config.py with DATABASE_URL setting
    with open(f'{PROJECT_DIR}/config.py', 'w') as f:
        f.write('''"""Application configuration for schema migration framework."""

import os

# Database connection URL — uses SQLite for local dev and testing
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./migrations_dev.db"
)

# Alembic configuration
ALEMBIC_INI_PATH = os.path.join(os.path.dirname(__file__), "alembic.ini")

# Migration settings
MIGRATION_DIR = os.path.join(os.path.dirname(__file__), "alembic", "versions")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
''')

    # alembic.ini stub
    with open(f'{PROJECT_DIR}/alembic.ini', 'w') as f:
        f.write('''[alembic]
# Alembic configuration file — stub for schema-migrations project

script_location = alembic
sqlalchemy.url = sqlite:///./migrations_dev.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
''')

    print(f'Initial project scaffold created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
