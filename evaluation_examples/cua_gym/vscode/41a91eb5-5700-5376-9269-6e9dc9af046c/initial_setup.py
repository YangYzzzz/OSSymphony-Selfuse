"""
Initial Setup: Create a JavaScript project with ESLint and Jest configured.
Task ID: vscode_wf_061
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_061'
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


def create_initial():
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # NOTE: Do NOT create reports/ directory - task requires agent to set that up
    # NOTE: Do NOT create .vscode/tasks.json - that is the task output

    # --- package.json ---
    package_json = {
        "name": "dashboard-analytics",
        "version": "1.2.0",
        "description": "Analytics dashboard for internal metrics tracking",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest",
            "lint": "eslint src/"
        },
        "dependencies": {
            "express": "^4.18.2",
            "lodash": "^4.17.21",
            "moment": "^2.29.4"
        },
        "devDependencies": {
            "eslint": "^8.50.0",
            "jest": "^29.7.0"
        },
        "license": "MIT"
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- .eslintrc.json ---
    eslintrc = {
        "env": {
            "browser": False,
            "node": True,
            "es2021": True,
            "jest": True
        },
        "parserOptions": {
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "rules": {
            "no-unused-vars": "warn",
            "no-console": "off",
            "semi": ["error", "always"],
            "quotes": ["error", "single"],
            "indent": ["error", 2]
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # --- jest.config.js ---
    jest_config = """module.exports = {
  testEnvironment: 'node',
  collectCoverageFrom: ['src/**/*.js'],
  coverageDirectory: 'reports/coverage',
  coverageReporters: ['text', 'lcov', 'json-summary'],
  testMatch: ['**/tests/**/*.test.js'],
  verbose: true,
};
"""
    with open(f'{PROJECT_DIR}/jest.config.js', 'w') as f:
        f.write(jest_config)

    # --- src/index.js ---
    index_js = """'use strict';

const express = require('express');
const { calculateMetrics } = require('./utils/metrics');
const { formatReport } = require('./utils/formatter');

const app = express();
const PORT = process.env.PORT || 3000;

// TODO: Add authentication middleware before production release
app.use(express.json());

app.get('/api/metrics', (req, res) => {
  const startDate = req.query.start || '2024-01-01';
  const endDate = req.query.end || '2024-12-31';
  const metrics = calculateMetrics(startDate, endDate);
  res.json(metrics);
});

app.get('/api/report', (req, res) => {
  // FIXME: This endpoint sometimes returns stale cached data
  const report = formatReport();
  res.json(report);
});

// TODO: Implement WebSocket support for real-time dashboard updates
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.listen(PORT, () => {
  console.log(`Dashboard server running on port ${PORT}`);
});

module.exports = app;
"""
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write(index_js)

    # --- src/utils/metrics.js ---
    metrics_js = """'use strict';

const _ = require('lodash');
const moment = require('moment');

// TODO: Replace moment.js with date-fns for smaller bundle size
function calculateMetrics(startDate, endDate) {
  const start = moment(startDate);
  const end = moment(endDate);
  const daysDiff = end.diff(start, 'days');

  // FIXME: Revenue calculation does not account for refunds
  const dailyRevenue = generateDailyRevenue(daysDiff);
  const totalRevenue = _.sum(dailyRevenue);
  const avgRevenue = _.mean(dailyRevenue);

  return {
    period: { start: startDate, end: endDate, days: daysDiff },
    revenue: {
      total: Math.round(totalRevenue * 100) / 100,
      average: Math.round(avgRevenue * 100) / 100,
      daily: dailyRevenue,
    },
    // TODO: Add customer acquisition cost (CAC) metrics
    visitors: {
      total: Math.floor(Math.random() * 50000) + 10000,
      unique: Math.floor(Math.random() * 30000) + 5000,
    },
  };
}

function generateDailyRevenue(days) {
  const revenues = [];
  for (let i = 0; i < days; i++) {
    revenues.push(Math.round((Math.random() * 5000 + 1000) * 100) / 100);
  }
  return revenues;
}

module.exports = { calculateMetrics };
"""
    with open(f'{PROJECT_DIR}/src/utils/metrics.js', 'w') as f:
        f.write(metrics_js)

    # --- src/utils/formatter.js ---
    formatter_js = """'use strict';

const moment = require('moment');

