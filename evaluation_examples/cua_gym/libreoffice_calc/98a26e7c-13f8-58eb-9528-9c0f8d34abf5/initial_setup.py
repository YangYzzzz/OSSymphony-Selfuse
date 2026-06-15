"""
Initial Setup: RSS feed reader project that crashes on malformed XML
Task ID: osworld_multi_apps_vscode_debug_crash_011
Domain: multi_apps (VSCode + Python)

Creates an RSS reader project at /home/user/Desktop/rss_reader/ with:
  - fetcher.py: HTTP fetcher for RSS feed URLs
  - parser.py: XML parser WITHOUT error handling (will crash on malformed XML)
  - display.py: Output/display functions
  - main.py: Entry point

VSCode is opened with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/Desktop/rss_reader'
TASK_ID = 'osworld_multi_apps_vscode_debug_crash_011'


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


def create_project_files():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- fetcher.py ---
    fetcher_content = '''\
"""
fetcher.py - HTTP fetcher for RSS feed URLs
"""
import urllib.request
import urllib.error


def fetch_feed(url: str) -> str:
    """Fetch the raw content of an RSS feed URL.

    Args:
        url: The URL of the RSS feed to fetch.

    Returns:
        The raw XML string of the feed.

    Raises:
        urllib.error.URLError: If the request fails.
    """
    headers = {
        'User-Agent': 'RSSReader/1.0 (+https://example.com/rssreader)'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode('utf-8', errors='replace')


def fetch_feeds(urls: list) -> dict:
    """Fetch multiple RSS feed URLs.

    Args:
        urls: List of feed URLs to fetch.

    Returns:
        A dict mapping url -> raw XML string (or None if fetch failed).
    """
    results = {}
    for url in urls:
        try:
            results[url] = fetch_feed(url)
        except Exception as e:
            print(f"[fetcher] Failed to fetch {url}: {e}")
            results[url] = None
    return results
'''

    # --- parser.py (WITHOUT error handling — will crash on malformed XML) ---
    parser_content = '''\
"""
parser.py - RSS/Atom XML parser
"""
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional


def parse_feed(xml_string: str) -> List[Dict]:
    """Parse a raw RSS/Atom XML string and return a list of feed items.

    Args:
        xml_string: The raw XML content of the RSS/Atom feed.

    Returns:
        A list of dicts, each representing one feed item with keys:
        'title', 'link', 'description', 'pubDate'.
    """
    root = ET.fromstring(xml_string)

    items = []

    # Support RSS 2.0
    channel = root.find('channel')
    if channel is not None:
        for item in channel.findall('item'):
            entry = {
                'title': _get_text(item, 'title'),
                'link': _get_text(item, 'link'),
                'description': _get_text(item, 'description'),
                'pubDate': _get_text(item, 'pubDate'),
            }
            items.append(entry)
        return items

    # Support Atom
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('atom:entry', ns):
        link_elem = entry.find('atom:link', ns)
        link = link_elem.get('href') if link_elem is not None else None
        item = {
            'title': _get_text(entry, 'atom:title', ns),
            'link': link,
            'description': _get_text(entry, 'atom:summary', ns),
            'pubDate': _get_text(entry, 'atom:updated', ns),
        }
        items.append(item)

    return items


def _get_text(element, tag: str, ns: Optional[dict] = None) -> Optional[str]:
    """Helper to safely get text from a child element."""
    child = element.find(tag, ns) if ns else element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None


def parse_feeds(feed_contents: dict) -> dict:
    """Parse multiple feeds from their raw XML strings.

    Args:
        feed_contents: A dict mapping url -> raw XML string (None if fetch failed).

    Returns:
        A dict mapping url -> list of items (or empty list on failure).
    """
    results = {}
    for url, xml_string in feed_contents.items():
        if xml_string is None:
            results[url] = []
            continue
        items = parse_feed(xml_string)
        results[url] = items
    return results
'''

    # --- display.py ---
    display_content = '''\
"""
display.py - Display/output functions for RSS feed items
"""
from typing import List, Dict


def display_feed_items(url: str, items: List[Dict]) -> None:
    """Print the items from a single feed.

    Args:
        url: The feed URL (used as a header).
        items: List of feed item dicts.
    """
    print(f"\\n=== Feed: {url} ===")
    if not items:
        print("  (no items)")
        return
    for i, item in enumerate(items, 1):
        title = item.get("title") or "(no title)"
        link = item.get("link") or "(no link)"
        pub_date = item.get("pubDate") or ""
        print(f"  [{i}] {title}")
        print(f"       Link: {link}")
        if pub_date:
            print(f"       Date: {pub_date}")


def display_all_feeds(parsed_feeds: dict) -> None:
    """Display all parsed feed results.

    Args:
        parsed_feeds: A dict mapping url -> list of items.
    """
    total_items = sum(len(v) for v in parsed_feeds.values())
    print(f"\\nDisplaying {len(parsed_feeds)} feed(s), {total_items} total item(s).")
    for url, items in parsed_feeds.items():
        display_feed_items(url, items)
'''

    # --- main.py ---
    main_content = '''\
"""
main.py - Entry point for the RSS reader application
"""
from fetcher import fetch_feeds
from parser import parse_feeds
from display import display_all_feeds

# List of RSS feed URLs to read
FEED_URLS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
]


def main():
    print("RSS Reader starting...")
    print(f"Fetching {len(FEED_URLS)} feed(s)...\\n")

    # Fetch raw XML
    feed_contents = fetch_feeds(FEED_URLS)

    # Parse feeds (may crash on malformed XML)
    parsed_feeds = parse_feeds(feed_contents)

    # Display results
    display_all_feeds(parsed_feeds)

    print("\\nDone.")


if __name__ == "__main__":
    main()
'''

    # Write all files
    files = {
        'fetcher.py': fetcher_content,
        'parser.py': parser_content,
        'display.py': display_content,
        'main.py': main_content,
    }

    for filename, content in files.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    print(f'Project created at: {PROJECT_DIR}')


def setup_gui():
    """Open VSCode with the project folder."""
    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project_files()
setup_gui()
