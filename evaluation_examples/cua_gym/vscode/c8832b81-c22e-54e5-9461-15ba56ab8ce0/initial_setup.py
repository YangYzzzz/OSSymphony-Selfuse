"""
Initial Setup: Open VSCode workspace ~/projects/utils-lib with no watch expressions
Task ID: vscode_dbg_008
Domain: vs_code

Creates a Python utility library workspace with several source files.
The Run and Debug sidebar's Watch panel must have no expressions.
"""

import hashlib
import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_008'
WORKSPACE_DIR = f'{WORKDIR}/projects/utils-lib'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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


def create_workspace():
    """Create the utils-lib workspace with realistic Python utility files."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    os.makedirs(f'{WORKSPACE_DIR}/.vscode', exist_ok=True)

    # Main utility module: math_utils.py
    math_utils = '''\
"""
math_utils.py — Arithmetic and statistical utilities for utils-lib.
"""


def calculate_total(values):
    """Return the sum of a list of numeric values."""
    total = 0
    for v in values:
        total += v
    return total


def calculate_average(values):
    """Return the arithmetic mean of a list of numeric values."""
    if not values:
        return 0.0
    total = calculate_total(values)
    return total / len(values)


def calculate_discount(price, discount_pct):
    """Apply a percentage discount to a price and return the discounted value."""
    discount_amount = price * (discount_pct / 100.0)
    discounted = price - discount_amount
    return round(discounted, 2)


def clamp(value, min_val, max_val):
    """Clamp a value to [min_val, max_val]."""
    return max(min_val, min(max_val, value))
'''

    # String utilities: string_utils.py
    string_utils = '''\
"""
string_utils.py — String manipulation helpers for utils-lib.
"""


def slugify(text):
    """Convert a string to a URL-friendly slug."""
    text = text.lower().strip()
    import re
    text = re.sub(r'[^\\w\\s-]', '', text)
    text = re.sub(r'[\\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def truncate(text, max_length=80, suffix='...'):
    """Truncate text to max_length characters, appending suffix if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def count_words(text):
    """Return the number of words in a string."""
    return len(text.split())


def capitalize_words(text):
    """Capitalize the first letter of each word."""
    return ' '.join(word.capitalize() for word in text.split())
'''

    # File I/O utilities: file_utils.py
    file_utils = '''\
"""
file_utils.py — File and directory helper utilities for utils-lib.
"""

import os
import json


def read_json(path):
    """Read and return a JSON file as a Python dict."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path, data, indent=2):
    """Write a Python dict to a JSON file."""
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)


def list_files(directory, extension=None):
    """Return a list of file paths in a directory, optionally filtered by extension."""
    results = []
    for entry in os.scandir(directory):
        if entry.is_file():
            if extension is None or entry.name.endswith(extension):
                results.append(entry.path)
    return sorted(results)


def ensure_dir(path):
    """Create a directory (and parents) if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)
    return path
'''

    # Date utilities: date_utils.py
    date_utils = '''\
"""
date_utils.py — Date and time helper utilities for utils-lib.
"""

from datetime import datetime, timedelta


def format_date(dt, fmt='%Y-%m-%d'):
    """Format a datetime object as a string."""
    return dt.strftime(fmt)


def parse_date(date_str, fmt='%Y-%m-%d'):
    """Parse a date string into a datetime object."""
    return datetime.strptime(date_str, fmt)


def days_between(start_str, end_str, fmt='%Y-%m-%d'):
    """Return the number of days between two date strings."""
    start = parse_date(start_str, fmt)
    end = parse_date(end_str, fmt)
    return abs((end - start).days)


def add_business_days(start_date, num_days):
    """Add num_days business days (Mon-Fri) to start_date."""
    current = start_date
    added = 0
    while added < num_days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            added += 1
    return current
'''

    # Test file: test_math_utils.py
    test_math = '''\
