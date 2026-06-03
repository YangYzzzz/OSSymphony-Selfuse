"""
Initial Setup: Build Docker image and push to local registry
Task ID: os_adm_028
Domain: os (Docker)

Sets up:
- Docker installed and running
- A valid Dockerfile in /opt/myapp/
- A local Docker registry container running at localhost:5050
  (Note: port 5000 is used by the VM management server, so registry uses 5050)
- No 'myapp' image in the registry yet
- Terminal open for the user
"""

import os
import shlex
import subprocess
import time
import json
import base64

WORKDIR = '/home/user'
TASK_ID = 'os_adm_028'
SUDO_PASS = 'password'
REGISTRY_PORT = 5050


def run(cmd, check=True, shell=True, sudo=False):
    """Run a command, print output, and return result."""
    if sudo:
        cmd = f"echo '{SUDO_PASS}' | sudo -S bash -c '{cmd}'"
    print(f"  >> {cmd[:200]}")
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300)
    if result.stdout.strip():
        print(result.stdout.strip()[:500])
    if result.stderr.strip():
        stderr_lines = [l for l in result.stderr.strip().split('\n') if '[sudo]' not in l]
        if stderr_lines:
            print('\n'.join(stderr_lines)[:500])
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed (rc={result.returncode}): {cmd[:200]}")
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


def install_docker():
    """Install Docker CE on Ubuntu."""
    print("=== Installing Docker ===")
    run("apt-get update -qq", sudo=True)
    run("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ca-certificates curl gnupg lsb-release", sudo=True)

    run("install -m 0755 -d /etc/apt/keyrings", sudo=True)
    run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc", sudo=True)
    run("chmod a+r /etc/apt/keyrings/docker.asc", sudo=True)

    result = run("lsb_release -cs")
    codename = result.stdout.strip()
    result2 = run("dpkg --print-architecture")
    arch = result2.stdout.strip()
    repo_line = f"deb [arch={arch} signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu {codename} stable"

    run(f'echo "{repo_line}" > /etc/apt/sources.list.d/docker.list', sudo=True)

    run("apt-get update -qq", sudo=True)
    run("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin", sudo=True)

    run("systemctl start docker", sudo=True)
    run("systemctl enable docker", sudo=True)
    run("usermod -aG docker user", sudo=True, check=False)

    print("Docker installed successfully")
    run("docker --version", sudo=True)


def create_dockerfile():
    """Create a valid Dockerfile in /opt/myapp/."""
    print("=== Creating Dockerfile ===")
    run("mkdir -p /opt/myapp", sudo=True)

    dockerfile_content = '''FROM python:3.11-slim

LABEL maintainer="devops@techcorp.io"
LABEL version="1.0"
LABEL description="TechCorp internal microservice for data processing"

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask==3.0.0 requests==2.31.0

# Copy application code
COPY app.py /app/
COPY config.json /app/

EXPOSE 8080

ENV FLASK_ENV=production
ENV APP_PORT=8080

CMD ["python", "app.py"]
'''

    app_py = '''#!/usr/bin/env python3
"""TechCorp Data Processing Service v1.0"""
import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def load_config():
    with open("config.json") as f:
        return json.load(f)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route("/process", methods=["POST"])
def process_data():
    data = request.get_json()
    config = load_config()
    return jsonify({
        "processed": True,
        "items": len(data.get("items", [])),
        "service": config.get("service_name", "unknown")
    })

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 8080))
    app.run(host="0.0.0.0", port=port)
'''

    config_data = json.dumps({
        "service_name": "techcorp-data-processor",
        "version": "1.0.0",
        "log_level": "INFO",
        "max_workers": 4,
        "timeout_seconds": 30
    }, indent=2)

    for fname, content in [("Dockerfile", dockerfile_content), ("app.py", app_py), ("config.json", config_data)]:
        encoded = base64.b64encode(content.encode()).decode()
        run(f"echo {encoded} | base64 -d > /opt/myapp/{fname}", sudo=True)

    run("chmod -R a+r /opt/myapp", sudo=True)
    run("ls -la /opt/myapp/", sudo=True)
    print("Dockerfile and application files created in /opt/myapp/")


def start_registry():
    """Start a local Docker registry at localhost:REGISTRY_PORT."""
    print(f"=== Starting local Docker registry on port {REGISTRY_PORT} ===")
    # Remove any existing registry container first
    run("docker rm -f registry 2>/dev/null || true", sudo=True)
    run("docker pull registry:2", sudo=True)
    run(f"docker run -d -p {REGISTRY_PORT}:5000 --restart=always --name registry registry:2", sudo=True)
    # Wait for registry to be ready
    time.sleep(5)
    run("docker ps | grep registry", sudo=True)
    result = run(f"curl -s http://localhost:{REGISTRY_PORT}/v2/_catalog", check=False)
    print(f"Registry catalog: {result.stdout}")
    print(f"Local Docker registry running at localhost:{REGISTRY_PORT}")

    # Configure Docker daemon to allow insecure registry
    daemon_config = json.dumps({"insecure-registries": [f"localhost:{REGISTRY_PORT}"]})
    encoded = base64.b64encode(daemon_config.encode()).decode()
    run(f"echo {encoded} | base64 -d > /etc/docker/daemon.json", sudo=True)
    run("systemctl restart docker", sudo=True)
    time.sleep(3)
    # Restart registry after Docker restart
    run("docker start registry 2>/dev/null || true", sudo=True)
    time.sleep(3)
    result = run(f"curl -s http://localhost:{REGISTRY_PORT}/v2/_catalog", check=False)
    print(f"Registry catalog after restart: {result.stdout}")


def setup_initial():
    install_docker()
    create_dockerfile()
    start_registry()

    # Verify no myapp image exists in registry
    result = run(f"curl -s http://localhost:{REGISTRY_PORT}/v2/myapp/tags/list", check=False)
    print(f"Registry myapp state (should be empty/error): {result.stdout}")

    # Open a terminal for the user
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')
    print(f'Initial setup complete for {TASK_ID}')


setup_initial()
