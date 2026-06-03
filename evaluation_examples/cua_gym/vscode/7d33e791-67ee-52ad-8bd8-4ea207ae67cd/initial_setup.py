"""
Initial Setup: Create an HTML project with index.html containing paragraph elements on lines 15-20.
Task ID: vscode_web_007
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_007'
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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic HTML file where lines 15-20 contain <p> elements
    # that are NOT wrapped in <section class="articles">
    # Line count verification:
    #  1: <!DOCTYPE html>
    #  2: <html lang="en">
    #  3: <head>
    #  4:     <meta charset="UTF-8">
    #  5:     <meta name="viewport" ...>
    #  6:     <title>...</title>
    #  7:     <link rel="stylesheet" ...>
    #  8: </head>
    #  9: <body>
    # 10:     <header>
    # 11:         <h1>TechPulse</h1>
    # 12:         <nav><a href="/">Home</a> | <a href="/about">About</a></nav>
    # 13:     </header>
    # 14:     <main>
    # 15:         <p>Breaking: ...</p>
    # 16:         <p>Review: ...</p>
    # 17:         <p>Analysis: ...</p>
    # 18:         <p>Opinion: ...</p>
    # 19:         <p>Guide: ...</p>
    # 20:         <p>Report: ...</p>
    # 21:     </main>
    # ...
    lines = [
        '<!DOCTYPE html>',                                                              # 1
        '<html lang="en">',                                                             # 2
        '<head>',                                                                       # 3
        '    <meta charset="UTF-8">',                                                   # 4
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',   # 5
        '    <title>TechPulse - Latest Technology News</title>',                         # 6
        '    <link rel="stylesheet" href="styles.css">',                                # 7
        '</head>',                                                                      # 8
        '<body>',                                                                       # 9
        '    <header>',                                                                 # 10
        '        <h1>TechPulse</h1>',                                                   # 11
        '        <nav><a href="/">Home</a> | <a href="/about">About</a></nav>',         # 12
        '    </header>',                                                                # 13
        '    <main>',                                                                   # 14
        '        <p>Breaking: New AI Model Achieves Record Performance on Benchmark Tests</p>',      # 15
        '        <p>Review: The Latest Smartphone from Nexora Features a Revolutionary Camera</p>',  # 16
        '        <p>Analysis: How Cloud Computing is Reshaping Enterprise Infrastructure</p>',       # 17
        '        <p>Opinion: Open Source Software Continues to Drive Innovation Across Industries</p>', # 18
        '        <p>Guide: Getting Started with Rust for Systems Programming</p>',                   # 19
        '        <p>Report: Global Semiconductor Shortage Shows Signs of Recovery</p>',              # 20
        '    </main>',                                                                  # 21
        '    <footer>',                                                                 # 22
        '        <p>&copy; 2025 TechPulse. All rights reserved.</p>',                   # 23
        '    </footer>',                                                                # 24
        '</body>',                                                                      # 25
        '</html>',                                                                      # 26
    ]
    html_content = '\n'.join(lines) + '\n'
    with open(OUTPUT, 'w') as f:
        f.write(html_content)

    print(f'Initial file created: {OUTPUT}')

    # Also create a basic CSS file for realism
    css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 960px;
    margin: 0 auto;
    padding: 20px;
}

header {
    border-bottom: 2px solid #2c3e50;
    padding-bottom: 15px;
    margin-bottom: 30px;
}

header h1 {
    color: #2c3e50;
    font-size: 2.4em;
}

nav a {
    margin-right: 15px;
    text-decoration: none;
    color: #3498db;
}

footer {
    margin-top: 40px;
    padding-top: 15px;
    border-top: 1px solid #ccc;
    color: #777;
    font-size: 0.9em;
}
"""
    with open(f'{PROJECT_DIR}/styles.css', 'w') as f:
        f.write(css_content)

    print(f'CSS file created: {PROJECT_DIR}/styles.css')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)

    # Open the specific file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
