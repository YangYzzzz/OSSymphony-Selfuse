"""
Initial Setup: Docker-based development environment for webapp project
Task ID: osworld_multi_apps_sys_config_010
Domain: os (system configuration / Docker)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_config_010'
WEBAPP_DIR = '/home/user/projects/webapp'
SUDO_PASSWORD = 'password'


def sudo_run(cmd_list, timeout=300):
    """Run a command with sudo using the known password."""
    full_cmd = f"echo '{SUDO_PASSWORD}' | sudo -S {' '.join(shlex.quote(s) for s in cmd_list)}"
    result = subprocess.run(
        full_cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )
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
    """Install Docker and docker-compose if not already installed."""
    # Check if Docker is already installed
    result = subprocess.run(['which', 'docker'], capture_output=True, text=True)
    if result.returncode == 0:
        print('Docker already installed')
        return

    print('Installing Docker...')
    # Update apt and install docker.io
    sudo_run(['apt-get', 'update', '-y'], timeout=120)
    install_result = sudo_run(
        ['apt-get', 'install', '-y', 'docker.io', 'docker-compose'],
        timeout=300
    )
    if install_result.returncode != 0:
        print(f'apt install stderr: {install_result.stderr}')
        raise RuntimeError(f'Docker installation failed: {install_result.returncode}')

    # Add user to docker group so they can run docker without sudo
    sudo_run(['usermod', '-aG', 'docker', 'user'])

    # Start and enable Docker service
    sudo_run(['systemctl', 'start', 'docker'])
    sudo_run(['systemctl', 'enable', 'docker'])

    # Give Docker socket accessible to 'user' group
    sudo_run(['chmod', '666', '/var/run/docker.sock'])

    time.sleep(2)
    # Verify Docker is running
    verify = subprocess.run(['docker', '--version'], capture_output=True, text=True)
    print(f'Docker installed: {verify.stdout.strip()}')


def create_initial():
    # Step 1: Ensure Docker is installed
    install_docker()

    # Step 2: Create project directory structure
    os.makedirs(WEBAPP_DIR, exist_ok=True)

    # Step 3: Create a realistic package.json for a simple Node.js web app
    package_json = '''{
  "name": "webapp",
  "version": "1.0.0",
  "description": "A simple Node.js web application",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.0.3"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.0.0"
  },
  "keywords": ["nodejs", "express", "webapp"],
  "author": "Dev Team",
  "license": "MIT"
}
'''
    Path(f'{WEBAPP_DIR}/package.json').write_text(package_json)

    # Step 4: Create a realistic server.js with Express HTTP server on port 3000
    server_js = '''const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.status(200).json({
    status: 'ok',
    message: 'Welcome to the Webapp API',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

app.get('/api/users', (req, res) => {
  const users = [
    { id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'admin' },
    { id: 2, name: 'Bob Smith', email: 'bob@example.com', role: 'user' },
    { id: 3, name: 'Carol White', email: 'carol@example.com', role: 'user' }
  ];
  res.status(200).json({ users, total: users.length });
});

app.get('/api/products', (req, res) => {
  const products = [
    { id: 1, name: 'Widget Pro', price: 29.99, stock: 150 },
    { id: 2, name: 'Gadget Plus', price: 49.99, stock: 75 },
    { id: 3, name: 'Tool Basic', price: 14.99, stock: 300 }
  ];
  res.status(200).json({ products, total: products.length });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not Found', path: req.path });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
'''
    Path(f'{WEBAPP_DIR}/server.js').write_text(server_js)

    # Step 5: Ensure NO Dockerfile or docker-compose.yml exists (remove if accidentally present)
    for fname in ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', '.dockerignore']:
        fpath = os.path.join(WEBAPP_DIR, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f'Removed existing {fname} to match initial state')

    print(f'Initial webapp directory created at: {WEBAPP_DIR}')
    print(f'  - package.json: Node.js Express app configuration')
    print(f'  - server.js: Express HTTP server on port 3000')
    print(f'  - No Dockerfile (agent must create)')
    print(f'  - No docker-compose.yml (agent must create)')

    # Verify the directory listing
    result = subprocess.run(['ls', '-la', WEBAPP_DIR], capture_output=True, text=True)
    print(f'Directory contents:\n{result.stdout}')

    # GUI-ready startup: open a terminal in the webapp directory
    launch_gui(f'nautilus "{WEBAPP_DIR}"', delay_sec=1.5)
    launch_gui(
        'bash -c "DISPLAY=:0 gnome-terminal --working-directory=/home/user/projects/webapp"',
        delay_sec=2.0
    )
    print('GUI_READY: launched nautilus and gnome-terminal with DISPLAY=:0')


create_initial()
