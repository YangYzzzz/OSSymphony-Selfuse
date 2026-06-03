"""
Initial Setup: Create HTML file with three <li> elements not wrapped in a list container.
Open VSCode with the file and select the three <li> lines.
Task ID: vscode_lp_027
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_027'
OUTPUT = f'{WORKDIR}/{TASK_ID}.html'

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Navigation</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="main-header">
        <h1>Creative Studio</h1>
        <nav class="primary-nav">
            <li>Home</li>
            <li>Projects</li>
            <li>Contact</li>
        </nav>
    </header>
    <main>
        <section class="hero">
            <h2>Welcome to Our Studio</h2>
            <p>We craft beautiful digital experiences for brands worldwide.</p>
        </section>
        <section class="services">
            <h2>Our Services</h2>
            <ul class="service-list">
                <li>Web Design</li>
                <li>Brand Identity</li>
                <li>Mobile Development</li>
            </ul>
        </section>
    </main>
    <footer>
        <p>&copy; 2025 Creative Studio. All rights reserved.</p>
    </footer>
</body>
</html>
'''


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
    # Write the HTML file
    with open(OUTPUT, 'w') as f:
        f.write(HTML_CONTENT)
    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file, going to line 12 (first <li>)
    launch_gui(f'code --goto "{OUTPUT}:12:1"', delay_sec=3.0)

    # Give VSCode time to fully load the file
    time.sleep(2.0)

    # Use xdg-utils or python to send keystrokes for selection
    # Write a small helper script that uses python3-xlib to select lines 12-14
    select_script = '''
import subprocess, time

env_vars = {"DISPLAY": ":0"}

# Use dbus or gdbus to send commands to VSCode is complex.
# Instead, use the 'xte' tool from xautomation if available,
# or write keystrokes via /dev/uinput.
# Simplest: use python3 with Xlib to send key events.

try:
    from Xlib import X, display, XK
    from Xlib.ext.xtest import fake_input

    d = display.Display(":0")

    def press_key(keyname):
        keysym = XK.string_to_keysym(keyname)
        keycode = d.keysym_to_keycode(keysym)
        fake_input(d, X.KeyPress, keycode)
        d.sync()
        time.sleep(0.02)
        fake_input(d, X.KeyRelease, keycode)
        d.sync()
        time.sleep(0.02)

    def press_with_modifier(mod_name, key_name):
        mod_sym = XK.string_to_keysym(mod_name)
        mod_code = d.keysym_to_keycode(mod_sym)
        key_sym = XK.string_to_keysym(key_name)
        key_code = d.keysym_to_keycode(key_sym)
        fake_input(d, X.KeyPress, mod_code)
        d.sync()
        time.sleep(0.02)
        fake_input(d, X.KeyPress, key_code)
        d.sync()
        time.sleep(0.02)
        fake_input(d, X.KeyRelease, key_code)
        d.sync()
        time.sleep(0.02)
        fake_input(d, X.KeyRelease, mod_code)
        d.sync()
        time.sleep(0.05)

    # Go to beginning of line
    press_key("Home")
    time.sleep(0.1)

    # Select 3 lines downward: Shift+Down x3
    for _ in range(3):
        press_with_modifier("Shift_L", "Down")
        time.sleep(0.1)

    print("Lines 12-14 selected via Xlib")
    d.close()
except Exception as e:
    print(f"Xlib selection failed: {e}")
    print("File is open at line 12 - agent can manually select")
'''

    # Write and execute the selection helper
    helper_path = '/tmp/select_lines.py'
    with open(helper_path, 'w') as f:
        f.write(select_script)

    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    result = subprocess.run(
        ['python3', helper_path],
        env=env,
        capture_output=True,
        text=True,
        timeout=10
    )
    print(f'Selection script output: {result.stdout.strip()}')
    if result.stderr.strip():
        print(f'Selection script stderr: {result.stderr.strip()}')

    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
