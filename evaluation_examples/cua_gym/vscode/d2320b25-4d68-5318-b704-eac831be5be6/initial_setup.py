"""
Initial Setup: Open calc.js in VSCode with a Node.js debug launch configuration
Task ID: vscode_dbg_005
Domain: vs_code

Creates:
  - /home/user/projects/calculator/calc.js  (simple calculator script)
  - /home/user/projects/calculator/.vscode/launch.json  (Node.js Launch config)
  Opens VSCode with calc.js in the editor, ready for F5 debugging.

IMPORTANT: Does NOT create debug_output.txt — that file is only produced by
golden_patch.py (simulating the agent pressing F5 to run a debug session).
The reward script checks for debug_output.txt to determine task completion.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_005'
PROJECT_DIR = f'{WORKDIR}/projects/calculator'
CALC_JS = f'{PROJECT_DIR}/calc.js'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
LAUNCH_JSON = f'{VSCODE_DIR}/launch.json'


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Ensure debug_output.txt does NOT exist in the initial state.
    # This file is only created by golden_patch.py (after the debug session runs).
    # Removing it ensures reward(initial_env) == 0.0.
    debug_output = f'{PROJECT_DIR}/debug_output.txt'
    if os.path.exists(debug_output):
        os.remove(debug_output)
        print(f'Removed pre-existing debug_output.txt from initial env')

    # Create calc.js — a realistic calculator script with console output
    calc_js_content = """\
// Simple Calculator — calc.js
// Performs basic arithmetic operations and prints results

function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b === 0) {
        throw new Error("Division by zero is not allowed");
    }
    return a / b;
}

function runCalculations() {
    const pairs = [
        [15, 4],
        [120, 8],
        [37, 19],
        [256, 16],
        [88, 11],
    ];

    console.log("=== Calculator Results ===");
    for (const [x, y] of pairs) {
        console.log(`${x} + ${y} = ${add(x, y)}`);
        console.log(`${x} - ${y} = ${subtract(x, y)}`);
        console.log(`${x} * ${y} = ${multiply(x, y)}`);
        console.log(`${x} / ${y} = ${divide(x, y)}`);
        console.log("-------------------------");
    }
    console.log("All calculations complete.");
}

runCalculations();
"""
    with open(CALC_JS, 'w') as f:
        f.write(calc_js_content)
    print(f'Created: {CALC_JS}')

    # Create .vscode/launch.json — Node.js Launch Program config targeting calc.js
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Launch Program",
                "skipFiles": [
                    "<node_internals>/**"
                ],
                "program": "${workspaceFolder}/calc.js"
            }
        ]
    }
    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)
    print(f'Created: {LAUNCH_JSON}')

    # GUI-ready startup: open VSCode with the calculator project folder
    # so that calc.js is visible and ready for the agent to press F5
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Give VSCode time to load, then open the specific file
    time.sleep(2.0)
    launch_gui(f'code "{CALC_JS}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with calc.js, DISPLAY=:0')


create_initial()
