"""
Reward Script: Save personal/academic pages for first and last two authors of 'Attention Is All You Need'
  in a Chrome bookmark folder named 'Transformer Authors' under Bookmarks bar.
Task ID: osworld_multi_apps_bookmark_authors_001
Domain: chrome (multi-app)

Scoring rubric (sums to 1.0):
  Component 1: 'Transformer Authors' folder exists under Bookmarks bar (0.3 pts)
  Component 2: Folder contains exactly the 3 required authors by name
               (Ashish Vaswani, Lukasz Kaiser, Illia Polosukhin), no extra bookmarks (0.4 pts)
  Component 3: Each author bookmark URL is a non-empty, valid-looking academic/personal URL (0.3 pts)
"""

import json
import os

BOOKMARKS_FILE = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")

# Required authors (first + last two of Vaswani et al. 2017)
REQUIRED_AUTHOR_NAMES = {
    "ashish vaswani",
    "lukasz kaiser",
    "illia polosukhin",
}


def normalize_name(name):
    """Lowercase and strip for loose comparison."""
    return name.strip().lower()


def is_valid_url(url):
    """Return True if URL looks like a real personal/academic page (non-empty, has http/https)."""
    if not url:
        return False
    url = url.strip().lower()
    return url.startswith("http://") or url.startswith("https://")


def find_folder_in_bar(bar_children, folder_name):
    """Return folder node (dict) if a folder with the exact name exists, else None."""
    for node in bar_children:
        if node.get("type") == "folder" and node.get("name", "").strip() == folder_name:
            return node
    return None


def verify_task():
    total_score = 0.0

    # --- Load bookmarks file ---
    try:
        with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
            bm = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load Bookmarks file at {BOOKMARKS_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate bookmark bar children
    try:
        bar_children = bm["roots"]["bookmark_bar"]["children"]
    except Exception as e:
        print(f"CRITICAL: Cannot read bookmark_bar children: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: 'Transformer Authors' folder exists under Bookmarks bar (0.3 pts)
    # ---------------------------------------------------------------
    try:
        folder = find_folder_in_bar(bar_children, "Transformer Authors")
        if folder is not None:
            print("PASS: Component 1 — 'Transformer Authors' folder found under Bookmarks bar (0.3 pts)")
            total_score += 0.3
        else:
            folder_names = [n.get("name") for n in bar_children if n.get("type") == "folder"]
            print(f"FAIL: Component 1 — 'Transformer Authors' folder not found. "
                  f"Existing folders in bar: {folder_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if total_score == 0.0:
        # No folder found; skip further checks that depend on folder contents
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ---------------------------------------------------------------
    # Component 2: Folder contains exactly the 3 required author names, no extras (0.4 pts)
    # ---------------------------------------------------------------
    try:
        folder_children = folder.get("children", [])
        url_entries = [c for c in folder_children if c.get("type") == "url"]
        entry_names_norm = {normalize_name(c.get("name", "")) for c in url_entries}

        missing_authors = REQUIRED_AUTHOR_NAMES - entry_names_norm
        extra_entries = entry_names_norm - REQUIRED_AUTHOR_NAMES
        exact_count = len(url_entries) == 3

        if not missing_authors and not extra_entries and exact_count:
            print(f"PASS: Component 2 — Folder contains exactly 3 required authors "
                  f"(Ashish Vaswani, Lukasz Kaiser, Illia Polosukhin), no extras (0.4 pts)")
            total_score += 0.4
        else:
            if missing_authors:
                print(f"FAIL: Component 2 — Missing authors: {missing_authors}")
            if extra_entries:
                print(f"FAIL: Component 2 — Extra unexpected entries: {extra_entries}")
            if not exact_count:
                print(f"FAIL: Component 2 — Expected 3 bookmarks, found {len(url_entries)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: All 3 author URLs are valid-looking academic/personal URLs (0.3 pts)
    # ---------------------------------------------------------------
    try:
        folder_children = folder.get("children", [])
        url_entries = [c for c in folder_children if c.get("type") == "url"]

        invalid_entries = [
            f"{c.get('name', '')!r}: {c.get('url', '')!r}"
            for c in url_entries
            if not is_valid_url(c.get("url", ""))
        ]
        for entry in url_entries:
            if is_valid_url(entry.get("url", "")):
                print(f"  URL check OK: {entry.get('name', '')!r} -> {entry.get('url', '')}")

        if len(invalid_entries) == 0 and len(url_entries) >= 1:
            print(f"PASS: Component 3 — All author URLs are valid HTTP/HTTPS links (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Invalid or missing URLs: {invalid_entries}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
