"""
Initial Setup: Create a styled HTML page at ~/Documents/web_page.html
Task ID: pdf_mbc_068
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/web_page.html'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meridian Analytics - Q1 2025 Performance Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 30px;
            background-color: #f8f9fa;
            color: #2c3e50;
            line-height: 1.6;
        }
        h1 {
            color: #1a5276;
            border-bottom: 3px solid #2980b9;
            padding-bottom: 12px;
            font-size: 28px;
        }
        h2 {
            color: #2471a3;
            margin-top: 30px;
            font-size: 20px;
        }
        .subtitle {
            color: #7f8c8d;
            font-size: 14px;
            margin-top: -10px;
            margin-bottom: 25px;
        }
        .highlight {
            background-color: #eaf2f8;
            border-left: 4px solid #2980b9;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 4px 4px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        th {
            background-color: #2980b9;
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px 15px;
            border-bottom: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f2f7fb;
        }
        tr:hover {
            background-color: #e8f0fe;
        }
        .metric-positive {
            color: #27ae60;
            font-weight: bold;
        }
        .metric-negative {
            color: #e74c3c;
            font-weight: bold;
        }
        .footer {
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid #bdc3c7;
            font-size: 12px;
            color: #95a5a6;
            text-align: center;
        }
        ul {
            padding-left: 25px;
        }
        li {
            margin-bottom: 8px;
        }
    </style>
</head>
<body>
    <h1>Meridian Analytics - Q1 2025 Performance Report</h1>
    <p class="subtitle">Prepared by the Strategy & Operations Division | April 2025</p>

    <h2>Executive Summary</h2>
    <p>
        Meridian Analytics demonstrated strong growth across all business segments in the first quarter
        of 2025. Total revenue reached <strong style="color: #1a5276;">$4.82 million</strong>, representing
        a 17.3% increase compared to Q1 2024. Our expansion into the healthcare analytics vertical
        contributed significantly to this growth, accounting for 22% of new client acquisitions.
    </p>

    <div class="highlight">
        <strong>Key Achievement:</strong> The launch of our predictive modeling platform,
        <em>InsightForge Pro</em>, exceeded adoption targets by 40%, onboarding 138 enterprise
        clients within the first 60 days of availability.
    </div>

    <h2>Regional Revenue Breakdown</h2>
    <table>
        <thead>
            <tr>
                <th>Region</th>
                <th>Revenue (USD)</th>
                <th>Clients</th>
                <th>YoY Growth</th>
                <th>Avg. Contract Value</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>North America</td>
                <td>$2,145,000</td>
                <td>412</td>
                <td class="metric-positive">+19.8%</td>
                <td>$5,206</td>
            </tr>
            <tr>
                <td>Europe</td>
                <td>$1,280,000</td>
                <td>287</td>
                <td class="metric-positive">+14.2%</td>
                <td>$4,460</td>
            </tr>
            <tr>
                <td>Asia-Pacific</td>
                <td>$890,000</td>
                <td>195</td>
                <td class="metric-positive">+23.1%</td>
                <td>$4,564</td>
            </tr>
            <tr>
                <td>Latin America</td>
                <td>$325,000</td>
                <td>89</td>
                <td class="metric-positive">+11.7%</td>
                <td>$3,652</td>
            </tr>
            <tr>
                <td>Middle East & Africa</td>
                <td>$180,000</td>
                <td>43</td>
                <td class="metric-negative">-2.4%</td>
                <td>$4,186</td>
            </tr>
        </tbody>
    </table>

    <h2>Product Performance</h2>
    <p>
        Our three core product lines each showed distinct trajectories this quarter. The enterprise
        analytics suite maintained its position as the primary revenue driver, while the newly
        launched InsightForge Pro showed exceptional early traction.
    </p>
    <ul>
        <li><strong>Enterprise Analytics Suite:</strong> $2.91M revenue, 604 active licenses, renewal rate of 94.2%</li>
        <li><strong>InsightForge Pro:</strong> $1.14M revenue, 138 new enterprise clients, NPS score of 72</li>
        <li><strong>DataStream Connect:</strong> $770K revenue, 284 integrations deployed, uptime of 99.97%</li>
    </ul>

    <h2>Operational Highlights</h2>
    <p>
        The engineering team completed the migration of our core infrastructure to a multi-cloud
        architecture, reducing latency by 34% and achieving an overall platform availability of
        99.98%. Additionally, our customer success team expanded to 45 specialists, enabling us
        to reduce average ticket resolution time from 4.2 hours to 2.8 hours.
    </p>

    <div class="highlight">
        <strong>Looking Ahead:</strong> Q2 priorities include the beta launch of our AI-powered
        anomaly detection module, expansion of the APAC sales team, and the integration of
        natural language querying capabilities into InsightForge Pro.
    </div>

    <div class="footer">
        &copy; 2025 Meridian Analytics Inc. | Confidential - Internal Use Only | Report ID: MA-Q1-2025-047
    </div>
</body>
</html>"""

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'Initial file created: {OUTPUT}')

    # Open the HTML file in a browser so the agent can see it and convert it
    # The task requires converting HTML to PDF, so showing it in a browser is appropriate
    launch_gui(f'google-chrome "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Google Chrome with DISPLAY=:0')


create_initial()
