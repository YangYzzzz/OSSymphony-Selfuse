"""
Initial Setup: Set up Celery project structure for VSCode
Task ID: vscode_gf6_060
Domain: libreoffice_calc (actually vscode/python project)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_060'
PROJECT_DIR = f'{WORKDIR}/projects/python-celery'


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
    # Create the project directory structure
    os.makedirs(f'{PROJECT_DIR}/src/tasks', exist_ok=True)

    # Create src/__init__.py (empty)
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('')

    # Create src/tasks/__init__.py (empty)
    with open(f'{PROJECT_DIR}/src/tasks/__init__.py', 'w') as f:
        f.write('')

    # Create a basic README so the project folder isn't totally empty
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Python Celery Project

A distributed task processing application using Celery with Redis as the message broker.

## Project Structure

```
python-celery/
├── src/
│   ├── __init__.py
│   └── tasks/
│       └── __init__.py
├── tests/
└── README.md
```

## Getting Started

1. Create a virtual environment
2. Install dependencies (celery, redis, flower, pytest-celery)
3. Configure Celery app with Redis broker
4. Define task modules
5. Set up tests and debugging configuration
""")

    # Create a requirements.txt placeholder (no packages listed yet - agent should populate)
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("# Add project dependencies here\n")

    print(f'Initial project structure created at: {PROJECT_DIR}')
    print(f'  src/__init__.py')
    print(f'  src/tasks/__init__.py')
    print(f'  README.md')
    print(f'  requirements.txt')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
