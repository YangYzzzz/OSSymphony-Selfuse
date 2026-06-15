"""
Initial Setup: NeurIPS decade analysis task
Task ID: osworld_multi_apps_web_conference_015
Domain: multi_apps (libreoffice_calc + libreoffice_writer + chrome)

This task requires the agent to:
1. Research NeurIPS conference data (2015-2024) using Chrome
2. Create neurips_decade.ods with Data sheet and Chart sheet
3. Write neurips_evolution_essay.odt (~500 words) in Documents

Initial state: Chrome and LibreOffice are open and ready for use.
No pre-existing task files exist (agent must create them from scratch).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_conference_015'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'


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
    # Ensure Documents directory exists
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Remove any pre-existing task artifacts to ensure clean state
    for fname in [
        f'{WORKDIR}/neurips_decade.ods',
        f'{WORKDIR}/neurips_decade.xlsx',
        f'{DOCUMENTS_DIR}/neurips_evolution_essay.odt',
        f'{DOCUMENTS_DIR}/neurips_evolution_essay.docx',
    ]:
        if os.path.exists(fname):
            os.remove(fname)
            print(f'Removed pre-existing file: {fname}')

    print(f'Initial state ready: Documents dir exists at {DOCUMENTS_DIR}')
    print('No pre-existing task files — agent must research and create them.')

    # Open Chrome pointing to NeurIPS conference page for easy research
    launch_gui(
        'google-chrome --new-window "https://nips.cc/Conferences/"',
        delay_sec=3.0
    )

    # Open a blank LibreOffice Calc spreadsheet for the agent to use
    launch_gui(
        'libreoffice --calc',
        delay_sec=2.0
    )

    # Open a blank LibreOffice Writer document for the essay
    launch_gui(
        'libreoffice --writer',
        delay_sec=2.0
    )

    print('GUI_READY: Chrome (NeurIPS page), LibreOffice Calc, and LibreOffice Writer launched with DISPLAY=:0')


create_initial()
