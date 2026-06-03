"""
Initial Setup: Create a user snippet for JavaScript that generates a console.log statement
Task ID: vscode_code_014
Domain: vs_code

Pre-task state:
- VSCode is open
- No custom JavaScript user snippets exist (javascript.json should NOT be present)
- A sample JS workspace file is open so the agent can see a .js file context
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_014'
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
JS_SNIPPET_PATH = os.path.join(SNIPPETS_DIR, 'javascript.json')
WORKSPACE_DIR = os.path.join(HOME, 'workspace_js')
SAMPLE_JS_FILE = os.path.join(WORKSPACE_DIR, 'app.js')


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
    # 1. Ensure snippets directory exists (but remove any existing javascript.json)
    os.makedirs(SNIPPETS_DIR, exist_ok=True)

    # Remove any pre-existing javascript.json snippet so the initial state is clean
    if os.path.exists(JS_SNIPPET_PATH):
        os.remove(JS_SNIPPET_PATH)
        print(f'Removed pre-existing snippet: {JS_SNIPPET_PATH}')

    # 2. Create a sample JavaScript workspace for context
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    with open(SAMPLE_JS_FILE, 'w') as f:
        f.write("""// Sample JavaScript application
// This file is provided as context for the snippet task.

function greet(name) {
    // TODO: Add logging here using a snippet
    return `Hello, ${name}!`;
}

function calculateTotal(items) {
    let total = 0;
    for (const item of items) {
        total += item.price * item.quantity;
    }
    return total;
}

const products = [
    { name: 'Widget A', price: 29.99, quantity: 3 },
    { name: 'Widget B', price: 14.50, quantity: 7 },
    { name: 'Widget C', price: 49.99, quantity: 2 },
];

const total = calculateTotal(products);
greet('World');
""")
    print(f'Created sample JS file: {SAMPLE_JS_FILE}')

    # 3. GUI-ready startup: open VSCode with the JS workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
