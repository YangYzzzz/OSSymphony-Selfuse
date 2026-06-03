"""
Initial Setup: Configure nano text editor to show line numbers and enable smooth scrolling
Task ID: osworld_multi_apps_web_search_config_008
Domain: os (nano configuration)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_search_config_008'
NANORC_PATH = '/home/user/.nanorc'


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
    # Create a .nanorc file that does NOT contain linenumbers or smooth scroll settings
    # It has some other common nano settings to make it realistic
    nanorc_content = """## nano configuration file
## See man nanorc for documentation

# Enable syntax highlighting
include "/usr/share/nano/*.nanorc"

# Use auto-indent
set autoindent

# Allow multiple file buffers
set multibuffer

# Display line and column numbers at the bottom
set constantshow

# Backup files to ~/.nano/
set backup
set backupdir "~/.nano"
"""

    # Write the .nanorc file without line number or smooth scroll settings
    Path(NANORC_PATH).write_text(nanorc_content)
    print(f'Initial .nanorc created: {NANORC_PATH}')

    # Verify the initial state does NOT have the task-completion settings
    content = Path(NANORC_PATH).read_text()
    assert 'set linenumbers' not in content, 'ERROR: initial .nanorc must not contain set linenumbers'
    assert 'set smooth' not in content, 'ERROR: initial .nanorc must not contain set smooth'
    print('Verified: .nanorc does not contain linenumbers or smooth settings')

    # GUI-ready startup: open Terminal and Chrome as specified in context
    # Open GNOME Terminal
    launch_gui('gnome-terminal', delay_sec=2.0)
    # Open Chrome browser (for web search)
    launch_gui('google-chrome --new-window', delay_sec=2.0)
    print('GUI_READY: launched Terminal and Chrome with DISPLAY=:0')


create_initial()
