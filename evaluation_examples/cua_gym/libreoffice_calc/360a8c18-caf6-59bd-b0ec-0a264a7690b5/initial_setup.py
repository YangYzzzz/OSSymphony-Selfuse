"""
Initial Setup: Kubernetes-like multi-container orchestration on single host
Task ID: os_adm_069
Domain: os (libreoffice_calc listed but this is an OS/Docker task)

Creates a basic three-service docker-compose.yml WITHOUT:
- Resource limits
- Health checks
- Loki service or log driver
- Rolling update script
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_adm_069'

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
    project_dir = f'{WORKDIR}/orchestration-project'
    os.makedirs(project_dir, exist_ok=True)

    # --- Basic docker-compose.yml (no resource limits, no healthchecks, no loki) ---
    compose_content = """\
version: '3.8'

services:
  frontend:
    image: nginx:1.25-alpine
    container_name: orchestration-frontend
    ports:
      - "8080:80"
    volumes:
      - ./frontend/html:/usr/share/nginx/html:ro
    networks:
      - app-network
    restart: unless-stopped

  backend:
    image: python:3.11-slim
    container_name: orchestration-backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
    working_dir: /app
    command: ["python", "-m", "http.server", "5000"]
    networks:
      - app-network
    restart: unless-stopped
    environment:
      - CACHE_HOST=cache
      - CACHE_PORT=6379

  cache:
    image: redis:7-alpine
    container_name: orchestration-cache
    ports:
      - "6379:6379"
    volumes:
      - cache-data:/data
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  cache-data:
"""

    Path(f'{project_dir}/docker-compose.yml').write_text(compose_content)
    print(f'Created docker-compose.yml at {project_dir}/docker-compose.yml')

    # --- Create frontend content ---
    os.makedirs(f'{project_dir}/frontend/html', exist_ok=True)
    Path(f'{project_dir}/frontend/html/index.html').write_text("""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Orchestration Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        .status { padding: 10px; background: #e8f5e9; border-radius: 4px; margin: 10px 0; }
        .service { display: inline-block; margin: 5px; padding: 8px 16px; background: #3498db; color: white; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Multi-Container Orchestration Dashboard</h1>
        <div class="status">
            <h3>Active Services</h3>
            <span class="service">Frontend (nginx)</span>
            <span class="service">Backend (python)</span>
            <span class="service">Cache (redis)</span>
        </div>
        <p>Environment: Production</p>
        <p>Deployment Mode: Docker Compose</p>
    </div>
</body>
</html>
""")

    # --- Create backend app ---
    os.makedirs(f'{project_dir}/backend', exist_ok=True)
    Path(f'{project_dir}/backend/app.py').write_text("""\
#!/usr/bin/env python3
\"\"\"Simple backend service for orchestration demo.\"\"\"
import json
import http.server
import socketserver
import redis
import os
from datetime import datetime

PORT = 5000
CACHE_HOST = os.environ.get('CACHE_HOST', 'cache')
CACHE_PORT = int(os.environ.get('CACHE_PORT', 6379))

class HealthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'service': 'backend',
                'timestamp': datetime.utcnow().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'active_connections': 42,
                'requests_per_minute': 156,
                'uptime_seconds': 86400
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), HealthHandler) as httpd:
        print(f"Backend serving on port {PORT}")
        httpd.serve_forever()
""")

    # --- Create a simple README for context ---
    Path(f'{project_dir}/README.md').write_text("""\
# Multi-Container Orchestration Project

A three-service application stack running on Docker Compose:

- **Frontend**: Nginx serving static dashboard
- **Backend**: Python HTTP API with health endpoints
- **Cache**: Redis for session and data caching

## Current Status

Basic compose setup is in place. The following production features are needed:

- [ ] Resource limits (memory and CPU) for each service
- [ ] Health checks for service monitoring
- [ ] Centralized logging with Loki
- [ ] Rolling update script for zero-downtime deployments
""")

    print(f'Created project structure at {project_dir}/')

    # --- Open terminal and file manager for the task ---
    launch_gui(f'nautilus "{project_dir}"', delay_sec=1.5)
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched nautilus and terminal with DISPLAY=:0')


create_initial()
