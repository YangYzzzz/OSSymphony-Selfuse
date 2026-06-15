"""
Initial Setup: Node.js performance profiling project with CPU bottleneck
Task ID: vscode_gf6_027
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_027'
PROJECT_DIR = f'{WORKDIR}/projects/node-perf'

# nvm setup prefix for shell commands
NVM_PREFIX = 'export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '


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


def run_cmd(cmd, **kwargs):
    """Run a shell command and print output."""
    print(f'Running: {cmd[:200]}')
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        timeout=kwargs.get('timeout', 120),
        executable='/bin/bash'
    )
    if result.stdout:
        print(result.stdout[-500:])
    if result.returncode != 0 and result.stderr:
        print(f'STDERR: {result.stderr[-500:]}')
    return result


def create_initial():
    # Install Node.js 18 via nvm if not present
    node_check = subprocess.run('which node', shell=True, capture_output=True, text=True)
    if node_check.returncode != 0:
        print('Installing Node.js 18 via nvm...')
        run_cmd('curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash', timeout=60)
        run_cmd(NVM_PREFIX + 'nvm install 18', timeout=120)
        run_cmd(NVM_PREFIX + 'node --version && npm --version')

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src/workers', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "node-perf",
        "version": "1.0.0",
        "description": "Node.js API performance testing project",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "node --watch src/index.js"
        },
        "dependencies": {
            "express": "^4.18.2"
        },
        "keywords": ["nodejs", "api", "performance"],
        "author": "Dev Team",
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/index.js --- Express API with POST /api/process
    index_js = '''\
const express = require('express');
const { processNumbers } = require('./workers/processor');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

app.get('/health', (req, res) => {
    res.json({ status: 'ok', uptime: process.uptime() });
});

app.post('/api/process', async (req, res) => {
    try {
        const { numbers } = req.body;
        if (!Array.isArray(numbers)) {
            return res.status(400).json({ error: 'numbers must be an array' });
        }
        const startTime = Date.now();
        const result = processNumbers(numbers);
        const duration = Date.now() - startTime;
        res.json({
            result,
            processingTime: `${duration}ms`,
            itemCount: numbers.length
        });
    } catch (err) {
        console.error('Processing error:', err);
        res.status(500).json({ error: 'Internal processing error' });
    }
});

app.listen(PORT, () => {
    console.log(`Node-perf API server running on port ${PORT}`);
});
'''
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # --- src/workers/processor.js --- CPU bottleneck: synchronous JSON.parse in a loop
    processor_js = '''\
/**
 * Process an array of numbers through intensive computation.
 * WARNING: This implementation has a known CPU bottleneck -
 * synchronous JSON.parse/stringify in a tight loop blocks the event loop.
 */

function processNumbers(numbers) {
    const results = [];

    for (const item of numbers) {
        // CPU-intensive: synchronous JSON.parse in a loop (10,000 iterations)
        let processed = item;
        for (let i = 0; i < 10000; i++) {
            processed = JSON.parse(JSON.stringify(processed));
        }

        // Apply transformations after parsing
        const value = typeof processed === 'number' ? processed : Number(processed);
        results.push({
            original: item,
            squared: value * value,
            sqrt: Math.sqrt(Math.abs(value)),
            normalized: value / (Math.abs(value) + 1),
            timestamp: Date.now()
        });
    }

    return results;
}

module.exports = { processNumbers };
'''
    with open(f'{PROJECT_DIR}/src/workers/processor.js', 'w') as f:
        f.write(processor_js)

    # --- .gitignore ---
    gitignore = '''\
node_modules/
.clinic/
*.heapsnapshot
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = '''\
# Node Performance API

A Node.js Express API for processing arrays of numbers.

## Endpoints

- `GET /health` - Health check
- `POST /api/process` - Process an array of numbers

## Usage

```bash
npm install
npm start
```

Send a POST request:
```bash
curl -X POST http://localhost:3000/api/process \\
  -H "Content-Type: application/json" \\
  -d '{"numbers": [1, 2, 3, 4, 5]}'
```

## Known Issues

The processing endpoint is slow under load due to synchronous operations
in the processor module.
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Install npm dependencies
    print('Installing npm dependencies...')
    run_cmd(NVM_PREFIX + f'cd {PROJECT_DIR} && npm install', timeout=120)

    print(f'Initial project created: {PROJECT_DIR}')

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
