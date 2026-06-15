"""
Initial Setup: Create React TypeScript snippets task — initial state
Task ID: vscode_code_096
Domain: vs_code

Sets up VSCode with NO typescriptreact.json snippets file, so the agent must
create the four React TypeScript snippets from scratch.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_096'
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
SNIPPET_FILE = os.path.join(SNIPPETS_DIR, 'typescriptreact.json')

# A sample React TypeScript workspace for the agent to work in
WORKSPACE_DIR = os.path.join(HOME, TASK_ID)


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # 1. Ensure snippets directory exists
    os.makedirs(SNIPPETS_DIR, exist_ok=True)

    # 2. Remove any existing typescriptreact.json so the initial state is clean
    if os.path.exists(SNIPPET_FILE):
        os.remove(SNIPPET_FILE)
        print(f'Removed existing snippet file: {SNIPPET_FILE}')

    # 3. Create a simple React TypeScript workspace for the agent to work in
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a sample .tsx file so VSCode opens with a TypeScript React context
    sample_tsx = os.path.join(WORKSPACE_DIR, 'App.tsx')
    if not os.path.exists(sample_tsx):
        with open(sample_tsx, 'w') as f:
            f.write(
                "// React TypeScript App\n"
                "// TODO: Create snippets for rfc, ust, uef, and hook\n\n"
                "import React from 'react';\n\n"
                "function App() {\n"
                "  return (\n"
                "    <div>\n"
                "      <h1>Hello, React TypeScript!</h1>\n"
                "    </div>\n"
                "  );\n"
                "}\n\n"
                "export default App;\n"
            )
        print(f'Created sample .tsx file: {sample_tsx}')

    print(f'Initial state ready: {SNIPPET_FILE} does not exist')
    print(f'Workspace: {WORKSPACE_DIR}')

    # 4. Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with workspace, DISPLAY=:0')


create_initial()
