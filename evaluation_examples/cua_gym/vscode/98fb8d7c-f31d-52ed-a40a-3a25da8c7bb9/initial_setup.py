"""
Initial Setup: Open ~/projects/test-runner in VSCode with test.js (no breakpoints)
Task ID: vscode_dbg_012
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import sqlite3
import hashlib
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_012'
PROJECT_DIR = f'{WORKDIR}/projects/test-runner'
JS_FILE = f'{PROJECT_DIR}/test.js'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create test.js — line 15 must be console.log(i) inside a for loop
    # Lines 1-14 come before line 15, line 15 is console.log(i)
    js_content = """\
// test-runner: basic loop test
// Runs a series of iteration checks

const assert = require('assert');

function runTests() {
    let results = [];

    // Test 1: basic iteration test
    for (let i = 0; i < 10; i++) {
        // Process each iteration value
        let value = i * 2;
        let label = 'iteration-' + i;
        results.push({ i, value, label });
        console.log(i);
        if (i === 0) {
            assert.strictEqual(value, 0);
        } else if (i === 5) {
            assert.strictEqual(value, 10);
        }
    }

    // Test 2: verify results array
    assert.strictEqual(results.length, 10);
    console.log('All tests passed. Results:', results.length);

    // Test 3: check specific entries
    const midpoint = results[5];
    assert.strictEqual(midpoint.i, 5);
    assert.strictEqual(midpoint.value, 10);
    assert.strictEqual(midpoint.label, 'iteration-5');

    return results;
}

module.exports = { runTests };

if (require.main === module) {
    try {
        const r = runTests();
        console.log('Success:', r.length, 'iterations completed');
    } catch (e) {
        console.error('Test failed:', e.message);
        process.exit(1);
    }
}
"""
    with open(JS_FILE, 'w') as f:
        f.write(js_content)
    print(f'Created: {JS_FILE}')

    # Verify line 15 is console.log(i)
    with open(JS_FILE, 'r') as f:
        lines = f.readlines()
    line15 = lines[14].strip()  # 0-indexed: line 15 = index 14
    print(f'Line 15: {repr(line15)}')
    assert 'console.log(i)' in line15, f'Line 15 must contain console.log(i), got: {line15}'

    # Create package.json for the project
    package_json = {
        "name": "test-runner",
        "version": "1.0.0",
        "description": "Simple test runner with iteration tests",
        "main": "test.js",
        "scripts": {
            "test": "node test.js",
            "start": "node test.js"
        },
        "keywords": ["testing", "node"],
        "author": "dev",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created: {PROJECT_DIR}/package.json')

    # Ensure no breakpoints exist in VSCode workspace storage for this project
    # The workspace storage folder is the MD5 hash of the workspace URI
    workspace_uri = f'file://{PROJECT_DIR}'
    ws_hash = hashlib.md5(workspace_uri.encode('utf-8')).hexdigest()
    ws_storage_dir = f'{WORKDIR}/.config/Code/User/workspaceStorage/{ws_hash}'

    if os.path.exists(ws_storage_dir):
        db_path = f'{ws_storage_dir}/state.vscdb'
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Remove any existing breakpoints
            cursor.execute("DELETE FROM ItemTable WHERE key = 'debug.breakpoint'")
            conn.commit()
            conn.close()
            print(f'Cleared breakpoints from workspace storage: {ws_storage_dir}')
    else:
        print(f'Workspace storage not yet created (will be created by VSCode): {ws_storage_dir}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')
    print(f'Initial file created: {JS_FILE}')
    print(f'No breakpoints set — initial state ready for task')


create_initial()
