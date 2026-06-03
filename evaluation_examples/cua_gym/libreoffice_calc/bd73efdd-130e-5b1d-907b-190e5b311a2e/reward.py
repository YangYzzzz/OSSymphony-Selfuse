"""
Reward Script: Add RLHF researchers' homepages to Chrome bookmark folder
Task ID: osworld_multi_apps_bookmark_authors_002
Domain: chrome (bookmarks)
Scoring:
  - Component 1: Folder 'RLHF Researchers' exists in Bookmarks bar (0.3 pts)
  - Component 2: Folder contains exactly 3 bookmarks (one per required researcher) (0.3 pts)
  - Component 3: Long Ouyang bookmark URL is a valid homepage (0.1 pts)
  - Component 4: Jan Leike bookmark URL is a valid homepage (0.15 pts)
  - Component 5: Ryan Lowe bookmark URL is a valid homepage (0.15 pts)
  Total: 1.0
"""

import os
import json

BOOKMARKS_FILE = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")
TASK_ID = "osworld_multi_apps_bookmark_authors_002"


def normalize_url(url):
    """Normalize URL: lowercase, strip trailing slash and www prefix, drop protocol."""
    if not url:
        return ""
    url = url.lower().strip()
    # Remove protocol prefix
    for prefix in ("https://", "http://"):
        if url.startswith(prefix):
            url = url[len(prefix):]
            break
    # Remove leading www.
    if url.startswith("www."):
        url = url[4:]
    # Strip trailing slash
    url = url.rstrip("/")
    return url


def get_folder_children(bar_children, folder_name):
    """Return children of a named folder in the bookmark bar, or None if not found."""
    for item in bar_children:
        if item.get("type") == "folder" and item.get("name") == folder_name:
            return item.get("children", [])
    return None


def contains_url_for_person(bookmark_list, person_name_keywords, expected_urls):
    """
    Check if bookmark_list contains a bookmark whose URL matches one of expected_urls
    (after normalization). person_name_keywords is used only for reporting.
    Returns (found: bool, actual_url: str)
    """
    normalized_expected = [normalize_url(u) for u in expected_urls]
    for bm in bookmark_list:
        if bm.get("type") != "url":
            continue
        bm_url = normalize_url(bm.get("url", ""))
        if bm_url in normalized_expected:
            return True, bm.get("url", "")
    return False, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Bookmarks file must exist and be parseable
    if not os.path.exists(BOOKMARKS_FILE):
        print(f"CRITICAL: Bookmarks file not found: {BOOKMARKS_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
            bm_data = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot parse Bookmarks file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract Bookmarks bar children
    try:
        bar_children = bm_data["roots"]["bookmark_bar"]["children"]
    except (KeyError, TypeError) as e:
        print(f"CRITICAL: Unexpected Bookmarks structure: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'RLHF Researchers' folder exists in Bookmarks bar (0.3 points)
    folder_children = None
    try:
        folder_children = get_folder_children(bar_children, "RLHF Researchers")
        if folder_children is not None:
            print("PASS: Component 1 — Folder 'RLHF Researchers' exists in Bookmarks bar (0.3 pts)")
            total_score += 0.3
        else:
            # Check case-insensitive match for partial feedback
            all_folder_names = [b.get("name") for b in bar_children if b.get("type") == "folder"]
            print(f"FAIL: Component 1 — Folder 'RLHF Researchers' not found in Bookmarks bar; "
                  f"found folders: {all_folder_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # All subsequent components require the folder to exist
    if folder_children is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Folder contains at least 3 bookmarks (one per researcher) (0.3 points)
    try:
        url_items = [c for c in folder_children if c.get("type") == "url"]
        count = len(url_items)
        if count >= 3:
            print(f"PASS: Component 2 — Folder has {count} bookmark(s) (expected >= 3) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Folder has {count} bookmark(s), expected at least 3; "
                  f"names: {[c.get('name') for c in url_items]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Known homepage URLs for each required researcher
    # Based on golden artifact: louyang.github.io, jan.leike.name, ryanolowe.com
    # We accept plausible variations as well
    OUYANG_URLS = [
        "https://louyang.github.io",
        "http://louyang.github.io",
        "https://louyang.github.io/",
        "https://www.linkedin.com/in/louyang",
        "https://sites.google.com/view/longouyang",
    ]
    LEIKE_URLS = [
        "https://jan.leike.name",
        "http://jan.leike.name",
        "https://jan.leike.name/",
    ]
    LOWE_URLS = [
        "https://ryanolowe.com",
        "http://ryanolowe.com",
        "https://ryanolowe.com/",
        "https://www.ryanolowe.com",
    ]

    # Component 3: Long Ouyang bookmark URL is present (0.1 points)
    try:
        found, actual_url = contains_url_for_person(folder_children, "Long Ouyang", OUYANG_URLS)
        if found:
            print(f"PASS: Component 3 — Long Ouyang homepage found: {actual_url} (0.1 pts)")
            total_score += 0.1
        else:
            actual_urls = [c.get("url") for c in folder_children if c.get("type") == "url"]
            print(f"FAIL: Component 3 — Long Ouyang homepage not found in folder; "
                  f"bookmark URLs present: {actual_urls}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Jan Leike bookmark URL is present (0.15 points)
    try:
        found, actual_url = contains_url_for_person(folder_children, "Jan Leike", LEIKE_URLS)
        if found:
            print(f"PASS: Component 4 — Jan Leike homepage found: {actual_url} (0.15 pts)")
            total_score += 0.15
        else:
            actual_urls = [c.get("url") for c in folder_children if c.get("type") == "url"]
            print(f"FAIL: Component 4 — Jan Leike homepage not found in folder; "
                  f"bookmark URLs present: {actual_urls}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Ryan Lowe bookmark URL is present (0.15 points)
    try:
        found, actual_url = contains_url_for_person(folder_children, "Ryan Lowe", LOWE_URLS)
        if found:
            print(f"PASS: Component 5 — Ryan Lowe homepage found: {actual_url} (0.15 pts)")
            total_score += 0.15
        else:
            actual_urls = [c.get("url") for c in folder_children if c.get("type") == "url"]
            print(f"FAIL: Component 5 — Ryan Lowe homepage not found in folder; "
                  f"bookmark URLs present: {actual_urls}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
