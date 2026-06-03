"""
Initial Setup: Open three files in VSCode with unsaved changes
Task ID: vscode_edit_057
Domain: vs_code

Strategy:
  1. Write the EDITED version of each file to disk.
  2. Open VSCode with all three files — VSCode loads the edited content into
     its in-memory buffer.
  3. After VSCode has loaded the files, overwrite each disk file with the
     PRE-EDIT version. VSCode detects the external change and shows the
     unsaved-changes indicator (dot) on each tab, because the buffer still
     holds the edited content that differs from the disk version.

  Note: xdotool is not available on this VM, so we rely on VSCode's
  external-change detection mechanism to create the dirty state.

  Golden state: disk files contain the EDITED version (what VSCode saves
  when the agent runs Save All).
"""

import os
import shlex
import subprocess
import time

DESKTOP = '/home/user/Desktop'

# ── EDITED content (VSCode buffer version) ───────────────────────────────────
# This is what VSCode loads into memory. After VSCode opens, we revert the
# disk files to PRE_EDIT so VSCode shows the dirty indicator.

FILE1_EDITED = """\
# Project utilities for DataSync pipeline
# Author: Sarah Chen  |  Team: Platform Engineering
# Last modified: 2025-03-14 — added retry helper and type hints

import os
import json
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


def read_config(config_path: str) -> dict[str, Any]:
    \"\"\"Load JSON configuration file and return as dictionary.\"\"\"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")
    with open(config_path, 'r') as f:
        return json.load(f)


def setup_logging(level: str = 'INFO') -> None:
    \"\"\"Configure root logger with timestamp format.\"\"\"
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def timestamp_now() -> str:
    \"\"\"Return current UTC timestamp as ISO-8601 string.\"\"\"
    return datetime.utcnow().isoformat() + 'Z'


def ensure_dir(path: str) -> None:
    \"\"\"Create directory (and parents) if it does not exist.\"\"\"
    os.makedirs(path, exist_ok=True)


def retry(func, max_attempts: int = 3, delay: float = 1.0):
    \"\"\"Retry a callable up to max_attempts times on exception.\"\"\"
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as exc:
            last_exc = exc
            if attempt < max_attempts:
                time.sleep(delay)
    raise last_exc
"""

FILE2_EDITED = """\
// Dashboard chart helpers — DataSync Analytics UI
// Maintainer: Marcus Johnson  |  Last updated: 2025-03-14
// Changes: added tooltipFormatter and pieChart builder

'use strict';

const CHART_COLORS = {
  primary: '#4A90D9',
  success: '#27AE60',
  warning: '#F39C12',
  danger:  '#E74C3C',
  neutral: '#95A5A6',
};

/**
 * Format a numeric value as a compact string (e.g. 1500 → "1.5K").
 * @param {number} value
 * @returns {string}
 */
function formatCompact(value) {
  if (value >= 1_000_000) return (value / 1_000_000).toFixed(1) + 'M';
  if (value >= 1_000)     return (value / 1_000).toFixed(1) + 'K';
  return String(value);
}

/**
 * Build a bar-chart configuration object for Chart.js.
 * @param {string[]} labels
 * @param {number[]} data
 * @param {string}   title
 * @returns {object}
 */
function buildBarChart(labels, data, title) {
  return {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: title,
        data,
        backgroundColor: CHART_COLORS.primary,
        borderRadius: 4,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
    },
  };
}

/**
 * Build a pie-chart configuration object for Chart.js.
 * @param {string[]} labels
 * @param {number[]} data
 * @param {string}   title
 * @returns {object}
 */
function buildPieChart(labels, data, title) {
  return {
    type: 'pie',
    data: {
      labels,
      datasets: [{ label: title, data, backgroundColor: Object.values(CHART_COLORS) }],
    },
    options: { responsive: true },
  };
}

module.exports = { CHART_COLORS, formatCompact, buildBarChart, buildPieChart };
"""

