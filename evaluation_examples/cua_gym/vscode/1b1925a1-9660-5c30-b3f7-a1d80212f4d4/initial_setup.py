"""
Initial Setup: Write a bash script deploy.sh for rolling deployment
Task ID: vscode_ops_072
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_072'
WORKSPACE_DIR = f'{WORKDIR}/deploy-scripts'


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
    # Create workspace directory
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create some existing project context files so the workspace isn't empty
    # but do NOT create deploy.sh — that's the task

    # A docker-compose.yml that references the services the deploy script will manage
    docker_compose = """\
version: '3.8'

services:
  web-1:
    image: myapp/web:latest
    ports:
      - "8081:80"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  web-2:
    image: myapp/web:latest
    ports:
      - "8082:80"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  web-3:
    image: myapp/web:latest
    ports:
      - "8083:80"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - web-1
      - web-2
      - web-3
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
"""
    with open(os.path.join(WORKSPACE_DIR, 'docker-compose.yml'), 'w') as f:
        f.write(docker_compose)

    # A README describing the project
    readme = """\
# Rolling Deployment Scripts

This repository contains deployment tooling for the web application cluster.

## Architecture

- 3 web containers (web-1, web-2, web-3) behind an nginx load balancer
- Each web container exposes a /health endpoint for monitoring
- Docker image: myapp/web

## Deployment Strategy

We use rolling deployments to minimize downtime:
1. Pull the latest Docker image
2. Stop and restart containers one at a time
3. Verify health after each container restart before proceeding

## Usage

Run `deploy.sh` to perform a rolling deployment of the latest image.
"""
    with open(os.path.join(WORKSPACE_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # An nginx config for context
    nginx_conf = """\
events {
    worker_connections 1024;
}

http {
    upstream webapp {
        server web-1:80;
        server web-2:80;
        server web-3:80;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://webapp;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /health {
            return 200 'OK';
            add_header Content-Type text/plain;
        }
    }
}
"""
    with open(os.path.join(WORKSPACE_DIR, 'nginx.conf'), 'w') as f:
        f.write(nginx_conf)

    print(f'Initial workspace created: {WORKSPACE_DIR}')
    print(f'Files: docker-compose.yml, README.md, nginx.conf')
    print(f'deploy.sh does NOT exist (task requires agent to create it)')

    # Install ShellCheck and shell-format extensions
    try:
        subprocess.run(['code', '--install-extension', 'timonwong.shellcheck'],
                       capture_output=True, text=True, timeout=60)
        print('Installed shellcheck extension')
    except Exception as e:
        print(f'Warning: could not install shellcheck extension: {e}')

    try:
        subprocess.run(['code', '--install-extension', 'foxundermoon.shell-format'],
                       capture_output=True, text=True, timeout=60)
        print('Installed shell-format extension')
    except Exception as e:
        print(f'Warning: could not install shell-format extension: {e}')

    # Open VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
