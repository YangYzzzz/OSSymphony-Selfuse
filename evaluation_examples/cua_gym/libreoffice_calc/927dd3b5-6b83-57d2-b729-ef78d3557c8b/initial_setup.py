"""
Initial Setup: Build a Kubernetes-ready Docker image for a Node.js application
Task ID: os_gf1_074
Domain: os (Docker/Kubernetes)

Creates:
- /opt/nodeapp/ with package.json and server.js (Node.js express app)
- Docker installed and running
- Local Docker registry running at localhost:5000
- NO Dockerfile (agent must create it)
- Terminal open for agent to work in
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'os_gf1_074'
NODEAPP_DIR = '/opt/nodeapp'
SUDO_PASS = 'password'


def run_cmd(cmd, shell=False, check=True, timeout=300, sudo=False):
    """Run a command and return result."""
    if sudo:
        # Write command to temp script to avoid quoting issues
        import tempfile
        if isinstance(cmd, list):
            cmd = " ".join(cmd)
        script = f"#!/bin/bash\n{cmd}\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(script)
            script_path = f.name
        os.chmod(script_path, 0o755)
        actual_cmd = f"echo '{SUDO_PASS}' | sudo -S bash {script_path}"
        print(f"  Running (sudo): {cmd[:120]}")
        result = subprocess.run(
            actual_cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout,
        )
        os.unlink(script_path)
    else:
        print(f"  Running: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout,
        )
    if result.stdout.strip():
        print(f"  stdout: {result.stdout.strip()[:200]}")
    if result.stderr.strip():
        stderr = result.stderr.strip()
        lines = [l for l in stderr.split('\n') if not l.startswith('[sudo]')]
        if lines:
            print(f"  stderr: {chr(10).join(lines)[:200]}")
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
    """Install Docker CE on Ubuntu 22.04."""
    print("=== Installing Docker ===")

    run_cmd("apt-get update -y", sudo=True, timeout=120)
    run_cmd("apt-get install -y ca-certificates curl gnupg lsb-release apt-transport-https", sudo=True, timeout=120)

    # Add Docker GPG key
    run_cmd("mkdir -p /etc/apt/keyrings", sudo=True)
    run_cmd("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes", sudo=True)

    # Add Docker repo
    result = subprocess.run(["lsb_release", "-cs"], capture_output=True, text=True)
    codename = result.stdout.strip()
    repo_line = f"deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu {codename} stable"
    run_cmd(f'echo "{repo_line}" > /etc/apt/sources.list.d/docker.list', sudo=True)

    run_cmd("apt-get update -y", sudo=True, timeout=120)
    run_cmd("apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin", sudo=True, timeout=180)

    # Start Docker and add user to docker group
    run_cmd("systemctl start docker", sudo=True, check=False)
    run_cmd("systemctl enable docker", sudo=True, check=False)
    run_cmd("usermod -aG docker user", sudo=True, check=False)
    time.sleep(3)

    run_cmd("docker --version", sudo=True)
    print("Docker installed successfully")


def start_local_registry():
    """Start a local Docker registry at localhost:5000."""
    print("=== Starting local Docker registry ===")

    # Configure Docker to allow insecure registry
    # Note: port 5000 is used by VM management agent, so we use port 5001 for registry
    daemon_json = '{"insecure-registries": ["localhost:5001"]}'
    run_cmd(f"mkdir -p /etc/docker && echo '{daemon_json}' > /etc/docker/daemon.json", sudo=True)

    # Restart Docker to pick up config
    run_cmd("systemctl restart docker", sudo=True, check=False)
    time.sleep(5)

    # Remove any existing registry container
    run_cmd("docker rm -f registry", sudo=True, check=False)
    time.sleep(1)

    # Start registry container on port 5001 (5000 is taken by VM agent)
    run_cmd(
        "docker run -d --restart=always -p 5001:5000 --name registry registry:2",
        sudo=True,
        timeout=120,
    )
    time.sleep(3)

    run_cmd("docker ps | grep registry", sudo=True)

    # Create a port redirect so localhost:5000 also works (iptables REDIRECT)
    # Actually, set up socat for transparent port forwarding
    run_cmd("apt-get install -y socat", sudo=True, check=False)
    # We skip 5000 forwarding because the VM agent uses it
    # Instead the task will use localhost:5001

    print("Local registry running at localhost:5001")


def create_node_app():
    """Create a simple Node.js Express application."""
    print("=== Creating Node.js application ===")

    run_cmd(f"mkdir -p {NODEAPP_DIR}", sudo=True)
    run_cmd(f"chown -R user:user {NODEAPP_DIR}", sudo=True)

    # package.json
    package_json = {
        "name": "k8s-nodeapp",
        "version": "1.0.0",
        "description": "Kubernetes-ready Node.js application for inventory management",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "test": "echo \"Error: no test specified\" && exit 1"
        },
        "dependencies": {
            "express": "^4.18.2"
        },
        "author": "DevOps Team <devops@techcorp.io>",
        "license": "MIT"
    }
    with open(os.path.join(NODEAPP_DIR, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)

    # server.js - Express app with /health endpoint
    server_js = '''\
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// In-memory inventory store
let inventory = [
  { id: 1, name: "Widget A", quantity: 150, price: 12.99 },
  { id: 2, name: "Gadget B", quantity: 85, price: 24.50 },
  { id: 3, name: "Component C", quantity: 320, price: 5.75 },
];

// Health check endpoint (for Kubernetes readiness/liveness probes)
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION || '1.0.0'
  });
});

// Get all inventory items
app.get('/api/inventory', (req, res) => {
  res.json({ items: inventory, count: inventory.length });
});

// Get single item
app.get('/api/inventory/:id', (req, res) => {
  const item = inventory.find(i => i.id === parseInt(req.params.id));
  if (!item) return res.status(404).json({ error: 'Item not found' });
  res.json(item);
});

// Add new item
app.post('/api/inventory', (req, res) => {
  const { name, quantity, price } = req.body;
  const newItem = {
    id: inventory.length > 0 ? Math.max(...inventory.map(i => i.id)) + 1 : 1,
    name, quantity, price
  };
  inventory.push(newItem);
  res.status(201).json(newItem);
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'Inventory Management API',
    version: '1.0.0',
    endpoints: ['/health', '/api/inventory']
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Inventory service running on port ${PORT}`);
});
'''
    with open(os.path.join(NODEAPP_DIR, "server.js"), "w") as f:
        f.write(server_js)

    print(f"Node.js app created at {NODEAPP_DIR}/")


def setup():
    install_docker()
    start_local_registry()
    create_node_app()

    # Open a terminal for the agent to work in
    launch_gui('gnome-terminal -- bash', delay_sec=2.0)

    # Also open the file manager showing the nodeapp directory
    launch_gui(f'nautilus "{NODEAPP_DIR}"', delay_sec=1.5)

    print(f"\n=== Initial setup complete ===")
    print(f"Node.js app at: {NODEAPP_DIR}/")
    print(f"Docker registry at: localhost:5001")
    print(f"Note: port 5000 is used by VM agent, registry on port 5001")
    print(f"No Dockerfile exists yet (agent must create it)")
    print("GUI_READY: launched terminal and file manager with DISPLAY=:0")


setup()
