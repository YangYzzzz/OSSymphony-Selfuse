"""
Initial Setup: Configure HTML auto-closing tags and auto-rename matching tags in VSCode settings.
Task ID: vscode_lp_045
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_045'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
HTML_FILE = os.path.join(WORKDIR, f'{TASK_ID}.html')


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


def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            import re
            content = f.read()
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # Step 1: Create a realistic HTML file for the task
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quarterly Sales Dashboard - Acme Corp</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f6f9;
            color: #333;
        }
        .dashboard-header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 24px;
        }
        .dashboard-header h1 {
            margin: 0 0 8px 0;
            font-size: 28px;
        }
        .dashboard-header p {
            margin: 0;
            opacity: 0.85;
            font-size: 14px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        .metric-card h3 {
            margin: 0 0 8px 0;
            font-size: 13px;
            text-transform: uppercase;
            color: #7f8c8d;
            letter-spacing: 0.5px;
        }
        .metric-card .value {
            font-size: 32px;
            font-weight: 700;
            color: #2c3e50;
        }
        .metric-card .change {
            font-size: 13px;
            margin-top: 4px;
        }
        .change.positive { color: #27ae60; }
        .change.negative { color: #e74c3c; }
        .data-table {
            width: 100%;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border-collapse: collapse;
            margin-bottom: 24px;
        }
        .data-table thead th {
            background: #ecf0f1;
            padding: 12px 16px;
            text-align: left;
            font-size: 13px;
            text-transform: uppercase;
            color: #7f8c8d;
            border-bottom: 2px solid #ddd;
        }
        .data-table tbody td {
            padding: 12px 16px;
            border-bottom: 1px solid #eee;
        }
        .data-table tbody tr:hover {
            background: #f8f9fa;
        }
        .section-title {
            font-size: 20px;
            color: #2c3e50;
            margin: 0 0 16px 0;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #95a5a6;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>Quarterly Sales Dashboard</h1>
        <p>Acme Corporation - Q1 2025 Performance Overview</p>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <h3>Total Revenue</h3>
            <div class="value">$2.4M</div>
            <div class="change positive">+12.3% vs Q4 2024</div>
        </div>
        <div class="metric-card">
            <h3>New Customers</h3>
            <div class="value">847</div>
            <div class="change positive">+8.7% vs Q4 2024</div>
        </div>
        <div class="metric-card">
            <h3>Avg Deal Size</h3>
            <div class="value">$18.5K</div>
            <div class="change negative">-2.1% vs Q4 2024</div>
        </div>
        <div class="metric-card">
            <h3>Win Rate</h3>
            <div class="value">34.2%</div>
            <div class="change positive">+1.8% vs Q4 2024</div>
        </div>
    </div>

    <h2 class="section-title">Top Performing Regions</h2>
    <table class="data-table">
        <thead>
            <tr>
                <th>Region</th>
                <th>Sales Rep</th>
                <th>Revenue</th>
                <th>Deals Closed</th>
                <th>Quota Attainment</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Northeast</td>
                <td>Sarah Chen</td>
                <td>$485,200</td>
                <td>28</td>
                <td>118%</td>
            </tr>
            <tr>
                <td>West Coast</td>
                <td>Marcus Johnson</td>
                <td>$412,800</td>
                <td>24</td>
                <td>106%</td>
            </tr>
            <tr>
                <td>Southeast</td>
                <td>Priya Patel</td>
                <td>$378,600</td>
                <td>22</td>
                <td>97%</td>
            </tr>
            <tr>
                <td>Midwest</td>
                <td>David Kim</td>
                <td>$341,900</td>
                <td>19</td>
                <td>88%</td>
            </tr>
            <tr>
                <td>Southwest</td>
                <td>Elena Rodriguez</td>
                <td>$298,400</td>
                <td>17</td>
                <td>82%</td>
            </tr>
            <tr>
                <td>Pacific Northwest</td>
                <td>James Okafor</td>
                <td>$267,100</td>
                <td>15</td>
                <td>76%</td>
            </tr>
            <tr>
                <td>Mountain</td>
                <td>Lisa Wang</td>
                <td>$215,000</td>
                <td>12</td>
                <td>63%</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        <p>Generated by Acme Analytics Platform | Data as of March 31, 2025</p>
    </div>
</body>
</html>
"""

    os.makedirs(WORKDIR, exist_ok=True)
    with open(HTML_FILE, 'w') as f:
        f.write(html_content)
    print(f'HTML file created: {HTML_FILE}')

    # Step 2: Ensure VSCode settings do NOT have the target settings
    # Set them explicitly to false so the initial state is clearly "not configured"
    settings = load_settings()
    settings['html.autoClosingTags'] = False
    settings['editor.linkedEditing'] = False
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Settings updated: autoClosingTags=false, linkedEditing=false')

    # Step 3: Launch VSCode with the HTML file
    launch_gui(f'code "{HTML_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
