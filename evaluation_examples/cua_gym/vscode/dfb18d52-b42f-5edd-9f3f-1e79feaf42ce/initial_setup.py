"""
Initial Setup: Create a JS file with a 20-line sequential algorithm for multi-cursor editing task.
Task ID: vscode_rf_038
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_038'
PROJECT_DIR = f'{WORKDIR}/projects/debug'
OUTPUT = f'{PROJECT_DIR}/steps.js'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Build a realistic sequential algorithm in JavaScript
    # Lines 1-9: preamble, lines 10-29: algorithm steps, lines 30+: closing
    lines = []

    # Lines 1-9: preamble
    lines.append('/**')
    lines.append(' * Data Pipeline Processor')
    lines.append(' * Processes raw sensor data through a sequential cleaning pipeline.')
    lines.append(' */')
    lines.append('')
    lines.append('const fs = require("fs");')
    lines.append('const path = require("path");')
    lines.append('')
    lines.append('function processPipeline(rawData) {')

    # Lines 10-29: 20 algorithm steps (these are the lines to be edited)
    lines.append('  let data = JSON.parse(JSON.stringify(rawData));')            # line 10
    lines.append('  data = data.filter(record => record.timestamp !== null);')   # line 11
    lines.append('  data = data.map(r => ({ ...r, timestamp: new Date(r.timestamp) }));')  # line 12
    lines.append('  data.sort((a, b) => a.timestamp - b.timestamp);')            # line 13
    lines.append('  data = data.filter(r => r.value >= 0 && r.value <= 1000);')  # line 14
    lines.append('  let mean = data.reduce((s, r) => s + r.value, 0) / data.length;')  # line 15
    lines.append('  let stdDev = Math.sqrt(data.reduce((s, r) => s + (r.value - mean) ** 2, 0) / data.length);')  # line 16
    lines.append('  data = data.filter(r => Math.abs(r.value - mean) <= 3 * stdDev);')  # line 17
    lines.append('  data = data.map(r => ({ ...r, normalized: (r.value - mean) / stdDev }));')  # line 18
    lines.append('  data = data.map(r => ({ ...r, sensorId: r.sensorId.trim().toUpperCase() }));')  # line 19
    lines.append('  let grouped = {};')                                          # line 20
    lines.append('  data.forEach(r => { grouped[r.sensorId] = grouped[r.sensorId] || []; grouped[r.sensorId].push(r); });')  # line 21
    lines.append('  Object.keys(grouped).forEach(k => { grouped[k].sort((a, b) => a.timestamp - b.timestamp); });')  # line 22
    lines.append('  data = data.map(r => ({ ...r, hour: r.timestamp.getHours() }));')  # line 23
    lines.append('  data = data.map(r => ({ ...r, dayOfWeek: r.timestamp.getDay() }));')  # line 24
    lines.append('  let duplicates = new Set();')                                # line 25
    lines.append('  data = data.filter(r => { let key = r.sensorId + "-" + r.timestamp.getTime(); if (duplicates.has(key)) return false; duplicates.add(key); return true; });')  # line 26
    lines.append('  data = data.map(r => ({ ...r, quality: r.value > mean ? "high" : "low" }));')  # line 27
    lines.append('  data = data.map((r, i) => ({ ...r, index: i + 1 }));')       # line 28
    lines.append('  let summary = { total: data.length, sensors: Object.keys(grouped).length, avgValue: mean.toFixed(2) };')  # line 29

    # Lines 30+: closing
    lines.append('  return { processedData: data, summary: summary, groups: grouped };')
    lines.append('}')
    lines.append('')
    lines.append('module.exports = { processPipeline };')

    content = '\n'.join(lines) + '\n'

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Also create a small helper file so the project feels realistic
    helper_path = f'{PROJECT_DIR}/config.json'
    if not os.path.exists(helper_path):
        import json
        config = {
            "inputDir": "./data/raw",
            "outputDir": "./data/processed",
            "logLevel": "debug",
            "maxRecords": 50000,
            "outlierThreshold": 3.0
        }
        with open(helper_path, 'w') as f:
            json.dump(config, f, indent=2)

    # Kill any existing VSCode instances for a clean state (use exact match to avoid killing python)
    subprocess.run(['pkill', '-x', 'code'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    # Launch VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)

    # Open the specific file
    launch_gui(f'code --goto "{OUTPUT}:10"', delay_sec=2.0)

    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
