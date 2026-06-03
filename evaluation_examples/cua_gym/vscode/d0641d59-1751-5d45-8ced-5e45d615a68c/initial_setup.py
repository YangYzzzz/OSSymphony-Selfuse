"""
Initial Setup: Use Go to Definition to navigate to where the 'calculateTax' function is defined
Task ID: vscode_code_038
Domain: vs_code

Initial state: project files exist but VSCode has NOT been opened with this project.
The workspace storage for file:///home/user/project must NOT exist.
The agent will open VSCode and perform Go to Definition themselves.
"""

import os
import json
import shutil

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_038'
PROJECT_DIR = f'{WORKDIR}/project'


def create_initial():
    # Remove any existing project directory to start fresh
    if os.path.exists(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)

    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create main.js — imports and uses calculateTax but does NOT define it
    main_js_content = """const { calculateTax } = require('./tax');

const price = 100;
const tax = calculateTax(price, 'CA');
console.log('Total:', price + tax);
"""
    main_js_path = os.path.join(PROJECT_DIR, 'main.js')
    with open(main_js_path, 'w') as f:
        f.write(main_js_content)
    print(f'Created: {main_js_path}')

    # Create tax.js — defines the calculateTax function starting at line 1
    tax_js_content = """function calculateTax(amount, state) {
  const rates = { 'CA': 0.0725, 'NY': 0.08, 'TX': 0.0625 };
  return amount * (rates[state] || 0.05);
}

module.exports = { calculateTax };
"""
    tax_js_path = os.path.join(PROJECT_DIR, 'tax.js')
    with open(tax_js_path, 'w') as f:
        f.write(tax_js_content)
    print(f'Created: {tax_js_path}')

    # Create package.json for better JS language server recognition
    package_json_content = {
        "name": "tax-calculator",
        "version": "1.0.0",
        "description": "A simple tax calculation utility",
        "main": "main.js",
        "scripts": {
            "start": "node main.js"
        }
    }
    package_json_path = os.path.join(PROJECT_DIR, 'package.json')
    with open(package_json_path, 'w') as f:
        json.dump(package_json_content, f, indent=2)
    print(f'Created: {package_json_path}')

    # CRITICAL: Remove any existing VSCode workspace storage for this project
    # so the initial state has NO workspace storage (score must be 0.0).
    workspace_storage_dir = os.path.join(
        WORKDIR, '.config', 'Code', 'User', 'workspaceStorage'
    )
    if os.path.exists(workspace_storage_dir):
        for entry in os.listdir(workspace_storage_dir):
            entry_path = os.path.join(workspace_storage_dir, entry)
            workspace_json = os.path.join(entry_path, 'workspace.json')
            if os.path.isfile(workspace_json):
                try:
                    with open(workspace_json, 'r') as f:
                        ws_data = json.load(f)
                    folder = ws_data.get('folder', '')
                    if 'home/user/project' in folder:
                        shutil.rmtree(entry_path)
                        print(f'Removed existing workspace storage: {entry_path}')
                except (json.JSONDecodeError, Exception):
                    pass

    # Also update globalStorage to remove this project from profileAssociations
    global_storage_path = os.path.join(
        WORKDIR, '.config', 'Code', 'User', 'globalStorage', 'storage.json'
    )
    if os.path.exists(global_storage_path):
        try:
            with open(global_storage_path, 'r') as f:
                gs_data = json.load(f)
            workspaces = gs_data.get('profileAssociations', {}).get('workspaces', {})
            keys_to_remove = [k for k in workspaces if 'home/user/project' in k]
            for k in keys_to_remove:
                del workspaces[k]
            if keys_to_remove:
                with open(global_storage_path, 'w') as f:
                    json.dump(gs_data, f, indent=2)
                print(f'Cleaned globalStorage profileAssociations for project')
        except (json.JSONDecodeError, Exception) as e:
            print(f'Note: could not update globalStorage: {e}')

    # DO NOT open VSCode — the initial state must have NO workspace storage
    # for file:///home/user/project. The agent will open VSCode themselves.
    print('Initial state created: project files exist, VSCode workspace storage NOT created')
    print(f'  - {main_js_path}')
    print(f'  - {tax_js_path}')
    print(f'  - {package_json_path}')


create_initial()
