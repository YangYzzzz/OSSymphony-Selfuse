"""
Initial Setup: Visit Papers With Code and record ImageNet SOTA top-10 in a Calc spreadsheet
Task ID: osworld_multi_apps_web_papers_007
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Initial state:
- Desktop is empty (no imagenet_sota.ods file)
- Chrome is open to https://paperswithcode.com/sota
- LibreOffice Calc is open (new blank document)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_007'
DESKTOP = '/home/user/Desktop'

# Ensure Desktop directory exists
os.makedirs(DESKTOP, exist_ok=True)

# Remove any pre-existing output file to ensure clean state
OUTPUT_FILE = os.path.join(DESKTOP, 'imagenet_sota.ods')
if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)
    print(f'Removed pre-existing file: {OUTPUT_FILE}')

def launch_gui(command: str, delay_sec: float = 1.5):
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

print('Setting up initial state...')

# Launch Chrome pointing at Papers With Code SOTA page
launch_gui(
    'google-chrome --new-window "https://paperswithcode.com/sota"',
    delay_sec=3.0
)

# Launch LibreOffice Calc with a new blank document
launch_gui(
    'libreoffice --calc --norestore',
    delay_sec=2.0
)

print(f'Initial state ready: Desktop is empty (no imagenet_sota.ods)')
print('GUI_READY: Chrome opened to https://paperswithcode.com/sota, LibreOffice Calc opened (blank)')
