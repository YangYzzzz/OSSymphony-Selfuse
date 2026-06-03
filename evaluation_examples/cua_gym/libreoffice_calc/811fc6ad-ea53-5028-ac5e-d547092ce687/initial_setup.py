"""
Initial Setup: Research work permit requirements for software engineer (India → Germany Blue Card)
Task ID: osworld_multi_apps_travel_permit_research_010
Domain: libreoffice_calc (artifact: .odt Writer document)

Initial state: Browser open with relevant official immigration websites accessible.
LibreOffice Writer is open with a blank document at the target path.
No prior Writer document with Blue Card content exists.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_010'
OUTPUT = f'{WORKDIR}/germany_blue_card_guide_india.odt'


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
    # The initial state has NO pre-existing guide document.
    # The task requires the agent to research and create it from scratch.
    # We only ensure the output file does NOT exist beforehand.
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
        print(f'Removed existing file: {OUTPUT}')

    # Open Chrome with the Make it in Germany website as the primary research source.
    # This simulates the initial state: browser open, ready for research.
    launch_gui(
        'google-chrome --no-sandbox --disable-gpu '
        '"https://www.make-it-in-germany.com/en/visa-residence/types/eu-blue-card" '
        '--new-window',
        delay_sec=3.0,
    )

    # Open a second tab with BAMF (German Federal Office for Migration and Refugees)
    launch_gui(
        'google-chrome --no-sandbox --disable-gpu '
        '"https://www.bamf.de/EN/Themen/MigrationAufenthalt/ZuwandererDrittstaaten/Migrathek/BlaueKarteEU/blauekarteeu-node.html"',
        delay_sec=2.0,
    )

    # Open LibreOffice Writer with a blank document at the target path
    # (Writer opens a new blank doc; the agent must fill it in)
    launch_gui(
        f'libreoffice --writer',
        delay_sec=2.0,
    )

    print(f'Initial state ready: no pre-existing guide at {OUTPUT}')
    print('GUI_READY: Chrome open with Make-it-in-Germany + BAMF tabs; LibreOffice Writer blank window launched.')


create_initial()
