"""
Initial Setup: Create polyglot project with empty .vscode/settings.json
Task ID: vscode_wf_057
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_057'
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
    # --- Create project directory structure ---
    os.makedirs(f'{PROJECT_DIR}/py_modules', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/js_modules', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/templates', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # --- Python files in py_modules/ ---
    with open(f'{PROJECT_DIR}/py_modules/__init__.py', 'w') as f:
        f.write('"""Polyglot project - Python modules."""\n')

    with open(f'{PROJECT_DIR}/py_modules/data_processor.py', 'w') as f:
        f.write('''"""Data processing utilities for customer analytics pipeline."""

import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class CustomerDataProcessor:
    """Processes raw customer transaction data and generates summary reports."""

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.transaction_cache: Dict[str, List[dict]] = {}

    def load_transactions(self, filepath: str) -> List[dict]:
        """Load transaction records from a CSV file."""
        transactions = []
        with open(filepath, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["amount"] = float(row["amount"])
                row["timestamp"] = datetime.fromisoformat(row["timestamp"])
                transactions.append(row)
        return transactions

    def aggregate_by_customer(self, transactions: List[dict]) -> Dict[str, dict]:
        """Group transactions by customer ID and compute summaries."""
        aggregated = {}
        for txn in transactions:
            cid = txn["customer_id"]
            if cid not in aggregated:
                aggregated[cid] = {
                    "customer_id": cid,
                    "total_spent": 0.0,
                    "transaction_count": 0,
                    "first_purchase": txn["timestamp"],
                    "last_purchase": txn["timestamp"],
                }
            aggregated[cid]["total_spent"] += txn["amount"]
            aggregated[cid]["transaction_count"] += 1
            if txn["timestamp"] < aggregated[cid]["first_purchase"]:
                aggregated[cid]["first_purchase"] = txn["timestamp"]
            if txn["timestamp"] > aggregated[cid]["last_purchase"]:
                aggregated[cid]["last_purchase"] = txn["timestamp"]
        return aggregated

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate a summary report of all processed transactions."""
        if output_path is None:
            output_path = os.path.join(self.output_dir, "summary_report.csv")
        return output_path
''')

    with open(f'{PROJECT_DIR}/py_modules/config.py', 'w') as f:
        f.write('''"""Configuration settings for the analytics pipeline."""

DATABASE_URL = "postgresql://analytics:secret@db.internal:5432/customers"
REDIS_URL = "redis://cache.internal:6379/0"
API_BASE_URL = "https://api.analytics-platform.com/v2"

MAX_BATCH_SIZE = 500
RETRY_ATTEMPTS = 3
REQUEST_TIMEOUT_SECONDS = 30

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CAD"]
DEFAULT_CURRENCY = "USD"
''')

    # --- JavaScript files in js_modules/ ---
    with open(f'{PROJECT_DIR}/js_modules/dashboard.js', 'w') as f:
        f.write('''/**
 * Dashboard controller for the analytics frontend.
 * Handles chart rendering, data fetching, and user interactions.
 */

const API_ENDPOINT = '/api/v2/analytics';
const REFRESH_INTERVAL_MS = 30000;

