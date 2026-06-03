"""
Initial Setup: Open browser to fastbook notebook URL; Desktop clean (no fastai_intro_code.py)
Task ID: osworld_multi_apps_code_to_writer_file_007
Domain: libreoffice_writer / multi-app (browser + writer)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_007'
DESKTOP = f'{WORKDIR}/Desktop'
TARGET_FILE = f'{DESKTOP}/fastai_intro_code.py'
NOTEBOOK_URL = 'https://raw.githubusercontent.com/fastai/fastbook/master/01_intro.ipynb'


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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any existing target file to ensure clean initial state
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)
        print(f'Removed existing file: {TARGET_FILE}')

    print(f'Desktop is clean: no {TARGET_FILE}')

    # GUI-ready startup: open browser at the notebook URL
    # Try chromium-browser first, then firefox as fallback
    browser_launched = False
    for browser_cmd in [
        f'chromium-browser "{NOTEBOOK_URL}"',
        f'google-chrome "{NOTEBOOK_URL}"',
        f'firefox "{NOTEBOOK_URL}"',
        f'xdg-open "{NOTEBOOK_URL}"',
    ]:
        try:
            launch_gui(browser_cmd, delay_sec=2.0)
            browser_launched = True
            print(f'GUI_READY: launched browser with URL: {NOTEBOOK_URL}')
            break
        except Exception as e:
            print(f'Failed to launch {browser_cmd}: {e}')
            continue

    if not browser_launched:
        print('WARNING: Could not launch browser. Agent will need to open it manually.')

    print('Initial state: browser open at notebook URL, Desktop has no fastai_intro_code.py')


create_initial()
