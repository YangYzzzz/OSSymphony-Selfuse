"""
Reward Script: Bookmark first/last-two authors and ArXiv page in Chrome
Task ID: osworld_multi_apps_bookmark_authors_015
Domain: chrome (Chrome bookmarks)
Scoring:
  Component 1: 'Speech Authors' folder exists under Bookmarks bar   (0.2)
  Component 2: Dario Amodei (first author) bookmarked in folder      (0.2)
  Component 3: Peng Qi (second-to-last author) bookmarked in folder  (0.2)
  Component 4: Ziang Xie (last author) bookmarked in folder          (0.2)
  Component 5: ArXiv page for Deep Speech 2 bookmarked in folder     (0.2)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bookmark_authors_015'

# Chrome bookmarks path (x86 Linux)
BOOKMARKS_FILE = os.path.expanduser('~/.config/google-chrome/Default/Bookmarks')


def find_folder(children, folder_name):
    """Find a folder by name in a list of bookmark children. Case-insensitive."""
    for item in children:
        if item.get('type') == 'folder' and item.get('name', '').lower() == folder_name.lower():
            return item
    return None


def get_all_urls_in_folder(folder):
    """Return a list of all URL entries in a folder (non-recursive)."""
    return [item for item in folder.get('children', []) if item.get('type') == 'url']


def url_matches_domain(url, domain_keyword):
    """
    Check if a URL contains a domain keyword (case-insensitive).
    Strips https/http/www for comparison.
    """
    url_lower = url.lower()
    return domain_keyword.lower() in url_lower


def url_matches_any(url, keywords):
    """Return True if URL matches any of the given keywords."""
    return any(url_matches_domain(url, kw) for kw in keywords)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load bookmarks file — precondition gate
    if not os.path.exists(BOOKMARKS_FILE):
        print(f"CRITICAL: Bookmarks file not found at {BOOKMARKS_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(BOOKMARKS_FILE, 'r') as f:
            bm = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot parse Bookmarks file: {e}")
        print("REWARD: 0.0")
        return 0.0

    bar_children = bm.get('roots', {}).get('bookmark_bar', {}).get('children', [])

    # Component 1: 'Speech Authors' folder exists under Bookmarks bar (0.2 points)
    try:
        speech_folder = find_folder(bar_children, 'Speech Authors')
        if speech_folder is not None:
            print("PASS: Component 1 — 'Speech Authors' folder found under Bookmarks bar (0.2 pts)")
            total_score += 0.2
        else:
            folder_names = [b.get('name') for b in bar_children if b.get('type') == 'folder']
            print(f"FAIL: Component 1 — 'Speech Authors' folder not found. Found folders: {folder_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Only continue checking folder contents if the folder was found
    if total_score < 0.2:
        # Folder not found — all remaining checks fail
        print("FAIL: Component 2 — 'Speech Authors' folder missing, cannot check Dario Amodei bookmark")
        print("FAIL: Component 3 — 'Speech Authors' folder missing, cannot check Peng Qi bookmark")
        print("FAIL: Component 4 — 'Speech Authors' folder missing, cannot check Ziang Xie bookmark")
        print("FAIL: Component 5 — 'Speech Authors' folder missing, cannot check ArXiv bookmark")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    folder_urls = get_all_urls_in_folder(speech_folder)
    all_urls = [item.get('url', '') for item in folder_urls]
    all_names = [item.get('name', '') for item in folder_urls]
    print(f"INFO: Found {len(folder_urls)} bookmark(s) in 'Speech Authors' folder")
    for i, item in enumerate(folder_urls):
        print(f"  [{i+1}] Name='{item.get('name')}' URL='{item.get('url')}'")

    # Component 2: Dario Amodei (first author) bookmark present (0.2 points)
    # Accept any URL that refers to Dario Amodei's homepage (dariusamodei, amodei, etc.)
    # or his profile on scholar/research sites
    try:
        dario_found = False
        dario_keywords = ['amodei', 'dario']
        for item in folder_urls:
            url = item.get('url', '')
            name = item.get('name', '')
            if url_matches_any(url, dario_keywords) or 'amodei' in name.lower() or 'dario' in name.lower():
                dario_found = True
                print(f"PASS: Component 2 — Dario Amodei bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
        if not dario_found:
            print(f"FAIL: Component 2 — No bookmark found for Dario Amodei. URLs present: {all_urls}")
        else:
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Peng Qi (second-to-last author) bookmark present (0.2 points)
    # Accept any URL that refers to Peng Qi's homepage or profile
    try:
        pengqi_found = False
        pengqi_keywords = ['pengqi', 'peng-qi', 'peng_qi']
        # Also check name field since Peng Qi's page may not have his name in URL
        for item in folder_urls:
            url = item.get('url', '')
            name = item.get('name', '')
            name_lower = name.lower()
            # Check by name first
            if ('peng qi' in name_lower or 'pengqi' in name_lower or 'peng-qi' in name_lower):
                pengqi_found = True
                print(f"PASS: Component 3 — Peng Qi bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
            # Check URL keywords
            if url_matches_any(url, pengqi_keywords):
                pengqi_found = True
                print(f"PASS: Component 3 — Peng Qi bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
            # Also accept Google Scholar URL for Peng Qi (scholar.google.com/citations?user=XVqyBPYAAAAJ)
            if 'scholar.google.com' in url and 'XVqyBPYAAAAJ' in url:
                pengqi_found = True
                print(f"PASS: Component 3 — Peng Qi Google Scholar bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
            # More relaxed: any scholar URL where the name says Peng Qi
            if 'scholar.google.com' in url and ('peng' in name_lower and 'qi' in name_lower):
                pengqi_found = True
                print(f"PASS: Component 3 — Peng Qi bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
        if not pengqi_found:
            print(f"FAIL: Component 3 — No bookmark found for Peng Qi. URLs present: {all_urls}, Names: {all_names}")
        else:
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Ziang Xie (last author) bookmark present (0.2 points)
    try:
        ziangxie_found = False
        ziangxie_keywords = ['zxie', 'ziangxie', 'ziang-xie', 'ziang_xie', 'xie']
        for item in folder_urls:
            url = item.get('url', '')
            name = item.get('name', '')
            name_lower = name.lower()
            if 'ziang' in name_lower or 'ziang xie' in name_lower or 'xie' in name_lower:
                ziangxie_found = True
                print(f"PASS: Component 4 — Ziang Xie bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
            if url_matches_any(url, ziangxie_keywords):
                ziangxie_found = True
                print(f"PASS: Component 4 — Ziang Xie bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
        if not ziangxie_found:
            print(f"FAIL: Component 4 — No bookmark found for Ziang Xie. URLs present: {all_urls}, Names: {all_names}")
        else:
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: ArXiv page for Deep Speech 2 bookmarked (0.2 points)
    # Deep Speech 2 ArXiv ID is 1512.02595
    try:
        arxiv_found = False
        for item in folder_urls:
            url = item.get('url', '')
            name = item.get('name', '')
            if 'arxiv.org' in url and '1512.02595' in url:
                arxiv_found = True
                print(f"PASS: Component 5 — Deep Speech 2 ArXiv bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
            # Also accept the abs redirect or PDF link
            if 'arxiv.org' in url and ('deep speech' in name.lower() or 'deep_speech' in name.lower()):
                arxiv_found = True
                print(f"PASS: Component 5 — ArXiv bookmark found: name='{name}' url='{url}' (0.2 pts)")
                break
        if not arxiv_found:
            print(f"FAIL: Component 5 — ArXiv page for Deep Speech 2 not found. URLs present: {all_urls}")
        else:
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
