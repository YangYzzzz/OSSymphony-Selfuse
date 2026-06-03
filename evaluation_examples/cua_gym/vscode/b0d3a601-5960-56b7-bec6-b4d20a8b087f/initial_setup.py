"""
Initial Setup: Install Indent Rainbow extension and configure custom colors
Task ID: vscode_ext_031
Domain: vs_code

Sets up VSCode in the pre-task state:
- Indent Rainbow extension is NOT installed
- indentRainbow.colors is NOT in settings.json
- A Python file with indented code is present for the agent to see visually
- VSCode is open with the Python file
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_031'
VSCODE_USER = os.path.join('/home/user', '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
SAMPLE_FILE = os.path.join(WORKDIR, f'{TASK_ID}_sample.py')


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


def ensure_extension_not_installed():
    """Make sure Indent Rainbow is NOT installed in initial state."""
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True
    )
    installed = result.stdout.strip().lower()
    if 'oderwat.indent-rainbow' in installed:
        subprocess.run(
            ['code', '--uninstall-extension', 'oderwat.indent-rainbow'],
            capture_output=True
        )
        print('Uninstalled oderwat.indent-rainbow to reset initial state.')
    else:
        print('oderwat.indent-rainbow is not installed (correct initial state).')


def setup_settings():
    """Ensure settings.json exists but does NOT contain indentRainbow.colors."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings (or start empty)
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove indentRainbow settings if they accidentally exist
    settings.pop('indentRainbow.colors', None)
    settings.pop('indentRainbow.includedLanguages', None)
    settings.pop('indentRainbow.excludedLanguages', None)

    # Ensure some basic settings are present for realism
    settings.setdefault('editor.fontSize', 14)
    settings.setdefault('editor.tabSize', 4)
    settings.setdefault('editor.wordWrap', 'off')

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Settings configured (no indentRainbow.colors): {SETTINGS_PATH}')


def create_sample_python_file():
    """Create a Python file with meaningful indented code for the agent to see."""
    content = '''\
# Data Processing Pipeline
# Demonstrates multiple indentation levels for Indent Rainbow

import os
import json
from typing import List, Dict, Optional


class DataProcessor:
    """Handles data ingestion and transformation."""

    def __init__(self, source_dir: str, output_dir: str):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.records: List[Dict] = []

    def load_data(self, filename: str) -> bool:
        """Load JSON data from a file."""
        filepath = os.path.join(self.source_dir, filename)
        try:
            with open(filepath, 'r') as f:
                raw = json.load(f)
                for item in raw:
                    if 'id' in item and 'value' in item:
                        self.records.append({
                            'id': item['id'],
                            'value': item['value'],
                            'processed': False
                        })
            return True
        except FileNotFoundError:
            print(f'File not found: {filepath}')
            return False
        except json.JSONDecodeError as e:
            print(f'JSON parse error: {e}')
            return False

    def transform(self, multiplier: float = 1.0) -> List[Dict]:
        """Apply transformation to loaded records."""
        results = []
        for record in self.records:
            if not record['processed']:
                try:
                    transformed_value = record['value'] * multiplier
                    if transformed_value > 0:
                        results.append({
                            'id': record['id'],
                            'original': record['value'],
                            'transformed': transformed_value
                        })
                        record['processed'] = True
                    else:
                        print(f"Skipping non-positive value for id={record['id']}")
                except TypeError as e:
                    print(f"Type error processing id={record['id']}: {e}")
        return results

    def save_results(self, results: List[Dict], filename: str) -> Optional[str]:
        """Save processed results to output directory."""
        os.makedirs(self.output_dir, exist_ok=True)
        outpath = os.path.join(self.output_dir, filename)
        with open(outpath, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'Saved {len(results)} records to {outpath}')
        return outpath


def main():
    processor = DataProcessor(
        source_dir='/home/user/data/input',
        output_dir='/home/user/data/output'
    )

    files = ['sales_q1.json', 'sales_q2.json', 'sales_q3.json']
    for fname in files:
        if processor.load_data(fname):
            results = processor.transform(multiplier=1.15)
            if results:
                out = processor.save_results(results, f'processed_{fname}')
                print(f'Output written: {out}')
            else:
                print(f'No results for {fname}')
        else:
            print(f'Skipped: {fname}')


if __name__ == '__main__':
    main()
'''
    with open(SAMPLE_FILE, 'w') as f:
        f.write(content)
    print(f'Sample Python file created: {SAMPLE_FILE}')


def create_initial():
    # 1. Ensure extension is not installed
    ensure_extension_not_installed()

    # 2. Configure settings without indentRainbow keys
    setup_settings()

    # 3. Create a sample Python file with multiple indent levels
    create_sample_python_file()

    # 4. Launch VSCode with the sample file (GUI-ready state)
    launch_gui(f'code "{SAMPLE_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
