"""
Reward Script: Automate morning data pipeline workspace setup
Task ID: osworld_multi_apps_workspace_init_010
Domain: multi_apps / os
Scoring:
  Component 1: Nautilus (file manager) open at ~/Data/etl-pipelines  (0.2 pts)
  Component 2: Chrome tab open at https://airflow.apache.org/docs/    (0.2 pts)
  Component 3: Chrome tab open at https://www.postgresql.org/docs/    (0.2 pts)
  Component 4: VSCode open with ~/Data/etl-pipelines folder           (0.2 pts)
  Component 5: Second terminal with .venv activated                   (0.2 pts)
  Total: 1.0

Verification approach:
  - Use /proc filesystem (no subprocess) to enumerate processes and their cmdlines/environs
  - Use urllib.request to query Chrome CDP on port 1337 for open tabs
  - Use VSCode workspace storage JSON for folder verification
"""

import os
import json
import urllib.request

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_workspace_init_010'
PROJECT_DIR = '/home/user/Data/etl-pipelines'
VENV_PATH = '/home/user/Data/etl-pipelines/.venv'


def get_all_proc_info():
    """
    Enumerate all processes via /proc filesystem.
    Returns list of dicts: {pid, cmdline, cwd, environ}
    Uses only Python builtins — no subprocess.
    """
    processes = []
    try:
        for entry in os.listdir('/proc'):
            if not entry.isdigit():
                continue
            pid = entry
            info = {'pid': pid, 'cmdline': '', 'cwd': None, 'environ': {}}
            try:
                with open(f'/proc/{pid}/cmdline', 'rb') as f:
                    raw = f.read()
                info['cmdline'] = raw.replace(b'\x00', b' ').decode('utf-8', errors='replace').strip()
            except Exception:
                pass
            try:
                info['cwd'] = os.readlink(f'/proc/{pid}/cwd')
            except Exception:
                pass
            try:
                with open(f'/proc/{pid}/environ', 'rb') as f:
                    env_data = f.read()
                for pair in env_data.split(b'\x00'):
                    decoded = pair.decode('utf-8', errors='replace')
                    if '=' in decoded:
                        k, v = decoded.split('=', 1)
                        info['environ'][k] = v
            except Exception:
                pass
            processes.append(info)
    except Exception:
        pass
    return processes


def query_chrome_cdp_tabs(port=1337):
    """Query Chrome DevTools Protocol to get open tab URLs. Returns list of URL strings."""
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json', timeout=5)
        tabs = json.loads(resp.read())
        return [tab.get('url', '') for tab in tabs if tab.get('type') == 'page']
    except Exception:
        return []


