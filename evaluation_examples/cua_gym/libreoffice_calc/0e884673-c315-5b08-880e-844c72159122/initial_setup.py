"""
Initial Setup: Docker health check configuration for web application container
Task ID: os_adm_054
Domain: os (Docker / docker-compose)

Creates:
- /opt/webapp/docker-compose.yml WITHOUT healthcheck configuration
- A simple Python HTTP server as the webapp (with /health endpoint)
- Installs Docker and Docker Compose if not present
- Starts the webapp container without health checks
- Opens a terminal and text editor showing the compose file
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_adm_054'
SUDO_PASS = 'password'


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


def sudo_run(cmd, timeout=300):
    """Run a shell command with sudo using password."""
    full_cmd = f"echo '{SUDO_PASS}' | sudo -S bash -c '{cmd}'"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True,
                            timeout=timeout)
    if result.returncode != 0:
        print(f"Command failed (rc={result.returncode}): {cmd}")
        print(f"STDOUT: {result.stdout[:500]}")
        print(f"STDERR: {result.stderr[:500]}")
    return result


def install_docker():
    """Install Docker and Docker Compose if not present."""
    result = subprocess.run(["which", "docker"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Docker already installed.")
    else:
        print("Installing Docker...")
        sudo_run("apt-get update -y", timeout=120)
        sudo_run("apt-get install -y ca-certificates curl gnupg lsb-release", timeout=120)

        sudo_run("mkdir -p /etc/apt/keyrings")
        sudo_run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | "
                 "gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg")
        sudo_run('echo "deb [arch=$(dpkg --print-architecture) '
                 'signed-by=/etc/apt/keyrings/docker.gpg] '
                 'https://download.docker.com/linux/ubuntu '
                 '$(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list')
        sudo_run("apt-get update -y", timeout=120)
        sudo_run("apt-get install -y docker-ce docker-ce-cli containerd.io "
                 "docker-compose-plugin", timeout=300)

    # Ensure Docker is running
    sudo_run("systemctl start docker")
    sudo_run("systemctl enable docker")
    # Add user to docker group so we can run docker without sudo
    sudo_run("usermod -aG docker user")
    time.sleep(3)

    # Verify docker works (use sudo for now since group change needs re-login)
    result = sudo_run("docker info")
    if result.returncode == 0:
        print("Docker is ready.")
    else:
        print("WARNING: Docker may not be fully ready.")


def create_webapp_image():
    """Create a simple webapp Docker image with a /health endpoint."""
    app_build_dir = "/tmp/webapp_build"
    os.makedirs(app_build_dir, exist_ok=True)

    app_code = '''\
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>WebApp Running</h1>")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    print("Server running on port 8080...")
    server.serve_forever()
'''
    Path(f"{app_build_dir}/app.py").write_text(app_code)

    dockerfile = '''\
FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
'''
    Path(f"{app_build_dir}/Dockerfile").write_text(dockerfile)

    print("Building webapp Docker image...")
    result = sudo_run(f"docker build -t webapp:latest {app_build_dir}", timeout=300)
    if result.returncode == 0:
        print("Webapp image built successfully.")
    else:
        print("WARNING: Image build may have failed.")


def create_compose_file():
    """Create docker-compose.yml WITHOUT healthcheck configuration."""
    compose_dir = "/opt/webapp"
    sudo_run(f"mkdir -p {compose_dir}")

    # docker-compose.yml WITHOUT healthcheck - this is the initial state
    compose_content = '''version: "3.8"

services:
  webapp:
    image: webapp:latest
    container_name: webapp
    ports:
      - "8080:8080"
    restart: unless-stopped
    environment:
      - APP_ENV=production
      - LOG_LEVEL=info
    networks:
      - webapp-net

networks:
  webapp-net:
    driver: bridge
'''

    # Write to temp then move with sudo
    tmp_path = "/tmp/docker-compose.yml"
    Path(tmp_path).write_text(compose_content)
    sudo_run(f"cp {tmp_path} {compose_dir}/docker-compose.yml")
    sudo_run(f"chown user:user {compose_dir}/docker-compose.yml")
    print(f"Created {compose_dir}/docker-compose.yml (without healthcheck)")


def start_container():
    """Start the webapp container using docker compose."""
    print("Starting webapp container...")
    result = sudo_run("docker compose -f /opt/webapp/docker-compose.yml up -d", timeout=120)
    time.sleep(5)

    # Verify container is running
    result = sudo_run("docker ps --filter name=webapp --format '{{.Names}} {{.Status}}'")
    print(f"Container status: {result.stdout.strip()}")

    # Verify health endpoint works
    result = subprocess.run("curl -sf http://localhost:8080/health", shell=True,
                            capture_output=True, text=True, timeout=10)
    print(f"Health endpoint response: {result.stdout.strip()}")


def setup_gui():
    """Open a terminal showing the docker-compose.yml and docker status."""
    launch_gui('gedit /opt/webapp/docker-compose.yml', delay_sec=2.0)
    launch_gui('gnome-terminal -- bash -c "echo === Docker Container Status ===; '
               'docker ps 2>/dev/null || sudo docker ps; echo; '
               'echo === docker-compose.yml ===; '
               'cat /opt/webapp/docker-compose.yml; exec bash"', delay_sec=1.5)
    print("GUI_READY: launched gedit and terminal with DISPLAY=:0")


def main():
    install_docker()
    create_webapp_image()
    create_compose_file()
    start_container()
    setup_gui()
    print(f"\nInitial setup complete for {TASK_ID}")
    print("docker-compose.yml created at /opt/webapp/docker-compose.yml WITHOUT healthcheck")


main()
