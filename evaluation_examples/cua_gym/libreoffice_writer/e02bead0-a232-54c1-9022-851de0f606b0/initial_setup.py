"""
Initial Setup: Fetch Gaussian Mixtures notebook, extract code cells, create gmm_code.py on Desktop,
               open in VSCode, create gmm_report.odt summary.
Task ID: osworld_multi_apps_code_to_writer_file_011
Domain: libreoffice_writer (multi-app: VSCode + LibreOffice Writer + Browser)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_011'
DESKTOP = f'{WORKDIR}/Desktop'


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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing output files to ensure clean initial state
    for fname in ['gmm_code.py', 'gmm_report.odt', 'gmm_report.docx']:
        for d in [DESKTOP, WORKDIR]:
            fpath = os.path.join(d, fname)
            if os.path.exists(fpath):
                os.remove(fpath)
                print(f'Removed pre-existing file: {fpath}')

    print('Initial state: Desktop is clean, no gmm_code.py or gmm_report.odt exist.')

    # Open a browser window pointing to the notebook URL so the agent can fetch it
    notebook_url = 'https://raw.githubusercontent.com/jakevdp/PythonDataScienceHandbook/master/notebooks/05.12-Gaussian-Mixtures.ipynb'
    launch_gui(f'google-chrome --new-window "{notebook_url}"', delay_sec=3.0)
    print(f'GUI_READY: Opened Chrome to {notebook_url} with DISPLAY=:0')


setup_initial()
