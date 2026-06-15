"""
Initial Setup: Junior Faculty Comparison - Web Research Task
Task ID: osworld_multi_apps_web_scholar_011
Domain: libreoffice_calc (multi_apps_web)

This script prepares the initial environment for a faculty hiring committee task.
The agent must look up three researchers on DBLP and Google Scholar, compute
publication metrics, and save results to junior_faculty_comparison.ods on Desktop.

Initial state:
  - Chrome browser open (for web research)
  - LibreOffice Calc open (blank new spreadsheet)
  - NO pre-existing junior_faculty_comparison.ods (agent must create it)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_scholar_011'
OUTPUT_FILE = f'{DESKTOP}/junior_faculty_comparison.ods'


def launch_gui(command: str, delay_sec: float = 1.5):
    """Launch a GUI application on the VM display without blocking script exit."""
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

    # Remove any pre-existing comparison file so the agent starts fresh
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f'Removed pre-existing file: {OUTPUT_FILE}')

    # Also remove any .ods files with this name in home directory
    alt_path = f'{WORKDIR}/junior_faculty_comparison.ods'
    if os.path.exists(alt_path):
        os.remove(alt_path)
        print(f'Removed pre-existing file: {alt_path}')

    print('Initial state: Desktop is clean, no comparison file exists.')

    # Launch Chrome for web research (DBLP, Google Scholar)
    launch_gui('google-chrome --new-window "https://dblp.org"', delay_sec=3.0)
    print('GUI_READY: Chrome launched with DBLP homepage')

    # Launch LibreOffice Calc with a blank new spreadsheet
    launch_gui('libreoffice --calc', delay_sec=2.5)
    print('GUI_READY: LibreOffice Calc launched (blank)')

    print('Setup complete. Agent should:')
    print('  1. Use Chrome to search DBLP and Google Scholar for each researcher')
    print('  2. Collect metrics: PhD year, total papers, citations, top venue, H-index')
    print('  3. Create junior_faculty_comparison.ods on Desktop with required columns')


setup_initial()
