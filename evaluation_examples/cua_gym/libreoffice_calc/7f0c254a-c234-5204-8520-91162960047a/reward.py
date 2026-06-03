"""
Reward Script: Prepare academic writing workspace
Task ID: osworld_multi_apps_workspace_init_012
Domain: multi_apps (OS / Chrome / VSCode)

Task: open ~/Documents/thesis in the file manager (Nautilus), terminal, and VSCode
      with LaTeX extension support, then load Overleaf and LaTeX Wikibook in Chrome,
      plus a third tab to https://library.mit.edu.

Scoring Rubric (total = 1.0):
  Component 1: Nautilus file manager is open showing ~/Documents/thesis       (0.20 pts)
  Component 2: Terminal (bash) is open with CWD = ~/Documents/thesis          (0.20 pts)
  Component 3: VSCode is open with ~/Documents/thesis workspace               (0.20 pts)
  Component 4: Chrome has a tab for https://www.overleaf.com                  (0.15 pts)
  Component 5: Chrome has a tab for https://en.wikibooks.org/wiki/LaTeX       (0.15 pts)
  Component 6: Chrome has a tab for https://library.mit.edu                   (0.10 pts)

Verification strategy:
  - Components 1-3 are verified via /proc filesystem (process list + CWD).
  - Components 4-6 are verified via the Chrome process cmdline (URLs passed at launch)
    and also corroborated by Chrome History sqlite database.
  - Chrome CDP is NOT used because Chrome was not launched with --remote-debugging-port.
"""

import os
import shutil
import sqlite3

THESIS_PATH = '/home/user/Documents/thesis'


# ---------------------------------------------------------------------------
# Helper: read all running processes as a list of (pid, cmdline, cwd) tuples
# ---------------------------------------------------------------------------

def get_processes():
    """Return list of (pid, cmdline_str, cwd) for every readable process."""
    procs = []
    try:
        for entry in os.listdir('/proc'):
            if not entry.isdigit():
                continue
            pid = entry
            try:
                with open(f'/proc/{pid}/cmdline', 'rb') as f:
                    cmdline = f.read().decode('utf-8', errors='replace').replace('\x00', ' ').strip()
                try:
                    cwd = os.readlink(f'/proc/{pid}/cwd')
                except OSError:
                    cwd = ''
                procs.append((pid, cmdline, cwd))
            except (PermissionError, FileNotFoundError):
                continue
    except Exception as e:
        print(f"ERROR: Could not iterate /proc: {e}")
    return procs


# ---------------------------------------------------------------------------
# Helper: get Chrome history URLs (copy DB to avoid lock)
# ---------------------------------------------------------------------------

def get_chrome_history_urls():
    """Return set of URLs from Chrome History, or empty set on failure."""
    src = '/home/user/.config/google-chrome/Default/History'
    dst = '/tmp/reward_chrome_history_copy.db'
    try:
        shutil.copy2(src, dst)
        conn = sqlite3.connect(dst)
        c = conn.cursor()
        c.execute('SELECT url FROM urls')
        urls = {row[0] for row in c.fetchall()}
        conn.close()
        return urls
    except Exception as e:
        print(f"WARN: Could not read Chrome history: {e}")
        return set()


# ---------------------------------------------------------------------------
# Helper: URL domain/path matching (tolerant of trailing slashes, www prefix)
# ---------------------------------------------------------------------------

def url_matches_domain(url, domain_fragment):
    """True if domain_fragment appears in the URL (case-insensitive)."""
    return domain_fragment.lower() in url.lower()


# ---------------------------------------------------------------------------
# Main verification
# ---------------------------------------------------------------------------

