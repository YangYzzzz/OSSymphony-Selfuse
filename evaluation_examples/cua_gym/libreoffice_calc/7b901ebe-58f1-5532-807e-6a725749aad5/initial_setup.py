"""
Initial Setup: Multi-source paper database comparing model efficiency approaches
Task ID: osworld_multi_apps_web_papers_013
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Sets up:
- Chrome browser open to ArXiv search for model pruning
- An empty LibreOffice Calc spreadsheet ready for data entry
- No efficiency_papers.ods exists yet (agent creates it)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_013'
DESKTOP = '/home/user/Desktop'

# The agent will create efficiency_papers.ods on Desktop
# Initial state: NO pre-existing efficiency_papers.ods
TARGET_FILE = f'{DESKTOP}/efficiency_papers.ods'


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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing efficiency_papers.ods to ensure clean state
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)
        print(f'Removed pre-existing file: {TARGET_FILE}')

    # Also remove any .xlsx variant
    xlsx_variant = f'{DESKTOP}/efficiency_papers.xlsx'
    if os.path.exists(xlsx_variant):
        os.remove(xlsx_variant)

    print(f'Initial state: No efficiency_papers.ods on Desktop (agent will create it)')
    print(f'Desktop path: {DESKTOP}')

    # Launch Chrome with ArXiv model pruning search as starting point
    launch_gui(
        'google-chrome "https://arxiv.org/search/?searchtype=all&query=model+pruning"',
        delay_sec=3.0
    )
    print('Launched Chrome with ArXiv model pruning search')

    # Launch LibreOffice Calc (blank spreadsheet for the agent to work with)
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('Launched LibreOffice Calc (blank)')

    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')


create_initial()
