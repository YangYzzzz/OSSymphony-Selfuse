"""
Reward Script: Multi-root VSCode workspace with per-folder tab sizes
Task ID: vscode_wf_014
Domain: vs-code (libreoffice_calc listed in config but task is VS Code)
Scoring:
  Component 1 (0.30) - .code-workspace file exists and is valid JSON with both folders
  Component 2 (0.20) - Workspace folders point to ~/frontend and ~/backend
  Component 3 (0.25) - frontend/.vscode/settings.json has editor.tabSize = 2
  Component 4 (0.25) - backend/.vscode/settings.json has editor.tabSize = 4
"""

import os
import json
import glob as glob_mod
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_014'


def find_workspace_file():
    """Find any .code-workspace file under /home/user (not in hidden dirs)."""
    # Check canonical path first
    canonical = os.path.join(WORKDIR, f'{TASK_ID}.code-workspace')
    if os.path.exists(canonical):
        return canonical
    # Search for any .code-workspace file
    for f in glob_mod.glob(os.path.join(WORKDIR, '*.code-workspace')):
        return f
    for f in glob_mod.glob(os.path.join(WORKDIR, '**', '*.code-workspace'), recursive=True):
        # Skip hidden directories
        if '/.' not in f.split(WORKDIR)[1]:
            return f
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .code-workspace file exists and is valid JSON (0.30 points)
    ws_path = None
    ws_data = None
    try:
        ws_path = find_workspace_file()
        if ws_path is not None:
            with open(ws_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments if present
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            ws_data = json.loads(content_clean)
            if 'folders' in ws_data and isinstance(ws_data['folders'], list) and len(ws_data['folders']) >= 2:
                print(f"PASS: Component 1 - Workspace file found at {ws_path} with {len(ws_data['folders'])} folders (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 - Workspace file found but 'folders' missing or < 2 entries")
        else:
            print("FAIL: Component 1 - No .code-workspace file found")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 - Workspace file exists but is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Workspace folders include ~/frontend and ~/backend (0.20 points)
    try:
        if ws_data is not None and 'folders' in ws_data:
            folder_paths = set()
            for folder in ws_data['folders']:
                p = folder.get('path', '')
                # Normalize: expand ~ and resolve
                p_expanded = os.path.expanduser(p)
                # Also handle relative paths from workspace file location
                if not os.path.isabs(p_expanded) and ws_path:
                    p_expanded = os.path.normpath(os.path.join(os.path.dirname(ws_path), p_expanded))
                folder_paths.add(os.path.normpath(p_expanded))

            frontend_path = os.path.normpath(os.path.join(WORKDIR, 'frontend'))
            backend_path = os.path.normpath(os.path.join(WORKDIR, 'backend'))

            has_frontend = frontend_path in folder_paths
            has_backend = backend_path in folder_paths

            if has_frontend and has_backend:
                print(f"PASS: Component 2 - Both frontend and backend folders present (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 - frontend={has_frontend}, backend={has_backend}. Found paths: {folder_paths}")
        else:
            print("FAIL: Component 2 - No workspace data available")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: frontend/.vscode/settings.json has editor.tabSize = 2 (0.25 points)
    try:
        frontend_settings_path = os.path.join(WORKDIR, 'frontend', '.vscode', 'settings.json')
        if os.path.exists(frontend_settings_path):
            with open(frontend_settings_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_clean)
            tab_size = settings.get('editor.tabSize')
            if tab_size == 2:
                print(f"PASS: Component 3 - frontend editor.tabSize = 2 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - frontend editor.tabSize = {tab_size}, expected 2")
        else:
            # Also check if tabSize is set in workspace-level settings for frontend
            if ws_data and 'settings' in ws_data:
                tab_size = ws_data['settings'].get('editor.tabSize')
                # Only if workspace-level is 2 AND there are folder-specific settings
                print(f"FAIL: Component 3 - No frontend/.vscode/settings.json found")
            else:
                print(f"FAIL: Component 3 - No frontend/.vscode/settings.json found")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 3 - frontend settings.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: backend/.vscode/settings.json has editor.tabSize = 4 (0.25 points)
    try:
        backend_settings_path = os.path.join(WORKDIR, 'backend', '.vscode', 'settings.json')
        if os.path.exists(backend_settings_path):
            with open(backend_settings_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_clean)
            tab_size = settings.get('editor.tabSize')
            if tab_size == 4:
                print(f"PASS: Component 4 - backend editor.tabSize = 4 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 - backend editor.tabSize = {tab_size}, expected 4")
        else:
            print(f"FAIL: Component 4 - No backend/.vscode/settings.json found")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 4 - backend settings.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
