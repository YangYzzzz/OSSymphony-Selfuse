"""
Initial Setup: Configure a Dev Container with Dockerfile for a Python scraper project
Task ID: vscode_rrt_019
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_019'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'scraper')


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
    # Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create main.py - a realistic web scraper
    main_py = '''\
#!/usr/bin/env python3
"""Web scraper for collecting product prices from example retailers."""

import requests
from bs4 import BeautifulSoup
import csv
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

URLS = [
    "https://example.com/products/electronics",
    "https://example.com/products/books",
    "https://example.com/products/clothing",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}


def fetch_page(url: str) -> str:
    """Fetch a single page with retry logic."""
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt+1} failed for {url}: {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch {url} after 3 attempts")


def parse_products(html: str) -> list:
    """Extract product name and price from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for item in soup.select(".product-card"):
        name = item.select_one(".product-name")
        price = item.select_one(".product-price")
        if name and price:
            products.append({
                "name": name.get_text(strip=True),
                "price": price.get_text(strip=True),
            })
    return products


def save_to_csv(products: list, output_path: str):
    """Write product data to CSV."""
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price"])
        writer.writeheader()
        writer.writerows(products)
    logger.info(f"Saved {len(products)} products to {output_path}")


def main():
    all_products = []
    for url in URLS:
        logger.info(f"Scraping {url}...")
        html = fetch_page(url)
        products = parse_products(html)
        all_products.extend(products)
        time.sleep(1)  # polite delay

    save_to_csv(all_products, "products.csv")
    logger.info(f"Total products scraped: {len(all_products)}")


if __name__ == "__main__":
    main()
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    # Create requirements.txt
    requirements = """\
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # Create a simple README
    readme = """\
# Product Price Scraper

A simple web scraper that collects product prices from example retail sites
and exports them to CSV format.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Output will be saved to `products.csv`.

## Features

- Retry logic with exponential backoff
- CSV export
- Configurable target URLs
- Polite scraping with delays between requests
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Create a small config file
    config_py = '''\
"""Scraper configuration constants."""

# Target domains
TARGET_DOMAINS = [
    "example.com",
]

# Request settings
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 1.0

# Output settings
OUTPUT_DIR = "output"
OUTPUT_FORMAT = "csv"
'''
    with open(os.path.join(PROJECT_DIR, 'config.py'), 'w') as f:
        f.write(config_py)

    # Ensure NO .devcontainer directory exists (task requires creating it)
    devcontainer_dir = os.path.join(PROJECT_DIR, '.devcontainer')
    if os.path.exists(devcontainer_dir):
        import shutil
        shutil.rmtree(devcontainer_dir)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: main.py, requirements.txt, README.md, config.py')
    print(f'No .devcontainer directory (task requires creating it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
