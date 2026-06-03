"""
Initial Setup: Python FastAPI project with directory structure and packages
Task ID: vscode_wf_048
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_048'
PROJECT = f'{WORKDIR}/project'


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
    dirs = [
        f'{PROJECT}/app/routers',
        f'{PROJECT}/app/models',
        f'{PROJECT}/tests',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Create __init__.py files
    init_files = [
        f'{PROJECT}/app/__init__.py',
        f'{PROJECT}/app/routers/__init__.py',
        f'{PROJECT}/app/models/__init__.py',
        f'{PROJECT}/tests/__init__.py',
    ]
    for f in init_files:
        with open(f, 'w') as fh:
            fh.write('')

    # Create app/main.py with a basic FastAPI app
    main_py = '''\
from fastapi import FastAPI

app = FastAPI(title="Project API", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
'''
    with open(f'{PROJECT}/app/main.py', 'w') as f:
        f.write(main_py)

    # Create a basic test file
    test_main = '''\
def test_placeholder():
    assert True
'''
    with open(f'{PROJECT}/tests/test_main.py', 'w') as f:
        f.write(test_main)

    # Install required packages
    packages = ['fastapi', 'uvicorn', 'pytest', 'httpx']
    for pkg in packages:
        subprocess.run(
            ['pip3', 'install', pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    print('Packages installed: fastapi, uvicorn, pytest, httpx')

    print(f'Project structure created at {PROJECT}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
