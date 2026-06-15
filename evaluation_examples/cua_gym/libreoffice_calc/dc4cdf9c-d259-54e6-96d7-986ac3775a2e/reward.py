"""
Reward Script: Bookmark authors from multi-agent learning paper in Chrome
Task ID: osworld_multi_apps_bookmark_authors_012
Domain: chrome (multi-app)
Scoring:
  Component 1: 'Multi-Agent Team' folder exists in Bookmarks bar           — 0.30 pts
  Component 2: All 4 required authors' pages are in the folder             — 0.50 pts
               (Bowen Baker, Yi Wu, Bob McGrew, Igor Mordatch, 0.125 each)
  Component 3: bookmarks_screenshot.png exists on Desktop as a valid PNG   — 0.20 pts
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bookmark_authors_012'

# Bookmark folder name expected
EXPECTED_FOLDER = 'Multi-Agent Team'

# Required authors and their expected bookmark names (case-insensitive partial match)
REQUIRED_AUTHORS = ['Bowen Baker', 'Yi Wu', 'Bob McGrew', 'Igor Mordatch']

# Chrome bookmarks file path
BOOKMARKS_FILE = os.path.join(WORKDIR, '.config', 'google-chrome', 'Default', 'Bookmarks')

# Screenshot path on Desktop
SCREENSHOT_PATH = os.path.join(WORKDIR, 'Desktop', 'bookmarks_screenshot.png')

# PNG magic bytes
PNG_MAGIC = b'\x89PNG\r\n\x1a\n'


def get_folder_from_bar(bar_children, folder_name):
    """Find a folder by name in bookmark bar children."""
    for item in bar_children:
        if item.get('type') == 'folder' and item.get('name', '').strip() == folder_name:
            return item
    return None


def get_all_bookmark_names_in_folder(folder):
    """Return list of bookmark names (type=url) inside the folder."""
    names = []
    for item in folder.get('children', []):
        if item.get('type') == 'url':
            names.append(item.get('name', ''))
    return names


def verify_task():
    total_score = 0.0

    # ---- Load bookmarks file ----
    try:
        with open(BOOKMARKS_FILE, 'r') as f:
            bm = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load Bookmarks file {BOOKMARKS_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    bar_children = bm.get('roots', {}).get('bookmark_bar', {}).get('children', [])

    # Component 1: 'Multi-Agent Team' folder exists in Bookmarks bar (0.30 pts)
    try:
        folder = get_folder_from_bar(bar_children, EXPECTED_FOLDER)
        if folder is not None:
            print(f"PASS: Component 1 — '{EXPECTED_FOLDER}' folder found in Bookmarks bar (0.30 pts)")
            total_score += 0.30
        else:
            folder_names = [b.get('name', '') for b in bar_children if b.get('type') == 'folder']
            print(f"FAIL: Component 1 — '{EXPECTED_FOLDER}' folder NOT found in Bookmarks bar. "
                  f"Existing folders: {folder_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        folder = None

    # Component 2: All 4 required authors' pages are in the folder (0.50 pts total, 0.125 each)
    try:
        if folder is None:
            # If folder doesn't exist, no authors can be present
            print(f"FAIL: Component 2 — Folder '{EXPECTED_FOLDER}' not found; cannot check authors (0.0/0.50 pts)")
        else:
            bm_names = get_all_bookmark_names_in_folder(folder)
            bm_names_lower = [n.lower() for n in bm_names]
            print(f"INFO: Bookmarks in '{EXPECTED_FOLDER}': {bm_names}")

            authors_found = 0
            for author in REQUIRED_AUTHORS:
                author_lower = author.lower()
                # Check by name substring match (case-insensitive)
                found = any(author_lower in bm_name or bm_name in author_lower
                            for bm_name in bm_names_lower)
                if found:
                    print(f"PASS: Component 2 — '{author}' bookmark found (0.125 pts)")
                    total_score += 0.125
                    authors_found += 1
                else:
                    print(f"FAIL: Component 2 — '{author}' bookmark NOT found in folder")

            print(f"INFO: Component 2 summary — {authors_found}/{len(REQUIRED_AUTHORS)} authors found "
                  f"({authors_found * 0.125:.3f}/0.50 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: bookmarks_screenshot.png exists on Desktop as a valid PNG (0.20 pts)
    try:
        if not os.path.exists(SCREENSHOT_PATH):
            print(f"FAIL: Component 3 — '{SCREENSHOT_PATH}' does not exist on Desktop")
        else:
            with open(SCREENSHOT_PATH, 'rb') as f:
                header = f.read(8)
            if header == PNG_MAGIC:
                file_size = os.path.getsize(SCREENSHOT_PATH)
                print(f"PASS: Component 3 — bookmarks_screenshot.png exists and is a valid PNG (size: {file_size} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — bookmarks_screenshot.png exists but is NOT a valid PNG "
                      f"(header: {header.hex()})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 3), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
