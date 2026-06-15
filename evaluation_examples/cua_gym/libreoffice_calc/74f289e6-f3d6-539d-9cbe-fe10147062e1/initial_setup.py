"""
Initial Setup: Faculty hiring trends analysis task
Task ID: osworld_multi_apps_web_faculty_013
Domain: libreoffice_calc

This script prepares the initial state for the task:
- Opens Chrome on the MIT CSAIL news page
- Opens LibreOffice Calc with a blank workbook
- No faculty analysis file exists yet (agent must create it by browsing web)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_faculty_013'
# The agent will create new_faculty_analysis.ods from scratch
TARGET_FILE = f'{WORKDIR}/new_faculty_analysis.ods'

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
    # Remove any existing analysis file so the agent starts fresh
    if os.path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)

    # Create a scratch/notes file to hint the agent about the task context
    # (This is NOT the output file - just a helper reference document)
    notes_path = f'{WORKDIR}/faculty_research_notes.txt'
    with open(notes_path, 'w') as f:
        f.write("""Faculty Hiring Analysis - Research Notes
==========================================

Task: Analyze faculty hiring trends at top CS departments (2020-2024)
Output file: new_faculty_analysis.ods

Departments to check:
1. MIT CSAIL: https://www.csail.mit.edu/news
2. Stanford CS: https://cs.stanford.edu/news
3. CMU SCS: https://www.scs.cmu.edu/news
4. Berkeley EECS: https://eecs.berkeley.edu/news/

Data to collect per faculty:
- Name
- Hired_By (MIT/Stanford/CMU/Berkeley)
- Joined_Year (2020-2024)
- PhD_Institution
- Research_Area

Output sheets needed:
- Sheet 1: Raw faculty data (Name, Hired_By, Joined_Year, PhD_Institution, Research_Area)
- Sheet 2: PhD feeder analysis (PhD_Institution, Count, Percentage)
- Sheet 3: Research area frequency table
""")

    print(f'Notes file created: {notes_path}')

    # Launch Chrome on the MIT CSAIL news page first
    launch_gui(
        'google-chrome --new-window "https://www.csail.mit.edu/news"',
        delay_sec=3.0
    )
    print('GUI_READY: launched Chrome on MIT CSAIL news page with DISPLAY=:0')

    # Launch LibreOffice Calc with a new empty spreadsheet
    launch_gui(
        'libreoffice --calc',
        delay_sec=2.0
    )
    print('GUI_READY: launched LibreOffice Calc (empty) with DISPLAY=:0')

create_initial()
