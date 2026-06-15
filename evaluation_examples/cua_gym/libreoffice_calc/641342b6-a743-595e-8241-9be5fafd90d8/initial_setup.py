"""
Initial Setup: Competitive analysis - browse Python, Ruby, Go pages, screenshot each, create ODT table
Task ID: osworld_multi_apps_sys_browser_os_009
Domain: multi_apps (Chrome + OS + LibreOffice Writer)

Initial state:
- Chrome open and ready
- Desktop is writable and clean (no screenshots, no language_comparison.odt)
- scrot is available for the agent to use
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_sys_browser_os_009'

# Files that the agent will create (must NOT pre-exist)
AGENT_OUTPUT_FILES = [
    os.path.join(DESKTOP, 'screenshot_1.png'),
    os.path.join(DESKTOP, 'screenshot_2.png'),
    os.path.join(DESKTOP, 'screenshot_3.png'),
    os.path.join(DESKTOP, 'language_comparison.odt'),
]


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

    # Clean up any pre-existing task output files so initial state is pristine
    for fpath in AGENT_OUTPUT_FILES:
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f'Removed pre-existing file: {fpath}')

    # Verify scrot is available (it should be pre-installed on OSWorld VMs)
    result = subprocess.run(['which', 'scrot'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'scrot is available at: {result.stdout.strip()}')
    else:
        # Try to install scrot
        print('scrot not found, attempting install...')
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'scrot'],
                       capture_output=True, text=True)

    print(f'Desktop path: {DESKTOP}')
    print('Initial state ready: no screenshots, no ODT file on Desktop')

    # GUI-ready startup: open Chrome so agent can start visiting URLs immediately
    launch_gui('google-chrome', delay_sec=2.0)
    print('GUI_READY: Chrome launched with DISPLAY=:0')


setup_initial()
