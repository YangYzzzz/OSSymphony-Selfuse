"""
Initial Setup: Create a blank document and professors CSV for mail merge task.
Task ID: writer_mt_044
Domain: libreoffice_writer
"""

import csv
import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_044'
OUTPUT_DOCX = f'{WORKDIR}/{TASK_ID}.docx'
DESKTOP = f'{WORKDIR}/Desktop'
CSV_PATH = f'{DESKTOP}/professors.csv'


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

    # --- Create the professors CSV with 10 records ---
    professors = [
        ['ProfessorName', 'Department', 'University', 'EmailAddress'],
        ['Dr. Sarah Chen', 'Computer Science', 'Stanford University', 's.chen@stanford.edu'],
        ['Dr. Marcus Johnson', 'Electrical Engineering', 'MIT', 'm.johnson@mit.edu'],
        ['Dr. Elena Rodriguez', 'Mathematics', 'UC Berkeley', 'e.rodriguez@berkeley.edu'],
        ['Dr. James Whitfield', 'Physics', 'Caltech', 'j.whitfield@caltech.edu'],
        ['Dr. Priya Sharma', 'Biomedical Engineering', 'Johns Hopkins University', 'p.sharma@jhu.edu'],
        ['Dr. Robert Kim', 'Chemistry', 'University of Chicago', 'r.kim@uchicago.edu'],
        ['Dr. Amanda Foster', 'Neuroscience', 'Columbia University', 'a.foster@columbia.edu'],
        ['Dr. David Nakamura', 'Mechanical Engineering', 'Georgia Tech', 'd.nakamura@gatech.edu'],
        ['Dr. Catherine Walsh', 'Economics', 'Harvard University', 'c.walsh@harvard.edu'],
        ['Dr. Michael Torres', 'Environmental Science', 'Yale University', 'm.torres@yale.edu'],
    ]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(professors)
    print(f'CSV created: {CSV_PATH}')

    # --- Create a blank document ---
    doc = Document()
    doc.save(OUTPUT_DOCX)
    print(f'Blank document created: {OUTPUT_DOCX}')

    # --- Launch LibreOffice Writer with the blank document ---
    launch_gui(f'libreoffice --writer "{OUTPUT_DOCX}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
