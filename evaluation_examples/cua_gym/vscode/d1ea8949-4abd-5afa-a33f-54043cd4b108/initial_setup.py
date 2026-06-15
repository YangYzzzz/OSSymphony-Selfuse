"""
Initial Setup: Change language mode from Plain Text to JavaScript
Task ID: vscode_code_070
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_070'
PROJECT_DIR = f'{WORKDIR}/project'
TARGET_FILE = f'{PROJECT_DIR}/Makefile.config'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # --- Create project directory and target file ---
    os.makedirs(PROJECT_DIR, exist_ok=True)

    js_content = """const config = {
  output: './dist',
  entry: './src/index.js',
  minify: true,
  sourceMaps: false
};
module.exports = config;
"""
    with open(TARGET_FILE, 'w') as f:
        f.write(js_content)
    print(f'Created file: {TARGET_FILE}')

    # --- Ensure VSCode settings do NOT have a language association for this file ---
    # This ensures VSCode shows 'Plain Text' for the file (no association set)
    os.makedirs(VSCODE_USER, exist_ok=True)
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        import re
        # Strip JSONC comments before parsing
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        settings = json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any existing files.associations entry for Makefile.config
    # to ensure VSCode treats it as Plain Text
    if 'files.associations' in settings:
        assoc = settings['files.associations']
        keys_to_remove = [k for k in assoc if 'Makefile.config' in k]
        for k in keys_to_remove:
            del assoc[k]
        if not assoc:
            del settings['files.associations']

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings cleaned (no Makefile.config association): {SETTINGS_PATH}')

    # --- GUI-ready startup: open VSCode with the target file ---
    launch_gui(f'code "{TARGET_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
