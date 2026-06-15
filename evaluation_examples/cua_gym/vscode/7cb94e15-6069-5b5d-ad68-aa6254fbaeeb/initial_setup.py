"""
Initial Setup: Delete temp.js, debug.js, and test_scratch.py from project root
Task ID: vscode_file_056
Domain: vs_code

Creates a project directory at /home/user/project with the following structure:
- project/
  - src/
    - app.js
    - main.py
  - temp.js         (temporary scratch file - agent will delete this)
  - debug.js        (debug artifact - agent will delete this)
  - test_scratch.py (temporary test - agent will delete this)
  - package.json
  - requirements.txt
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_056'
PROJECT_DIR = f'{WORKDIR}/project'


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


def write_file(path, lines):
    """Write a list of strings as lines to a file."""
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def create_initial():
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # --- src/app.js ---
    write_file(f'{PROJECT_DIR}/src/app.js', [
        '// app.js - Main application entry point',
        "const express = require('express');",
        'const app = express();',
        'const PORT = process.env.PORT || 3000;',
        '',
        'app.use(express.json());',
        '',
        "app.get('/', (req, res) => {",
        "    res.json({ message: 'Welcome to the API', version: '1.2.0' });",
        '});',
        '',
        "app.get('/health', (req, res) => {",
        '    res.json({ status: \'healthy\', uptime: process.uptime() });',
        '});',
        '',
        "app.post('/data', (req, res) => {",
        '    const { payload } = req.body;',
        '    if (!payload) {',
        "        return res.status(400).json({ error: 'Missing payload' });",
        '    }',
        "    res.json({ received: payload, timestamp: new Date().toISOString() });",
        '});',
        '',
        'app.listen(PORT, () => {',
        '    console.log(`Server running on port ${PORT}`);',
        '});',
        '',
        'module.exports = app;',
    ])

    # --- src/main.py ---
    write_file(f'{PROJECT_DIR}/src/main.py', [
        '#!/usr/bin/env python3',
        '# main.py - Data processing pipeline entry point',
        '',
        'import argparse',
        'import json',
        'import logging',
        'import os',
        'from pathlib import Path',
        '',
        'logging.basicConfig(',
        '    level=logging.INFO,',
        "    format='%(asctime)s [%(levelname)s] %(message)s'",
        ')',
        "logger = logging.getLogger(__name__)",
        '',
        '',
        'def load_config(config_path: str) -> dict:',
        '    with open(config_path, \'r\') as f:',
        '        return json.load(f)',
        '',
        '',
        'def process_records(records: list) -> list:',
        '    results = []',
        '    for record in records:',
        '        processed = {',
        "            'id': record.get('id'),",
        "            'value': record.get('value', 0) * 1.15,",
        "            'status': 'processed',",
        '        }',
        '        results.append(processed)',
        "    logger.info(f'Processed {len(results)} records')",
        '    return results',
        '',
        '',
        'def main():',
        "    parser = argparse.ArgumentParser(description='Data processing pipeline')",
        "    parser.add_argument('--config', default='config.json', help='Config file path')",
        "    parser.add_argument('--output', default='output.json', help='Output file path')",
        '    args = parser.parse_args()',
        '',
        "    logger.info('Starting pipeline')",
        '    config = load_config(args.config) if Path(args.config).exists() else {}',
        "    records = config.get('records', [])",
        '    results = process_records(records)',
        '',
        "    with open(args.output, 'w') as f:",
        '        json.dump(results, f, indent=2)',
        '',
        "    logger.info(f'Results written to {args.output}')",
        '',
        '',
        "if __name__ == '__main__':",
        '    main()',
    ])

    # --- temp.js (scratch file, to be deleted by agent) ---
    write_file(f'{PROJECT_DIR}/temp.js', [
        '// temp.js - Temporary scratch file (DELETE ME)',
        '// Used during development to test API responses',
        '// NOT needed in production',
        '',
        "const axios = require('axios');",
        '',
        'async function quickTest() {',
        '    try {',
        "        const res = await axios.get('http://localhost:3000/health');",
        "        console.log('Health check:', res.data);",
        '',
        "        const postRes = await axios.post('http://localhost:3000/data', {",
        "            payload: 'test-value-123'",
        '        });',
        "        console.log('Post response:', postRes.data);",
        '    } catch (err) {',
        "        console.error('Test failed:', err.message);",
        '    }',
        '}',
        '',
        'quickTest();',
    ])

    # --- debug.js (debug artifact, to be deleted by agent) ---
    write_file(f'{PROJECT_DIR}/debug.js', [
        '// debug.js - Debug helper (DELETE ME)',
        '// Dumps internal state and request/response logs',
        '// Created during sprint debugging session 2025-02-14',
        '',
        "const fs = require('fs');",
        "const path = require('path');",
        '',
        'function dumpState(label, data) {',
        '    const timestamp = new Date().toISOString();',
        '    const entry = `[${timestamp}] ${label}: ${JSON.stringify(data, null, 2)}\\n`;',
        '    fs.appendFileSync(path.join(__dirname, \'debug.log\'), entry);',
        '    console.debug(entry);',
        '}',
        '',
        'function traceRequest(req) {',
        '    dumpState(\'REQUEST\', {',
        '        method: req.method,',
        '        url: req.url,',
        '        headers: req.headers,',
        '        body: req.body,',
        '    });',
        '}',
        '',
        'function traceResponse(res, body) {',
        '    dumpState(\'RESPONSE\', {',
        '        status: res.statusCode,',
        '        body: body,',
        '    });',
        '}',
        '',
        'module.exports = { dumpState, traceRequest, traceResponse };',
    ])

    # --- test_scratch.py (temporary test, to be deleted by agent) ---
    write_file(f'{PROJECT_DIR}/test_scratch.py', [
        '#!/usr/bin/env python3',
        '# test_scratch.py - Temporary ad-hoc test (DELETE ME)',
        '# Quick sanity checks written during development',
        '# Superseded by proper test suite in tests/',
        '',
        'import json',
        'import os',
        'import sys',
        '',
        "sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))",
        '',
        '',
        'def quick_test_process_records():',
        '    from main import process_records',
        '    sample = [',
        "        {'id': 1, 'value': 100},",
        "        {'id': 2, 'value': 200},",
        "        {'id': 3, 'value': 0},",
        '    ]',
        '    results = process_records(sample)',
        '    assert len(results) == 3',
        '    assert results[0][\'value\'] == 115.0',
        '    assert results[1][\'value\'] == 230.0',
        "    assert results[0]['status'] == 'processed'",
        "    print('quick_test_process_records: PASSED')",
        '',
        '',
        "def quick_test_load_config(tmp_path='/tmp/test_config.json'):",
        '    from main import load_config',
        "    config_data = {'records': [{'id': 10, 'value': 50}]}",
        "    with open(tmp_path, 'w') as f:",
        '        json.dump(config_data, f)',
        '    loaded = load_config(tmp_path)',
        '    assert loaded == config_data',
        '    os.remove(tmp_path)',
        "    print('quick_test_load_config: PASSED')",
        '',
        '',
        "if __name__ == '__main__':",
        '    quick_test_process_records()',
        '    quick_test_load_config()',
        "    print('All scratch tests passed.')",
    ])

    # --- package.json ---
    import json
    package_data = {
        "name": "data-api-service",
        "version": "1.2.0",
        "description": "Lightweight REST API for data processing",
        "main": "src/app.js",
        "scripts": {
            "start": "node src/app.js",
            "dev": "nodemon src/app.js",
            "lint": "eslint src/",
            "test": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "axios": "^1.6.0",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "eslint": "^8.55.0",
            "jest": "^29.7.0",
            "nodemon": "^3.0.2",
            "supertest": "^6.3.3"
        },
        "engines": {
            "node": ">=18.0.0"
        },
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_data, f, indent=2)
        f.write('\n')

    # --- requirements.txt ---
    write_file(f'{PROJECT_DIR}/requirements.txt', [
        '# requirements.txt - Python dependencies for data processing pipeline',
        'argparse>=1.4.0',
        'requests>=2.31.0',
        'pandas>=2.1.0',
        'numpy>=1.26.0',
        'pydantic>=2.5.0',
        'python-dotenv>=1.0.0',
        'pytest>=7.4.0',
        'pytest-cov>=4.1.0',
    ])

    print(f'Project structure created at: {PROJECT_DIR}')
    print('Files created:')
    print('  project/src/app.js')
    print('  project/src/main.py')
    print('  project/temp.js         <- to be deleted by agent')
    print('  project/debug.js        <- to be deleted by agent')
    print('  project/test_scratch.py <- to be deleted by agent')
    print('  project/package.json')
    print('  project/requirements.txt')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder on DISPLAY=:0')


create_initial()
