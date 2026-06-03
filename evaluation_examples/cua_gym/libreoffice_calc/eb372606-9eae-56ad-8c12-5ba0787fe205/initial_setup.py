"""
Initial Setup: Research top restaurant chains and build database + article
Task ID: osworld_multi_apps_web_location_015
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc + LibreOffice Writer)

Initial state: Chrome, LibreOffice Calc (blank), and LibreOffice Writer (blank) are open.
The agent must research restaurant chain data and create the files from scratch.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'


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
    # Ensure Documents directory exists
    documents_dir = os.path.join(WORKDIR, 'Documents')
    os.makedirs(documents_dir, exist_ok=True)
    print(f'Documents directory ensured: {documents_dir}')

    # Launch Chrome for web research
    launch_gui('google-chrome "https://en.wikipedia.org/wiki/List_of_the_largest_fast_food_restaurant_chains"', delay_sec=3.0)

    # Launch LibreOffice Calc (blank new spreadsheet)
    launch_gui('libreoffice --calc --norestore', delay_sec=2.0)

    # Launch LibreOffice Writer (blank new document)
    launch_gui('libreoffice --writer --norestore', delay_sec=2.0)

    print('GUI_READY: launched Chrome, LibreOffice Calc, and LibreOffice Writer with DISPLAY=:0')


create_initial()
