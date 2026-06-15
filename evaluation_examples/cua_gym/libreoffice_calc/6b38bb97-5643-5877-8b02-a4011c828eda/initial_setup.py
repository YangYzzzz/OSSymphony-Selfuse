"""
Initial Setup: Zero-downtime deployment pipeline for Node.js with Nginx upstream switching
Task ID: os_adm_061
Domain: os (system administration)
"""

import os
import shlex
import subprocess
import time
import json
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_adm_061'
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


def run_cmd(cmd, check=True):
    """Run a shell command and print output for debugging."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"  stdout: {result.stdout.strip()[:500]}")
    if result.stderr.strip():
        print(f"  stderr: {result.stderr.strip()[:500]}")
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed (rc={result.returncode}): {cmd}")
    return result


def sudo(cmd, check=True):
    """Run command with sudo using password."""
    return run_cmd(f"echo '{SUDO_PASS}' | sudo -S {cmd}", check=check)


def create_initial():
    print("=== Setting up initial state for os_adm_061 ===")

    # 1. Install Nginx
    print("Installing Nginx...")
    sudo("apt-get update -qq", check=False)
    sudo("apt-get install -y -qq nginx curl", check=False)

    # Install Node.js (v18 LTS) if not present
    result = run_cmd("which node", check=False)
    if result.returncode != 0:
        print("Installing Node.js...")
        run_cmd("curl -fsSL https://deb.nodesource.com/setup_18.x -o /tmp/nodesource_setup.sh", check=False)
        sudo("bash /tmp/nodesource_setup.sh", check=False)
        sudo("apt-get install -y -qq nodejs", check=False)

    # Verify node is available
    run_cmd("node --version", check=False)
    run_cmd("npm --version", check=False)

    # Install PM2 globally
    result = run_cmd("which pm2", check=False)
    if result.returncode != 0:
        print("Installing PM2...")
        sudo("npm install -g pm2", check=False)

    # 2. Create Node.js v1 application at /opt/app-v1/
    print("Creating v1 application...")
    sudo("mkdir -p /opt/app-v1")
    sudo("chmod 777 /opt/app-v1")

    Path("/opt/app-v1/package.json").write_text(json.dumps({
        "name": "myapp-v1",
        "version": "1.0.0",
        "description": "Production Node.js application v1",
        "main": "server.js",
        "scripts": {"start": "node server.js"},
        "dependencies": {"express": "^4.18.0"}
    }, indent=2))

    Path("/opt/app-v1/server.js").write_text('''const http = require('http');

const PORT = process.env.PORT || 3000;
const VERSION = '1.0.0';

const server = http.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({ status: 'ok', version: VERSION }));
        return;
    }
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('<h1>MyApp v' + VERSION + '</h1><p>Running on port ' + PORT + '</p>');
});

server.listen(PORT, () => {
    console.log('App v' + VERSION + ' listening on port ' + PORT);
});
''')

    # 3. Create Node.js v2 application at /opt/app-v2/
    print("Creating v2 application...")
    sudo("mkdir -p /opt/app-v2")
    sudo("chmod 777 /opt/app-v2")

    Path("/opt/app-v2/package.json").write_text(json.dumps({
        "name": "myapp-v2",
        "version": "2.0.0",
        "description": "Production Node.js application v2",
        "main": "server.js",
        "scripts": {"start": "node server.js"},
        "dependencies": {"express": "^4.18.0"}
    }, indent=2))

    Path("/opt/app-v2/server.js").write_text('''const http = require('http');

const PORT = process.env.PORT || 3001;
const VERSION = '2.0.0';

const server = http.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({ status: 'ok', version: VERSION }));
        return;
    }
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('<h1>MyApp v' + VERSION + '</h1><p>Running on port ' + PORT + '</p>');
});

server.listen(PORT, () => {
    console.log('App v' + VERSION + ' listening on port ' + PORT);
});
''')

    # 4. Start v1 with PM2 on port 3000
    print("Starting v1 with PM2...")
    run_cmd("pm2 delete all 2>/dev/null; true")
    run_cmd("PORT=3000 pm2 start /opt/app-v1/server.js --name app-v1")
    run_cmd("pm2 save", check=False)
    time.sleep(2)

    # Verify v1 is running
    result = run_cmd("curl -s http://localhost:3000/health", check=False)
    print(f"  v1 health check: {result.stdout.strip()}")

    # 5. Configure Nginx as reverse proxy pointing ONLY to port 3000
    print("Configuring Nginx...")
    nginx_config = """upstream nodejs_app {
    server 127.0.0.1:3000;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        proxy_pass http://nodejs_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
"""
    # Write nginx config via a temp file + sudo cp to handle permissions
    Path("/tmp/nodejs-app-nginx.conf").write_text(nginx_config)
    sudo("cp /tmp/nodejs-app-nginx.conf /etc/nginx/sites-available/nodejs-app")

    sudo("rm -f /etc/nginx/sites-enabled/default", check=False)
    sudo("ln -sf /etc/nginx/sites-available/nodejs-app /etc/nginx/sites-enabled/nodejs-app")
    sudo("nginx -t")
    sudo("systemctl restart nginx")
    time.sleep(1)

    # Verify Nginx proxy works
    result = run_cmd("curl -s http://localhost/health", check=False)
    print(f"  Nginx proxy health: {result.stdout.strip()}")

    # 6. Enable passwordless sudo for user (agent needs sudo for deployment tasks)
    sudo("bash -c \"echo 'user ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/user-nopasswd\"")
    sudo("chmod 440 /etc/sudoers.d/user-nopasswd")

    # 7. Ensure /usr/local/bin/deploy_nodejs.sh does NOT exist (negative constraint)
    sudo("rm -f /usr/local/bin/deploy_nodejs.sh", check=False)

    print("=== Initial setup complete ===")
    print("  v1 running on port 3000 via PM2")
    print("  v2 code ready at /opt/app-v2/")
    print("  Nginx upstream points to port 3000 only")
    print("  No deployment script exists yet")

    # 7. Open a terminal for the task (GUI-ready state)
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
