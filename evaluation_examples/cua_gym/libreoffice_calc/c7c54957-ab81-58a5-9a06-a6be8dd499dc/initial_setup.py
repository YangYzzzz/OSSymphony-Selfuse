"""
Initial Setup: Install and configure Nginx as a reverse proxy for Node.js app
Task ID: os_adm_001
Domain: os (system administration)

Creates:
- A simple Node.js HTTP server on port 3000 (simulated)
- Ensures Nginx is NOT installed
- Opens a terminal for the user
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_adm_001'


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


SUDO_PASS = "password"

def run_cmd(cmd, check=False):
    """Run a shell command and return the result."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"stderr: {result.stderr}")
    return result

def run_sudo(cmd, check=False):
    """Run a command with sudo, piping in the password."""
    full_cmd = f"echo '{SUDO_PASS}' | sudo -S {cmd}"
    return run_cmd(full_cmd, check=check)


def create_initial():
    # --- Step 1: Create a simple Node.js app that listens on port 3000 ---
    app_dir = f"{WORKDIR}/node-app"
    os.makedirs(app_dir, exist_ok=True)

    # Create a Python-based HTTP server simulating a Node.js app on port 3000
    server_script = '''\
import http.server
import socketserver

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Welcome to My Node.js App</h1><p>Running on port 3000</p></body></html>')
    def log_message(self, format, *args):
        pass  # Suppress logging

with socketserver.TCPServer(("127.0.0.1", 3000), MyHandler) as httpd:
    httpd.serve_forever()
'''
    Path(f"{app_dir}/server.py").write_text(server_script)

    # Create a package.json to make it look like a Node.js project
    package_json = """\
{
    "name": "my-node-app",
    "version": "1.0.0",
    "description": "Sample Node.js application for reverse proxy setup",
    "main": "app.js",
    "scripts": {
        "start": "node app.js"
    }
}
"""
    Path(f"{app_dir}/package.json").write_text(package_json)

    print(f"Node.js app directory created at {app_dir}/")

    # --- Step 2: Start the app on port 3000 in the background ---
    # Kill any existing process on port 3000 first
    run_cmd("fuser -k 3000/tcp 2>/dev/null || true")
    time.sleep(0.5)

    # Start the simulated app in background
    subprocess.Popen(
        ["python3", f"{app_dir}/server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)

    # Verify the app is running
    result = run_cmd("curl -s http://localhost:3000/")
    if "Node.js App" in result.stdout:
        print("App is running on port 3000")
    else:
        print(f"Warning: App may not be running on port 3000. curl output: {result.stdout[:200]}")

    # --- Step 3: Ensure Nginx is NOT installed ---
    # Check if nginx is installed and remove it if so
    check = run_cmd("dpkg -l nginx 2>/dev/null | grep '^ii'")
    if check.returncode == 0 and 'nginx' in check.stdout:
        print("Nginx found installed, removing...")
        run_sudo("apt-get remove --purge -y nginx nginx-common nginx-core 2>/dev/null")
        run_sudo("apt-get autoremove -y 2>/dev/null")
        # Clean up any leftover config files
        run_sudo("rm -rf /etc/nginx 2>/dev/null")
        print("Nginx removed.")
    else:
        print("Nginx is not installed (expected initial state).")

    # --- Step 4: Open a terminal for the user ---
    launch_gui('gnome-terminal', delay_sec=1.5)
    print("GUI_READY: launched terminal with DISPLAY=:0")


create_initial()
