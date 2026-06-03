"""
Initial Setup: Create an npm-package project directory for GitHub Actions release pipeline task.
Task ID: vscode_gf3_090
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_090'
PROJECT_DIR = f'{WORKDIR}/projects/npm-package'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/test', exist_ok=True)

    # ---- package.json ----
    package_json = {
        "name": "@acmecorp/data-transform-utils",
        "version": "1.2.3",
        "description": "Lightweight data transformation utilities for ETL pipelines and API response normalization",
        "main": "src/index.js",
        "scripts": {
            "test": "jest --coverage",
            "lint": "eslint src/ test/",
            "build": "babel src -d dist"
        },
        "keywords": [
            "data-transformation",
            "etl",
            "normalization",
            "utilities"
        ],
        "author": "Priya Ramanathan <priya.ramanathan@acmecorp.dev>",
        "license": "MIT",
        "repository": {
            "type": "git",
            "url": "https://github.com/acmecorp/data-transform-utils.git"
        },
        "bugs": {
            "url": "https://github.com/acmecorp/data-transform-utils/issues"
        },
        "homepage": "https://github.com/acmecorp/data-transform-utils#readme",
        "devDependencies": {
            "@babel/cli": "^7.23.0",
            "@babel/core": "^7.23.0",
            "@babel/preset-env": "^7.23.0",
            "eslint": "^8.52.0",
            "jest": "^29.7.0"
        },
        "dependencies": {
            "lodash": "^4.17.21",
            "dayjs": "^1.11.10"
        },
        "engines": {
            "node": ">=18.0.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # ---- src/index.js ----
    index_js = '''\
const _ = require('lodash');
const dayjs = require('dayjs');

/**
 * Flatten a nested object into dot-notation keys.
 * @param {Object} obj - The object to flatten
 * @param {string} prefix - Key prefix for recursion
 * @returns {Object} Flattened object
 */
function flattenObject(obj, prefix = '') {
  return Object.keys(obj).reduce((acc, key) => {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (_.isPlainObject(obj[key])) {
      Object.assign(acc, flattenObject(obj[key], fullKey));
    } else {
      acc[fullKey] = obj[key];
    }
    return acc;
  }, {});
}

/**
 * Normalize API timestamps to ISO 8601 format.
 * Handles Unix timestamps (seconds & ms), ISO strings, and common date formats.
 * @param {string|number} timestamp - Raw timestamp value
 * @returns {string} ISO 8601 formatted string
 */
function normalizeTimestamp(timestamp) {
  if (typeof timestamp === 'number') {
    // Distinguish seconds vs milliseconds
    const ts = timestamp > 1e12 ? timestamp : timestamp * 1000;
    return dayjs(ts).toISOString();
  }
  const parsed = dayjs(timestamp);
  if (!parsed.isValid()) {
    throw new Error(`Invalid timestamp: ${timestamp}`);
  }
  return parsed.toISOString();
}

/**
 * Remove null, undefined, and empty string values from an object (deep).
 * @param {Object} obj - Input object
 * @returns {Object} Cleaned object
 */
function removeEmpty(obj) {
  return _.omitBy(obj, (value) => {
    if (_.isPlainObject(value)) {
      const cleaned = removeEmpty(value);
      return Object.keys(cleaned).length === 0;
    }
    return value === null || value === undefined || value === '';
  });
}

/**
 * Map an array of objects to a lookup dictionary keyed by a given field.
 * @param {Array} items - Array of objects
 * @param {string} keyField - Field name to use as dictionary key
 * @returns {Object} Lookup dictionary
 */
function toLookup(items, keyField) {
  return items.reduce((acc, item) => {
    const key = _.get(item, keyField);
    if (key !== undefined) {
      acc[key] = item;
    }
    return acc;
  }, {});
}

module.exports = {
  flattenObject,
  normalizeTimestamp,
  removeEmpty,
  toLookup,
};
'''
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # ---- src/validators.js ----
    validators_js = '''\
const _ = require('lodash');

/**
 * Validate that required fields are present and non-empty in a data record.
 * @param {Object} record - Data record to validate
 * @param {string[]} requiredFields - List of required field names
 * @returns {{ valid: boolean, missing: string[] }}
 */
function validateRequired(record, requiredFields) {
  const missing = requiredFields.filter((field) => {
    const value = _.get(record, field);
    return value === undefined || value === null || value === '';
  });
  return { valid: missing.length === 0, missing };
}

/**
 * Check that a numeric value falls within an expected range.
 * @param {number} value
 * @param {number} min
 * @param {number} max
 * @returns {boolean}
 */
function inRange(value, min, max) {
  return typeof value === 'number' && value >= min && value <= max;
}

module.exports = { validateRequired, inRange };
'''
    with open(f'{PROJECT_DIR}/src/validators.js', 'w') as f:
        f.write(validators_js)

    # ---- test/index.test.js ----
    test_js = '''\
const { flattenObject, normalizeTimestamp, removeEmpty, toLookup } = require('../src/index');

describe('flattenObject', () => {
  test('flattens nested object to dot notation', () => {
    const input = { user: { name: 'Alice', address: { city: 'Seattle' } } };
    expect(flattenObject(input)).toEqual({
      'user.name': 'Alice',
      'user.address.city': 'Seattle',
    });
  });

  test('handles flat objects unchanged', () => {
    expect(flattenObject({ a: 1, b: 2 })).toEqual({ a: 1, b: 2 });
  });
});

describe('normalizeTimestamp', () => {
  test('converts Unix seconds to ISO string', () => {
    const result = normalizeTimestamp(1700000000);
    expect(result).toMatch(/2023-11-14T/);
  });

  test('converts Unix milliseconds to ISO string', () => {
    const result = normalizeTimestamp(1700000000000);
    expect(result).toMatch(/2023-11-14T/);
  });

  test('throws on invalid input', () => {
    expect(() => normalizeTimestamp('not-a-date')).toThrow('Invalid timestamp');
  });
});

describe('removeEmpty', () => {
  test('strips null and undefined values', () => {
    expect(removeEmpty({ a: 1, b: null, c: undefined, d: '' })).toEqual({ a: 1 });
  });
});

describe('toLookup', () => {
  test('creates lookup by specified key', () => {
    const items = [
      { id: 'x1', name: 'Widget' },
      { id: 'x2', name: 'Gadget' },
    ];
    const lookup = toLookup(items, 'id');
    expect(lookup['x1'].name).toBe('Widget');
    expect(lookup['x2'].name).toBe('Gadget');
  });
});
'''
    with open(f'{PROJECT_DIR}/test/index.test.js', 'w') as f:
        f.write(test_js)

    # ---- .gitignore ----
    gitignore = '''\
node_modules/
dist/
coverage/
.env
*.log
.DS_Store
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # ---- README.md ----
    readme = '''\
# @acmecorp/data-transform-utils

Lightweight data transformation utilities for ETL pipelines and API response normalization.

## Installation

```bash
npm install @acmecorp/data-transform-utils
```

## Usage

```js
const { flattenObject, normalizeTimestamp, removeEmpty, toLookup } = require('@acmecorp/data-transform-utils');

// Flatten nested API responses
const flat = flattenObject({ user: { name: 'Alice', role: 'admin' } });
// => { 'user.name': 'Alice', 'user.role': 'admin' }

// Normalize timestamps from various sources
normalizeTimestamp(1700000000);    // Unix seconds
normalizeTimestamp('2023-11-14');  // Date string
```

## API

### `flattenObject(obj, prefix?)`
Flatten a nested object into dot-notation keys.

### `normalizeTimestamp(timestamp)`
Normalize timestamps to ISO 8601 format. Accepts Unix seconds, milliseconds, ISO strings, and common date formats.

### `removeEmpty(obj)`
Recursively remove null, undefined, and empty string values.

### `toLookup(items, keyField)`
Convert an array of objects into a dictionary keyed by a specified field.

## Development

```bash
npm install
npm test
npm run lint
```

## License

MIT
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # ---- .babelrc ----
    babelrc = {
        "presets": [
            ["@babel/preset-env", {"targets": {"node": "18"}}]
        ]
    }
    with open(f'{PROJECT_DIR}/.babelrc', 'w') as f:
        json.dump(babelrc, f, indent=2)

    # ---- .eslintrc.json ----
    eslintrc = {
        "env": {
            "node": True,
            "jest": True,
            "es2021": True
        },
        "extends": "eslint:recommended",
        "parserOptions": {
            "ecmaVersion": "latest"
        },
        "rules": {
            "no-unused-vars": "warn",
            "no-console": "off"
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # NOTE: .github/workflows/ directory is NOT created — that's the agent's task
    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: package.json, src/index.js, src/validators.js, test/index.test.js, .gitignore, README.md, .babelrc, .eslintrc.json')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
