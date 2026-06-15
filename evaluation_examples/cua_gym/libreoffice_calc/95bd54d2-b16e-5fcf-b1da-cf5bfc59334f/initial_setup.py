"""
Initial Setup: Install Writer's Tools extension for LibreOffice Writer
Task ID: osworld_multi_apps_ext_install_006
Domain: multi_apps (LibreOffice Writer + Chrome)

Initial state:
- LibreOffice Writer is open (no file, just the Writer application)
- Chrome is open (available for downloading the extension)
- Writer's Tools extension is NOT installed
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_ext_install_006'


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


def ensure_extension_not_installed():
    """Make sure Writer's Tools extension is not installed in initial state."""
    try:
        result = subprocess.run(
            ['unopkg', 'list'],
            capture_output=True,
            text=True
        )
        if 'WritersTools' in result.stdout or 'com.waanders.WritersTools' in result.stdout:
            subprocess.run(
                ['unopkg', 'remove', 'com.waanders.WritersTools'],
                capture_output=True
            )
            print('Removed pre-existing WritersTools extension')
        else:
            print('Writer\'s Tools extension is not installed (correct initial state)')
    except Exception as e:
        print(f'Extension check: {e}')


def clean_downloads():
    """Ensure Downloads folder is empty (no pre-downloaded extension files)."""
    downloads_dir = os.path.join(WORKDIR, 'Downloads')
    os.makedirs(downloads_dir, exist_ok=True)
    for fname in os.listdir(downloads_dir):
        if fname.lower().endswith('.oxt') and 'writers' in fname.lower():
            os.remove(os.path.join(downloads_dir, fname))
            print(f'Removed pre-existing file: {fname}')


def setup_initial():
    # Step 1: Ensure extension is not installed
    ensure_extension_not_installed()

    # Step 2: Clean Downloads folder of any pre-existing extension files
    clean_downloads()

    # Step 3: Launch Chrome browser (agent will use it to navigate to extensions website)
    launch_gui('google-chrome --new-window https://extensions.libreoffice.org/', delay_sec=3.0)
    print('Launched Chrome browser')

    # Step 4: Launch LibreOffice Writer (the app where the extension needs to be installed)
    launch_gui('libreoffice --writer', delay_sec=3.0)
    print('Launched LibreOffice Writer')

    print(f'GUI_READY: Initial state prepared - LibreOffice Writer and Chrome open, Writer\'s Tools NOT installed')


setup_initial()
