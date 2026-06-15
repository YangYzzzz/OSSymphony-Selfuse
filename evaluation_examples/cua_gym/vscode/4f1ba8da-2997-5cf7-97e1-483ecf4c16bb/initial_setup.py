"""
Initial Setup: Emmet abbreviation expansion in VSCode HTML file
Task ID: vscode_prod_046
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_046'
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

    # Basic HTML boilerplate with NO navigation structure
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Riverside Cafe - Home</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Welcome to Riverside Cafe</h1>
        <p>Serving artisan coffee and fresh pastries since 2018</p>
    </header>

    <main>
        <section>
            <h2>Our Story</h2>
            <p>Nestled along the riverbank in downtown Portland, Riverside Cafe has been
            a beloved gathering spot for locals and visitors alike. Our commitment to
            sourcing ethically grown beans and locally baked goods sets us apart.</p>
        </section>

        <section>
            <h2>Hours of Operation</h2>
            <p>Monday - Friday: 6:30 AM - 7:00 PM</p>
            <p>Saturday - Sunday: 8:00 AM - 5:00 PM</p>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Riverside Cafe. All rights reserved.</p>
    </footer>
</body>
</html>
"""

    # Create a basic CSS file to make the project realistic
    css_content = """/* Riverside Cafe - Main Stylesheet */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', serif;
    line-height: 1.6;
    color: #333;
    background-color: #faf8f5;
}

header {
    background-color: #5b3a29;
    color: #fff;
    padding: 2rem;
    text-align: center;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

main {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}

section {
    margin-bottom: 2rem;
}

h2 {
    color: #5b3a29;
    margin-bottom: 0.5rem;
}

footer {
    text-align: center;
    padding: 1rem;
    background-color: #eee;
    margin-top: 2rem;
}
"""

    with open(OUTPUT, 'w') as f:
        f.write(html_content)
    print(f'Initial file created: {OUTPUT}')

    with open(f'{PROJECT_DIR}/styles.css', 'w') as f:
        f.write(css_content)
    print(f'CSS file created: {PROJECT_DIR}/styles.css')

    # Open VSCode with the project folder and the index.html file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
