"""
Reward Script: Set up complete frontend workspace for Vue.js project
Task ID: osworld_multi_apps_workspace_init_009
Domain: multi_app (os + chrome + vscode)
Scoring:
  - Component 1: Nautilus open with /home/user/Projects/vue-dashboard (0.25 pts)
  - Component 2: Terminal shell with CWD /home/user/Projects/vue-dashboard (0.25 pts)
  - Component 3: VSCode open with /home/user/Projects/vue-dashboard folder (0.25 pts)
  - Component 4: Chrome tabs contain vuejs.org/guide and vitejs.dev/guide (0.25 pts)
"""

import os
import shutil
import sqlite3
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_workspace_init_009'
VUE_DASHBOARD_PATH = '/home/user/Projects/vue-dashboard'


def get_all_proc_cmdlines():
    """
    Read all process command lines from /proc filesystem.
    Returns list of (pid, cmdline_str).
    Does NOT use subprocess — reads /proc directly.
    """
    proc_infos = []
    try:
        for pid in os.listdir('/proc'):
            if pid.isdigit():
                try:
                    with open(f'/proc/{pid}/cmdline', 'rb') as f:
                        raw = f.read()
                    cmdline = raw.replace(b'\x00', b' ').decode('utf-8', errors='replace').strip()
                    if cmdline:
                        proc_infos.append((pid, cmdline))
                except (PermissionError, FileNotFoundError, OSError):
                    pass
    except Exception:
        pass
    return proc_infos


def get_process_cwd(pid):
    """
    Read the CWD of a process via /proc/<pid>/cwd symlink.
    Returns resolved path string, or None on error.
    """
    try:
        return os.readlink(f'/proc/{pid}/cwd')
    except (OSError, PermissionError):
        return None


