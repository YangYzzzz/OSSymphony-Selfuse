"""
Initial Setup: Conference Acceptance Rates Research Task
Task ID: osworld_multi_apps_web_conference_013
Domain: multi_apps (Chrome + LibreOffice Calc + LibreOffice Writer)

This task requires the agent to:
1. Research acceptance rates for 5 conferences (NeurIPS, ICML, ICLR, ACL, CVPR) over 6 years (2019-2024)
2. Create acceptance_rates.ods on Desktop with conditional formatting
3. Create acceptance_analysis.odt in Documents with analysis table and paragraph

Initial state: Chrome open (for web research), LibreOffice Calc and Writer available.
No data files exist yet - agent must collect data and create them.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_conference_013'

# Target output paths (must NOT exist in initial state)
CALC_OUTPUT = f'{WORKDIR}/Desktop/acceptance_rates.ods'
WRITER_OUTPUT = f'{WORKDIR}/Documents/acceptance_analysis.odt'


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
    # Ensure target directories exist (but NOT the output files themselves)
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    # Remove any pre-existing target files to ensure clean initial state
    for path in [CALC_OUTPUT, WRITER_OUTPUT]:
        if os.path.exists(path):
            os.remove(path)
            print(f'Removed pre-existing file: {path}')

    print(f'Initial state prepared: Desktop and Documents directories exist')
    print(f'Target files do NOT exist yet (agent must create them):')
    print(f'  - {CALC_OUTPUT}')
    print(f'  - {WRITER_OUTPUT}')

    # GUI-ready startup: open Chrome for web research
    # The agent needs to browse to conference websites, Wikipedia, OpenReview
    launch_gui('google-chrome --new-window "https://openreview.net/"', delay_sec=3.0)

    # Also open LibreOffice Calc (blank) so agent can start entering data
    launch_gui('libreoffice --calc', delay_sec=2.0)

    # Open LibreOffice Writer (blank) so agent can start writing analysis
    launch_gui('libreoffice --writer', delay_sec=2.0)

    print('GUI_READY: launched Chrome, LibreOffice Calc, and LibreOffice Writer with DISPLAY=:0')


create_initial()
