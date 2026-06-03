"""
Reward Script: Multi-root workspace with independent linter settings
Task ID: vscode_web_041
Domain: vscode
Scoring:
  Component 1 (0.15): Workspace file exists and is valid JSON
  Component 2 (0.30): Workspace defines both client/ and server/ folders
  Component 3 (0.25): Client folder has React-specific ESLint settings
  Component 4 (0.25): Server folder has Node.js-specific ESLint settings
  Component 5 (0.05): Workspace-level settings present
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'fullstack-app')
TASK_ID = 'vscode_web_041'


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) but not inside strings
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def find_workspace_file():
    """Find a .code-workspace file in the project root."""
    for name in os.listdir(PROJECT_DIR):
        if name.endswith('.code-workspace'):
            return os.path.join(PROJECT_DIR, name)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Workspace file exists and is valid JSON (0.15 points)
    workspace_path = None
    workspace_data = None
    try:
        workspace_path = find_workspace_file()
        if workspace_path is not None:
            workspace_data = load_jsonc(workspace_path)
            if isinstance(workspace_data, dict):
                print(f"PASS: Component 1 — Workspace file exists and is valid JSON: {os.path.basename(workspace_path)} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Workspace file is not a JSON object")
        else:
            print(f"FAIL: Component 1 — No .code-workspace file found in {PROJECT_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if workspace_data is None:
        # Can't proceed without a valid workspace file
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Workspace defines both client/ and server/ folders (0.30 points)
    try:
        folders = workspace_data.get('folders', [])
        folder_paths = []
        for f in folders:
            if isinstance(f, dict) and 'path' in f:
                folder_paths.append(f['path'])

        # Normalize paths: strip trailing slashes, get basename-like comparison
        normalized = [p.rstrip('/').split('/')[-1] if '/' in p else p.rstrip('/') for p in folder_paths]

        has_client = any(p in ('client', 'client/') or p.endswith('/client') for p in folder_paths)
        has_server = any(p in ('server', 'server/') or p.endswith('/server') for p in folder_paths)

        if has_client and has_server:
            print(f"PASS: Component 2 — Workspace defines both client and server folders: {folder_paths} (0.30 pts)")
            total_score += 0.30
        else:
            missing = []
            if not has_client:
                missing.append('client')
            if not has_server:
                missing.append('server')
            print(f"FAIL: Component 2 — Missing folder(s): {missing}. Found: {folder_paths}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Client folder has React-specific ESLint settings (0.25 points)
    try:
        client_settings_path = os.path.join(PROJECT_DIR, 'client', '.vscode', 'settings.json')
        if os.path.exists(client_settings_path):
            client_settings = load_jsonc(client_settings_path)

            # React-specific: should validate JSX/React file types
            eslint_validate = client_settings.get('eslint.validate', [])
            # Check for React-related entries (javascriptreact, typescriptreact, jsx, tsx)
            react_types = {'javascriptreact', 'typescriptreact', 'jsx', 'tsx'}
            has_react_lint = any(
                (isinstance(v, str) and v in react_types) or
                (isinstance(v, dict) and v.get('language', '') in react_types)
                for v in eslint_validate
            )

            # Also check for other React-specific settings
            has_emmet_jsx = 'emmet.includeLanguages' in client_settings
            has_react_indicator = has_react_lint or has_emmet_jsx

            if has_react_indicator:
                print(f"PASS: Component 3 — Client has React-specific ESLint settings (eslint.validate={eslint_validate}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Client settings lack React-specific linting config. eslint.validate={eslint_validate}")
        else:
            # Check if workspace file itself has folder-specific settings
            # Some workspace configs embed per-folder settings differently
            print(f"FAIL: Component 3 — No client/.vscode/settings.json found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Server folder has Node.js-specific ESLint settings (0.25 points)
    try:
        server_settings_path = os.path.join(PROJECT_DIR, 'server', '.vscode', 'settings.json')
        if os.path.exists(server_settings_path):
            server_settings = load_jsonc(server_settings_path)

            # Node.js-specific: should have eslint config, possibly nodePath, node env
            eslint_validate = server_settings.get('eslint.validate', [])
            has_node_path = 'eslint.nodePath' in server_settings
            has_eslint_options = 'eslint.options' in server_settings
            has_js_validate = any(
                (isinstance(v, str) and v == 'javascript') or
                (isinstance(v, dict) and v.get('language', '') == 'javascript')
                for v in eslint_validate
            )

            # Server should have ESLint configured for Node (not React)
            react_types = {'javascriptreact', 'typescriptreact', 'jsx', 'tsx'}
            has_react = any(
                (isinstance(v, str) and v in react_types) or
                (isinstance(v, dict) and v.get('language', '') in react_types)
                for v in eslint_validate
            )

            # Node-specific: has JS validation AND (no React types OR has nodePath)
            is_node_specific = (has_js_validate or has_eslint_options) and (not has_react or has_node_path)

            if is_node_specific:
                print(f"PASS: Component 4 — Server has Node.js-specific ESLint settings (eslint.validate={eslint_validate}, nodePath={has_node_path}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Server settings lack Node.js-specific linting config. Settings: {server_settings}")
        else:
            print(f"FAIL: Component 4 — No server/.vscode/settings.json found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Workspace-level settings present (0.05 points)
    try:
        ws_settings = workspace_data.get('settings', {})
        if isinstance(ws_settings, dict) and len(ws_settings) > 0:
            print(f"PASS: Component 5 — Workspace has top-level settings ({len(ws_settings)} keys) (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — Workspace file has no top-level settings")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
