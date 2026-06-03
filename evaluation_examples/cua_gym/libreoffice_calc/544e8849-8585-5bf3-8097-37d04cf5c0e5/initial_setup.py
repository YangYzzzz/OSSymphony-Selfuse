"""
Initial Setup: Create /opt/webapp/ with a Dockerfile for a Python Flask web app.
Task ID: os_gf2_007
Domain: os (Docker Compose)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_007'
WEBAPP_DIR = '/opt/webapp'

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

def sudo_run(cmd_args):
    """Run a command with sudo, piping password via stdin."""
    proc = subprocess.run(
        ['sudo', '-S'] + cmd_args,
        input='password\n', text=True,
        capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"sudo command failed: {proc.stderr}")

def create_initial():
    # 1. Create /opt/webapp/ directory (needs sudo for /opt)
    sudo_run(['mkdir', '-p', WEBAPP_DIR])
    sudo_run(['chmod', '777', WEBAPP_DIR])

    # 2. Create a realistic Flask app (app.py) that reads DATABASE_URL and REDIS_URL
    app_py_content = '''import os
from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://app:secret@localhost:5432/appdb")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

@app.route("/")
def index():
    return jsonify({"status": "ok", "service": "webapp"})

@app.route("/health")
def health():
    checks = {"database": False, "cache": False}
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        checks["database"] = True
    except Exception:
        pass
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
        checks["cache"] = True
    except Exception:
        pass
    return jsonify(checks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
'''
    with open(os.path.join(WEBAPP_DIR, 'app.py'), 'w') as f:
        f.write(app_py_content)

    # 3. Create requirements.txt
    requirements_content = '''flask==3.0.0
psycopg2-binary==2.9.9
redis==5.0.1
gunicorn==21.2.0
'''
    with open(os.path.join(WEBAPP_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # 4. Create Dockerfile
    dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
'''
    with open(os.path.join(WEBAPP_DIR, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

    # 5. Verify no docker-compose.yml exists (remove if present)
    compose_path = os.path.join(WEBAPP_DIR, 'docker-compose.yml')
    if os.path.exists(compose_path):
        os.remove(compose_path)
    # Also remove docker-compose.yaml variant
    compose_yaml_path = os.path.join(WEBAPP_DIR, 'docker-compose.yaml')
    if os.path.exists(compose_yaml_path):
        os.remove(compose_yaml_path)

    print(f'Initial state created:')
    print(f'  {WEBAPP_DIR}/Dockerfile')
    print(f'  {WEBAPP_DIR}/app.py')
    print(f'  {WEBAPP_DIR}/requirements.txt')
    print(f'  No docker-compose.yml present')

    # 6. GUI-ready: open a terminal at /opt/webapp/ so the agent can start working
    launch_gui('gnome-terminal --working-directory=/opt/webapp', delay_sec=1.5)
    # Also open the file manager to /opt/webapp for visibility
    launch_gui('nautilus "/opt/webapp"', delay_sec=1.0)
    print('GUI_READY: launched terminal and file manager with DISPLAY=:0')

create_initial()
