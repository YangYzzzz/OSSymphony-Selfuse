"""
Initial Setup: Git stash workflow in VSCode
Task ID: vscode_ops_084
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_084'
REPO_DIR = f'{WORKDIR}/workspace'


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"  stdout: {result.stdout}")
        print(f"  stderr: {result.stderr}")
    return result


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
    # Clean up any existing workspace
    if os.path.exists(REPO_DIR):
        import shutil
        shutil.rmtree(REPO_DIR)

    os.makedirs(REPO_DIR, exist_ok=True)

    # Initialize git repo with 'main' as default branch
    run_cmd('git init -b main', cwd=REPO_DIR)
    run_cmd('git config user.email "developer@example.com"', cwd=REPO_DIR)
    run_cmd('git config user.name "Developer"', cwd=REPO_DIR)

    # Create initial committed version of nginx.conf
    nginx_conf_initial = """worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
}

http {
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;

    server {
        listen 80 default_server;
        server_name _;

        root /var/www/html;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
}
"""

    docker_compose_initial = """version: '3.8'

services:
  web:
    image: nginx:1.24-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./html:/var/www/html:ro
    restart: unless-stopped
    networks:
      - frontend

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
    restart: unless-stopped
    networks:
      - frontend
      - backend

  db:
    image: postgres:15-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=secret123
    restart: unless-stopped
    networks:
      - backend

volumes:
  pgdata:

networks:
  frontend:
  backend:
"""

    # Write initial committed files
    with open(os.path.join(REPO_DIR, 'nginx.conf'), 'w') as f:
        f.write(nginx_conf_initial)

    with open(os.path.join(REPO_DIR, 'docker-compose.yml'), 'w') as f:
        f.write(docker_compose_initial)

    # Create a README too for more realism
    readme_content = """# Web Application Stack

A containerized web application with Nginx reverse proxy, Node.js API, and PostgreSQL database.

## Quick Start

```bash
docker-compose up -d
```

## Architecture

- **web**: Nginx reverse proxy serving static files
- **api**: Node.js Express API server
- **db**: PostgreSQL 15 database

## Configuration

- Nginx config: `nginx.conf`
- Docker services: `docker-compose.yml`
- API environment variables are set in docker-compose.yml
"""
    with open(os.path.join(REPO_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Create a simple API placeholder
    api_dir = os.path.join(REPO_DIR, 'api')
    os.makedirs(api_dir, exist_ok=True)
    with open(os.path.join(api_dir, 'server.js'), 'w') as f:
        f.write("""const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/v1/users', (req, res) => {
    res.json([
        { id: 1, name: 'Sarah Chen', role: 'admin' },
        { id: 2, name: 'Marcus Johnson', role: 'developer' },
        { id: 3, name: 'Priya Patel', role: 'analyst' },
    ]);
});

app.listen(port, () => {
    console.log(`API server running on port ${port}`);
});
""")

    with open(os.path.join(api_dir, 'Dockerfile'), 'w') as f:
        f.write("""FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
""")

    with open(os.path.join(api_dir, 'package.json'), 'w') as f:
        f.write("""{
  "name": "api-server",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3"
  }
}
""")

    # Create html directory
    html_dir = os.path.join(REPO_DIR, 'html')
    os.makedirs(html_dir, exist_ok=True)
    with open(os.path.join(html_dir, 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Web Application</title>
</head>
<body>
    <h1>Welcome to the Web Application</h1>
    <p>API endpoint: <a href="/api/v1/users">/api/v1/users</a></p>
</body>
</html>
""")

    # Initial commit with all files
    run_cmd('git add -A', cwd=REPO_DIR)
    run_cmd('git commit -m "Initial commit: web stack with nginx, api, and postgres"', cwd=REPO_DIR)

    # Create a second commit for more history
    with open(os.path.join(REPO_DIR, '.gitignore'), 'w') as f:
        f.write("""node_modules/
.env
*.log
pgdata/
""")
    run_cmd('git add .gitignore', cwd=REPO_DIR)
    run_cmd('git commit -m "Add .gitignore for node_modules and env files"', cwd=REPO_DIR)

    # Create 'hotfix' branch (from current main)
    run_cmd('git branch hotfix', cwd=REPO_DIR)

    # Now make uncommitted changes to nginx.conf (add rate limiting and upstream)
    nginx_conf_modified = """worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 1024;
}

http {
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;

    # Rate limiting zone
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    upstream api_backend {
        server api:3000;
        keepalive 32;
    }

    server {
        listen 80 default_server;
        server_name _;

        root /var/www/html;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }

        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://api_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
"""

    docker_compose_modified = """version: '3.8'

services:
  web:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./html:/var/www/html:ro
      - ./certs:/etc/nginx/certs:ro
    restart: unless-stopped
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_HOST=cache
    depends_on:
      - db
      - cache
    restart: unless-stopped
    networks:
      - frontend
      - backend

  db:
    image: postgres:15-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=secret123
    restart: unless-stopped
    networks:
      - backend

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    networks:
      - backend

volumes:
  pgdata:

networks:
  frontend:
  backend:
"""

    # Write the modified (uncommitted) files
    with open(os.path.join(REPO_DIR, 'nginx.conf'), 'w') as f:
        f.write(nginx_conf_modified)

    with open(os.path.join(REPO_DIR, 'docker-compose.yml'), 'w') as f:
        f.write(docker_compose_modified)

    # Verify the state
    result = run_cmd('git status', cwd=REPO_DIR)
    print(f"Git status:\n{result.stdout}")

    result = run_cmd('git branch -a', cwd=REPO_DIR)
    print(f"Branches:\n{result.stdout}")

    result = run_cmd('git diff --stat', cwd=REPO_DIR)
    print(f"Changed files:\n{result.stdout}")

    print(f'Initial workspace created: {REPO_DIR}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{REPO_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
