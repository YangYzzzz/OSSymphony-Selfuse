"""
Initial Setup: Create index.html with basic HTML template, open in VSCode
Task ID: vscode_web_006
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_006'
PROJECT_DIR = f'{WORKDIR}/projects/website'
OUTPUT = f'{PROJECT_DIR}/index.html'


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

    # Create a realistic index.html with an empty line 10 inside <body>
    # Lines are numbered 1-based:
    # 1:  <!DOCTYPE html>
    # 2:  <html lang="en">
    # 3:  <head>
    # 4:      <meta charset="UTF-8">
    # 5:      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    # 6:      <title>Stellar Design Agency</title>
    # 7:      <link rel="stylesheet" href="styles.css">
    # 8:  </head>
    # 9:  <body>
    # 10: (empty - cursor goes here)
    # 11:
    # 12:     <script src="app.js"></script>
    # 13: </body>
    # 14: </html>

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stellar Design Agency</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

    <!-- Page content will be added above -->
    <script src="app.js"></script>
</body>
</html>
"""

    with open(OUTPUT, 'w') as f:
        f.write(html_content)
    print(f'Initial file created: {OUTPUT}')

    # Also create a basic styles.css and app.js for realism
    css_content = """/* Stellar Design Agency - Main Stylesheet */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 0;
}

main {
    padding: 2rem 0;
}

footer {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 0;
    text-align: center;
}
"""

    js_content = """// Stellar Design Agency - Main Application Script
document.addEventListener('DOMContentLoaded', function() {
    console.log('Stellar Design Agency website loaded');
});
"""

    with open(f'{PROJECT_DIR}/styles.css', 'w') as f:
        f.write(css_content)

    with open(f'{PROJECT_DIR}/app.js', 'w') as f:
        f.write(js_content)

    print(f'Supporting files created in {PROJECT_DIR}')

    # Open VSCode with the project folder and the index.html file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code --goto "{OUTPUT}:10:1"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
