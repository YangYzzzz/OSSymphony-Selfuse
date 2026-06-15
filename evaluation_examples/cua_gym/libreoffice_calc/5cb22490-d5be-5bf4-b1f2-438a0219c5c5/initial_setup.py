"""
Initial Setup: Configure structured logging with structlog in python-structlog project
Task ID: vscode_gf6_072
Domain: vscode (libreoffice_calc mapped to vscode task)
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_072'
PROJECT_DIR = f'{WORKDIR}/projects/python-structlog'


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
    os.makedirs(f'{PROJECT_DIR}/src/api', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/middleware', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- src/__init__.py ---
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('')

    # --- src/api/__init__.py ---
    with open(f'{PROJECT_DIR}/src/api/__init__.py', 'w') as f:
        f.write('')

    # --- src/api/users.py (5 endpoints with print() statements) ---
    users_py = '''\
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

app = FastAPI(title="User Management API", version="1.0.0")

# In-memory user store
users_db: dict = {}


class UserCreate(BaseModel):
    name: str
    email: str
    role: Optional[str] = "member"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


@app.get("/users")
def list_users(skip: int = 0, limit: int = 20):
    """List all users with pagination."""
    print(f"Listing users with skip={skip}, limit={limit}")
    all_users = list(users_db.values())
    result = all_users[skip : skip + limit]
    print(f"Returning {len(result)} users out of {len(all_users)} total")
    return {"users": result, "total": len(all_users)}


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    """Create a new user."""
    print(f"Creating user: {user.name} ({user.email})")
    user_id = str(uuid.uuid4())
    user_record = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "created_at": datetime.utcnow().isoformat(),
    }
    users_db[user_id] = user_record
    print(f"User created successfully with id={user_id}")
    return user_record


@app.get("/users/{user_id}")
def get_user(user_id: str):
    """Retrieve a specific user by ID."""
    print(f"Fetching user with id={user_id}")
    if user_id not in users_db:
        print(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    print(f"Found user: {users_db[user_id]['name']}")
    return users_db[user_id]


@app.put("/users/{user_id}")
def update_user(user_id: str, updates: UserUpdate):
    """Update an existing user."""
    print(f"Updating user {user_id} with {updates.dict(exclude_unset=True)}")
    if user_id not in users_db:
        print(f"User not found for update: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in updates.dict(exclude_unset=True).items():
        users_db[user_id][field] = value
    users_db[user_id]["updated_at"] = datetime.utcnow().isoformat()
    print(f"User {user_id} updated successfully")
    return users_db[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str):
    """Delete a user by ID."""
    print(f"Deleting user with id={user_id}")
    if user_id not in users_db:
        print(f"User not found for deletion: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    deleted = users_db.pop(user_id)
    print(f"User {deleted['name']} deleted successfully")
    return None
'''
    with open(f'{PROJECT_DIR}/src/api/users.py', 'w') as f:
        f.write(users_py)

    # --- Create virtual environment and install fastapi + uvicorn ---
    print("Creating virtual environment...")
    subprocess.run(
        ['python3', '-m', 'venv', '--without-pip', f'{PROJECT_DIR}/venv'],
        check=True, capture_output=True, text=True,
    )
    # Bootstrap pip into the venv
    print("Bootstrapping pip into venv...")
    subprocess.run(
        ['bash', '-c', f'curl -sS https://bootstrap.pypa.io/get-pip.py | {PROJECT_DIR}/venv/bin/python3'],
        check=True, capture_output=True, text=True,
    )
    print("Installing fastapi and uvicorn...")
    subprocess.run(
        [f'{PROJECT_DIR}/venv/bin/pip', 'install', 'fastapi', 'uvicorn', 'pydantic'],
        check=True, capture_output=True, text=True,
    )
    print("Base dependencies installed.")

    # --- Create a basic pyproject.toml ---
    pyproject = '''\
[project]
name = "python-structlog"
version = "0.1.0"
description = "User Management API with structured logging"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["pytest"]
'''
    with open(f'{PROJECT_DIR}/pyproject.toml', 'w') as f:
        f.write(pyproject)

    print(f'Initial project created: {PROJECT_DIR}')

    # --- GUI-ready: open VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
