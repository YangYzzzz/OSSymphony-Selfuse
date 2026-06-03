"""
Reward Script: VSCode regex search for IP addresses
Task ID: vscode_ops_034
Domain: vscode
Scoring:
  Component 1 (0.35): Search sidebar is the active view
  Component 2 (0.35): Regex mode is enabled in the search view
  Component 3 (0.30): The IP address regex pattern is set in the search query
"""

import os
import json
import sqlite3
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_034'

# Expected IP regex pattern (or close variant)
EXPECTED_PATTERN = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'


def find_workspace_state_db():
    """Find the workspace-level state.vscdb file."""
    pattern = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage', '*', 'state.vscdb')
    matches = glob.glob(pattern)
    if matches:
        return matches[0]
    return None


def read_workspace_state(db_path, key):
    """Read a value from the workspace state database."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT value FROM ItemTable WHERE key=?', (key,))
        row = cur.fetchone()
        conn.close()
        if row:
            return row[0]
    except Exception as e:
        print(f"ERROR: Failed to read key '{key}' from {db_path}: {e}")
    return None


def is_ip_regex_pattern(pattern_str):
    """Check if the pattern is an IP address regex (allowing minor variants)."""
    import re
    if not pattern_str:
        return False
    # Normalize whitespace
    p = pattern_str.strip()
    # Check for key structural elements of an IP regex:
    # Must contain digit quantifiers like \d{1,3} or \d+ or [0-9]{1,3}
    # Must contain escaped dots (\.)
    # Must have at least 3 escaped dots (for 4 octets)
    has_digit_class = bool(re.search(r'(\\d|\\[0-9\\]|\[0-9\])', p))
    dot_count = p.count('\\.')
    if has_digit_class and dot_count >= 3:
        return True
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find workspace state database
    db_path = find_workspace_state_db()
    if not db_path:
        print("CRITICAL: No workspace state.vscdb found")
        print("REWARD: 0.0")
        return 0.0
    print(f"INFO: Found workspace state DB: {db_path}")

    # Component 1: Search sidebar is the active view (0.35 points)
    try:
        active_viewlet = read_workspace_state(db_path, 'workbench.sidebar.activeviewletid')
        if active_viewlet and active_viewlet.strip('"') == 'workbench.view.search':
            print(f"PASS: Component 1 - Search sidebar is active (value: {active_viewlet}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - Expected search sidebar active, found: {active_viewlet}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Regex mode is enabled (0.35 points)
    try:
        search_memento_raw = read_workspace_state(db_path, 'memento/workbench.view.search')
        if search_memento_raw:
            search_memento = json.loads(search_memento_raw) if isinstance(search_memento_raw, str) else search_memento_raw
            regex_enabled = search_memento.get('query.regex', False)
            if regex_enabled is True:
                print(f"PASS: Component 2 - Regex mode is enabled (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - Regex mode not enabled, query.regex={regex_enabled}")
        else:
            print(f"FAIL: Component 2 - No search memento found (search may not have been used)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: IP address regex pattern is set in search query (0.30 points)
    try:
        search_memento_raw = read_workspace_state(db_path, 'memento/workbench.view.search')
        if search_memento_raw:
            search_memento = json.loads(search_memento_raw) if isinstance(search_memento_raw, str) else search_memento_raw
            content_pattern = search_memento.get('query.contentPattern', '')
            if content_pattern and is_ip_regex_pattern(content_pattern):
                print(f"PASS: Component 3 - IP regex pattern found: '{content_pattern}' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 - Expected IP regex pattern, found: '{content_pattern}'")
        else:
            # Also check search history as fallback
            history_raw = read_workspace_state(db_path, 'workbench.search.history')
            if history_raw:
                history = json.loads(history_raw) if isinstance(history_raw, str) else history_raw
                searches = history.get('search', [])
                ip_found = any(is_ip_regex_pattern(s) for s in searches)
                if ip_found:
                    print(f"PASS: Component 3 - IP regex pattern found in search history (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 - No IP regex in search history: {searches}")
            else:
                print(f"FAIL: Component 3 - No search memento or history found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
