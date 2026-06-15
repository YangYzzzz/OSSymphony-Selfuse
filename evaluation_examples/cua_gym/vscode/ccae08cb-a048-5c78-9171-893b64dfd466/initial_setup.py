"""
Initial Setup: Create VSCode workspace with docker-compose project (no tasks.json)
Task ID: vscode_td_027
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_027'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'microservices')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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

    # Create a realistic docker-compose.yml with 3 services
    docker_compose = {
        "version": "3.8",
        "services": {
            "api": {
                "build": "./api",
                "ports": ["8080:8080"],
                "environment": [
                    "DATABASE_URL=postgres://app_user:s3cret@db:5432/microservices_db",
                    "REDIS_URL=redis://cache:6379/0",
                    "LOG_LEVEL=info"
                ],
                "depends_on": ["db", "cache"],
                "restart": "unless-stopped",
                "volumes": ["./api:/app"],
                "networks": ["backend"]
            },
            "db": {
                "image": "postgres:15-alpine",
                "environment": [
                    "POSTGRES_USER=app_user",
                    "POSTGRES_PASSWORD=s3cret",
                    "POSTGRES_DB=microservices_db"
                ],
                "volumes": ["pgdata:/var/lib/postgresql/data"],
                "ports": ["5432:5432"],
                "restart": "unless-stopped",
                "networks": ["backend"]
            },
            "cache": {
                "image": "redis:7-alpine",
                "ports": ["6379:6379"],
                "restart": "unless-stopped",
                "volumes": ["redis_data:/data"],
                "networks": ["backend"]
            }
        },
        "volumes": {
            "pgdata": None,
            "redis_data": None
        },
        "networks": {
            "backend": {
                "driver": "bridge"
            }
        }
    }

    # Write docker-compose.yml as YAML-formatted text for realism
    compose_yaml = """version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://app_user:s3cret@db:5432/microservices_db
      - REDIS_URL=redis://cache:6379/0
      - LOG_LEVEL=info
    depends_on:
      - db
      - cache
    restart: unless-stopped
    volumes:
      - ./api:/app
    networks:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=app_user
      - POSTGRES_PASSWORD=s3cret
      - POSTGRES_DB=microservices_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - backend

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  pgdata:
  redis_data:

networks:
  backend:
    driver: bridge
"""

    with open(os.path.join(PROJECT_DIR, 'docker-compose.yml'), 'w') as f:
        f.write(compose_yaml)

    # Create a simple api directory with a Dockerfile for realism
    api_dir = os.path.join(PROJECT_DIR, 'api')
    os.makedirs(api_dir, exist_ok=True)

    with open(os.path.join(api_dir, 'Dockerfile'), 'w') as f:
        f.write("""FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
""")

    with open(os.path.join(api_dir, 'requirements.txt'), 'w') as f:
        f.write("fastapi==0.104.1\nuvicorn==0.24.0\npsycopg2-binary==2.9.9\nredis==5.0.1\n")

    with open(os.path.join(api_dir, 'main.py'), 'w') as f:
        f.write("""from fastapi import FastAPI
import os

app = FastAPI(title="Microservices API")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api"}

@app.get("/")
async def root():
    return {"message": "Microservices API v1.0"}
""")

    # Ensure NO .vscode/tasks.json exists
    tasks_json_path = os.path.join(VSCODE_DIR, 'tasks.json')
    if os.path.exists(tasks_json_path):
        os.remove(tasks_json_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'docker-compose.yml with 3 services: api, db, cache')
    print(f'No .vscode/tasks.json present')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
