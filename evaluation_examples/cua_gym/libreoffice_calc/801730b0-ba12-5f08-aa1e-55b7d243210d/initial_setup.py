"""
Initial Setup: Collect ML conference best paper awards and build cross-conference table
Task ID: osworld_multi_apps_web_conference_011
Domain: libreoffice_calc (multi-app: Chrome, LibreOffice Calc, LibreOffice Writer)

Initial state:
- Clean Desktop (no pre-existing output files)
- Chrome open to starting search page
- LibreOffice Calc open with empty new spreadsheet
- LibreOffice Writer open with empty new document
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_conference_011'
DESKTOP = '/home/user/Desktop'


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


def setup_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing output files to ensure a clean start
    for fname in ['ml_best_papers.ods', 'ml_best_papers.xlsx',
                  'best_papers_summary.odt', 'best_papers_summary.docx']:
        fpath = os.path.join(DESKTOP, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f'Removed pre-existing file: {fpath}')

    print('Desktop cleaned. No pre-existing output files.')

    # Launch Chrome open to a relevant starting page (NeurIPS blog for best papers)
    launch_gui(
        'google-chrome --new-window "https://blog.neurips.cc"',
        delay_sec=3.0
    )

    # Launch LibreOffice Calc with an empty new spreadsheet
    launch_gui(
        'libreoffice --calc --norestore',
        delay_sec=2.0
    )

    # Launch LibreOffice Writer with an empty new document
    launch_gui(
        'libreoffice --writer --norestore',
        delay_sec=2.0
    )

    print('GUI_READY: Chrome, LibreOffice Calc, and LibreOffice Writer launched with DISPLAY=:0')
    print(f'Task: Research NeurIPS/ICML/ICLR best paper award winners 2021-2024')
    print(f'Expected output 1: {DESKTOP}/ml_best_papers.ods')
    print(f'Expected output 2: {DESKTOP}/best_papers_summary.odt')


setup_initial()
