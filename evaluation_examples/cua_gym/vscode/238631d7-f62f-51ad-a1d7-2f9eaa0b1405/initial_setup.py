"""
Initial Setup: Add cursors and type commas in matrix.py
Task ID: vscode_edit_051
Domain: vs_code

Creates ~/Desktop/matrix.py - a 30-line Python file with a 2D sensor array.
Lines 15-20 have a missing comma at column 15 (1-indexed) between a number
and the next number. The agent will add cursors on lines 15-20 at column 15
and type a comma at each position.
"""

import os
import shlex
import subprocess
import time

DESKTOP = '/home/user/Desktop'
OUTPUT = f'{DESKTOP}/matrix.py'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # 30-line Python file. Lines 15-20 (1-indexed) are sensor_data rows
    # where a comma is missing between two numbers.
    # Layout on those lines (0-indexed positions):
    #   0-3:   "    " (4-space indent)
    #   4:     "["
    #   5+:    first few numbers with commas/spaces
    #   12-13: a 2-digit number (the target — last digit at index 13)
    #   14:    " " (space — no comma; cursor at column 15 goes here)
    #   15+:   remaining numbers
    #
    # Example line 15: "    [5, 10, 30 40, 50, 60, 70, 80],"
    #                   01234567890123456...
    #                             ^   ^ index 13='0', index 14=' '

    content = (
        "# matrix.py - 2D grid data for spatial analysis module\n"
        "# Dataset: 6x8 pressure sensor grid readings (engineering units)\n"
        "\n"
        "import numpy as np\n"
        "\n"
        "GRID_ROWS = 6\n"
        "GRID_COLS = 8\n"
        "\n"
        "# Raw sensor readings organized as a 2D array.\n"
        "# Each inner list represents one row of the grid (west to east).\n"
        "# Values are integer readings from pressure sensors (in kPa).\n"
        "\n"
        "sensor_data = [\n"
        "    [8, 16, 33, 49, 52, 61, 74, 87],\n"
        "    [5, 10, 30 40, 50, 60, 70, 80],\n"   # line 15 — missing comma at col 15
        "    [5, 12, 25 37, 48, 51, 63, 74],\n"   # line 16 — missing comma at col 15
        "    [3, 11, 24 36, 47, 58, 69, 72],\n"   # line 17 — missing comma at col 15
        "    [7, 15, 29 41, 53, 64, 76, 88],\n"   # line 18 — missing comma at col 15
        "    [6, 14, 28 45, 57, 68, 71, 83],\n"   # line 19 — missing comma at col 15
        "    [4, 13, 27 42, 56, 67, 78, 92],\n"   # line 20 — missing comma at col 15
        "    [9, 18, 35, 46, 59, 62, 75, 96],\n"
        "]\n"
        "\n"
        "# Compute row averages using numpy\n"
        "row_avgs = np.mean(sensor_data, axis=1)\n"
        "\n"
        "# Compute column averages\n"
        "col_avgs = np.mean(sensor_data, axis=0)\n"
        "\n"
        'print("Grid loaded.")\n'
    )

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(content)

    lines = content.splitlines()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines: {len(lines)}')
    for i in range(14, 20):  # lines 15-20 (0-indexed: 14-19)
        line = lines[i]
        print(f'  Line {i+1}: col14={repr(line[13])}, col15={repr(line[14])}, content={repr(line)}')

    # GUI-ready startup: open VSCode with the Desktop folder
    launch_gui(f'code "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
