"""
Reward Script: Compare version1.py and version2.py using VSCode diff editor
Task ID: vscode_stu_084
Domain: vscode
Scoring:
  Component 1 (0.5): Diff editor is open in VSCode workspace state
  Component 2 (0.3): version1.py is referenced in the diff editor
  Component 3 (0.2): version2.py is referenced in the diff editor
"""

import os
import json
import sqlite3
import glob


TASK_ID = 'vscode_stu_084'
HOME = '/home/user'
EXPECTED_FILE1 = 'version1.py'
EXPECTED_FILE2 = 'version2.py'
EXPECTED_DIR = '/home/user/cs101/hw6'


def get_workspace_editor_state():
    """
    Read the VSCode workspace state database to find open editors.
    Returns the parsed editor state or None.
    """
    ws_dbs = glob.glob(os.path.join(HOME, '.config/Code/User/workspaceStorage/*/state.vscdb'))
    for ws_db in ws_dbs:
        try:
            db = sqlite3.connect(ws_db)
            cursor = db.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key='memento/workbench.parts.editor'")
            row = cursor.fetchone()
            db.close()
            if row:
                return json.loads(row[0])
        except Exception as e:
            print(f"WARN: Could not read {ws_db}: {e}")
    return None


def find_editors_in_grid(node):
    """Recursively find all editors in the serialized grid structure."""
    editors = []
    if not isinstance(node, dict):
        return editors
    if node.get('type') == 'leaf':
        data = node.get('data', {})
        for ed in data.get('editors', []):
            editors.append(ed)
    elif node.get('type') == 'branch':
        for child in node.get('data', []):
            editors.extend(find_editors_in_grid(child))
    return editors


def get_process_cmdlines():
    """
    Fallback: Check VSCode process command lines for --diff flag.
    Returns list of command line strings for code processes.
    """
    cmdlines = []
    try:
        for pid_dir in glob.glob('/proc/[0-9]*/cmdline'):
            try:
                with open(pid_dir, 'r') as f:
                    cmdline = f.read().replace('\x00', ' ').strip()
                    if '/usr/share/code/code' in cmdline or 'code' in cmdline:
                        cmdlines.append(cmdline)
            except (PermissionError, FileNotFoundError):
                continue
    except Exception:
        pass
    return cmdlines


def verify_task():
    """
    Verify that the VSCode diff editor is open comparing version1.py and version2.py.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Primary method: Check workspace state database
    editor_state = get_workspace_editor_state()
    diff_editor_found = False
    file1_in_diff = False
    file2_in_diff = False

    if editor_state:
        grid = editor_state.get('editorpart.state', {}).get('serializedGrid', {}).get('root', {})
        editors = find_editors_in_grid(grid)
        print(f"INFO: Found {len(editors)} editor(s) in workspace state")

        for ed in editors:
            editor_id = ed.get('id', '')
            if editor_id == 'workbench.editors.diffEditorInput':
                diff_editor_found = True
                print(f"INFO: Diff editor found in workspace state DB")

                # Parse the editor value to check which files are being compared
                try:
                    val = json.loads(ed.get('value', '{}'))
                    primary = val.get('primarySerialized', '{}')
                    secondary = val.get('secondarySerialized', '{}')

                    # Parse nested JSON strings
                    if isinstance(primary, str):
                        primary = json.loads(primary)
                    if isinstance(secondary, str):
                        secondary = json.loads(secondary)

                    primary_path = primary.get('resourceJSON', {}).get('fsPath', '')
                    secondary_path = secondary.get('resourceJSON', {}).get('fsPath', '')

                    print(f"INFO: Diff primary file: {primary_path}")
                    print(f"INFO: Diff secondary file: {secondary_path}")

                    # Check if version1.py and version2.py are referenced
                    # They can be in either primary or secondary position
                    all_paths = [primary_path, secondary_path]
                    for p in all_paths:
                        if EXPECTED_FILE1 in os.path.basename(p):
                            file1_in_diff = True
                        if EXPECTED_FILE2 in os.path.basename(p):
                            file2_in_diff = True
                except Exception as e:
                    print(f"WARN: Could not parse diff editor value: {e}")
    else:
        print("WARN: No workspace state database found, trying process fallback")

    # Fallback: Check process command lines if DB check didn't find diff
    if not diff_editor_found:
        cmdlines = get_process_cmdlines()
        for cmdline in cmdlines:
            if '--diff' in cmdline:
                diff_editor_found = True
                print(f"INFO: Found --diff in process command line")
                if EXPECTED_FILE1 in cmdline:
                    file1_in_diff = True
                if EXPECTED_FILE2 in cmdline:
                    file2_in_diff = True
                break

    # Component 1: Diff editor is open (0.5 points)
    # This is the core task requirement: the diff editor must be active
    try:
        if diff_editor_found:
            print(f"PASS: Component 1 -- Diff editor is open in VSCode (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- No diff editor found in VSCode workspace state or processes")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: version1.py is part of the diff comparison (0.3 points)
    try:
        if diff_editor_found and file1_in_diff:
            print(f"PASS: Component 2 -- version1.py is referenced in the diff editor (0.3 pts)")
            total_score += 0.3
        else:
            if not diff_editor_found:
                print(f"FAIL: Component 2 -- No diff editor to check for version1.py")
            else:
                print(f"FAIL: Component 2 -- version1.py not found in diff editor file references")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: version2.py is part of the diff comparison (0.2 points)
    try:
        if diff_editor_found and file2_in_diff:
            print(f"PASS: Component 3 -- version2.py is referenced in the diff editor (0.2 pts)")
            total_score += 0.2
        else:
            if not diff_editor_found:
                print(f"FAIL: Component 3 -- No diff editor to check for version2.py")
            else:
                print(f"FAIL: Component 3 -- version2.py not found in diff editor file references")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
