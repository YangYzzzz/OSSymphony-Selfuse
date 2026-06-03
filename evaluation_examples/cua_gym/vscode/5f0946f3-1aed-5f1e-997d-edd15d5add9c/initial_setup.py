"""
Initial Setup: Set up VSCode with 4 named terminals and empty keybindings.json
Task ID: vscode_rrt_095
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, "keybindings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")


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
    # 1. Create workspace directory with some realistic project files
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a simple full-stack project structure
    os.makedirs(os.path.join(WORKSPACE_DIR, "server"), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE_DIR, "client", "src"), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE_DIR, "database"), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE_DIR, "tests"), exist_ok=True)

    with open(os.path.join(WORKSPACE_DIR, "server", "app.py"), "w") as f:
        f.write("""from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users')
def get_users():
    return jsonify({"users": []})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
""")

    with open(os.path.join(WORKSPACE_DIR, "client", "src", "App.js"), "w") as f:
        f.write("""import React, { useState, useEffect } from 'react';

function App() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetch('/api/users')
            .then(res => res.json())
            .then(data => setUsers(data.users));
    }, []);

    return (
        <div className="App">
            <h1>User Dashboard</h1>
            {users.map(u => <p key={u.id}>{u.name}</p>)}
        </div>
    );
}

export default App;
""")

    with open(os.path.join(WORKSPACE_DIR, "database", "schema.sql"), "w") as f:
        f.write("""CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

    with open(os.path.join(WORKSPACE_DIR, "tests", "test_api.py"), "w") as f:
        f.write("""import unittest
import requests

class TestUserAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:5001'

    def test_get_users(self):
        resp = requests.get(f'{self.BASE_URL}/api/users')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('users', resp.json())

    def test_create_user(self):
        data = {'name': 'Alice', 'email': 'alice@example.com'}
        resp = requests.post(f'{self.BASE_URL}/api/users', json=data)
        self.assertEqual(resp.status_code, 201)

if __name__ == '__main__':
    unittest.main()
""")

    # 2. Set keybindings.json to empty array (initial state: no keybindings)
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(KEYBINDINGS_PATH, "w") as f:
        json.dump([], f, indent=4)
    print(f"Keybindings file created (empty): {KEYBINDINGS_PATH}")

    # 3. Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)

    # 4. Open 4 named terminals using xdotool to send VSCode keyboard shortcuts
    # First, we use VSCode's integrated terminal API via command line
    # We'll create a script that uses xdotool to open terminals
    terminal_script = os.path.join(HOME, "_open_terminals.sh")
    with open(terminal_script, "w") as f:
        f.write("""#!/bin/bash
export DISPLAY=:0

# Wait for VSCode to fully load
sleep 4

# Function to open a new terminal and rename it
open_named_terminal() {
    local name="$1"

    # Open new terminal: Ctrl+Shift+`
    xdotool key ctrl+shift+grave
    sleep 1.5

    # Rename terminal via command palette
    # Open command palette: Ctrl+Shift+P
    xdotool key ctrl+shift+p
    sleep 0.8

    # Type the rename command
    xdotool type --delay 30 "Terminal: Rename"
    sleep 0.8

    # Press Enter to select the command
    xdotool key Return
    sleep 0.8

    # Type the terminal name
    xdotool type --delay 30 "$name"
    sleep 0.3

    # Confirm
    xdotool key Return
    sleep 0.5
}

# Open and name 4 terminals
open_named_terminal "Server"
open_named_terminal "Client"
open_named_terminal "Database"
open_named_terminal "Tests"

echo "All 4 terminals created and named."
""")
    os.chmod(terminal_script, 0o755)

    # Run the terminal creation script in background
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        ["bash", terminal_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )

    print(f"Workspace created at: {WORKSPACE_DIR}")
    print(f"GUI_READY: launched VSCode with DISPLAY=:0")
    print("Terminal creation script launched in background.")


create_initial()
