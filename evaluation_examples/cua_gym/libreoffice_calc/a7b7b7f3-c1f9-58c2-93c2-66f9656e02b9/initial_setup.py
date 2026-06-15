"""
Initial Setup: Download ZIP archives from programming workshop page
Task ID: osworld_multi_apps_web_download_003
Domain: multi_apps (Chrome + OS)

Sets up:
  - ~/workshop_materials directory (empty) as download target
  - Local HTTP server serving a workshop page with ZIP download links
  - Actual ZIP files (exercise1.zip, exercise2.zip, exercise3.zip, solutions.zip)
  - Chrome opened on the workshop page
"""

import os
import shlex
import subprocess
import time
import zipfile
import http.server
import threading
import signal

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_download_003'
WORKSHOP_DIR = f'{WORKDIR}/workshop_server'
DOWNLOAD_DIR = f'{WORKDIR}/workshop_materials'
SERVER_PORT = 8765

# ── Helpers ──────────────────────────────────────────────────────────────────

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI application on the VM display without blocking."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_zip_with_content(zip_path: str, filename: str, content: str):
    """Create a ZIP file containing one text file with given content."""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, content)


# ── Step 1: Create workshop server directory with ZIP files ───────────────────

os.makedirs(WORKSHOP_DIR, exist_ok=True)

# exercise1.zip — Python basics exercises
create_zip_with_content(
    zip_path=f'{WORKSHOP_DIR}/exercise1.zip',
    filename='exercise1_python_basics.py',
    content='''# Exercise 1: Python Basics
# Complete the following functions

def greet(name: str) -> str:
    """Return a greeting string for the given name."""
    # TODO: implement
    pass

def sum_list(numbers: list) -> int:
    """Return the sum of all numbers in the list."""
    # TODO: implement
    pass

def find_max(numbers: list) -> int:
    """Return the maximum value in the list."""
    # TODO: implement
    pass

if __name__ == '__main__':
    print(greet("Alice"))          # Expected: Hello, Alice!
    print(sum_list([1, 2, 3, 4]))  # Expected: 10
    print(find_max([3, 1, 4, 1, 5, 9, 2, 6]))  # Expected: 9
'''
)

# exercise2.zip — Data structures exercises
create_zip_with_content(
    zip_path=f'{WORKSHOP_DIR}/exercise2.zip',
    filename='exercise2_data_structures.py',
    content='''# Exercise 2: Data Structures
# Work with lists, dictionaries, and sets

def remove_duplicates(items: list) -> list:
    """Return list with duplicates removed, preserving original order."""
    # TODO: implement without using set directly on the list
    pass

def word_frequency(text: str) -> dict:
    """Return a dictionary mapping each word to its frequency."""
    # TODO: implement
    pass

def merge_sorted_lists(list1: list, list2: list) -> list:
    """Merge two sorted lists into a single sorted list."""
    # TODO: implement without using sorted()
    pass

if __name__ == '__main__':
    print(remove_duplicates([1, 2, 2, 3, 4, 4, 5]))  # [1, 2, 3, 4, 5]
    print(word_frequency("the cat sat on the mat"))    # {'the': 2, 'cat': 1, ...}
    print(merge_sorted_lists([1, 3, 5], [2, 4, 6]))    # [1, 2, 3, 4, 5, 6]
'''
)

# exercise3.zip — File I/O exercises
create_zip_with_content(
    zip_path=f'{WORKSHOP_DIR}/exercise3.zip',
    filename='exercise3_file_io.py',
    content='''# Exercise 3: File I/O Operations
# Practice reading and writing files

import os
import json
import csv

def read_csv_to_dicts(filepath: str) -> list:
    """Read a CSV file and return a list of dictionaries."""
    # TODO: implement using csv.DictReader
    pass

def write_json_report(data: dict, output_path: str) -> None:
    """Write data dictionary to a JSON file with pretty formatting."""
    # TODO: implement
    pass

def count_lines_words(filepath: str) -> tuple:
    """Return (line_count, word_count) for the given text file."""
    # TODO: implement
    pass

def filter_csv_rows(filepath: str, column: str, value: str) -> list:
    """Return rows where column equals value."""
    # TODO: implement
    pass

if __name__ == '__main__':
    # Test with sample files
    sample_csv = "name,score\\nAlice,95\\nBob,87\\nCarol,92\\n"
    with open('/tmp/test_scores.csv', 'w') as f:
        f.write(sample_csv)

    rows = read_csv_to_dicts('/tmp/test_scores.csv')
    print(rows)  # [{'name': 'Alice', 'score': '95'}, ...]
'''
)

