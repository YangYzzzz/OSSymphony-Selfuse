"""
Initial Setup: Add custom keyboard shortcut Ctrl+Shift+L for Transform to Lowercase
Task ID: vscode_prod_016
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_016'
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')
PROJECT_DIR = os.path.join(HOME, 'projects', 'textutils')
SAMPLE_FILE = os.path.join(PROJECT_DIR, 'sample.txt')


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
    # 1. Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # 2. Create sample.txt with mixed-case text content
    sample_content = """Product Requirements Document - TextUtils v2.3
============================================

Executive Summary
-----------------
The TextUtils project aims to DELIVER a comprehensive SET of text
manipulation UTILITIES for developers and CONTENT creators. This
document OUTLINES the key features, TIMELINE, and resource
REQUIREMENTS for the upcoming release.

Key Features
------------
1. BULK Text Transformation
   - Convert SELECTED text to uppercase, lowercase, or Title Case
   - Support for MULTIPLE cursor selections
   - PRESERVE formatting while changing case

2. Smart LINE Operations
   - SORT lines alphabetically or by LENGTH
   - REMOVE duplicate lines from SELECTION
   - REVERSE line order within selected BLOCK

3. Advanced FIND and Replace
   - REGEX-powered search with capture GROUPS
   - BATCH replacement across multiple FILES
   - PREVIEW changes before applying

Team Members
------------
Lead Developer: Sarah CHEN (sarah.chen@textutils.dev)
QA Engineer: Marcus JOHNSON (marcus.j@textutils.dev)
UX Designer: Priya SHARMA (priya.s@textutils.dev)
Backend Lead: James O'BRIEN (james.ob@textutils.dev)

Timeline
--------
Phase 1: CORE utilities - March 15, 2025
Phase 2: ADVANCED features - April 30, 2025
Phase 3: INTEGRATION testing - May 15, 2025
Phase 4: PUBLIC release - June 1, 2025

Notes
-----
The CURRENT implementation uses a modular ARCHITECTURE that allows
EASY extension of FUNCTIONALITY. Each utility is IMPLEMENTED as an
independent MODULE that can be LOADED on demand.
"""
    with open(SAMPLE_FILE, 'w') as f:
        f.write(sample_content)
    print(f'Created sample file: {SAMPLE_FILE}')

    # 3. Create a couple of extra project files for realism
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write("# TextUtils\n\nA collection of text manipulation utilities.\n\n## Installation\n\n```bash\nnpm install textutils\n```\n")

    utils_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(utils_dir, exist_ok=True)
    with open(os.path.join(utils_dir, 'transform.js'), 'w') as f:
        f.write("""// Text transformation utilities
function toLowerCase(text) {
    return text.toLowerCase();
}

function toUpperCase(text) {
    return text.toUpperCase();
}

function toTitleCase(text) {
    return text.replace(/\\w\\S*/g, (txt) => {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

module.exports = { toLowerCase, toUpperCase, toTitleCase };
""")

    # 4. Ensure keybindings.json is an empty array (no custom bindings)
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'Created empty keybindings.json: {KEYBINDINGS_PATH}')

    # 5. Launch VSCode with the project folder and open sample.txt
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{SAMPLE_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
