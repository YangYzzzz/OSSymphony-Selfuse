"""
Initial Setup: Open ~/projects/data-processor in VSCode and prepare for logpoint task
Task ID: vscode_dbg_013
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_013'
PROJECT_DIR = f'{WORKDIR}/projects/data-processor'
PROCESS_JS = f'{PROJECT_DIR}/process.js'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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

    # Create process.js with realistic content
    # Line 20 (1-indexed) is: "        processItem(item);"
    process_js_content = """\
/**
 * Data Processor Module
 * Handles batch processing of data items
 */

const fs = require('fs');

function processItem(item) {
    if (!item || typeof item !== "object") return null;
    return {
        id: item.id,
        name: (item.name || '').trim(),
        value: Number(item.value) || 0,
        processed: true
    };
}

function processAll(items) {
    for (const item of items) {
        processItem(item);
        const result = processItem(item);
        console.log(result);
    }
}

function loadData(filePath) {
    try {
        const raw = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(raw);
    } catch (err) {
        console.error("Error loading data:", err.message);
        return [];
    }
}

module.exports = { processItem, processAll, loadData };

if (require.main === module) {
    const items = loadData('./data.json');
    processAll(items);
}
"""
    with open(PROCESS_JS, 'w') as f:
        f.write(process_js_content)
    print(f'Created: {PROCESS_JS}')

    # Verify line 20 content
    lines = process_js_content.split('\n')
    print(f'Line 20: {repr(lines[19])}')  # 0-indexed index 19 = line 20

    # Create sample data.json with realistic content
    data_json = [
        {"id": 1, "name": "Alpha Widget", "value": 142.50},
        {"id": 2, "name": "Beta Component", "value": 89.99},
        {"id": 3, "name": "Gamma Module", "value": 215.00},
        {"id": 4, "name": "Delta Assembly", "value": 67.25},
        {"id": 5, "name": "Epsilon Unit", "value": 310.75},
        {"id": 6, "name": "Zeta Part", "value": 55.00},
        {"id": 7, "name": "Eta Device", "value": 198.40},
        {"id": 8, "name": "Theta Piece", "value": 423.60}
    ]
    with open(f'{PROJECT_DIR}/data.json', 'w') as f:
        json.dump(data_json, f, indent=2)
    print(f'Created: {PROJECT_DIR}/data.json')

    # Create package.json
    package_json = {
        "name": "data-processor",
        "version": "1.0.0",
        "description": "Data processing pipeline utility",
        "main": "process.js",
        "scripts": {
            "start": "node process.js"
        },
        "author": "Dev Team",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created: {PROJECT_DIR}/package.json')

    # Create a minimal launch.json WITHOUT any breakpoints or logpoints
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Run Data Processor",
                "program": "${workspaceFolder}/process.js",
                "console": "integratedTerminal"
            }
        ]
    }
    with open(f'{VSCODE_DIR}/launch.json', 'w') as f:
        json.dump(launch_json, f, indent=4)
    print(f'Created: {VSCODE_DIR}/launch.json')

    print(f'Project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with data-processor project at DISPLAY=:0')


create_initial()
