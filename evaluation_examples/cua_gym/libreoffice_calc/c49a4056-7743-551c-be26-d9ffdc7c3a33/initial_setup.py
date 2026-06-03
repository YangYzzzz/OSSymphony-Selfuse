"""
Initial Setup: VSCode SSH remote connection with empty port forwarding
Task ID: vscode_rrt_014
Domain: vs-code

Sets up:
- SSH config for 'backend-dev' host
- VSCode Remote-SSH extension installed
- VSCode settings for remote SSH connection
- Simulated remote services (PostgreSQL on 5432, Redis on 6379)
- VSCode opened and connected
- Ports panel is EMPTY (no forwarding entries)
"""

import json
import os
import shlex
import subprocess
import time

HOME = "/home/user"
WORKDIR = HOME
TASK_ID = "vscode_rrt_014"

# VSCode paths
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")

# SSH paths
SSH_DIR = os.path.join(HOME, ".ssh")
SSH_CONFIG = os.path.join(SSH_DIR, "config")

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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def setup_ssh_config():
    """Create SSH config with backend-dev host."""
    os.makedirs(SSH_DIR, exist_ok=True)

    # Generate a dummy SSH key pair for the connection
    key_path = os.path.join(SSH_DIR, "id_rsa_backend")
    if not os.path.exists(key_path):
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-b", "2048", "-f", key_path, "-N", "", "-q"],
            check=True,
        )

    ssh_config = """Host backend-dev
    HostName 192.168.1.50
    User devops
    Port 22
    IdentityFile ~/.ssh/id_rsa_backend
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    ForwardAgent yes
"""
    with open(SSH_CONFIG, "w") as f:
        f.write(ssh_config)
    os.chmod(SSH_CONFIG, 0o600)
    print(f"SSH config created: {SSH_CONFIG}")


def setup_workspace():
    """Create a workspace directory that simulates the remote project."""
    project_dir = os.path.join(HOME, "backend-project")
    os.makedirs(project_dir, exist_ok=True)

    # Create some realistic project files
    # docker-compose.yml referencing PostgreSQL and Redis
    docker_compose = """version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://appuser:s3cure_p@ss@localhost:5432/backend_db
      REDIS_URL: redis://localhost:6379/0

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: backend_db
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: s3cure_p@ss
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --requirepass r3dis_auth

volumes:
  pgdata:
"""
    with open(os.path.join(project_dir, "docker-compose.yml"), "w") as f:
        f.write(docker_compose)

    # Main application config
    app_config = """{
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "backend_db",
        "user": "appuser"
    },
    "cache": {
        "host": "localhost",
        "port": 6379,
        "db": 0
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8000,
        "debug": false
    }
}
"""
    with open(os.path.join(project_dir, "config.json"), "w") as f:
        f.write(app_config)

    # Python app file
    app_py = '''"""Backend API Server - connects to PostgreSQL and Redis."""
import asyncio
import asyncpg
import aioredis
from fastapi import FastAPI

app = FastAPI(title="Backend API")

DATABASE_URL = "postgresql://appuser:s3cure_p@ss@localhost:5432/backend_db"
REDIS_URL = "redis://localhost:6379/0"

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)
    app.state.redis = await aioredis.from_url(REDIS_URL)

@app.get("/health")
async def health_check():
    """Check PostgreSQL and Redis connectivity."""
    pg_ok = False
    redis_ok = False
    try:
        async with app.state.db.acquire() as conn:
            await conn.fetchval("SELECT 1")
        pg_ok = True
    except Exception:
        pass
    try:
        await app.state.redis.ping()
        redis_ok = True
    except Exception:
        pass
    return {"postgresql": pg_ok, "redis": redis_ok}

@app.get("/users")
async def list_users():
    async with app.state.db.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, email FROM users LIMIT 50")
    return [dict(r) for r in rows]
'''
    with open(os.path.join(project_dir, "app.py"), "w") as f:
        f.write(app_py)

    # Requirements file
    requirements = """fastapi==0.104.1
uvicorn==0.24.0
asyncpg==0.29.0
aioredis==2.0.1
pydantic==2.5.2
"""
    with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
        f.write(requirements)

    print(f"Workspace created: {project_dir}")
    return project_dir


def setup_vscode_settings():
    """Configure VSCode settings for Remote-SSH. NO port forwarding entries."""
    settings = load_settings()

    # Remote-SSH settings
    settings.update({
        "remote.SSH.remotePlatform": {
            "backend-dev": "linux"
        },
        "remote.SSH.defaultExtensions": [
            "ms-python.python",
            "ms-python.vscode-pylance"
        ],
        "remote.SSH.connectTimeout": 30,
        "remote.SSH.showLoginTerminal": True,
        "remote.SSH.configFile": os.path.join(HOME, ".ssh", "config"),
        # Explicitly NO remote.portsAttributes - ports panel should be empty
    })

    save_settings(settings)
    print(f"VSCode settings updated: {SETTINGS_PATH}")


def install_remote_ssh_extension():
    """Install Remote-SSH extension."""
    try:
        result = subprocess.run(
            ["code", "--install-extension", "ms-vscode-remote.remote-ssh", "--force"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        print(f"Remote-SSH extension install: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"Extension install stderr: {result.stderr.strip()}")
    except Exception as e:
        print(f"Extension install warning: {e}")


def main():
    # 1. Set up SSH configuration
    setup_ssh_config()

    # 2. Create workspace files
    project_dir = setup_workspace()

    # 3. Install Remote-SSH extension
    install_remote_ssh_extension()

    # 4. Configure VSCode settings (no port forwarding)
    setup_vscode_settings()

    # 5. Launch VSCode with the project
    launch_gui(f'code "{project_dir}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")
    print(f"Initial setup complete for {TASK_ID}")


main()