def verify_task():
    """
    Verify that the Vue.js frontend workspace is fully set up:
    1. Nautilus is open showing ~/Projects/vue-dashboard
    2. A terminal shell has CWD set to ~/Projects/vue-dashboard
    3. VSCode is open with ~/Projects/vue-dashboard as the workspace folder
    4. Chrome has tabs open for vuejs.org/guide and vitejs.dev/guide
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vue-dashboard directory must exist
    if not os.path.isdir(VUE_DASHBOARD_PATH):
        print(f"CRITICAL: vue-dashboard directory not found at {VUE_DASHBOARD_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read all process cmdlines once
    procs = get_all_proc_cmdlines()

    # -----------------------------------------------------------------------
    # Component 1: Nautilus open with vue-dashboard (0.25 points)
    # Task-introduced change: Nautilus was NOT running on initial_env.
    # Only passes when Nautilus is launched with the vue-dashboard path.
    # -----------------------------------------------------------------------
    try:
        nautilus_found = False
        for pid, cmdline in procs:
            # Must be the main nautilus process (not a subprocess/helper) and must
            # have been launched with the vue-dashboard path argument
            if 'nautilus' in cmdline and 'vue-dashboard' in cmdline and '--type=' not in cmdline:
                nautilus_found = True
                print(f"PASS: Component 1 — Nautilus running with vue-dashboard (pid {pid}: {cmdline[:100]})")
                break

        if nautilus_found:
            total_score += 0.25
        else:
            print("FAIL: Component 1 — Nautilus not found running with vue-dashboard path")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Terminal shell with CWD = vue-dashboard (0.25 points)
    # Task-introduced change: No shell was in vue-dashboard CWD on initial_env.
    # -----------------------------------------------------------------------
    try:
        terminal_in_vue_dashboard = False

        # Find all bash/sh/zsh processes and check their CWD via /proc
        for pid, cmdline in procs:
            # Match interactive shell processes (not wrapper scripts)
            basename = cmdline.strip().split()[0] if cmdline.strip() else ''
            shell_name = os.path.basename(basename)
            if shell_name in ('bash', 'sh', 'zsh', 'fish'):
                cwd = get_process_cwd(pid)
                if cwd and (cwd == VUE_DASHBOARD_PATH or cwd.rstrip('/') == VUE_DASHBOARD_PATH.rstrip('/')):
                    terminal_in_vue_dashboard = True
                    print(f"PASS: Component 2 — Shell process (pid {pid}, {shell_name}) has CWD {cwd}")
                    break

        if terminal_in_vue_dashboard:
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — No shell process found with CWD = {VUE_DASHBOARD_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: VSCode open with vue-dashboard folder (0.25 points)
    # Task-introduced change: VSCode was NOT running on initial_env (no VSCode procs).
    # -----------------------------------------------------------------------
    try:
        vscode_with_vue = False

        # Method 1: Check VSCode process cmdline — main process is launched with the folder path
        for pid, cmdline in procs:
            if '/usr/share/code/code' in cmdline and 'vue-dashboard' in cmdline and '--type=' not in cmdline:
                vscode_with_vue = True
                print(f"PASS: Component 3 — VSCode running with vue-dashboard (pid {pid}: {cmdline[:120]})")
                break

        # Method 2: Check VSCode storage.json for active workspace association
        # This captures cases where VSCode was opened without path argument but has the workspace
        if not vscode_with_vue:
            storage_path = '/home/user/.config/Code/User/globalStorage/storage.json'
            if os.path.exists(storage_path):
                try:
                    with open(storage_path) as f:
                        storage_data = json.load(f)

                    vue_uri = 'file:///home/user/Projects/vue-dashboard'
                    # Check profileAssociations workspaces
                    profile_assoc = storage_data.get('profileAssociations', {})
                    workspaces = profile_assoc.get('workspaces', {})
                    backup_folders = storage_data.get('backupWorkspaces', {}).get('folders', [])

                    workspace_found = (
                        vue_uri in workspaces or
                        any('vue-dashboard' in f.get('folderUri', '') for f in backup_folders)
                    )

                    # VSCode must also be currently running
                    vscode_running = any(
                        '/usr/share/code/code' in cmdline and '--type=' not in cmdline
                        for _, cmdline in procs
                    )

                    if workspace_found and vscode_running:
                        vscode_with_vue = True
                        print(f"PASS: Component 3 — VSCode running with vue-dashboard workspace confirmed via storage.json")
                except Exception as e:
                    print(f"INFO: Could not read VSCode storage.json: {e}")

        if vscode_with_vue:
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — VSCode not found running with vue-dashboard workspace")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Chrome with vuejs.org/guide AND vitejs.dev/guide tabs (0.25 points)
    # Task-introduced change: Chrome was NOT running on initial_env, no history entries.
    # Both URLs must be present (launched together as the workspace setup).
    # -----------------------------------------------------------------------
    try:
        vuejs_tab_found = False
        vitejs_tab_found = False

        # Method 1: Check Chrome main process cmdline — URLs passed as arguments on launch
        for pid, cmdline in procs:
            if '/opt/google/chrome/chrome' in cmdline and '--type=' not in cmdline and 'crashpad' not in cmdline:
                if 'vuejs.org/guide' in cmdline:
                    vuejs_tab_found = True
                    print(f"PASS: Component 4a — Chrome cmdline contains vuejs.org/guide")
                if 'vitejs.dev/guide' in cmdline or 'vite.dev/guide' in cmdline:
                    vitejs_tab_found = True
                    print(f"PASS: Component 4b — Chrome cmdline contains vitejs.dev/guide")

        # Method 2: Check Chrome history DB by copying it (avoids SQLite lock issues)
        if not (vuejs_tab_found and vitejs_tab_found):
            HISTORY_DB = '/home/user/.config/google-chrome/Default/History'
            tmp_db = '/tmp/chrome_history_reward_copy.db'

            if os.path.exists(HISTORY_DB):
                try:
                    shutil.copy2(HISTORY_DB, tmp_db)
                    conn = sqlite3.connect(tmp_db)
                    c = conn.cursor()
                    c.execute('SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 50')
                    rows = c.fetchall()
                    conn.close()

                    for (url,) in rows:
                        url_lower = url.lower()
                        if 'vuejs.org/guide' in url_lower:
                            vuejs_tab_found = True
                            print(f"PASS: Component 4a — vuejs.org/guide in Chrome history: {url}")
                        if 'vitejs.dev/guide' in url_lower or 'vite.dev/guide' in url_lower:
                            vitejs_tab_found = True
                            print(f"PASS: Component 4b — vitejs.dev/guide in Chrome history: {url}")
                except Exception as e:
                    print(f"INFO: Could not read Chrome history DB: {e}")

        if vuejs_tab_found and vitejs_tab_found:
            total_score += 0.25
            print(f"PASS: Component 4 — Both Chrome tabs verified (vuejs.org/guide and vitejs.dev/guide)")
        elif vuejs_tab_found or vitejs_tab_found:
            total_score += 0.1
            print(f"PARTIAL: Component 4 — Only one tab found (vuejs: {vuejs_tab_found}, vitejs: {vitejs_tab_found}) — 0.1 pts")
        else:
            print(f"FAIL: Component 4 — Neither Chrome tab found for vuejs.org/guide or vitejs.dev/guide")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
