"""
Initial Setup: ML Project Resource Collection
Task ID: osworld_multi_apps_sys_browser_os_007
Domain: multi_apps (OS + Chrome + LibreOffice Writer)

Creates:
  - /home/user/ml_project/          (project directory)
  - /home/user/ml_project/data/     (empty; agent downloads iris.csv here)
  - /home/user/ml_project/docs/     (empty; agent saves screenshot and HTML here)

Does NOT create:
  - iris.csv (agent must download it)
  - sklearn_iris_docs.png (agent must screenshot it)
  - uci_iris.html (agent must save HTML)
  - README.odt (agent must create it)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_browser_os_007'
PROJECT_DIR = f'{WORKDIR}/ml_project'


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
    # Create the ml_project directory structure
    data_dir = os.path.join(PROJECT_DIR, 'data')
    docs_dir = os.path.join(PROJECT_DIR, 'docs')

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    print(f'Created directory: {PROJECT_DIR}')
    print(f'Created directory: {data_dir}')
    print(f'Created directory: {docs_dir}')

    # Verify directories are empty (no pre-existing task artifacts)
    assert not os.path.exists(os.path.join(data_dir, 'iris.csv')), \
        'iris.csv should NOT pre-exist in initial state'
    assert not os.path.exists(os.path.join(docs_dir, 'sklearn_iris_docs.png')), \
        'sklearn_iris_docs.png should NOT pre-exist in initial state'
    assert not os.path.exists(os.path.join(docs_dir, 'uci_iris.html')), \
        'uci_iris.html should NOT pre-exist in initial state'
    assert not os.path.exists(os.path.join(PROJECT_DIR, 'README.odt')), \
        'README.odt should NOT pre-exist in initial state'

    print('Initial state verified: all task artifacts absent.')

    # GUI-ready startup: open Chrome (agent starts by visiting URLs)
    # Also open a file manager to show the project directory
    launch_gui('google-chrome', delay_sec=2.0)
    launch_gui(f'nautilus "{PROJECT_DIR}"', delay_sec=1.5)

    print('GUI_READY: launched Chrome and Nautilus with DISPLAY=:0')


create_initial()
