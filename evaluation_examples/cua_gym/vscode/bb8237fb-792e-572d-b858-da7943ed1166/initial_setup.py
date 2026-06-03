"""
Initial Setup: Create workspace for VSCode Python file creation task
Task ID: vscode_stu_042
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_042'
WORKSPACE = f'{WORKDIR}/cs101/hw5'


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
    # Create the workspace directory
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create some realistic existing homework files so the workspace isn't empty
    # hw5_utils.py - a helper module from previous work
    with open(os.path.join(WORKSPACE, 'hw5_utils.py'), 'w') as f:
        f.write('''"""Utility functions for CS101 Homework 5."""


def read_numbers(filename):
    """Read a list of integers from a text file, one per line."""
    numbers = []
    with open(filename, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line:
                numbers.append(int(line))
    return numbers


def write_numbers(filename, numbers):
    """Write a list of integers to a text file, one per line."""
    with open(filename, 'w') as fh:
        for num in numbers:
            fh.write(f"{num}\\n")
''')

    # sample_data.txt - test data for sorting exercises
    with open(os.path.join(WORKSPACE, 'sample_data.txt'), 'w') as f:
        f.write('42\n17\n83\n5\n91\n33\n68\n12\n56\n74\n')

    # README.md - assignment instructions
    with open(os.path.join(WORKSPACE, 'README.md'), 'w') as f:
        f.write('''# CS101 - Homework 5: Sorting Algorithms

## Instructions

1. Create a file called `sorting.py` with a proper Python module structure.
2. Implement at least two sorting algorithms (e.g., bubble sort, insertion sort).
3. Use `hw5_utils.py` to read and write test data.
4. Test your implementations with `sample_data.txt`.

## Due Date
April 10, 2026

## Grading
- Code structure and readability: 20%
- Correctness of sorting algorithms: 60%
- Testing and edge cases: 20%
''')

    print(f'Workspace created: {WORKSPACE}')
    print(f'Files: hw5_utils.py, sample_data.txt, README.md')

    # NOTE: sorting.py does NOT exist yet - that's what the agent must create

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