# solutions.zip — Reference solutions for all exercises
create_zip_with_content(
    zip_path=f'{WORKSHOP_DIR}/solutions.zip',
    filename='all_solutions.py',
    content='''# Workshop Solutions — Programming Fundamentals
# Reference implementations for Exercises 1-3

# ── Exercise 1 Solutions ──────────────────────────────────────────────────────

def greet(name: str) -> str:
    return f"Hello, {name}!"

def sum_list(numbers: list) -> int:
    return sum(numbers)

def find_max(numbers: list) -> int:
    if not numbers:
        raise ValueError("List is empty")
    result = numbers[0]
    for n in numbers[1:]:
        if n > result:
            result = n
    return result

# ── Exercise 2 Solutions ──────────────────────────────────────────────────────

def remove_duplicates(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def word_frequency(text: str) -> dict:
    freq = {}
    for word in text.lower().split():
        freq[word] = freq.get(word, 0) + 1
    return freq

def merge_sorted_lists(list1: list, list2: list) -> list:
    result = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i]); i += 1
        else:
            result.append(list2[j]); j += 1
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result

# ── Exercise 3 Solutions ──────────────────────────────────────────────────────

import os, json, csv

def read_csv_to_dicts(filepath: str) -> list:
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))

def write_json_report(data: dict, output_path: str) -> None:
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def count_lines_words(filepath: str) -> tuple:
    with open(filepath) as f:
        lines = f.readlines()
    words = sum(len(line.split()) for line in lines)
    return (len(lines), words)

def filter_csv_rows(filepath: str, column: str, value: str) -> list:
    rows = read_csv_to_dicts(filepath)
    return [r for r in rows if r.get(column) == value]
'''
)

print(f'ZIP files created in {WORKSHOP_DIR}:')
for fname in sorted(os.listdir(WORKSHOP_DIR)):
    fpath = os.path.join(WORKSHOP_DIR, fname)
    print(f'  {fname} ({os.path.getsize(fpath)} bytes)')


