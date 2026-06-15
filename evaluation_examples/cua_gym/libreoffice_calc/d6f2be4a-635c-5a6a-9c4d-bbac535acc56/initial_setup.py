"""
Initial Setup: Incomplete web_scraper.py with urls.txt on Desktop for VSCode task
Task ID: osworld_multi_apps_vscode_run_capture_008
Domain: multi_apps (VSCode + OS)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_008'


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
    # Ensure Desktop directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    # --- Create urls.txt ---
    urls_path = os.path.join(WORKDIR, 'urls.txt')
    urls_content = """https://www.python.org
https://www.wikipedia.org
https://www.github.com
https://www.stackoverflow.com
https://www.bbc.com
"""
    with open(urls_path, 'w') as f:
        f.write(urls_content)
    print(f'Created: {urls_path}')

    # --- Create incomplete web_scraper.py ---
    web_scraper_path = os.path.join(WORKDIR, 'web_scraper.py')
    web_scraper_content = '''#!/usr/bin/env python3
"""
Web Scraper: reads URLs from urls.txt, fetches each page title,
and prints all titles.
"""

import requests
from bs4 import BeautifulSoup

URLS_FILE = '/home/user/Desktop/urls.txt'


def get_page_title(url):
    """Fetch the HTML title of a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # TODO: Complete the parsing logic to extract the page title
        # Hint: use soup.find() or soup.title to get the <title> tag
        title = None  # Replace this line with the correct parsing code
        if title:
            return title.strip()
        else:
            return 'No title found'
    except Exception as e:
        return f'Error: {e}'


def main():
    with open(URLS_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        title = get_page_title(url)
        print(f'{url}: {title}')


if __name__ == '__main__':
    main()
'''
    with open(web_scraper_path, 'w') as f:
        f.write(web_scraper_content)
    print(f'Created: {web_scraper_path}')

    # Ensure requests and beautifulsoup4 are installed
    subprocess.run(
        ['pip3', 'install', 'requests', 'beautifulsoup4'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print('Dependencies checked: requests, beautifulsoup4')

    # GUI-ready startup: open VSCode with the web_scraper.py file
    launch_gui(f'code "{web_scraper_path}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with web_scraper.py (DISPLAY=:0)')


create_initial()
