"""
Initial Setup: Navigate Chrome to httpbin.org/get, take screenshot, save to Desktop
Task ID: osworld_multi_apps_sys_browser_os_003
Domain: os / chrome
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_browser_os_003'
DESKTOP = f'{WORKDIR}/Desktop'
SCREENSHOT_PATH = f'{DESKTOP}/httpbin_screenshot.png'


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


def setup_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Ensure any pre-existing screenshot is removed (task requires agent to create it)
    if os.path.isfile(SCREENSHOT_PATH):
        os.remove(SCREENSHOT_PATH)
        print(f'Removed pre-existing screenshot: {SCREENSHOT_PATH}')

    # Check available screenshot tools
    for tool in ['scrot', 'gnome-screenshot', 'import']:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'Screenshot tool available: {tool} at {result.stdout.strip()}')
            break
    else:
        print('Warning: No screenshot tool (scrot/gnome-screenshot/import) found in PATH.')

    print(f'Initial state prepared. Desktop: {DESKTOP}')
    print(f'No screenshot exists yet at: {SCREENSHOT_PATH}')

    # Launch Chrome with a neutral/default page (not httpbin.org)
    # The agent must navigate to httpbin.org/get and take the screenshot
    launch_gui('google-chrome --new-window "https://www.google.com"', delay_sec=3.0)
    print('GUI_READY: launched Chrome with DISPLAY=:0')


setup_initial()
