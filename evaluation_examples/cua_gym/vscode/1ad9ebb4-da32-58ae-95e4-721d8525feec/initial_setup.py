"""
Initial Setup: Create VSCode workspace with Dockerfile, no tasks.json
Task ID: vscode_ops_035
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_035'
PROJECT_DIR = os.path.join(WORKDIR, 'myapp')


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic Dockerfile
    dockerfile_content = """\
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    with open(os.path.join(PROJECT_DIR, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

    # Create a realistic requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write("fastapi==0.104.1\nuvicorn==0.24.0\npsycopg2-binary==2.9.9\nsqlalchemy==2.0.23\npydantic==2.5.2\n")

    # Create a simple main.py
    main_py = """\
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MyApp API", version="1.0.0")


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Welcome to MyApp API"}
"""
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    # Create .dockerignore
    with open(os.path.join(PROJECT_DIR, '.dockerignore'), 'w') as f:
        f.write("__pycache__\n*.pyc\n.env\n.git\n.vscode\n*.egg-info\n")

    # Ensure NO .vscode/tasks.json exists (the task is to create it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    tasks_path = os.path.join(vscode_dir, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial workspace created: {PROJECT_DIR}')
    print(f'  Dockerfile: {os.path.join(PROJECT_DIR, "Dockerfile")}')
    print(f'  .vscode/tasks.json exists: {os.path.exists(tasks_path)}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