"""
test_math_utils.py — Unit tests for math_utils.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math_utils import calculate_total, calculate_average, calculate_discount, clamp


def test_calculate_total():
    assert calculate_total([10, 20, 30]) == 60
    assert calculate_total([]) == 0
    assert calculate_total([100]) == 100


def test_calculate_average():
    assert calculate_average([10, 20, 30]) == 20.0
    assert calculate_average([]) == 0.0


def test_calculate_discount():
    assert calculate_discount(100.0, 10) == 90.0
    assert calculate_discount(200.0, 25) == 150.0


def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10


if __name__ == '__main__':
    test_calculate_total()
    test_calculate_average()
    test_calculate_discount()
    test_clamp()
    print("All tests passed.")
'''

    # README
    readme = '''\
# utils-lib

A collection of lightweight Python utility functions for common operations.

## Modules

- **math_utils.py** — Arithmetic, statistical, and financial calculations
- **string_utils.py** — String manipulation and formatting helpers
- **file_utils.py** — File system operations and JSON I/O
- **date_utils.py** — Date parsing, formatting, and business-day arithmetic

## Usage

```python
from math_utils import calculate_total, calculate_average

prices = [29.99, 14.50, 49.95, 8.00]
total = calculate_total(prices)
avg = calculate_average(prices)
print(f"Total: {total:.2f}, Average: {avg:.2f}")
```

## Tests

Run from the project root:

```
python tests/test_math_utils.py
```
'''

    # VSCode launch config (no watch expressions defined here — user must add them)
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": True
            },
            {
                "name": "Debug math_utils",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/math_utils.py",
                "console": "integratedTerminal",
                "justMyCode": True
            }
        ]
    }

    # Write all source files
    os.makedirs(f'{WORKSPACE_DIR}/tests', exist_ok=True)
    with open(f'{WORKSPACE_DIR}/math_utils.py', 'w') as f:
        f.write(math_utils)
    with open(f'{WORKSPACE_DIR}/string_utils.py', 'w') as f:
        f.write(string_utils)
    with open(f'{WORKSPACE_DIR}/file_utils.py', 'w') as f:
        f.write(file_utils)
    with open(f'{WORKSPACE_DIR}/date_utils.py', 'w') as f:
        f.write(date_utils)
    with open(f'{WORKSPACE_DIR}/tests/test_math_utils.py', 'w') as f:
        f.write(test_math)
    with open(f'{WORKSPACE_DIR}/README.md', 'w') as f:
        f.write(readme)
    with open(f'{WORKSPACE_DIR}/.vscode/launch.json', 'w') as f:
        json.dump(launch_config, f, indent=4)

    print(f'Workspace created: {WORKSPACE_DIR}')


def clear_watch_expressions():
    """
    Ensure no watch expressions exist for this workspace in VSCode storage.

    VSCode stores debug watch expressions in workspaceStorage under a hash of
    the workspace path. We clear any such storage to guarantee a clean state.
    """
    workspace_path_for_hash = WORKSPACE_DIR
    # VSCode hashes the workspace URI: vscode-file://vscode-app/<path>
    # The storage key is based on the URI path.
    # We iterate and remove any watch expressions stored in workspaceStorage.
    workspace_storage_base = f'{VSCODE_USER}/workspaceStorage'
    if not os.path.exists(workspace_storage_base):
        print('No workspaceStorage found — watch panel will be empty by default.')
        return

    for entry in os.listdir(workspace_storage_base):
        entry_path = os.path.join(workspace_storage_base, entry)
        workspace_json = os.path.join(entry_path, 'workspace.json')
        if not os.path.isfile(workspace_json):
            continue
        try:
            with open(workspace_json, 'r') as f:
                ws_data = json.load(f)
            folder = ws_data.get('folder', '')
            # Match if this storage corresponds to our workspace
            if 'utils-lib' in folder or WORKSPACE_DIR in folder:
                # Remove debug watch expression memento if present
                backup_dir = os.path.join(entry_path, 'backup')
                if os.path.exists(backup_dir):
                    for bfile in os.listdir(backup_dir):
                        bfile_path = os.path.join(backup_dir, bfile)
                        if os.path.isfile(bfile_path):
                            try:
                                with open(bfile_path, 'r') as f:
                                    content = json.load(f)
                                # Remove watch expressions if present
                                changed = False
                                if 'debug.watchExpressions' in content:
                                    del content['debug.watchExpressions']
                                    changed = True
                                if changed:
                                    with open(bfile_path, 'w') as f:
                                        json.dump(content, f, indent=2)
                                    print(f'Cleared watch expressions in: {bfile_path}')
                            except (json.JSONDecodeError, IOError):
                                pass
        except (json.JSONDecodeError, IOError):
            continue

    print('Watch panel state cleared (no watch expressions in initial env).')


def setup_vscode_settings():
    """Configure global VSCode user settings."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Ensure Python extension is configured for this workspace
    settings.setdefault('python.defaultInterpreterPath', '/usr/bin/python3')
    # Ensure debug panel starts clean
    settings['debug.openDebug'] = 'openOnDebugBreak'
    settings['debug.toolBarLocation'] = 'docked'

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings updated: {SETTINGS_PATH}')


def main():
    # 1. Create workspace files
    create_workspace()

    # 2. Clear any pre-existing watch expressions
    clear_watch_expressions()

    # 3. Update VSCode settings
    setup_vscode_settings()

    # 4. Launch VSCode with the workspace (GUI-ready)
    print('Launching VSCode with utils-lib workspace...')
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with DISPLAY=:0')
    print(f'Initial env ready. Watch panel has no expressions.')


main()