def verify_task():
    """
    Verify that the academic writing workspace has been set up correctly.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0
    procs = get_processes()

    # Precondition: ~/Documents/thesis must exist (gate only, not scored)
    if not os.path.isdir(THESIS_PATH):
        print(f"CRITICAL: {THESIS_PATH} does not exist. Workspace cannot be set up.")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Component 1: Nautilus file manager is open showing ~/Documents/thesis
    # (0.20 points)
    # Verification: a 'nautilus' process exists whose cmdline includes the
    # thesis path.
    # ------------------------------------------------------------------
    try:
        nautilus_open = False
        for pid, cmdline, cwd in procs:
            if 'nautilus' in cmdline and THESIS_PATH in cmdline:
                nautilus_open = True
                break
        if nautilus_open:
            print(f"PASS: Component 1 — Nautilus is open showing {THESIS_PATH} (0.20 pts)")
            total_score += 0.20
        else:
            # Also accept: nautilus is running and CWD is thesis (some implementations)
            for pid, cmdline, cwd in procs:
                if 'nautilus' in cmdline and cwd == THESIS_PATH:
                    nautilus_open = True
                    break
            if nautilus_open:
                print(f"PASS: Component 1 — Nautilus running with thesis CWD (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — Nautilus not found open with {THESIS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Terminal is open with CWD = ~/Documents/thesis
    # (0.20 points)
    # Verification: a 'bash' process (from gnome-terminal or similar) has
    # its CWD set to the thesis directory.
    # ------------------------------------------------------------------
    try:
        terminal_ready = False
        for pid, cmdline, cwd in procs:
            # Match a bare bash process (terminal shell) with the thesis CWD
            if cmdline.strip().startswith('bash') and cwd == THESIS_PATH:
                terminal_ready = True
                break
        if terminal_ready:
            print(f"PASS: Component 2 — Terminal bash CWD is {THESIS_PATH} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No bash process found with CWD={THESIS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: VSCode is open with ~/Documents/thesis
    # (0.20 points)
    # Verification: a 'code' process has the thesis path in its cmdline,
    # OR VSCode's workspaceStorage contains a workspace.json pointing to it.
    # ------------------------------------------------------------------
    try:
        vscode_ready = False

        # Primary check: VSCode process cmdline
        for pid, cmdline, cwd in procs:
            if '/usr/share/code/code' in cmdline and THESIS_PATH in cmdline and '--type' not in cmdline:
                vscode_ready = True
                break

        # Fallback: check VSCode workspaceStorage
        if not vscode_ready:
            ws_dir = '/home/user/.config/Code/User/workspaceStorage'
            if os.path.isdir(ws_dir):
                import json
                for folder_hash in os.listdir(ws_dir):
                    ws_json = os.path.join(ws_dir, folder_hash, 'workspace.json')
                    if os.path.isfile(ws_json):
                        try:
                            with open(ws_json) as f:
                                ws_data = json.load(f)
                            folder_uri = ws_data.get('folder', '')
                            if THESIS_PATH in folder_uri:
                                vscode_ready = True
                                break
                        except Exception:
                            pass

        if vscode_ready:
            print(f"PASS: Component 3 — VSCode is open with {THESIS_PATH} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — VSCode not found open with {THESIS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Components 4-6: Chrome tabs
    # Verification strategy:
    #   Primary: inspect the Chrome process cmdline (URLs passed at launch)
    #   Fallback: Chrome History sqlite database
    # ------------------------------------------------------------------

    # Collect Chrome process cmdline
    chrome_cmdline = ''
    for pid, cmdline, cwd in procs:
        if '/opt/google/chrome/chrome' in cmdline and '--type' not in cmdline and 'crashpad' not in cmdline and 'zygote' not in cmdline:
            chrome_cmdline = cmdline
            break

    chrome_history_urls = get_chrome_history_urls()

    def chrome_has_url(domain_fragment):
        """Check Chrome cmdline or history for a URL matching domain_fragment."""
        if url_matches_domain(chrome_cmdline, domain_fragment):
            return True
        for hist_url in chrome_history_urls:
            if url_matches_domain(hist_url, domain_fragment):
                return True
        return False

    # ------------------------------------------------------------------
    # Component 4: Chrome has a tab for Overleaf
    # (0.15 points)
    # ------------------------------------------------------------------
    try:
        if chrome_has_url('overleaf.com'):
            print("PASS: Component 4 — Chrome has Overleaf tab (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 4 — No Overleaf tab found in Chrome")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------
    # Component 5: Chrome has a tab for LaTeX Wikibook
    # (0.15 points)
    # ------------------------------------------------------------------
    try:
        if chrome_has_url('wikibooks.org/wiki/LaTeX'):
            print("PASS: Component 5 — Chrome has LaTeX Wikibook tab (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 5 — No LaTeX Wikibook tab found in Chrome")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ------------------------------------------------------------------
    # Component 6: Chrome has a tab for MIT library portal
    # (0.10 points)
    # ------------------------------------------------------------------
    try:
        if chrome_has_url('library.mit.edu') or chrome_has_url('libraries.mit.edu'):
            print("PASS: Component 6 — Chrome has MIT library tab (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 6 — No MIT library tab found in Chrome")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
