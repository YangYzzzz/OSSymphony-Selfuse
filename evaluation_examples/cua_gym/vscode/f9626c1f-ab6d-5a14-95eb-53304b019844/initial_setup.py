"""
Initial Setup: Re-indent messy.html using VSCode format document
Task ID: vscode_edit_061
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_061'
DESKTOP = '/home/user/Desktop'
OUTPUT = f'{DESKTOP}/messy.html'

VSCODE_USER = '/home/user/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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


def setup_vscode_settings():
    """Configure VSCode to use 4-space indentation."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    settings.update({
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "editor.detectIndentation": False,
        "[html]": {
            "editor.tabSize": 4,
            "editor.insertSpaces": True
        }
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings updated: {SETTINGS_PATH}')


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    # A 45-line HTML file with inconsistent indentation:
    # - some lines use tabs
    # - some lines use 2 spaces
    # - some lines use 4 spaces
    # - some lines have no indentation
    messy_html = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Online Bookstore - Featured Titles</title>
	<link rel="stylesheet" href="styles.css">
    <link rel="icon" href="favicon.ico">
</head>
<body>
<header>
  <nav>
    <ul>
            <li><a href="/">Home</a></li>
      <li><a href="/catalog">Catalog</a></li>
	<li><a href="/about">About Us</a></li>
            <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>
<main>
    <section class="featured">
    <h1>Featured Books This Month</h1>
      <article class="book-card">
    <h2>The Midnight Library</h2>
        <p class="author">by Matt Haig</p>
      <p class="description">Between life and death there is a library. In this library, the shelves go on forever.</p>
	<span class="price">$14.99</span>
      </article>
      <article class="book-card">
        <h2>Educated</h2>
      <p class="author">by Tara Westover</p>
	<p class="description">A memoir about a young woman who grows up in a survivalist family and educates herself.</p>
        <span class="price">$16.99</span>
  </article>
  </section>
  <aside class="sidebar">
    <h3>Categories</h3>
<ul>
      <li>Fiction</li>
      	<li>Non-Fiction</li>
	<li>Science</li>
    <li>History</li>
    </ul>
  </aside>
</main>
<footer>
<p>&copy; 2025 Online Bookstore. All rights reserved.</p>
</footer>
</body>
</html>
"""

    with open(OUTPUT, 'w') as f:
        f.write(messy_html)

    print(f'Initial file created: {OUTPUT}')

    # Configure VSCode settings first
    setup_vscode_settings()

    # GUI-ready startup: open VSCode with the messy.html file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
