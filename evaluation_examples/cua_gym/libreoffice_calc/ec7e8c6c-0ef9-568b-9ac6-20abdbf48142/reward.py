"""
Reward Script: Find corresponding author from NeurIPS paper and open their Semantic Scholar profile
Task ID: osworld_multi_apps_paper_scholar_browse_002
Domain: multi_apps (Chrome + PDF)

Scoring Rubric:
  Component 1: Chrome history contains a visit to semanticscholar.org/author/ URL (0.5 pts)
  Component 2: The Semantic Scholar author URL corresponds to Sergey Levine (contains 'Levine' or 'Sergey'
               or 'levine' or specific author ID) (0.5 pts)

Task: Read a NeurIPS paper PDF on the desktop, identify the corresponding author (Sergey Levine,
      marked with *), then open their Semantic Scholar profile in Chrome.
"""

import os
import sqlite3
import shutil

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_002'

# Chrome history DB path
HISTORY_DB = os.path.expanduser('~/.config/google-chrome/Default/History')

# The corresponding author in the PDF is Sergey Levine (marked with *)
# Expected Semantic Scholar profile URL pattern: semanticscholar.org/author/<name-slug>/<id>
EXPECTED_DOMAIN = 'semanticscholar.org'
EXPECTED_PATH_PREFIX = '/author/'
# The author name keywords that must appear in the URL path
AUTHOR_KEYWORDS = ['levine', 'sergey']


def get_chrome_history_urls():
    """
    Read Chrome browsing history from the SQLite database.
    Makes a copy first to avoid database lock issues with running Chrome.
    Returns list of (url, title) tuples.
    """
    if not os.path.exists(HISTORY_DB):
        print(f"FAIL: Chrome History DB not found at {HISTORY_DB}")
        return []
    try:
        tmp_db = '/tmp/reward_history_check.db'
        shutil.copy2(HISTORY_DB, tmp_db)
        conn = sqlite3.connect(tmp_db)
        c = conn.cursor()
        c.execute('SELECT url, title FROM urls ORDER BY last_visit_time DESC')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"ERROR: Could not read Chrome history: {e}")
        return []


def verify_task():
    """
    Verify task completion with progressive scoring.
    Task: Open Sergey Levine's Semantic Scholar author profile in Chrome.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Get all Chrome history URLs
    history_urls = get_chrome_history_urls()
    print(f"INFO: Found {len(history_urls)} URLs in Chrome history")

    # Component 1: Chrome history contains a visit to semanticscholar.org/author/ (0.5 points)
    # This FAILS on initial_env (only Google.com in history) and PASSES on golden_env
    try:
        scholar_author_urls = []
        for url, title in history_urls:
            if url and EXPECTED_DOMAIN in url and EXPECTED_PATH_PREFIX in url:
                scholar_author_urls.append((url, title))

        if scholar_author_urls:
            print(f"PASS: Component 1 — Found {len(scholar_author_urls)} Semantic Scholar author page(s) in history (0.5 pts)")
            for u, t in scholar_author_urls:
                print(f"  URL: {u}  Title: {t}")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — No semanticscholar.org/author/ URL found in Chrome history")
            print(f"  Current history URLs: {[u for u, _ in history_urls[:5]]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The Semantic Scholar author URL is for Sergey Levine (0.5 points)
    # Checks that at least one of the author URLs contains 'Levine' or 'Sergey' (case-insensitive)
    # in the URL path, confirming the correct corresponding author was identified.
    # This FAILS on initial_env (no scholar URLs at all) and PASSES on golden_env.
    try:
        if total_score >= 0.5:  # Only check if Component 1 passed
            levine_urls = []
            for url, title in history_urls:
                if url and EXPECTED_DOMAIN in url and EXPECTED_PATH_PREFIX in url:
                    url_lower = url.lower()
                    # Check if any author keyword appears in the URL
                    if any(kw in url_lower for kw in AUTHOR_KEYWORDS):
                        levine_urls.append((url, title))

            if levine_urls:
                print(f"PASS: Component 2 — Found Sergey Levine's Semantic Scholar profile URL (0.5 pts)")
                for u, t in levine_urls:
                    print(f"  URL: {u}  Title: {t}")
                total_score += 0.5
            else:
                # Also check by title: page title may contain "Sergey Levine"
                levine_by_title = []
                for url, title in history_urls:
                    if url and EXPECTED_DOMAIN in url and EXPECTED_PATH_PREFIX in url:
                        if title and ('levine' in title.lower() or 'sergey' in title.lower()):
                            levine_by_title.append((url, title))

                if levine_by_title:
                    print(f"PASS: Component 2 — Found Sergey Levine's profile by page title (0.5 pts)")
                    for u, t in levine_by_title:
                        print(f"  URL: {u}  Title: {t}")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 2 — Semantic Scholar author URLs found but none match 'Levine' or 'Sergey'")
                    for url, title in history_urls:
                        if EXPECTED_DOMAIN in url and EXPECTED_PATH_PREFIX in url:
                            print(f"  Found URL: {url}  Title: {title}")
        else:
            print(f"SKIP: Component 2 — Skipped because Component 1 failed (no scholar URLs in history)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
