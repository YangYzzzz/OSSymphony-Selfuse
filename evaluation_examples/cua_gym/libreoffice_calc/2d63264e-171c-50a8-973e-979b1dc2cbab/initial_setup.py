"""
Initial Setup: Install 'Dark Reader' Chrome extension task
Task ID: osworld_multi_apps_ext_install_010
Domain: chrome

Initial state: Chrome is open WITHOUT Dark Reader extension installed.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_ext_install_010'
CHROME_USER_DATA = os.path.expanduser('~/.config/google-chrome')
CHROME_DEFAULT = os.path.join(CHROME_USER_DATA, 'Default')
PREFS_FILE = os.path.join(CHROME_DEFAULT, 'Preferences')
DARK_READER_EXT_ID = 'eimadpbcbfnmbkopoojfekhnkhdbieeh'
EXTENSIONS_DIR = os.path.join(CHROME_DEFAULT, 'Extensions')


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


def ensure_dark_reader_not_installed():
    """Ensure Dark Reader is NOT installed in the initial state."""
    # Remove Dark Reader extension directory if it exists
    dr_ext_dir = os.path.join(EXTENSIONS_DIR, DARK_READER_EXT_ID)
    if os.path.exists(dr_ext_dir):
        import shutil
        shutil.rmtree(dr_ext_dir)
        print(f'Removed existing Dark Reader extension from {dr_ext_dir}')

    # Remove Dark Reader from Preferences if it exists
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, 'r') as f:
            try:
                prefs = json.load(f)
            except json.JSONDecodeError:
                prefs = {}

        ext_settings = prefs.get('extensions', {}).get('settings', {})
        if DARK_READER_EXT_ID in ext_settings:
            del ext_settings[DARK_READER_EXT_ID]
            print(f'Removed Dark Reader from Preferences')
            with open(PREFS_FILE, 'w') as f:
                json.dump(prefs, f)

    print('Initial state verified: Dark Reader is NOT installed.')


def setup_initial():
    """Set up the initial state: Chrome open without Dark Reader."""
    # Kill any running Chrome instances to safely modify files
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    time.sleep(2)

    # Ensure Dark Reader is not installed
    ensure_dark_reader_not_installed()

    # Launch Chrome with remote debugging port (standard OSWorld setup)
    # Open Chrome at a regular website (NOT news.ycombinator.com - agent must navigate there)
    launch_gui(
        'google-chrome --remote-debugging-port=1337 --no-first-run --no-default-browser-check "https://www.google.com"',
        delay_sec=3.0
    )

    print(f'GUI_READY: Chrome launched with DISPLAY=:0 (without Dark Reader)')
    print('Initial state: Chrome open without Dark Reader extension.')


setup_initial()
