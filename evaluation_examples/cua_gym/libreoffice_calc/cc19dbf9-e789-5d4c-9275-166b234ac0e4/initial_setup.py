"""
Initial Setup: Foundation Models Paper Collection Task
Task ID: osworld_multi_apps_web_papers_015
Domain: libreoffice_calc (multi-app: also uses LibreOffice Writer and Chrome)

Initial state: Empty desktop with Chrome, LibreOffice Calc, and LibreOffice Writer installed.
The agent needs to research and collect papers from ArXiv, Papers With Code, and ICML 2024,
build a Calc spreadsheet database and a Writer APA reference list.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_015'
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
    # Ensure Documents directory exists (standard location for output files)
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    print(f'Documents directory ensured: {DOCUMENTS_DIR}')

    # The task starts from a clean desktop — no pre-existing task files.
    # The agent must collect papers by browsing the web and then create:
    #   - /home/user/Documents/foundation_models_db.ods
    #   - /home/user/Documents/foundation_models_refs.odt

    # GUI-ready startup: open Chrome with ArXiv as a starting point,
    # and open blank LibreOffice Calc and Writer windows for the agent to use.
    # Launch Chrome first pointing to ArXiv cs.AI
    launch_gui(
        'google-chrome --new-window "https://arxiv.org/search/?searchtype=all&query=foundation+model+survey&start=0"',
        delay_sec=2.0,
    )

    # Open a blank LibreOffice Calc for the agent to build the database
    launch_gui('libreoffice --calc', delay_sec=2.0)

    # Open a blank LibreOffice Writer for the agent to build the reference list
    launch_gui('libreoffice --writer', delay_sec=1.5)

    print('GUI_READY: launched Chrome (ArXiv), LibreOffice Calc, and LibreOffice Writer with DISPLAY=:0')


create_initial()
