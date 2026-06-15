"""
Initial Setup: Singapore Restaurant Guide Research Task
Task ID: osworld_multi_apps_web_location_012
Domain: libreoffice_calc

This script sets up the initial GUI state for an agent that will:
1. Research 15 hawker centres and restaurants across 5 cuisine categories
2. Collect data from Google Maps, TripAdvisor, and Michelin Guide
3. Compute distances from Marina Bay Sands
4. Save results as singapore_restaurant_guide.xlsx
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_012'

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
    # The task requires the agent to research restaurants and create the file from scratch.
    # Initial state: Chrome open to TripAdvisor Singapore restaurants page,
    # and LibreOffice Calc open with a blank new spreadsheet.

    # Open Chrome to TripAdvisor Singapore restaurants page
    launch_gui(
        'google-chrome --new-window "https://www.tripadvisor.com/Restaurants-g294265-Singapore.html"',
        delay_sec=3.0
    )

    # Open LibreOffice Calc with a blank spreadsheet
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print(f'GUI_READY: launched Chrome (TripAdvisor Singapore) and LibreOffice Calc with DISPLAY=:0')

create_initial()