def verify_task():
    """
    Verify that all required workspace components have been launched.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0
    processes = get_all_proc_info()

    # ----------------------------------------------------------------
    # Component 1: Nautilus (file manager) open at ~/Data/etl-pipelines (0.2 pts)
    # ----------------------------------------------------------------
    try:
        nautilus_found = False
        for proc in processes:
            cmdline = proc['cmdline']
            # Look for nautilus process whose cmdline includes the project path
            if 'nautilus' in cmdline and 'etl-pipelines' in cmdline and 'grep' not in cmdline:
                nautilus_found = True
                print(f"PASS: Component 1 — Nautilus open at {PROJECT_DIR} (PID {proc['pid']}) (0.2 pts)")
                break

        if not nautilus_found:
            print(f"FAIL: Component 1 — Nautilus with {PROJECT_DIR} not found in running processes")
        else:
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Chrome tab open at https://airflow.apache.org/docs/ (0.2 pts)
    # ----------------------------------------------------------------
    try:
        airflow_tab_found = False

        # First check: Chrome process cmdline may include the URL on startup
        for proc in processes:
            cmdline = proc['cmdline']
            if ('/opt/google/chrome/chrome' in cmdline or 'google-chrome' in cmdline):
                if 'airflow.apache.org' in cmdline and '--type=' not in cmdline:
                    airflow_tab_found = True
                    break

        # Second check: query CDP for live tab list (handles tabs opened after launch)
        if not airflow_tab_found:
            open_tabs = query_chrome_cdp_tabs(port=1337)
            for url in open_tabs:
                if 'airflow.apache.org' in url and '/docs' in url:
                    airflow_tab_found = True
                    break
            # Also try port 9222 (socat bridge)
            if not airflow_tab_found:
                open_tabs_9222 = query_chrome_cdp_tabs(port=9222)
                for url in open_tabs_9222:
                    if 'airflow.apache.org' in url and '/docs' in url:
                        airflow_tab_found = True
                        break

        if airflow_tab_found:
            print(f"PASS: Component 2 — Chrome tab with https://airflow.apache.org/docs/ found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Chrome tab with airflow.apache.org/docs not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Chrome tab open at https://www.postgresql.org/docs/ (0.2 pts)
    # ----------------------------------------------------------------
    try:
        pg_tab_found = False

        # First check: Chrome process cmdline
        for proc in processes:
            cmdline = proc['cmdline']
            if ('/opt/google/chrome/chrome' in cmdline or 'google-chrome' in cmdline):
                if 'postgresql.org' in cmdline and '--type=' not in cmdline:
                    pg_tab_found = True
                    break

        # Second check: query CDP for live tab list
        if not pg_tab_found:
            open_tabs = query_chrome_cdp_tabs(port=1337)
            for url in open_tabs:
                if 'postgresql.org' in url and '/docs' in url:
                    pg_tab_found = True
                    break
            if not pg_tab_found:
                open_tabs_9222 = query_chrome_cdp_tabs(port=9222)
                for url in open_tabs_9222:
                    if 'postgresql.org' in url and '/docs' in url:
                        pg_tab_found = True
                        break

        if pg_tab_found:
            print(f"PASS: Component 3 — Chrome tab with https://www.postgresql.org/docs/ found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Chrome tab with postgresql.org/docs not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: VSCode open with ~/Data/etl-pipelines folder (0.2 pts)
    # ----------------------------------------------------------------
    try:
        vscode_found = False

        # Check for VSCode main process (code binary) with etl-pipelines in cmdline
        for proc in processes:
            cmdline = proc['cmdline']
            if '/usr/share/code/code' in cmdline and 'etl-pipelines' in cmdline:
                if '--type=' not in cmdline and 'zygote' not in cmdline and 'crashpad' not in cmdline:
                    vscode_found = True
                    print(f"PASS: Component 4 — VSCode open with {PROJECT_DIR} (PID {proc['pid']}) (0.2 pts)")
                    break

        if not vscode_found:
            # Fallback: check VSCode workspace storage for a matching folder entry,
            # combined with any VSCode process running
            vscode_running = any(
                '/usr/share/code/code' in proc['cmdline'] and '--type=' not in proc['cmdline']
                and 'zygote' not in proc['cmdline'] and 'crashpad' not in proc['cmdline']
                for proc in processes
            )
            ws_storage_base = '/home/user/.config/Code/User/workspaceStorage'
            if vscode_running and os.path.isdir(ws_storage_base):
                for ws_id in os.listdir(ws_storage_base):
                    ws_json = os.path.join(ws_storage_base, ws_id, 'workspace.json')
                    if os.path.exists(ws_json):
                        try:
                            with open(ws_json) as f:
                                ws_data = json.load(f)
                            folder = ws_data.get('folder', '')
                            if 'etl-pipelines' in folder:
                                vscode_found = True
                                print(f"PASS: Component 4 — VSCode running with workspace folder={folder} (0.2 pts)")
                                break
                        except Exception:
                            pass

        if not vscode_found:
            print(f"FAIL: Component 4 — VSCode with {PROJECT_DIR} not found")
        else:
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: Terminal with .venv activated (0.2 pts)
    # ----------------------------------------------------------------
    try:
        venv_terminal_found = False

        # Find bash processes whose environment has VIRTUAL_ENV pointing to .venv
        for proc in processes:
            cmdline = proc['cmdline'].strip()
            # A terminal bash process has cmdline == 'bash' or '-bash'
            if cmdline in ('bash', '-bash') or cmdline.endswith(' bash'):
                env = proc['environ']
                virtual_env = env.get('VIRTUAL_ENV', '')
                if 'etl-pipelines/.venv' in virtual_env or virtual_env == VENV_PATH:
                    venv_terminal_found = True
                    print(
                        f"PASS: Component 5 — Terminal (PID {proc['pid']}) with "
                        f"VIRTUAL_ENV={virtual_env}, CWD={proc['cwd']} (0.2 pts)"
                    )
                    break

        if not venv_terminal_found:
            print(f"FAIL: Component 5 — No terminal with VIRTUAL_ENV={VENV_PATH} found")
        else:
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ----------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint — runs directly on the VM
verify_task()
