"""
Initial Setup: Migrate Python project from setup.py to Poetry
Task ID: vscode_gf6_056
Domain: vscode

Creates ~/projects/python-poetry with:
  - src/myapp/__init__.py (FastAPI app)
  - setup.py (old-style)
  - requirements.txt
  - tests/test_main.py
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_056'
PROJECT_DIR = f'{WORKDIR}/projects/python-poetry'

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

def ensure_python311():
    """Ensure Python 3.11 is installed (task context says it should be available)."""
    result = subprocess.run(['python3.11', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Python 3.11 already available: {result.stdout.strip()}")
        return
    print("Installing Python 3.11...")
    cmds = [
        "echo 'password' | sudo -S apt-get update -qq",
        "echo 'password' | sudo -S apt-get install -y -qq software-properties-common",
        "echo 'password' | sudo -S add-apt-repository -y ppa:deadsnakes/ppa",
        "echo 'password' | sudo -S apt-get update -qq",
        "echo 'password' | sudo -S apt-get install -y -qq python3.11 python3.11-venv python3.11-dev",
    ]
    for cmd in cmds:
        subprocess.run(cmd, shell=True, capture_output=True, timeout=120)
    result = subprocess.run(['python3.11', '--version'], capture_output=True, text=True)
    print(f"Python 3.11 installed: {result.stdout.strip()}")

def create_initial():
    # Ensure Python 3.11 is available (per task context)
    ensure_python311()

    # Create project directories
    os.makedirs(f'{PROJECT_DIR}/src/myapp', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- src/myapp/__init__.py ---
    init_content = '''\
"""MyApp - A FastAPI-based REST API service."""

__version__ = "0.1.0"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="MyApp",
    description="A lightweight inventory management API",
    version=__version__,
)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0

# In-memory store
_items: dict[str, Item] = {}

@app.get("/")
async def root():
    return {"message": "Welcome to MyApp API", "version": __version__}

@app.get("/items", response_model=List[Item])
async def list_items():
    return list(_items.values())

@app.get("/items/{item_name}", response_model=Item)
async def get_item(item_name: str):
    if item_name not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return _items[item_name]

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    if item.name in _items:
        raise HTTPException(status_code=409, detail="Item already exists")
    _items[item.name] = item
    return item

@app.delete("/items/{item_name}", status_code=204)
async def delete_item(item_name: str):
    if item_name not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_name]
'''
    with open(f'{PROJECT_DIR}/src/myapp/__init__.py', 'w') as f:
        f.write(init_content)

    # --- setup.py ---
    setup_content = '''\
from setuptools import setup, find_packages

setup(
    name="myapp",
    version="0.1.0",
    description="A lightweight inventory management API",
    author="Development Team",
    author_email="dev@myapp.example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "mypy>=1.7.0",
        ],
    },
)
'''
    with open(f'{PROJECT_DIR}/setup.py', 'w') as f:
        f.write(setup_content)

    # --- requirements.txt ---
    requirements_content = '''\
fastapi>=0.104.0
uvicorn>=0.24.0
sqlalchemy>=2.0.0
pytest>=7.4.0
black>=23.0.0
mypy>=1.7.0
'''
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements_content)

    # --- tests/test_main.py ---
    test_content = '''\
"""Basic tests for MyApp API."""

import pytest


def test_placeholder():
    """Placeholder test to be expanded after migration."""
    assert True


def test_version():
    """Verify version string format."""
    from myapp import __version__
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)
'''
    with open(f'{PROJECT_DIR}/tests/test_main.py', 'w') as f:
        f.write(test_content)

    # --- tests/__init__.py ---
    with open(f'{PROJECT_DIR}/tests/__init__.py', 'w') as f:
        f.write('')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  - src/myapp/__init__.py')
    print(f'  - setup.py')
    print(f'  - requirements.txt')
    print(f'  - tests/test_main.py')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
