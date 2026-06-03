"""
Initial Setup: VSCode for Julia development (pre-task state)
Task ID: osworld_multi_apps_vscode_ext_script_007
Domain: multi_apps / vscode

Initial state:
  - VSCode is open
  - julialang.language-julia extension is NOT installed
  - ~/Desktop/stats.jl does NOT exist
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_007'
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

    # Remove stats.jl if it accidentally exists (ensure clean initial state)
    stats_jl = os.path.join(DESKTOP, 'stats.jl')
    if os.path.exists(stats_jl):
        os.remove(stats_jl)
        print(f'Removed pre-existing {stats_jl}')

    # Uninstall Julia extension if accidentally present (ensure initial state)
    julia_ext = 'julialang.language-julia'
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True
    )
    if julia_ext in result.stdout:
        subprocess.run(
            ['code', '--uninstall-extension', julia_ext],
            capture_output=True, text=True
        )
        print(f'Uninstalled {julia_ext} to reset to initial state')
    else:
        print(f'Confirmed: {julia_ext} is not installed (correct initial state)')

    print(f'Initial state ready: no stats.jl, no Julia extension')

    # GUI-ready startup: open VSCode
    launch_gui('code', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


setup_initial()
