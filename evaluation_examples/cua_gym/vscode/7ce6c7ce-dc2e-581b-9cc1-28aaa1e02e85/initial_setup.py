"""
Initial Setup: Set up VSCode with no custom keybindings
Task ID: vscode_stu_073
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_073'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')


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
    # Create a workspace directory with a sample Python file
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    python_file = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(python_file, 'w') as f:
        f.write('''\
import math
import sys


def calculate_circle_area(radius):
    """Calculate the area of a circle given its radius."""
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return math.pi * radius ** 2


def calculate_sphere_volume(radius):
    """Calculate the volume of a sphere given its radius."""
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return (4 / 3) * math.pi * radius ** 3


def main():
    radii = [1.0, 2.5, 3.7, 5.0, 10.0]
    print("Circle Area and Sphere Volume Calculator")
    print("=" * 45)
    for r in radii:
        area = calculate_circle_area(r)
        volume = calculate_sphere_volume(r)
        print(f"Radius: {r:6.1f}  |  Area: {area:10.2f}  |  Volume: {volume:12.2f}")
    print("=" * 45)
    print("Calculations complete.")


if __name__ == "__main__":
    main()
''')

    # Ensure VSCode user config directory exists but NO custom keybindings
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Remove any existing keybindings.json to ensure clean initial state
    if os.path.exists(KEYBINDINGS_PATH):
        os.remove(KEYBINDINGS_PATH)

    print(f'Initial workspace created: {WORKSPACE_DIR}')
    print(f'Python file created: {python_file}')
    print(f'No custom keybindings.json (removed if existed)')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    # Also open the Python file specifically
    launch_gui(f'code "{python_file}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
