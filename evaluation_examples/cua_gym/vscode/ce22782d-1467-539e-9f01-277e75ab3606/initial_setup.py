"""
Initial Setup: Set up a .editorconfig file in a project with mixed formatting
Task ID: vscode_lp_075
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_075'
PROJECT_DIR = f'{WORKDIR}/workspace'

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
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # --- Python files using TABS (inconsistent formatting) ---
    with open(f'{PROJECT_DIR}/src/data_processor.py', 'w') as f:
        f.write('''\
import csv
import json
from datetime import datetime

class DataProcessor:
\tdef __init__(self, input_path, output_path):
\t\tself.input_path = input_path
\t\tself.output_path = output_path
\t\tself.records = []
\t\tself.errors = []

\tdef load_csv(self):
\t\t"""Load records from CSV file."""
\t\twith open(self.input_path, 'r') as f:
\t\t\treader = csv.DictReader(f)
\t\t\tfor row in reader:
\t\t\t\ttry:
\t\t\t\t\trecord = {
\t\t\t\t\t\t'name': row['name'],
\t\t\t\t\t\t'email': row['email'],
\t\t\t\t\t\t'amount': float(row['amount']),
\t\t\t\t\t\t'date': datetime.strptime(row['date'], '%Y-%m-%d')
\t\t\t\t\t}
\t\t\t\t\tself.records.append(record)
\t\t\t\texcept (KeyError, ValueError) as e:
\t\t\t\t\tself.errors.append(str(e))

\tdef filter_by_amount(self, min_amount):
\t\t"""Filter records by minimum amount."""
\t\treturn [r for r in self.records if r['amount'] >= min_amount]

\tdef export_json(self, records=None):
\t\t"""Export records to JSON file."""
\t\tdata = records or self.records
\t\twith open(self.output_path, 'w') as f:
\t\t\tjson.dump(data, f, indent=2, default=str)

\tdef get_summary(self):
\t\t"""Return summary statistics."""
\t\tif not self.records:
\t\t\treturn {'count': 0, 'total': 0, 'average': 0}
\t\tamounts = [r['amount'] for r in self.records]
\t\treturn {
\t\t\t'count': len(amounts),
\t\t\t'total': sum(amounts),
\t\t\t'average': sum(amounts) / len(amounts)
\t\t}
''')

    with open(f'{PROJECT_DIR}/tests/test_processor.py', 'w') as f:
        f.write('''\
import unittest
import os
import tempfile
from src.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
\tdef setUp(self):
\t\tself.temp_dir = tempfile.mkdtemp()
\t\tself.input_file = os.path.join(self.temp_dir, 'test_input.csv')
\t\tself.output_file = os.path.join(self.temp_dir, 'test_output.json')
\t\twith open(self.input_file, 'w') as f:
\t\t\tf.write('name,email,amount,date\\n')
\t\t\tf.write('Alice Wang,alice@example.com,1500.00,2025-01-15\\n')
\t\t\tf.write('Bob Martinez,bob@example.com,2300.50,2025-02-20\\n')
\t\t\tf.write('Carol Singh,carol@example.com,890.75,2025-03-10\\n')

\tdef test_load_csv(self):
\t\tprocessor = DataProcessor(self.input_file, self.output_file)
\t\tprocessor.load_csv()
\t\tself.assertEqual(len(processor.records), 3)

\tdef test_filter_by_amount(self):
\t\tprocessor = DataProcessor(self.input_file, self.output_file)
\t\tprocessor.load_csv()
\t\tresults = processor.filter_by_amount(1000)
\t\tself.assertEqual(len(results), 2)

\tdef test_get_summary(self):
\t\tprocessor = DataProcessor(self.input_file, self.output_file)
\t\tprocessor.load_csv()
\t\tsummary = processor.get_summary()
\t\tself.assertEqual(summary['count'], 3)
\t\tself.assertAlmostEqual(summary['total'], 4691.25)

if __name__ == '__main__':
\tunittest.main()
''')

    # --- JavaScript files using 4-space indentation (inconsistent) ---
    with open(f'{PROJECT_DIR}/src/api_client.js', 'w') as f:
        f.write('''\
const https = require('https');

class ApiClient {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.timeout = 30000;
        this.retryCount = 3;
    }

    async fetchData(endpoint, params = {}) {
        const url = new URL(`${this.baseUrl}/${endpoint}`);
        Object.entries(params).forEach(([key, value]) => {
            url.searchParams.append(key, value);
        });

        for (let attempt = 1; attempt <= this.retryCount; attempt++) {
            try {
                const response = await this._makeRequest(url.toString());
                return JSON.parse(response);
            } catch (error) {
                if (attempt === this.retryCount) {
                    throw new Error(`Failed after ${this.retryCount} attempts: ${error.message}`);
                }
                await this._delay(1000 * attempt);
            }
        }
    }

    async postData(endpoint, body) {
        const url = `${this.baseUrl}/${endpoint}`;
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            }
        };
        return this._makeRequest(url, options, JSON.stringify(body));
    }

    _makeRequest(url, options = {}, body = null) {
        return new Promise((resolve, reject) => {
            const req = https.request(url, options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => resolve(data));
            });
            req.on('error', reject);
            req.setTimeout(this.timeout, () => {
                req.destroy();
                reject(new Error('Request timeout'));
            });
            if (body) req.write(body);
            req.end();
        });
    }

    _delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

module.exports = ApiClient;
''')

    with open(f'{PROJECT_DIR}/src/utils.js', 'w') as f:
        f.write('''\
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj);
    if (obj instanceof Array) {
        return obj.map(item => deepClone(item));
    }
    const clonedObj = {};
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            clonedObj[key] = deepClone(obj[key]);
        }
    }
    return clonedObj;
}

module.exports = { formatCurrency, debounce, deepClone };
''')

    # --- YAML files using 2-space indentation (inconsistent) ---
    with open(f'{PROJECT_DIR}/config/database.yml', 'w') as f:
        f.write('''\
development:
  adapter: postgresql
  host: localhost
  port: 5432
  database: myapp_dev
  username: dev_user
  password: dev_secret_123
  pool: 5
  encoding: unicode

production:
  adapter: postgresql
  host: db.production.internal
  port: 5432
  database: myapp_prod
  username: prod_user
  password: <%= ENV['DB_PASSWORD'] %>
  pool: 25
  encoding: unicode
  ssl_mode: verify-full

test:
  adapter: sqlite3
  database: ":memory:"
  pool: 1
  timeout: 5000
''')

    with open(f'{PROJECT_DIR}/config/ci.yaml', 'w') as f:
        f.write('''\
name: CI Pipeline
on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run linter
        run: python -m flake8 src/

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: python -m pytest tests/ -v
''')

    # --- Additional project files ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''\
# Data Processing Toolkit

A utility library for processing CSV data, making API calls, and managing
configuration across multiple environments.

## Setup

```bash
pip install -r requirements.txt
npm install
```

## Usage

```python
from src.data_processor import DataProcessor

processor = DataProcessor('input.csv', 'output.json')
processor.load_csv()
summary = processor.get_summary()
```

## Running Tests

```bash
python -m pytest tests/ -v
npm test
```
''')

    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write('''\
{
    "name": "data-processing-toolkit",
    "version": "1.2.0",
    "description": "Utility library for data processing and API integration",
    "main": "src/api_client.js",
    "scripts": {
        "test": "jest",
        "lint": "eslint src/"
    },
    "dependencies": {
        "dotenv": "^16.3.1"
    },
    "devDependencies": {
        "jest": "^29.7.0",
        "eslint": "^8.56.0"
    }
}
''')

    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''\
flask==3.0.2
requests==2.31.0
pandas==2.2.0
pytest==8.0.0
flake8==7.0.0
''')

    # Ensure NO .editorconfig file exists (this is what the task asks the agent to create)
    editorconfig_path = f'{PROJECT_DIR}/.editorconfig'
    if os.path.exists(editorconfig_path):
        os.remove(editorconfig_path)

    print(f'Project workspace created: {PROJECT_DIR}')
    print('Files created:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        for f in files:
            print(f'  {os.path.join(root, f)}')

    # Install EditorConfig extension
    try:
        subprocess.run(['code', '--install-extension', 'EditorConfig.EditorConfig'],
                      capture_output=True, text=True, timeout=30)
        print('EditorConfig extension installed')
    except Exception as e:
        print(f'Extension install note: {e}')

    # GUI-ready startup: open VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
