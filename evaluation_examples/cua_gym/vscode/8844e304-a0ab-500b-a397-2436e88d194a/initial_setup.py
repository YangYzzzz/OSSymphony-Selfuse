"""
Initial Setup: Create styles.css with 3-digit hex shorthand color codes
Task ID: vscode_gs_066
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_066'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
OUTPUT = f'{PROJECT_DIR}/styles.css'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic styles.css with 3-digit hex shorthand codes
    css_content = """/* Main Stylesheet for WebApp */
/* Author: Frontend Team */
/* Last updated: 2025-11-20 */

:root {
    --primary-color: #336699;
    --text-dark: #000;
    --accent-magenta: #f0f;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-dark);
    background-color: #fff;
}

header {
    background-color: var(--primary-color);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

header h1 {
    color: #fff;
    font-size: 1.8rem;
    font-weight: 600;
}

nav a {
    color: #f5f5f5;
    text-decoration: none;
    margin-left: 1.5rem;
    transition: opacity 0.3s ease;
}

nav a:hover {
    opacity: 0.8;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-title {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.btn-primary {
    background-color: var(--primary-color);
    color: #f9f9f9;
    padding: 0.5rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn-primary:hover {
    filter: brightness(1.1);
}

.highlight {
    border-left: 4px solid var(--accent-magenta);
    padding-left: 1rem;
}

footer {
    text-align: center;
    padding: 2rem;
    color: #666;
    font-size: 0.9rem;
}
"""
    with open(OUTPUT, 'w') as f:
        f.write(css_content)
    print(f'Initial file created: {OUTPUT}')

    # Also create a basic index.html so the project looks realistic
    index_path = f'{PROJECT_DIR}/index.html'
    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebApp</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>WebApp</h1>
        <nav>
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
        </nav>
    </header>
    <div class="container">
        <div class="card">
            <h2 class="card-title">Welcome</h2>
            <p>This is the main content area.</p>
            <button class="btn-primary">Get Started</button>
        </div>
    </div>
    <footer>
        <p>&copy; 2025 WebApp. All rights reserved.</p>
    </footer>
</body>
</html>
"""
    with open(index_path, 'w') as f:
        f.write(index_content)
    print(f'Supporting file created: {index_path}')

    # Launch VSCode with the project folder, opening styles.css
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
