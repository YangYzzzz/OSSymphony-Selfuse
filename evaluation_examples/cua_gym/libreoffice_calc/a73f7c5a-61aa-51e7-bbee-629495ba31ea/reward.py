"""
Reward Script: Create Chrome bookmark folder 'Graph Learning Authors' with author pages
Task ID: osworld_multi_apps_bookmark_authors_007
Domain: chrome (bookmarks)
Scoring:
  Component 1: Folder 'Graph Learning Authors' exists in Bookmarks bar — 0.3 pts
  Component 2: Folder contains exactly 2 bookmarks — 0.3 pts
  Component 3: Bookmarks correspond to Thomas Kipf and Max Welling pages — 0.4 pts
  Total: 1.0
"""

import os
import json

BOOKMARKS_FILE = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")

# Known legitimate academic/personal pages for Thomas Kipf and Max Welling
# Accept any URL that plausibly belongs to these researchers
KIPF_DOMAIN_KEYWORDS = ["tkipf", "kipf", "thomas-kipf", "thomaskipf"]
WELLING_DOMAIN_KEYWORDS = ["welling", "max-welling", "maxwelling", "uva.nl/m.welling", "fnwi.uva.nl"]


def url_matches_author(url, keywords):
    """Check if a URL corresponds to an author by checking for their name/identity in the URL."""
    url_lower = url.lower()
    return any(kw.lower() in url_lower for kw in keywords)


def get_folder_in_bar(bar_children, folder_name):
    """Find a folder in bookmark_bar children by exact name (case-insensitive)."""
    for item in bar_children:
        if item.get("type") == "folder" and item.get("name", "").strip().lower() == folder_name.lower():
            return item
    return None


def verify_task():
    """
    Verify that Chrome bookmarks contain the 'Graph Learning Authors' folder
    under the Bookmarks bar with pages for Thomas Kipf and Max Welling.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load bookmarks file — precondition gate
    try:
        with open(BOOKMARKS_FILE, "r") as f:
            bm = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load Bookmarks file {BOOKMARKS_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get bookmark bar children
    try:
        bar_children = bm["roots"]["bookmark_bar"]["children"]
    except (KeyError, TypeError) as e:
        print(f"CRITICAL: Cannot read bookmark_bar children: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Folder 'Graph Learning Authors' exists in Bookmarks bar (0.3 points)
    # This FAILS on initial (no such folder), PASSES on golden.
    try:
        folder = get_folder_in_bar(bar_children, "Graph Learning Authors")
        if folder is not None:
            print("PASS: Component 1 — Folder 'Graph Learning Authors' found in Bookmarks bar (0.3 pts)")
            total_score += 0.3
        else:
            folder_names = [b.get("name") for b in bar_children if b.get("type") == "folder"]
            print(f"FAIL: Component 1 — No folder named 'Graph Learning Authors' in Bookmarks bar. Found folders: {folder_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Folder contains exactly 2 bookmarks (0.3 points)
    # This FAILS on initial (no folder), PASSES on golden (folder has 2 entries).
    try:
        if folder is not None:
            url_children = [c for c in folder.get("children", []) if c.get("type") == "url"]
            count = len(url_children)
            if count == 2:
                print(f"PASS: Component 2 — Folder contains exactly 2 bookmarks (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Expected exactly 2 bookmarks in folder, found {count}")
        else:
            print("FAIL: Component 2 — Skipped (folder not found in Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bookmarks correspond to Thomas Kipf and Max Welling pages (0.4 points)
    # This FAILS on initial (no folder), PASSES on golden.
    try:
        if folder is not None:
            url_children = [c for c in folder.get("children", []) if c.get("type") == "url"]
            bookmark_urls = [c.get("url", "") for c in url_children]
            bookmark_names = [c.get("name", "") for c in url_children]
            print(f"  Bookmarks in folder: {list(zip(bookmark_names, bookmark_urls))}")

            kipf_found = any(url_matches_author(u, KIPF_DOMAIN_KEYWORDS) for u in bookmark_urls)
            welling_found = any(url_matches_author(u, WELLING_DOMAIN_KEYWORDS) for u in bookmark_urls)

            # Also check bookmark names for author identification
            if not kipf_found:
                kipf_found = any(
                    any(kw.lower() in name.lower() for kw in ["kipf", "thomas"])
                    for name in bookmark_names
                )
            if not welling_found:
                welling_found = any(
                    any(kw.lower() in name.lower() for kw in ["welling", "max"])
                    for name in bookmark_names
                )

            if kipf_found and welling_found:
                print("PASS: Component 3 — Bookmarks identified for both Thomas Kipf and Max Welling (0.4 pts)")
                total_score += 0.4
            elif kipf_found:
                print("FAIL: Component 3 — Thomas Kipf bookmark found but Max Welling bookmark missing/unrecognized")
                print(f"  URLs: {bookmark_urls}")
            elif welling_found:
                print("FAIL: Component 3 — Max Welling bookmark found but Thomas Kipf bookmark missing/unrecognized")
                print(f"  URLs: {bookmark_urls}")
            else:
                print("FAIL: Component 3 — Neither Thomas Kipf nor Max Welling bookmarks recognized")
                print(f"  URLs: {bookmark_urls}")
        else:
            print("FAIL: Component 3 — Skipped (folder not found in Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
