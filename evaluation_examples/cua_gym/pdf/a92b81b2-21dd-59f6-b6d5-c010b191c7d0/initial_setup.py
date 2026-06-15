"""
Initial Setup: Create analytics data JSON and prepare reports directory
Task ID: pdf_aw_048
Domain: pdf
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_048'
DATA_DIR = f'{WORKDIR}/data'
REPORTS_DIR = f'{WORKDIR}/reports'
DATA_FILE = f'{DATA_DIR}/analytics.json'


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
    # Create directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Create realistic analytics data
    analytics_data = {
        "monthly_visitors": {
            "description": "Website visitors by month for 2025",
            "labels": [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],
            "values": [
                12450, 13200, 15800, 17300, 19500, 22100,
                24800, 23600, 21400, 19800, 18200, 20500
            ]
        },
        "product_revenue": {
            "description": "Revenue by product category in Q4 2025 (USD)",
            "labels": [
                "Cloud Storage", "Analytics Pro", "Security Suite",
                "DevOps Tools", "API Gateway", "Data Pipeline"
            ],
            "values": [
                145200, 98700, 112400, 87300, 63500, 76800
            ]
        },
        "traffic_sources": {
            "description": "Website traffic sources distribution",
            "labels": [
                "Organic Search", "Direct", "Social Media",
                "Email Campaigns", "Paid Ads", "Referral"
            ],
            "values": [
                38.5, 22.1, 16.8, 10.4, 7.9, 4.3
            ]
        },
        "conversion_data": {
            "description": "Ad spend vs conversion rate across 20 campaigns",
            "ad_spend": [
                500, 1200, 800, 3500, 1500, 2200, 4000, 2800, 950, 1800,
                3200, 600, 2500, 1100, 4500, 700, 3800, 1600, 2900, 2100
            ],
            "conversion_rate": [
                2.1, 3.8, 2.9, 5.2, 3.5, 4.1, 5.8, 4.6, 2.5, 3.9,
                5.0, 2.3, 4.3, 3.2, 6.1, 2.6, 5.5, 3.6, 4.8, 4.0
            ],
            "campaign_names": [
                "Spring Promo", "Summer Sale", "Blog Series", "Enterprise Push",
                "Newsletter", "Webinar", "Product Launch", "Case Studies",
                "Social Boost", "Retargeting", "Holiday Deal", "Trial Offer",
                "Partner Co-op", "Content Syndication", "Annual Event",
                "Brand Awareness", "Feature Release", "Upsell Campaign",
                "Win-back", "Loyalty Program"
            ]
        }
    }

    with open(DATA_FILE, 'w') as f:
        json.dump(analytics_data, f, indent=2)

    print(f'Analytics data created: {DATA_FILE}')
    print(f'Reports directory ready: {REPORTS_DIR}')

    # Verify reports dir is empty (no pre-existing dashboard)
    existing = os.listdir(REPORTS_DIR)
    if existing:
        for item in existing:
            path = os.path.join(REPORTS_DIR, item)
            if os.path.isfile(path):
                os.remove(path)
        print('Cleaned reports directory')

    # Open a text editor showing the data file so the agent can see it
    launch_gui(f'xdg-open "{DATA_FILE}"', delay_sec=2.0)
    # Also open the file manager at the reports directory
    launch_gui(f'nautilus "{REPORTS_DIR}"', delay_sec=1.0)
    print('GUI_READY: launched required app(s) with DISPLAY=:0')


create_initial()
