"""
Initial Setup: Delete line 14 from ~/Desktop/script.sh using VSCode
Task ID: vscode_edit_007
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_007'
OUTPUT = f'{WORKDIR}/Desktop/script.sh'


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
    desktop_dir = f'{WORKDIR}/Desktop'
    os.makedirs(desktop_dir, exist_ok=True)

    # 20-line shell script with realistic content
    # Line 14 is the debug echo that should be deleted by the agent
    script_content = """\
#!/bin/bash
# deploy.sh — Application deployment script
# Author: DevOps Team
# Version: 2.1.0

APP_NAME="my-web-app"
DEPLOY_DIR="/var/www/${APP_NAME}"
LOG_FILE="/var/log/${APP_NAME}/deploy.log"

echo "Starting deployment of ${APP_NAME}..."
mkdir -p "${DEPLOY_DIR}"
cd "${DEPLOY_DIR}" || exit 1
git pull origin main
echo "DEBUG: temporary output"
pip install -r requirements.txt
systemctl stop "${APP_NAME}" 2>/dev/null || true
cp -r ./dist/* "${DEPLOY_DIR}/"
systemctl start "${APP_NAME}"
echo "Deployment complete. Check ${LOG_FILE} for details."
exit 0
"""

    with open(OUTPUT, 'w') as f:
        f.write(script_content)

    # Make script executable
    os.chmod(OUTPUT, 0o755)

    print(f'Initial file created: {OUTPUT}')

    # Verify line count
    with open(OUTPUT, 'r') as f:
        lines = f.readlines()
    print(f'Line count: {len(lines)} (expected 20)')
    print(f'Line 14: {lines[13].rstrip()!r} (expected: echo "DEBUG: temporary output")')

    # GUI-ready startup: open the script.sh file in VSCode
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