FILE3_EDITED = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DataSync — Status Dashboard</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f0f2f5;
      color: #333;
    }
    header {
      background: #1a73e8;
      color: #fff;
      padding: 1rem 2rem;
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    header h1 { font-size: 1.4rem; font-weight: 600; }
    .badge {
      background: #34a853;
      border-radius: 12px;
      padding: 2px 10px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.05em;
    }
    nav {
      background: #fff;
      border-bottom: 1px solid #e0e0e0;
      padding: 0.5rem 2rem;
      display: flex;
      gap: 1.5rem;
    }
    nav a { text-decoration: none; color: #1a73e8; font-size: 0.9rem; }
    nav a:hover { text-decoration: underline; }
    main { padding: 2rem; }
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-top: 1.5rem;
    }
    .card {
      background: #fff;
      border-radius: 8px;
      padding: 1.25rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .card h2 { font-size: 0.85rem; color: #666; margin-bottom: 0.5rem; }
    .card .value { font-size: 2rem; font-weight: 700; color: #1a73e8; }
  </style>
</head>
<body>
  <header>
    <h1>DataSync Dashboard</h1>
    <span class="badge">LIVE</span>
  </header>
  <nav>
    <a href="#">Overview</a>
    <a href="#">Pipelines</a>
    <a href="#">Alerts</a>
    <a href="#">Settings</a>
  </nav>
  <main>
    <p>System operational as of <strong>2025-03-15 09:42 UTC</strong>.</p>
    <div class="card-grid">
      <div class="card"><h2>Records Processed</h2><div class="value">1.24M</div></div>
      <div class="card"><h2>Active Pipelines</h2><div class="value">38</div></div>
      <div class="card"><h2>Error Rate</h2><div class="value">0.3%</div></div>
      <div class="card"><h2>Avg Latency</h2><div class="value">142ms</div></div>
    </div>
  </main>
</body>
</html>
"""

# ── PRE-EDIT content (written to disk after VSCode loads the files) ───────────
# VSCode detects these as external changes, marking each tab as dirty.

FILE1_PRE_EDIT = """\
# Project utilities for DataSync pipeline
# Author: Sarah Chen  |  Team: Platform Engineering

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def read_config(config_path: str) -> dict:
    \"\"\"Load JSON configuration file and return as dictionary.\"\"\"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")
    with open(config_path, 'r') as f:
        return json.load(f)


def setup_logging(level: str = 'INFO') -> None:
    \"\"\"Configure root logger with timestamp format.\"\"\"
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def timestamp_now() -> str:
    \"\"\"Return current UTC timestamp as ISO-8601 string.\"\"\"
    return datetime.utcnow().isoformat() + 'Z'


def ensure_dir(path: str) -> None:
    \"\"\"Create directory (and parents) if it does not exist.\"\"\"
    os.makedirs(path, exist_ok=True)
"""

FILE2_PRE_EDIT = """\
// Dashboard chart helpers — DataSync Analytics UI
// Maintainer: Marcus Johnson  |  Last updated: 2025-03-10

'use strict';

const CHART_COLORS = {
  primary: '#4A90D9',
  success: '#27AE60',
  warning: '#F39C12',
  danger:  '#E74C3C',
  neutral: '#95A5A6',
};

/**
 * Format a numeric value as a compact string (e.g. 1500 → "1.5K").
 * @param {number} value
 * @returns {string}
 */
function formatCompact(value) {
  if (value >= 1_000_000) return (value / 1_000_000).toFixed(1) + 'M';
  if (value >= 1_000)     return (value / 1_000).toFixed(1) + 'K';
  return String(value);
}

/**
 * Build a bar-chart configuration object for Chart.js.
 * @param {string[]} labels
 * @param {number[]} data
 * @param {string}   title
 * @returns {object}
 */
function buildBarChart(labels, data, title) {
  return {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: title,
        data,
        backgroundColor: CHART_COLORS.primary,
        borderRadius: 4,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
    },
  };
}

module.exports = { CHART_COLORS, formatCompact, buildBarChart };
"""

FILE3_PRE_EDIT = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DataSync — Status Dashboard</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f0f2f5;
      color: #333;
    }
    header {
      background: #1a73e8;
      color: #fff;
      padding: 1rem 2rem;
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    header h1 { font-size: 1.4rem; font-weight: 600; }
    .badge {
      background: #34a853;
      border-radius: 12px;
      padding: 2px 10px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.05em;
    }
    main { padding: 2rem; }
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-top: 1.5rem;
    }
    .card {
      background: #fff;
      border-radius: 8px;
      padding: 1.25rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .card h2 { font-size: 0.85rem; color: #666; margin-bottom: 0.5rem; }
    .card .value { font-size: 2rem; font-weight: 700; color: #1a73e8; }
  </style>
</head>
<body>
  <header>
    <h1>DataSync Dashboard</h1>
    <span class="badge">LIVE</span>
  </header>
  <main>
    <p>System operational as of <strong>2025-03-15 09:42 UTC</strong>.</p>
    <div class="card-grid">
      <div class="card"><h2>Records Processed</h2><div class="value">1.24M</div></div>
      <div class="card"><h2>Active Pipelines</h2><div class="value">38</div></div>
      <div class="card"><h2>Error Rate</h2><div class="value">0.3%</div></div>
      <div class="card"><h2>Avg Latency</h2><div class="value">142ms</div></div>
    </div>
  </main>
</body>
</html>
"""


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # 1. Create Desktop directory
    os.makedirs(DESKTOP, exist_ok=True)

    # 2. Write the EDITED (buffer) versions to disk first
    for fname, content in [
        ('file1.py',   FILE1_EDITED),
        ('file2.js',   FILE2_EDITED),
        ('file3.html', FILE3_EDITED),
    ]:
        fpath = os.path.join(DESKTOP, fname)
        with open(fpath, 'w') as f:
            f.write(content)
        print(f'Created (edited version): {fpath}')

    # 3. Open VSCode with all three files — VSCode loads the edited content
    #    into its in-memory buffer
    files = (
        f'"{DESKTOP}/file1.py" '
        f'"{DESKTOP}/file2.js" '
        f'"{DESKTOP}/file3.html"'
    )
    launch_gui(f'code --new-window {files}', delay_sec=6.0)
    print('VSCode opened with three files. Waiting for full load...')
    time.sleep(3.0)  # extra wait to ensure files are fully loaded into buffer

    # 4. Overwrite disk files with PRE-EDIT content.
    #    VSCode detects the external file change and marks each tab as dirty
    #    (unsaved-changes indicator dot appears).
    for fname, content in [
        ('file1.py',   FILE1_PRE_EDIT),
        ('file2.js',   FILE2_PRE_EDIT),
        ('file3.html', FILE3_PRE_EDIT),
    ]:
        fpath = os.path.join(DESKTOP, fname)
        with open(fpath, 'w') as f:
            f.write(content)
        print(f'Reverted disk file to pre-edit version: {fpath}')

    print('All three VSCode tabs now show unsaved-changes indicator (dot).')
    print('GUI_READY: VSCode open with three dirty tabs on DISPLAY=:0')


create_initial()
