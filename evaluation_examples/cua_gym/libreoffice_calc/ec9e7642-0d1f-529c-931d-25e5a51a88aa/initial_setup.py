"""
Initial Setup: Search Semantic Scholar for RAG papers and record in Calc
Task ID: osworld_multi_apps_web_papers_010
Domain: libreoffice_calc

Initial state:
- Chrome is open with Semantic Scholar search for 'retrieval augmented generation'
- LibreOffice Calc is open with a new empty spreadsheet
- No rag_papers.ods file exists on the Desktop yet
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_010'
DESKTOP = f'{WORKDIR}/Desktop'


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


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing rag_papers file to start fresh
    for ext in ['ods', 'xlsx', 'csv']:
        target = os.path.join(DESKTOP, f'rag_papers.{ext}')
        if os.path.exists(target):
            os.remove(target)
            print(f'Removed pre-existing: {target}')

    print(f'Desktop directory ready: {DESKTOP}')
    print('No rag_papers file pre-exists (agent must create it)')

    # GUI-ready startup:
    # 1. Open Chrome with Semantic Scholar search for retrieval augmented generation
    search_url = (
        'https://www.semanticscholar.org/search'
        '?q=retrieval+augmented+generation'
        '&sort=Relevance'
        '&year=2022-2024'
    )
    launch_gui(f'google-chrome --new-window "{search_url}"', delay_sec=3.0)

    # 2. Open LibreOffice Calc with a new empty spreadsheet
    launch_gui('libreoffice --calc --norestore', delay_sec=2.0)

    print('GUI_READY: launched Chrome (Semantic Scholar) and LibreOffice Calc with DISPLAY=:0')


create_initial()
