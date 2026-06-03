"""
Initial Setup: Collect missing wallpapers from GitHub repository
Task ID: osworld_multi_apps_collect_missing_002
Domain: os (multi-app: Chrome + Nautilus)

Initial state: ~/Pictures/Wallpapers contains a subset of wallpapers from
https://github.com/elementary/wallpapers. Some wallpapers are missing.
Chrome is open and Nautilus shows ~/Pictures/Wallpapers.
"""

import os
import shlex
import subprocess
import time
import urllib.request
import urllib.parse

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_collect_missing_002'
WALLPAPERS_DIR = '/home/user/Pictures/Wallpapers'

# All 16 wallpapers in the GitHub repo backgrounds/ directory
ALL_WALLPAPERS = [
    "A Large Body of Water Surrounded By Mountains.jpg",
    "A Trail of Footprints In The Sand.jpg",
    "Ashim DSilva.jpg",
    "Canazei Granite Ridges.jpg",
    "Martin Adams.jpg",
    "Morskie Oko.jpg",
    "Mr. Lee.jpg",
    "Nattu Adnan.jpg",
    "Photo by SpaceX.jpg",
    "Photo of Valley.jpg",
    "Snow-Capped Mountain.jpg",
    "Sunset by the Pier.jpg",
    "Tj Holowaychuk.jpg",
    "Viktor Forgacs.jpg",
    "odin-dark.jpg",
    "odin.jpg",
]

# Subset to include in the initial state (10 of 16; 6 will be missing)
INITIAL_WALLPAPERS = [
    "A Large Body of Water Surrounded By Mountains.jpg",
    "A Trail of Footprints In The Sand.jpg",
    "Canazei Granite Ridges.jpg",
    "Martin Adams.jpg",
    "Mr. Lee.jpg",
    "Nattu Adnan.jpg",
    "Photo of Valley.jpg",
    "Tj Holowaychuk.jpg",
    "Viktor Forgacs.jpg",
    "odin.jpg",
]

BASE_URL = "https://raw.githubusercontent.com/elementary/wallpapers/main/backgrounds/"


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
    # Create the Wallpapers directory
    os.makedirs(WALLPAPERS_DIR, exist_ok=True)
    print(f'Created directory: {WALLPAPERS_DIR}')

    # Download only the initial subset of wallpapers
    for filename in INITIAL_WALLPAPERS:
        dest = os.path.join(WALLPAPERS_DIR, filename)
        if os.path.exists(dest):
            print(f'Already exists, skipping: {filename}')
            continue
        encoded = urllib.parse.quote(filename)
        url = BASE_URL + encoded
        try:
            urllib.request.urlretrieve(url, dest)
            print(f'Downloaded: {filename}')
        except Exception as e:
            print(f'ERROR downloading {filename}: {e}')

    # List what we have
    files = sorted(os.listdir(WALLPAPERS_DIR))
    print(f'\nInitial state: {len(files)} wallpapers in {WALLPAPERS_DIR}')
    for f in files:
        print(f'  {f}')

    missing = [w for w in ALL_WALLPAPERS if w not in files]
    print(f'\nMissing wallpapers ({len(missing)}):')
    for m in missing:
        print(f'  {m}')

    # GUI-ready startup: open Chrome and Nautilus showing ~/Pictures/Wallpapers
    launch_gui('google-chrome "https://github.com/elementary/wallpapers"', delay_sec=3.0)
    launch_gui(f'nautilus "{WALLPAPERS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Chrome and Nautilus with DISPLAY=:0')


create_initial()
