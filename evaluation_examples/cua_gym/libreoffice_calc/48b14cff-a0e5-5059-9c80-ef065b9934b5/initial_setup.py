"""
Initial Setup: Research world's top food festivals and compile event database
Task ID: osworld_multi_apps_web_location_014
Domain: libreoffice_calc

Initial state: Chrome and LibreOffice Calc are open, ready for agent to
research and create food_festivals_world.ods on the Desktop.
No pre-existing food_festivals_world.ods file exists (agent must create it).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_014'
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


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing output file so the task starts clean
    output_path = os.path.join(DESKTOP, 'food_festivals_world.ods')
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f'Removed existing file: {output_path}')

    print(f'Desktop ready at: {DESKTOP}')
    print(f'No food_festivals_world.ods present — agent must research and create it.')

    # GUI-ready startup: open Chrome (for web research) and LibreOffice Calc (blank)
    launch_gui('google-chrome --new-window "https://www.cntraveler.com"', delay_sec=3.0)
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')


create_initial()
