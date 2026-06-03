"""
Initial Setup: Web to Doc - Kubernetes Pods Documentation
Task ID: osworld_multi_apps_web_to_doc_009
Domain: multi_apps (Chrome + LibreOffice Writer)

Initial state:
- Chrome is open (no specific URL)
- Desktop is empty (no k8s_pods.docx file)
- The agent must visit the Kubernetes Pods page and save the documentation
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_to_doc_009'


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
    # Ensure Desktop directory exists and is empty of task artifact
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any existing k8s_pods.docx from Desktop (idempotent)
    target_file = os.path.join(DESKTOP, 'k8s_pods.docx')
    if os.path.exists(target_file):
        os.remove(target_file)
        print(f'Removed existing file: {target_file}')

    print(f'Desktop is clean: no k8s_pods.docx present')

    # GUI-ready startup: open Chrome (initial state requirement)
    # Kill any existing Chrome instances first to ensure clean state
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    time.sleep(1.0)

    # Launch Chrome with remote debugging port (required for OSWorld)
    launch_gui(
        'google-chrome --remote-debugging-port=1337 --no-first-run --no-default-browser-check',
        delay_sec=3.0
    )

    print(f'GUI_READY: Chrome launched with DISPLAY=:0')
    print(f'Initial state: Desktop is empty, Chrome is open')


setup_initial()
