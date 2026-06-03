"""
Reward Script: Complete web_scraper.py parsing logic and capture output to page_titles.txt
Task ID: osworld_multi_apps_vscode_run_capture_008
Domain: multi_apps / vscode + os
Scoring:
  Component 1 (0.4): web_scraper.py has complete BeautifulSoup parsing logic (placeholder replaced)
  Component 2 (0.3): page_titles.txt exists on the Desktop
  Component 3 (0.3): page_titles.txt contains substantive output (URL: title lines, at least one real title)
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_008'

WEB_SCRAPER_PATH = os.path.join(WORKDIR, 'web_scraper.py')
PAGE_TITLES_PATH = os.path.join(WORKDIR, 'page_titles.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: web_scraper.py must exist (it should exist in both initial and golden)
    if not os.path.isfile(WEB_SCRAPER_PATH):
        print(f"CRITICAL: web_scraper.py not found at {WEB_SCRAPER_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: web_scraper.py has complete parsing logic (0.4 points)
    # The initial file has 'title = None  # Replace this line with the correct parsing code'
    # The golden file replaces that with actual BeautifulSoup parsing (e.g., soup.title.string)
    try:
        with open(WEB_SCRAPER_PATH, 'r') as f:
            scraper_content = f.read()

        # Check that the placeholder line is gone
        has_placeholder = 'title = None' in scraper_content

        # Check that actual BeautifulSoup parsing is present
        # Valid patterns: soup.title.string, soup.find('title').text, soup.find('title').get_text(), etc.
        has_bs4_parsing = bool(
            re.search(r'soup\.(title|find\s*\(\s*["\']title["\'])', scraper_content)
        ) and 'title = None' not in scraper_content

        if has_bs4_parsing and not has_placeholder:
            print(f"PASS: Component 1 — web_scraper.py has complete BeautifulSoup parsing logic (placeholder replaced)")
            total_score += 0.4
        elif has_placeholder:
            print(f"FAIL: Component 1 — web_scraper.py still contains placeholder 'title = None'")
        else:
            print(f"FAIL: Component 1 — No BeautifulSoup title parsing found in web_scraper.py")

    except Exception as e:
        print(f"ERROR: Component 1 — could not read web_scraper.py: {e}")

    # Component 2: page_titles.txt exists on the Desktop (0.3 points)
    try:
        if os.path.isfile(PAGE_TITLES_PATH):
            file_size = os.path.getsize(PAGE_TITLES_PATH)
            if file_size > 0:
                print(f"PASS: Component 2 — page_titles.txt exists and is non-empty ({file_size} bytes)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — page_titles.txt exists but is empty")
        else:
            print(f"FAIL: Component 2 — page_titles.txt does not exist at {PAGE_TITLES_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — could not check page_titles.txt existence: {e}")

    # Component 3: page_titles.txt contains substantive output with URL: title format (0.3 points)
    # At least one line should have 'url: title' format with a non-error title
    try:
        if os.path.isfile(PAGE_TITLES_PATH):
            with open(PAGE_TITLES_PATH, 'r') as f:
                titles_content = f.read()

            lines = [l.strip() for l in titles_content.splitlines() if l.strip()]

            # Check for URL: title format lines
            url_title_lines = [l for l in lines if re.match(r'https?://', l) and ': ' in l]

            # Check for at least one successful (non-error) title
            successful_titles = [l for l in url_title_lines if not l.endswith(': Error:') and 'Error:' not in l.split(': ', 1)[-1]]

            if len(url_title_lines) >= 1 and len(successful_titles) >= 1:
                print(f"PASS: Component 3 — page_titles.txt contains {len(url_title_lines)} URL:title lines, {len(successful_titles)} successful")
                total_score += 0.3
            elif len(url_title_lines) >= 1:
                print(f"FAIL: Component 3 — page_titles.txt has URL:title lines but none with successful titles (all errors)")
            else:
                print(f"FAIL: Component 3 — page_titles.txt does not contain expected URL: title format lines")
                print(f"  Content preview: {titles_content[:200]}")
        else:
            print(f"FAIL: Component 3 — page_titles.txt does not exist, skipping content check")
    except Exception as e:
        print(f"ERROR: Component 3 — could not read page_titles.txt: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