// FIXME: Date formatting is inconsistent between report sections
function formatReport() {
  const timestamp = moment().format('YYYY-MM-DD HH:mm:ss');
  return {
    generatedAt: timestamp,
    title: 'Weekly Analytics Summary',
    sections: [
      {
        name: 'Revenue Overview',
        // TODO: Pull real data from database instead of mock values
        data: { weekly: 34521.87, monthly: 142350.00, quarterly: 423890.50 },
      },
      {
        name: 'User Engagement',
        data: { activeUsers: 2847, sessionDuration: '4m 32s', bounceRate: '23.4%' },
      },
    ],
  };
}

// TODO: Add CSV export functionality for stakeholder reports
function formatCSV(data) {
  // Placeholder for CSV formatting
  return data;
}

module.exports = { formatReport, formatCSV };
"""
    with open(f'{PROJECT_DIR}/src/utils/formatter.js', 'w') as f:
        f.write(formatter_js)

    # --- src/utils/validator.js ---
    validator_js = """'use strict';

// FIXME: Email regex does not handle all valid RFC 5322 formats
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;

function validateEmail(email) {
  return EMAIL_REGEX.test(email);
}

function validateDateRange(start, end) {
  const startDate = new Date(start);
  const endDate = new Date(end);
  // TODO: Add timezone-aware date validation
  if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
    return { valid: false, error: 'Invalid date format' };
  }
  if (startDate >= endDate) {
    return { valid: false, error: 'Start date must be before end date' };
  }
  return { valid: true };
}

module.exports = { validateEmail, validateDateRange };
"""
    with open(f'{PROJECT_DIR}/src/utils/validator.js', 'w') as f:
        f.write(validator_js)

    # --- tests/metrics.test.js ---
    metrics_test = """'use strict';

const { calculateMetrics } = require('../src/utils/metrics');

describe('calculateMetrics', () => {
  test('returns correct period information', () => {
    const result = calculateMetrics('2024-01-01', '2024-01-31');
    expect(result.period.days).toBe(30);
    expect(result.period.start).toBe('2024-01-01');
    expect(result.period.end).toBe('2024-01-31');
  });

  test('returns revenue object with required fields', () => {
    const result = calculateMetrics('2024-01-01', '2024-03-01');
    expect(result.revenue).toHaveProperty('total');
    expect(result.revenue).toHaveProperty('average');
    expect(result.revenue).toHaveProperty('daily');
    expect(result.revenue.daily).toHaveLength(60);
  });

  // TODO: Add edge case tests for single-day periods
  test('returns visitor metrics', () => {
    const result = calculateMetrics('2024-06-01', '2024-06-30');
    expect(result.visitors.total).toBeGreaterThan(0);
    expect(result.visitors.unique).toBeGreaterThan(0);
    expect(result.visitors.unique).toBeLessThanOrEqual(result.visitors.total);
  });
});
"""
    with open(f'{PROJECT_DIR}/tests/metrics.test.js', 'w') as f:
        f.write(metrics_test)

    # --- tests/validator.test.js ---
    validator_test = """'use strict';

const { validateEmail, validateDateRange } = require('../src/utils/validator');

describe('validateEmail', () => {
  test('accepts valid emails', () => {
    expect(validateEmail('user@example.com')).toBe(true);
    expect(validateEmail('admin@company.co.uk')).toBe(true);
  });

  // FIXME: This test should also cover edge cases with + and . in local part
  test('rejects invalid emails', () => {
    expect(validateEmail('not-an-email')).toBe(false);
    expect(validateEmail('@missing-local.com')).toBe(false);
  });
});

describe('validateDateRange', () => {
  test('accepts valid date ranges', () => {
    const result = validateDateRange('2024-01-01', '2024-12-31');
    expect(result.valid).toBe(true);
  });

  test('rejects invalid date ranges', () => {
    const result = validateDateRange('2024-12-31', '2024-01-01');
    expect(result.valid).toBe(false);
  });
});
"""
    with open(f'{PROJECT_DIR}/tests/validator.test.js', 'w') as f:
        f.write(validator_test)

    # --- .gitignore ---
    gitignore = """node_modules/
reports/
coverage/
*.log
.env
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files with TODO comments: src/index.js, src/utils/metrics.js, src/utils/formatter.js, src/utils/validator.js')
    print(f'Files with FIXME comments: src/index.js, src/utils/metrics.js, src/utils/formatter.js, src/utils/validator.js')

    # GUI-ready: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
