"""
Initial Setup: Browse ACL Anthology ACL 2023 and record LLM-related papers in Calc
Task ID: osworld_multi_apps_web_papers_006
Domain: libreoffice_calc

Initial state:
- Documents folder exists
- No 'acl2023_llm_papers.ods' file in Documents (agent must create it)
- Chrome opened to ACL Anthology ACL 2023 page
- LibreOffice Calc opened (blank, ready for data entry)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_006'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
TARGET_FILE = f'{DOCUMENTS_DIR}/acl2023_llm_papers.ods'
ACL_URL = 'https://aclanthology.org/events/acl-2023/'


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
    # Ensure Documents directory exists
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    print(f'Documents directory ready: {DOCUMENTS_DIR}')

    # Remove any pre-existing output file to ensure clean initial state
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)
        print(f'Removed pre-existing file: {TARGET_FILE}')
    else:
        print(f'No pre-existing file found (clean state): {TARGET_FILE}')

    # GUI-ready startup:
    # 1. Open Chrome to ACL Anthology ACL 2023 page
    launch_gui(f'google-chrome --new-window "{ACL_URL}"', delay_sec=3.0)
    print(f'GUI_READY: Chrome opened at {ACL_URL}')

    # 2. Open LibreOffice Calc (blank, ready for agent to enter data)
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: LibreOffice Calc opened (blank)')

    print(f'Initial setup complete. Agent should:')
    print(f'  1. Browse ACL Anthology ACL 2023 for LLM-related papers')
    print(f'  2. Record Title, Authors, Anthology_URL in LibreOffice Calc')
    print(f'  3. Save as {TARGET_FILE}')


setup_initial()
