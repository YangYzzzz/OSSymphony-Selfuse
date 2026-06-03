"""
Initial Setup: Create a Node.js project with Mocha tests, no launch.json
Task ID: vscode_td_075
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_075'
PROJECT_DIR = f'{WORKDIR}/projects/node-lib'


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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/test', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/.bin', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/mocha/bin', exist_ok=True)

    # package.json
    package_json = {
        "name": "node-lib",
        "version": "1.2.0",
        "description": "A utility library for string and array operations",
        "main": "src/index.js",
        "scripts": {
            "test": "mocha test/",
            "start": "node src/index.js"
        },
        "keywords": ["utility", "string", "array"],
        "author": "Sarah Chen <sarah.chen@devteam.io>",
        "license": "MIT",
        "devDependencies": {
            "mocha": "^10.2.0",
            "chai": "^4.3.7"
        },
        "dependencies": {
            "lodash": "^4.17.21"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js - main library
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write('''/**
 * node-lib - Utility library for string and array operations
 */

function capitalize(str) {
    if (typeof str !== 'string') return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    const clone = Array.isArray(obj) ? [] : {};
    for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            clone[key] = deepClone(obj[key]);
        }
    }
    return clone;
}

function flatten(arr, depth = Infinity) {
    return depth > 0
        ? arr.reduce((acc, val) => acc.concat(
            Array.isArray(val) ? flatten(val, depth - 1) : val
          ), [])
        : arr.slice();
}

function uniqueBy(arr, keyFn) {
    const seen = new Set();
    return arr.filter(item => {
        const key = keyFn(item);
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
    });
}

module.exports = { capitalize, deepClone, flatten, uniqueBy };
''')

    # test/index.test.js - Mocha test file
    with open(f'{PROJECT_DIR}/test/index.test.js', 'w') as f:
        f.write("""const assert = require('assert');
const { capitalize, deepClone, flatten, uniqueBy } = require('../src/index');

describe('capitalize', function () {
    it('should capitalize the first letter', function () {
        assert.strictEqual(capitalize('hello'), 'Hello');
    });

    it('should return empty string for non-string input', function () {
        assert.strictEqual(capitalize(123), '');
    });

    it('should handle empty string', function () {
        assert.strictEqual(capitalize(''), '');
    });
});

describe('deepClone', function () {
    it('should create a deep copy of an object', function () {
        const original = { a: 1, b: { c: 2 } };
        const cloned = deepClone(original);
        cloned.b.c = 99;
        assert.strictEqual(original.b.c, 2);
    });

    it('should handle arrays', function () {
        const original = [1, [2, 3], { a: 4 }];
        const cloned = deepClone(original);
        assert.deepStrictEqual(cloned, original);
    });

    it('should handle null', function () {
        assert.strictEqual(deepClone(null), null);
    });
});

describe('flatten', function () {
    it('should flatten nested arrays', function () {
        assert.deepStrictEqual(flatten([1, [2, [3, [4]]]]), [1, 2, 3, 4]);
    });

    it('should respect depth parameter', function () {
        assert.deepStrictEqual(flatten([1, [2, [3]]], 1), [1, 2, [3]]);
    });
});

describe('uniqueBy', function () {
    it('should remove duplicates by key function', function () {
        const items = [
            { id: 1, name: 'Alice' },
            { id: 2, name: 'Bob' },
            { id: 1, name: 'Alice Duplicate' },
        ];
        const result = uniqueBy(items, item => item.id);
        assert.strictEqual(result.length, 2);
    });
});
""")

    # test/helpers.test.js - additional test file
    with open(f'{PROJECT_DIR}/test/helpers.test.js', 'w') as f:
        f.write("""const assert = require('assert');

describe('Environment checks', function () {
    this.timeout(5000);

    it('should have Node.js version >= 14', function () {
        const major = parseInt(process.version.slice(1).split('.')[0], 10);
        assert.ok(major >= 14, 'Node.js version should be at least 14');
    });

    it('should have correct working directory', function () {
        assert.ok(process.cwd().length > 0);
    });
});
""")

    # Create a simulated mocha binary in node_modules/.bin/
    with open(f'{PROJECT_DIR}/node_modules/.bin/mocha', 'w') as f:
        f.write('#!/usr/bin/env node\nrequire("../mocha/bin/mocha");\n')
    os.chmod(f'{PROJECT_DIR}/node_modules/.bin/mocha', 0o755)

    # Create mocha bin entry
    with open(f'{PROJECT_DIR}/node_modules/mocha/bin/mocha', 'w') as f:
        f.write('#!/usr/bin/env node\nconsole.log("mocha v10.2.0");\n')
    os.chmod(f'{PROJECT_DIR}/node_modules/mocha/bin/mocha', 0o755)

    # Create mocha package.json
    with open(f'{PROJECT_DIR}/node_modules/mocha/package.json', 'w') as f:
        json.dump({"name": "mocha", "version": "10.2.0", "main": "index.js"}, f, indent=2)

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# node-lib

A utility library for string and array operations in Node.js.

## Installation

```bash
npm install
```

## Running Tests

```bash
npm test
```

This runs Mocha on the `test/` directory.

## API

- `capitalize(str)` - Capitalize first letter of a string
- `deepClone(obj)` - Deep clone an object or array
- `flatten(arr, depth)` - Flatten nested arrays
- `uniqueBy(arr, keyFn)` - Remove duplicates by key function
""")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write('node_modules/\n.env\ncoverage/\n')

    # Ensure NO .vscode/launch.json exists (task requirement)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(f'{vscode_dir}/launch.json'):
        os.remove(f'{vscode_dir}/launch.json')

    print(f'Initial project created: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
