"""
Initial Setup: Co-authorship analysis for Stanford NLP Group
Task ID: osworld_multi_apps_web_scholar_014
Domain: libreoffice_calc

This task requires the agent to:
1. Visit https://nlp.stanford.edu/people/ to get the faculty list
2. Check DBLP pages for each faculty member
3. Find co-authored papers between Stanford NLP faculty
4. Build a Calc co-authorship matrix and identify frequent collaboration pairs
5. Save result as 'stanford_nlp_coauthorship.ods' on the Desktop

Initial state: Chrome and LibreOffice Calc are available; no pre-existing spreadsheet.
The agent must create the file from scratch using web research.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_scholar_014'


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

    # No pre-existing spreadsheet — the agent must create it from scratch.
    # The task involves web research (Stanford NLP website + DBLP) and then
    # building the co-authorship spreadsheet.

    # Create a simple text reminder on Desktop so the agent knows the target filename
    reminder_path = os.path.join(DESKTOP, 'task_info.txt')
    with open(reminder_path, 'w') as f:
        f.write("Task: Build co-authorship analysis for Stanford NLP Group\n")
        f.write("Steps:\n")
        f.write("1. Visit https://nlp.stanford.edu/people/ for faculty list\n")
        f.write("2. For each faculty, check DBLP page for co-authored papers\n")
        f.write("3. Find papers with 2+ Stanford NLP authors\n")
        f.write("4. Build co-authorship matrix in LibreOffice Calc\n")
        f.write("5. Save as 'stanford_nlp_coauthorship.ods' on Desktop\n")
        f.write("\nTarget file: /home/user/Desktop/stanford_nlp_coauthorship.ods\n")
        f.write("\nSheet 1: Faculty list with DBLP URLs\n")
        f.write("Sheet 2: Co-authorship matrix (faculty names as row/col headers, value = shared paper count)\n")
        f.write("Sheet 3: Sorted collaboration pairs by shared paper count (descending)\n")

    print(f"Task info file created: {reminder_path}")

    # GUI-ready startup: open Chrome at Stanford NLP people page and LibreOffice Calc
    # Open Chrome pointing to the Stanford NLP faculty page
    launch_gui(
        'google-chrome --new-window "https://nlp.stanford.edu/people/"',
        delay_sec=3.0
    )

    # Open a blank LibreOffice Calc for the agent to start building the spreadsheet
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print('GUI_READY: launched Chrome (Stanford NLP page) and LibreOffice Calc with DISPLAY=:0')


create_initial()
