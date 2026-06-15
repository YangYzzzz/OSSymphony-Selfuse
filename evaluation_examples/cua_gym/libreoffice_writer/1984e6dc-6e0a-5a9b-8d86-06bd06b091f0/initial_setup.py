"""
Initial Setup: Register CSV as data source for mail merge
Task ID: writer_mt_002
Domain: libreoffice_writer

Creates:
  - /home/user/Desktop/employees.csv with 20 rows of employee data
  - /home/user/writer_mt_002.docx blank document
  - Opens LibreOffice Writer with the blank document
"""

import csv
import os
import shlex
import subprocess
import time

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_002'
DESKTOP = f'{WORKDIR}/Desktop'
CSV_PATH = f'{DESKTOP}/employees.csv'
DOC_PATH = f'{WORKDIR}/{TASK_ID}.docx'


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


def create_csv():
    """Create employees.csv with 20 rows of realistic employee data."""
    os.makedirs(DESKTOP, exist_ok=True)

    employees = [
        ["EmployeeID", "FirstName", "LastName", "Department", "Email"],
        ["E001", "Sarah", "Chen", "Engineering", "sarah.chen@acmecorp.com"],
        ["E002", "Marcus", "Johnson", "Marketing", "marcus.johnson@acmecorp.com"],
        ["E003", "Priya", "Patel", "Finance", "priya.patel@acmecorp.com"],
        ["E004", "James", "O'Brien", "Engineering", "james.obrien@acmecorp.com"],
        ["E005", "Aiko", "Tanaka", "Human Resources", "aiko.tanaka@acmecorp.com"],
        ["E006", "David", "Kim", "Sales", "david.kim@acmecorp.com"],
        ["E007", "Elena", "Rodriguez", "Marketing", "elena.rodriguez@acmecorp.com"],
        ["E008", "Michael", "Foster", "Engineering", "michael.foster@acmecorp.com"],
        ["E009", "Fatima", "Al-Hassan", "Finance", "fatima.alhassan@acmecorp.com"],
        ["E010", "Robert", "Williams", "Operations", "robert.williams@acmecorp.com"],
        ["E011", "Lisa", "Martinez", "Human Resources", "lisa.martinez@acmecorp.com"],
        ["E012", "Thomas", "Anderson", "Sales", "thomas.anderson@acmecorp.com"],
        ["E013", "Mei", "Wong", "Engineering", "mei.wong@acmecorp.com"],
        ["E014", "Carlos", "Gutierrez", "Marketing", "carlos.gutierrez@acmecorp.com"],
        ["E015", "Sophie", "Laurent", "Finance", "sophie.laurent@acmecorp.com"],
        ["E016", "Daniel", "Nguyen", "Operations", "daniel.nguyen@acmecorp.com"],
        ["E017", "Rachel", "Thompson", "Sales", "rachel.thompson@acmecorp.com"],
        ["E018", "Ahmed", "Khalil", "Engineering", "ahmed.khalil@acmecorp.com"],
        ["E019", "Julia", "Schneider", "Human Resources", "julia.schneider@acmecorp.com"],
        ["E020", "Kevin", "Park", "Marketing", "kevin.park@acmecorp.com"],
    ]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(employees)

    print(f'CSV created: {CSV_PATH} ({len(employees) - 1} rows)')


def create_blank_doc():
    """Create a blank Writer document."""
    doc = Document()
    doc.save(DOC_PATH)
    print(f'Blank document created: {DOC_PATH}')


def main():
    create_csv()
    create_blank_doc()

    # Open LibreOffice Writer with the blank document
    launch_gui(f'libreoffice --writer "{DOC_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


main()
