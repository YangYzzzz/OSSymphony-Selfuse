"""
Reward Script: Create a split terminal in VSCode
Task ID: vscode_stu_039
Domain: vscode
Scoring:
  Component 1 (0.5): Layout info shows a tab with 2+ terminals (split view)
  Component 2 (0.3): Split terminals have roughly equal relative sizes
  Component 3 (0.2): At least 2 VSCode integrated terminal bash processes running
"""

import os
import json
import sqlite3
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_039'
VSCODE_WORKSPACE_STORAGE = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage')
SHELL_INTEGRATION_MARKER = 'vs/workbench/contrib/terminal/browser/media/shellIntegration'


def find_state_vscdb():
    """Find the most recent state.vscdb in VSCode workspace storage."""
    pattern = os.path.join(VSCODE_WORKSPACE_STORAGE, '*', 'state.vscdb')
    candidates = glob.glob(pattern)
    if not candidates:
        return None
    # If multiple workspaces, pick the most recently modified
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


def get_terminal_layout(db_path):
    """Read terminal.integrated.layoutInfo from the VSCode state database."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT value FROM ItemTable WHERE key='terminal.integrated.layoutInfo'")
        row = cur.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        return None
    except Exception as e:
        print(f"ERROR: Failed to read state DB: {e}")
        return None


def count_vscode_terminal_processes():
    """Count running VSCode integrated terminal bash processes via /proc."""
    count = 0
    try:
        for pid in os.listdir('/proc'):
            if not pid.isdigit():
                continue
            try:
                cmdline_path = os.path.join('/proc', pid, 'cmdline')
                with open(cmdline_path, 'rb') as f:
                    cmdline = f.read().decode('utf-8', errors='replace')
                # VSCode integrated terminals are bash with shellIntegration init file
                if 'bash' in cmdline and SHELL_INTEGRATION_MARKER in cmdline:
                    count += 1
            except (PermissionError, FileNotFoundError, ProcessLookupError):
                continue
    except Exception as e:
        print(f"ERROR: Cannot enumerate processes: {e}")
    return count


def verify_task():
    """
    Verify that VSCode has a split terminal (2 terminal panes side by side).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the VSCode workspace state database
    db_path = find_state_vscdb()
    if not db_path:
        print("CRITICAL: No VSCode workspace state database found")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Using state DB: {db_path}")

    # Read terminal layout info
    layout = get_terminal_layout(db_path)
    if not layout:
        print("CRITICAL: No terminal layout info found in state DB")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Layout info: {json.dumps(layout, indent=2)}")

    tabs = layout.get('tabs', [])

    # Component 1: At least one tab has 2+ terminals (split view) (0.5 points)
    try:
        max_terminals_in_tab = 0
        split_tab = None
        for tab in tabs:
            terminals = tab.get('terminals', [])
            if len(terminals) > max_terminals_in_tab:
                max_terminals_in_tab = len(terminals)
                split_tab = tab

        if max_terminals_in_tab >= 2:
            print(f"PASS: Component 1 — Found tab with {max_terminals_in_tab} terminals (split view) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — No tab with 2+ terminals found. Max terminals in a tab: {max_terminals_in_tab}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        split_tab = None

    # Component 2: Split terminals have roughly equal relative sizes (0.3 points)
    # In a proper split, each pane should have relativeSize ~0.5
    try:
        if split_tab and max_terminals_in_tab >= 2:
            terminals = split_tab.get('terminals', [])
            sizes = [t.get('relativeSize', 0) for t in terminals]
            # Check that all sizes are roughly equal (within tolerance)
            # For a 2-way split, each should be ~0.5; for 3-way, ~0.33, etc.
            expected_size = 1.0 / len(sizes)
            all_roughly_equal = all(abs(s - expected_size) < 0.15 for s in sizes)
            sizes_sum_ok = abs(sum(sizes) - 1.0) < 0.05

            if all_roughly_equal and sizes_sum_ok:
                print(f"PASS: Component 2 — Terminal sizes are roughly equal: {sizes} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Terminal sizes not equal. Sizes: {sizes}, expected ~{expected_size} each")
        else:
            print(f"FAIL: Component 2 — No split tab found, cannot check sizes")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: At least 2 VSCode integrated terminal bash processes running (0.2 points)
    try:
        proc_count = count_vscode_terminal_processes()
        if proc_count >= 2:
            print(f"PASS: Component 3 — {proc_count} VSCode terminal processes running (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Only {proc_count} VSCode terminal process(es) running, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
