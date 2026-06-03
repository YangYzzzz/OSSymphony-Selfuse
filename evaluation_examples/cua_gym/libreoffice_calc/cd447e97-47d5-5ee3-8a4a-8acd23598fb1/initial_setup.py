"""
Initial Setup: Import CSV website traffic data workflow
Task ID: calc_wf_023
Domain: libreoffice_calc

Creates a CSV file 'web_traffic.csv' on the Desktop with 90 rows of website
traffic data (Date, Page, Visitors, Bounce Rate, Avg Time) spanning 12 weeks.
Approximately 6 rows have blank Visitors cells. Opens LibreOffice Calc with
a blank workbook for the agent to work with.
"""

import csv
import os
import random
import shlex
import subprocess
import time
from datetime import datetime, timedelta

WORKDIR = '/home/user'
TASK_ID = 'calc_wf_023'
CSV_PATH = f'{WORKDIR}/Desktop/web_traffic.csv'
XLSX_PATH = f'{WORKDIR}/{TASK_ID}.xlsx'

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
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    random.seed(42)

    pages = [
        '/home', '/products', '/about', '/contact', '/blog',
        '/pricing', '/features', '/docs', '/support', '/careers',
        '/blog/seo-tips', '/blog/marketing-guide', '/products/enterprise',
        '/docs/api-reference', '/features/analytics'
    ]

    # Generate 90 rows spanning 12 weeks (84 days)
    start_date = datetime(2025, 1, 6)  # Monday, week 2

    rows = []
    blank_indices = random.sample(range(90), 6)  # 6 rows with blank Visitors

    for i in range(90):
        day_offset = int(i * 84 / 90)  # spread across 84 days
        date = start_date + timedelta(days=day_offset)
        page = random.choice(pages)

        if i in blank_indices:
            visitors = ''
        else:
            # Base visitors vary by page popularity
            base = {
                '/home': 1200, '/products': 800, '/pricing': 600,
                '/features': 500, '/blog': 450, '/about': 300,
                '/contact': 250, '/docs': 400, '/support': 350,
                '/careers': 200, '/blog/seo-tips': 380,
                '/blog/marketing-guide': 320, '/products/enterprise': 280,
                '/docs/api-reference': 410, '/features/analytics': 370
            }.get(page, 300)
            # Add weekly growth trend + daily noise
            week_num = day_offset // 7
            visitors = int(base * (1 + week_num * 0.03) + random.randint(-80, 80))

        bounce_rate = round(random.uniform(25.0, 65.0), 1)
        avg_time = round(random.uniform(45.0, 320.0), 1)

        rows.append([
            date.strftime('%Y-%m-%d'),
            page,
            visitors,
            bounce_rate,
            avg_time
        ])

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Page', 'Visitors', 'Bounce Rate', 'Avg Time'])
        writer.writerows(rows)

    print(f'CSV file created: {CSV_PATH}')
    print(f'Total rows: {len(rows)}, Blank Visitors rows: {len(blank_indices)}')

    # Open LibreOffice Calc with a blank workbook so the agent can import the CSV
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')

create_initial()