class DashboardController {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.charts = new Map();
    this.filters = {
      dateRange: { start: null, end: null },
      customerSegment: 'all',
      currency: 'USD',
    };
    this.refreshTimer = null;
  }

  async initialize() {
    await this.loadInitialData();
    this.renderCharts();
    this.attachEventListeners();
    this.startAutoRefresh();
  }

  async loadInitialData() {
    const params = new URLSearchParams({
      segment: this.filters.customerSegment,
      currency: this.filters.currency,
    });
    const response = await fetch(`${API_ENDPOINT}/summary?${params}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    this.data = await response.json();
  }

  renderCharts() {
    const revenueData = this.data.revenue_by_month;
    const segmentData = this.data.customer_segments;
    console.log('Charts rendered:', revenueData.length, 'months,', segmentData.length, 'segments');
  }

  attachEventListeners() {
    document.getElementById('date-filter').addEventListener('change', (e) => {
      this.filters.dateRange = JSON.parse(e.target.value);
      this.refresh();
    });
  }

  startAutoRefresh() {
    this.refreshTimer = setInterval(() => this.refresh(), REFRESH_INTERVAL_MS);
  }

  async refresh() {
    await this.loadInitialData();
    this.renderCharts();
  }

  destroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
    this.charts.clear();
  }
}

export default DashboardController;
''')

    with open(f'{PROJECT_DIR}/js_modules/utils.js', 'w') as f:
        f.write('''/**
 * Utility functions for data formatting and validation.
 */

export function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount);
}

export function formatDate(dateStr, locale = 'en-US') {
  const date = new Date(dateStr);
  return date.toLocaleDateString(locale, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function debounce(fn, delay = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

export function validateEmail(email) {
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
  return pattern.test(email);
}
''')

    with open(f'{PROJECT_DIR}/js_modules/package.json', 'w') as f:
        json.dump({
            "name": "analytics-dashboard",
            "version": "2.1.0",
            "description": "Customer analytics dashboard frontend",
            "main": "dashboard.js",
            "scripts": {
                "start": "node server.js",
                "build": "webpack --mode production",
                "test": "jest --coverage"
            },
            "dependencies": {
                "express": "^4.18.2",
                "chart.js": "^4.4.0"
            }
        }, f, indent=2)

    # --- HTML/CSS files in templates/ ---
    with open(f'{PROJECT_DIR}/templates/dashboard.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analytics Dashboard</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="main-header">
    <h1>Customer Analytics</h1>
    <nav class="top-nav">
      <ul>
        <li><a href="#overview" class="active">Overview</a></li>
        <li><a href="#segments">Segments</a></li>
        <li><a href="#trends">Trends</a></li>
        <li><a href="#settings">Settings</a></li>
      </ul>
    </nav>
  </header>

  <main class="dashboard-container" id="dashboard">
    <section class="metric-cards">
      <div class="card">
        <h3>Total Revenue</h3>
        <p class="metric-value" id="total-revenue">$0.00</p>
        <span class="metric-change positive">+12.5%</span>
      </div>
      <div class="card">
        <h3>Active Customers</h3>
        <p class="metric-value" id="active-customers">0</p>
        <span class="metric-change positive">+8.3%</span>
      </div>
      <div class="card">
        <h3>Avg Order Value</h3>
        <p class="metric-value" id="avg-order">$0.00</p>
        <span class="metric-change negative">-2.1%</span>
      </div>
    </section>

    <section class="charts-grid">
      <div class="chart-panel" id="revenue-chart"></div>
      <div class="chart-panel" id="segment-chart"></div>
    </section>

    <section class="filters">
      <label for="date-filter">Date Range:</label>
      <select id="date-filter">
        <option value="7d">Last 7 Days</option>
        <option value="30d" selected>Last 30 Days</option>
        <option value="90d">Last 90 Days</option>
      </select>
    </section>
  </main>

  <script type="module" src="../js_modules/dashboard.js"></script>
</body>
</html>
''')

    with open(f'{PROJECT_DIR}/templates/styles.css', 'w') as f:
        f.write('''/* Analytics Dashboard Styles */

:root {
  --primary-color: #2563eb;
  --secondary-color: #7c3aed;
  --success-color: #059669;
  --danger-color: #dc2626;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.6;
}

.main-header {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-nav ul {
  display: flex;
  list-style: none;
  gap: 1.5rem;
}

.top-nav a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.top-nav a.active,
.top-nav a:hover {
  color: white;
}

.dashboard-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.metric-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  margin: 0.5rem 0;
}

.metric-change {
  font-size: 0.875rem;
  font-weight: 600;
}

.metric-change.positive { color: var(--success-color); }
.metric-change.negative { color: var(--danger-color); }

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-panel {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  min-height: 300px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
}

.filters {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filters select {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 0.875rem;
}
''')

    # --- Create a Jinja template file ---
    with open(f'{PROJECT_DIR}/templates/report.jinja', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ report_title }}</title>
</head>
<body>
  <h1>{{ report_title }}</h1>
  <p>Generated on: {{ generation_date }}</p>
  <table>
    <thead>
      <tr>
        {% for header in headers %}
        <th>{{ header }}</th>
        {% endfor %}
      </tr>
    </thead>
    <tbody>
      {% for row in data %}
      <tr>
        {% for cell in row %}
        <td>{{ cell }}</td>
        {% endfor %}
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
''')

    # --- Create empty .vscode/settings.json ---
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Project structure created at {PROJECT_DIR}')
    print(f'Empty settings.json at {PROJECT_DIR}/.vscode/settings.json')

    # --- Launch VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
