"""
Initial Setup: US B-2 Tourist Visa Research and Writer Guide Task
Task ID: osworld_multi_apps_travel_permit_research_007
Domain: multi_apps (Chrome browser + LibreOffice Writer)

Initial state:
- Chrome browser is open with travel.state.gov loaded for research
- No prior Writer document exists on the Desktop
- Desktop is clean so the agent can save the new file there
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_007'
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

    # Remove any pre-existing guide document from Desktop to ensure clean initial state
    guide_path = os.path.join(DESKTOP, 'us_b2_visa_comprehensive_guide.odt')
    if os.path.exists(guide_path):
        os.remove(guide_path)
        print(f'Removed pre-existing file: {guide_path}')

    print(f'Desktop directory ready: {DESKTOP}')
    print('Initial state: No Writer document exists. Browser will be opened for research.')

    # Open Chrome browser with the official US visa information page
    # This gives the agent a starting point for research
    launch_gui(
        'google-chrome --new-window "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html"',
        delay_sec=3.0
    )

    print('GUI_READY: Chrome browser launched with travel.state.gov loaded (DISPLAY=:0)')
    print(f'Task: Agent should research US B-2 visa requirements and create us_b2_visa_comprehensive_guide.odt on Desktop')


setup_initial()
