"""
Initial Setup: Property-based testing with Hypothesis in a Python project
Task ID: vscode_gf6_069
Domain: vscode

Creates ~/projects/python-hypothesis with:
- src/sorting.py (bubble_sort, merge_sort, quick_sort)
- src/string_utils.py (parse_date, format_date)
- venv/ with pytest installed
- NO tests, NO hypothesis, NO pytest.ini, NO .vscode/tasks.json
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_069'
PROJECT = f'{WORKDIR}/projects/python-hypothesis'


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
    # Create project structure
    os.makedirs(f'{PROJECT}/src', exist_ok=True)

    # --- src/__init__.py ---
    with open(f'{PROJECT}/src/__init__.py', 'w') as f:
        f.write('')

    # --- src/sorting.py ---
    sorting_code = '''\
"""Sorting algorithm implementations for performance comparison."""


def bubble_sort(lst):
    """Sort a list using the bubble sort algorithm.

    Args:
        lst: A list of comparable elements.

    Returns:
        A new sorted list.
    """
    arr = list(lst)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def merge_sort(lst):
    """Sort a list using the merge sort algorithm.

    Args:
        lst: A list of comparable elements.

    Returns:
        A new sorted list.
    """
    arr = list(lst)
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists into a single sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(lst):
    """Sort a list using the quick sort algorithm.

    Args:
        lst: A list of comparable elements.

    Returns:
        A new sorted list.
    """
    arr = list(lst)
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)
'''
    with open(f'{PROJECT}/src/sorting.py', 'w') as f:
        f.write(sorting_code)

    # --- src/string_utils.py ---
    string_utils_code = '''\
"""String utility functions for date parsing and formatting."""

from datetime import datetime


def parse_date(s):
    """Parse a date string in YYYY-MM-DD format.

    Args:
        s: A string in 'YYYY-MM-DD' format.

    Returns:
        A datetime.date object.

    Raises:
        ValueError: If the string is not in the expected format.
    """
    return datetime.strptime(s, "%Y-%m-%d").date()


def format_date(d):
    """Format a date object as a YYYY-MM-DD string.

    Args:
        d: A datetime.date object.

    Returns:
        A string in 'YYYY-MM-DD' format.
    """
    return d.strftime("%Y-%m-%d")
'''
    with open(f'{PROJECT}/src/string_utils.py', 'w') as f:
        f.write(string_utils_code)

    # --- Create virtual environment with pytest ---
    print("Creating virtual environment...")
    subprocess.run(
        ['python3', '-m', 'venv', '--without-pip', f'{PROJECT}/venv'],
        check=True,
        capture_output=True,
        text=True,
    )
    # Bootstrap pip into the venv
    print("Bootstrapping pip in venv...")
    subprocess.run(
        ['bash', '-c',
         f'curl -sS https://bootstrap.pypa.io/get-pip.py | {PROJECT}/venv/bin/python3'],
        check=True,
        capture_output=True,
        text=True,
    )
    print("Installing pytest in venv...")
    subprocess.run(
        [f'{PROJECT}/venv/bin/pip', 'install', 'pytest'],
        check=True,
        capture_output=True,
        text=True,
    )
    print("pytest installed successfully.")

    # Verify no hypothesis is installed
    result = subprocess.run(
        [f'{PROJECT}/venv/bin/pip', 'list'],
        capture_output=True,
        text=True,
    )
    print(f"Installed packages:\n{result.stdout}")

    print(f'Initial project created: {PROJECT}')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
