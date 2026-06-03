"""
Initial Setup: Desktop file organizer task - creates initial Desktop files
Task ID: osworld_multi_apps_desktop_organizer_014
Domain: os (multi-apps desktop organizer)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'osworld_multi_apps_desktop_organizer_014'


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

    # Remove any previously created task folders if they exist (idempotent reset)
    for folder in ['Work', 'Personal']:
        folder_path = os.path.join(DESKTOP, folder)
        if os.path.exists(folder_path):
            import shutil
            shutil.rmtree(folder_path)

    # Remove file_index.txt if exists (idempotent reset)
    index_path = os.path.join(DESKTOP, 'file_index.txt')
    if os.path.exists(index_path):
        os.remove(index_path)

    # Create the 8 files on the Desktop with realistic dummy content

    # 1. q2_report.docx — a Word document (create as empty binary placeholder using bytes)
    # Using a minimal valid docx-like approach via text file with docx extension
    # to keep it simple and portable; actual content doesn't matter for this OS task
    q2_report = os.path.join(DESKTOP, 'q2_report.docx')
    with open(q2_report, 'wb') as f:
        # Write a minimal placeholder (not a real docx, but sufficient for file organizer task)
        f.write(b'Q2 Financial Report 2025\n\nRevenue: $2,450,000\nExpenses: $1,820,000\nNet Income: $630,000\n')
    print(f'Created: {q2_report}')

    # 2. strategy_2025.pptx — a PowerPoint presentation placeholder
    strategy = os.path.join(DESKTOP, 'strategy_2025.pptx')
    with open(strategy, 'wb') as f:
        f.write(b'Strategic Plan 2025\n\nSlide 1: Executive Summary\nSlide 2: Market Analysis\nSlide 3: Growth Targets\n')
    print(f'Created: {strategy}')

    # 3. expense_tracker.xlsx — a spreadsheet placeholder
    expense = os.path.join(DESKTOP, 'expense_tracker.xlsx')
    with open(expense, 'wb') as f:
        f.write(b'Expense Tracker 2025\n\nDate,Category,Amount\n2025-01-15,Travel,450.00\n2025-01-20,Meals,85.50\n')
    print(f'Created: {expense}')

    # 4. team_photo.jpg — a JPEG image placeholder (minimal JPEG header)
    team_photo = os.path.join(DESKTOP, 'team_photo.jpg')
    with open(team_photo, 'wb') as f:
        # Minimal JPEG magic bytes
        f.write(b'\xff\xd8\xff\xe0' + b'\x00' * 100 + b'\xff\xd9')
    print(f'Created: {team_photo}')

    # 5. personal_journal.txt — a text journal file
    journal = os.path.join(DESKTOP, 'personal_journal.txt')
    with open(journal, 'w') as f:
        f.write('Personal Journal - March 2025\n\n')
        f.write('March 1: Started a new fitness routine today. Feeling motivated!\n')
        f.write('March 5: Visited the local farmers market with friends.\n')
        f.write('March 10: Finished reading "The Midnight Library" - highly recommend.\n')
    print(f'Created: {journal}')

    # 6. sales_presentation.pptx — another PowerPoint placeholder
    sales_ppt = os.path.join(DESKTOP, 'sales_presentation.pptx')
    with open(sales_ppt, 'wb') as f:
        f.write(b'Sales Presentation Q1 2025\n\nSlide 1: Sales Overview\nSlide 2: Regional Breakdown\nSlide 3: Top Performers\n')
    print(f'Created: {sales_ppt}')

    # 7. revenue_model.xlsx — another spreadsheet placeholder
    revenue = os.path.join(DESKTOP, 'revenue_model.xlsx')
    with open(revenue, 'wb') as f:
        f.write(b'Revenue Model 2025\n\nMonth,Product,Revenue\nJanuary,Software,185000\nFebruary,Software,210000\n')
    print(f'Created: {revenue}')

    # 8. vacation_photo.png — a PNG image placeholder (minimal PNG header)
    vacation_photo = os.path.join(DESKTOP, 'vacation_photo.png')
    with open(vacation_photo, 'wb') as f:
        # Minimal PNG magic bytes
        f.write(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100)
    print(f'Created: {vacation_photo}')

    print(f'\nAll 8 Desktop files created in: {DESKTOP}')
    print('No Work/ or Personal/ folders exist yet.')
    print('No file_index.txt exists yet.')

    # GUI-ready startup: Open Nautilus file manager on Desktop
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager on Desktop with DISPLAY=:0')


create_initial()
