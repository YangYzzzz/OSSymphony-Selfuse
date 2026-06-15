"""
Initial Setup: VSCode Mocha debug project without launch.json
Task ID: vscode_dbg_039
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_039'
PROJECT_DIR = f'{WORKDIR}/projects/mocha-debug'
# Use nvm-installed npm; fallback to PATH lookup
NVM_NODE_BIN = f'{WORKDIR}/.nvm/versions/node/v18.20.8/bin'
NPM_BIN = f'{NVM_NODE_BIN}/npm'

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
    os.makedirs(f'{PROJECT_DIR}/test', exist_ok=True)

    # Create package.json with mocha as devDependency
    package_json = {
        "name": "mocha-debug",
        "version": "1.0.0",
        "description": "A sample Node.js project with Mocha tests",
        "main": "index.js",
        "scripts": {
            "test": "mocha --recursive test/"
        },
        "keywords": [],
        "author": "Dev Team",
        "license": "MIT",
        "devDependencies": {
            "mocha": "^10.2.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f'Created: {PROJECT_DIR}/package.json')

    # Create a realistic test file
    test_js_content = '''const assert = require('assert');

describe('Calculator', function () {
  describe('#add()', function () {
    it('should return 4 when adding 2 and 2', function () {
      assert.strictEqual(2 + 2, 4);
    });

    it('should return 0 when adding positive and negative numbers', function () {
      assert.strictEqual(5 + (-5), 0);
    });
  });

  describe('#multiply()', function () {
    it('should return 6 when multiplying 2 and 3', function () {
      assert.strictEqual(2 * 3, 6);
    });

    it('should return 0 when multiplying by zero', function () {
      assert.strictEqual(5 * 0, 0);
    });
  });

  describe('#divide()', function () {
    it('should return 2 when dividing 6 by 3', function () {
      assert.strictEqual(6 / 3, 2);
    });

    it('should return Infinity when dividing by zero', function () {
      assert.strictEqual(1 / 0, Infinity);
    });
  });
});
'''
    with open(f'{PROJECT_DIR}/test/test.js', 'w') as f:
        f.write(test_js_content)
    print(f'Created: {PROJECT_DIR}/test/test.js')

    # Create a simple index.js
    index_js_content = '''// Calculator module
function add(a, b) {
  return a + b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) return Infinity;
  return a / b;
}

module.exports = { add, multiply, divide };
'''
    with open(f'{PROJECT_DIR}/index.js', 'w') as f:
        f.write(index_js_content)
    print(f'Created: {PROJECT_DIR}/index.js')

    # Install mocha via npm so node_modules/mocha/bin/_mocha exists
    print('Installing mocha via npm...')
    # Set up environment with nvm node in PATH
    env = os.environ.copy()
    env['PATH'] = NVM_NODE_BIN + ':' + env.get('PATH', '/usr/bin:/bin')
    result = subprocess.run(
        [NPM_BIN, 'install'],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=120,
        env=env
    )
    if result.returncode != 0:
        print(f'npm install stderr: {result.stderr}')
        print(f'npm install stdout: {result.stdout}')
        # Try installing mocha directly if npm install fails
        result2 = subprocess.run(
            [NPM_BIN, 'install', 'mocha', '--save-dev'],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )
        if result2.returncode != 0:
            print(f'Warning: npm install failed: {result2.stderr}')
        else:
            print('Mocha installed successfully via npm install mocha --save-dev')
    else:
        print('npm install completed successfully')

    # Verify no .vscode directory exists (it should not)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)
        print(f'Removed pre-existing .vscode directory to ensure clean initial state')

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder using DISPLAY=:0')

create_initial()