# ── Step 2: Create the workshop HTML page ────────────────────────────────────

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Python Programming Workshop — Sample Code Downloads</title>
  <style>
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 30px 20px;
      background: #f5f7fa;
      color: #333;
    }}
    h1 {{
      color: #2c3e50;
      border-bottom: 3px solid #3498db;
      padding-bottom: 10px;
    }}
    h2 {{
      color: #34495e;
      margin-top: 30px;
    }}
    .intro {{
      background: #eaf4fb;
      border-left: 4px solid #3498db;
      padding: 12px 18px;
      border-radius: 4px;
      margin: 20px 0;
    }}
    .download-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}
    .download-card {{
      background: #fff;
      border: 1px solid #dce3ec;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.06);
      transition: box-shadow 0.2s;
    }}
    .download-card:hover {{
      box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}
    .download-card h3 {{
      margin: 0 0 8px;
      color: #2c3e50;
      font-size: 1.05em;
    }}
    .download-card p {{
      margin: 0 0 14px;
      color: #666;
      font-size: 0.9em;
      line-height: 1.5;
    }}
    .btn-download {{
      display: inline-block;
      background: #3498db;
      color: #fff;
      padding: 8px 18px;
      border-radius: 5px;
      text-decoration: none;
      font-size: 0.9em;
      font-weight: 600;
      transition: background 0.2s;
    }}
    .btn-download:hover {{
      background: #2980b9;
    }}
    .btn-solutions {{
      background: #27ae60;
    }}
    .btn-solutions:hover {{
      background: #229954;
    }}
    footer {{
      margin-top: 50px;
      text-align: center;
      color: #999;
      font-size: 0.85em;
    }}
  </style>
</head>
<body>
  <h1>Python Programming Workshop</h1>
  <div class="intro">
    <strong>Welcome!</strong> Below you will find all sample code files and exercises for this workshop.
    Download the ZIP archives to your local machine to get started.
  </div>

  <h2>Exercise Files</h2>
  <div class="download-grid">
    <div class="download-card">
      <h3>Exercise 1 — Python Basics</h3>
      <p>Practice fundamental Python syntax: functions, string formatting, and basic algorithms. Includes 3 starter functions to complete.</p>
      <a class="btn-download" href="/exercise1.zip" download>Download exercise1.zip</a>
    </div>

    <div class="download-card">
      <h3>Exercise 2 — Data Structures</h3>
      <p>Hands-on work with lists, dictionaries, and sets. Implement duplicate removal, word frequency counting, and list merging.</p>
      <a class="btn-download" href="/exercise2.zip" download>Download exercise2.zip</a>
    </div>

    <div class="download-card">
      <h3>Exercise 3 — File I/O</h3>
      <p>Learn to read CSV files, write JSON reports, and process text files. Covers the <code>csv</code> and <code>json</code> standard library modules.</p>
      <a class="btn-download" href="/exercise3.zip" download>Download exercise3.zip</a>
    </div>

    <div class="download-card">
      <h3>Reference Solutions</h3>
      <p>Complete reference implementations for all exercises. Review after attempting each exercise on your own.</p>
      <a class="btn-download btn-solutions" href="/solutions.zip" download>Download solutions.zip</a>
    </div>
  </div>

  <footer>
    &copy; 2025 Python Programming Workshop &mdash; All rights reserved
  </footer>
</body>
</html>
"""

with open(f'{WORKSHOP_DIR}/index.html', 'w') as f:
    f.write(HTML_CONTENT)

print(f'Workshop HTML page created: {WORKSHOP_DIR}/index.html')


# ── Step 3: Create the empty download target directory ───────────────────────

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
# Ensure directory is empty (remove any leftover files)
for fname in os.listdir(DOWNLOAD_DIR):
    fpath = os.path.join(DOWNLOAD_DIR, fname)
    if os.path.isfile(fpath):
        os.remove(fpath)
print(f'Download directory ready (empty): {DOWNLOAD_DIR}')


# ── Step 4: Start local HTTP server serving the workshop files ───────────────

# Kill any leftover server on the same port
subprocess.run(
    ['bash', '-c', f'fuser -k {SERVER_PORT}/tcp 2>/dev/null; true'],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
time.sleep(0.5)

# Launch the HTTP server as a background process so it persists after the script exits
server_cmd = (
    f'python3 -m http.server {SERVER_PORT} --directory "{WORKSHOP_DIR}"'
)
server_env = os.environ.copy()
server_env["DISPLAY"] = ":0"
subprocess.Popen(
    ['bash', '-c', server_cmd],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    env=server_env,
)
time.sleep(1.5)

print(f'HTTP server started on port {SERVER_PORT}, serving {WORKSHOP_DIR}')


# ── Step 5: Kill any existing Chrome, set download dir, open workshop page ───

# Kill existing Chrome instances so we can write Preferences cleanly
subprocess.run(['pkill', '-f', 'google-chrome'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(['pkill', '-f', 'chromium'],       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2.0)

# Configure Chrome default download directory to ~/workshop_materials
import json as _json

CHROME_PREFS = os.path.expanduser('~/.config/google-chrome/Default/Preferences')
if os.path.exists(CHROME_PREFS):
    try:
        with open(CHROME_PREFS, 'r') as f:
            prefs = _json.load(f)
    except Exception:
        prefs = {}
else:
    os.makedirs(os.path.dirname(CHROME_PREFS), exist_ok=True)
    prefs = {}

# Set default download directory and disable download prompt
prefs.setdefault('download', {})
prefs['download']['default_directory'] = DOWNLOAD_DIR
prefs['download']['prompt_for_download'] = False
prefs['download']['directory_upgrade'] = True

# Also set safebrowsing to avoid warnings on ZIP downloads
prefs.setdefault('safebrowsing', {})
prefs['safebrowsing']['enabled'] = True

# Disable first-run / restore session prompts
prefs.setdefault('profile', {})
prefs['profile']['exit_type'] = 'Normal'
prefs['profile']['exited_cleanly'] = True
prefs.setdefault('session', {})
prefs['session']['restore_on_startup'] = 5  # open new tab page (not restore)

with open(CHROME_PREFS, 'w') as f:
    _json.dump(prefs, f, indent=2)

print(f'Chrome download directory configured: {DOWNLOAD_DIR}')

# ── Step 6: Launch Chrome on the workshop page ───────────────────────────────

WORKSHOP_URL = f'http://localhost:{SERVER_PORT}/index.html'

chrome_flags = (
    '--remote-debugging-port=1337 '
    '--no-first-run '
    '--no-default-browser-check '
    '--disable-extensions-except= '
    f'"{WORKSHOP_URL}"'
)
launch_gui(f'google-chrome {chrome_flags}', delay_sec=3.0)

# Start socat bridge (port 9222 → 1337) for CDP access
subprocess.run(['pkill', '-f', 'socat.*9222'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.3)
subprocess.Popen(
    ['socat', 'tcp-listen:9222,fork', 'tcp:localhost:1337'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

print(f'GUI_READY: Chrome opened on {WORKSHOP_URL}')
print(f'  Download target: {DOWNLOAD_DIR} (empty)')
print(f'  Available ZIPs: exercise1.zip, exercise2.zip, exercise3.zip, solutions.zip')
