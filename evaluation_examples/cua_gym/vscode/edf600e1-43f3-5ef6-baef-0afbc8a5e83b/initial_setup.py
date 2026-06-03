"""
Initial Setup: Create a snippet for CSS that generates a flexbox container layout.
Task ID: vscode_code_019
Domain: vs_code

Initial state: VSCode is open with no CSS snippets.
The css.json snippets file must not exist (or be empty) so the agent can create it.
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
CSS_SNIPPET_PATH = os.path.join(SNIPPETS_DIR, 'css.json')
WORKSPACE_DIR = os.path.join(HOME, 'css_project')
SAMPLE_CSS = os.path.join(WORKSPACE_DIR, 'style.css')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Ensure snippets directory exists
    os.makedirs(SNIPPETS_DIR, exist_ok=True)

    # Remove any existing CSS snippets to ensure clean initial state
    # (the agent must create the snippet from scratch)
    if os.path.exists(CSS_SNIPPET_PATH):
        os.remove(CSS_SNIPPET_PATH)
        print(f'Removed existing CSS snippet: {CSS_SNIPPET_PATH}')

    # Write an empty CSS snippets file to make it clear there are no snippets
    with open(CSS_SNIPPET_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Created empty CSS snippets file: {CSS_SNIPPET_PATH}')

    # Create a sample CSS workspace for the agent to work in
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    css_content = """/* style.css - Web App Styles */

/* Navigation */
nav {
    background-color: #2c3e50;
    padding: 1rem 2rem;
    color: white;
}

nav ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

nav li {
    display: inline-block;
    margin-right: 1.5rem;
}

/* Main content area */
.main-content {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Card component */
.card {
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.75rem;
}

/* Button styles */
.btn {
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    transition: background-color 0.2s;
}

.btn-primary {
    background-color: #3498db;
    color: white;
}

.btn-primary:hover {
    background-color: #2980b9;
}

.btn-secondary {
    background-color: #95a5a6;
    color: white;
}

/* Typography */
h1 { font-size: 2rem; color: #2c3e50; }
h2 { font-size: 1.5rem; color: #34495e; }
h3 { font-size: 1.2rem; color: #34495e; }

p {
    line-height: 1.6;
    color: #555;
}

/* Form elements */
input, textarea, select {
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    padding: 0.5rem 0.75rem;
    width: 100%;
}

input:focus, textarea:focus {
    border-color: #3498db;
    outline: none;
}
"""
    with open(SAMPLE_CSS, 'w') as f:
        f.write(css_content)
    print(f'Created sample CSS file: {SAMPLE_CSS}')

    # GUI-ready startup: Open VSCode with the CSS project
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    # Also open the sample CSS file directly
    launch_gui(f'code "{SAMPLE_CSS}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
