"""
Initial Setup: VSCode with 8 extensions installed and enabled
Task ID: vscode_ext_018
Domain: vs_code
"""

import json
import os
import re
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(HOME, 'workspace')

# The 8 extensions to install (all enabled — no disabled list)
EXTENSIONS = [
    'ms-python.python',          # Python support (brings debugpy + pylance as deps)
    'esbenp.prettier-vscode',    # Code formatter
    'eamodio.gitlens',           # Git supercharged
    'pkief.material-icon-theme', # File icon theme
    'formulahendry.code-runner', # Run code snippets
    'streetsidesoftware.code-spell-checker',  # Spell checker (8th extension)
]


def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings: dict):
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def install_extension(ext_id: str):
    """Install a VSCode extension via CLI."""
    result = subprocess.run(
        ['code', '--install-extension', ext_id, '--force'],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f'  Installed: {ext_id}')
    else:
        print(f'  WARN: {ext_id}: {result.stderr.strip()[:200]}')
    return result.returncode == 0


def create_workspace():
    """Create a sample workspace directory with files for VSCode to open."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # main.py
    main_py = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(main_py, 'w') as f:
        f.write("""# Sample Python project
import os

def greet(name: str) -> str:
    \"\"\"Return a greeting message.\"\"\"
    return f"Hello, {name}!"

def calculate_total(items: list) -> float:
    \"\"\"Sum a list of numeric items.\"\"\"
    return sum(items)

if __name__ == '__main__':
    print(greet('World'))
    total = calculate_total([10.5, 20.0, 15.75, 8.25])
    print(f"Total: {total}")
""")

    # utils.js
    utils_js = os.path.join(WORKSPACE_DIR, 'utils.js')
    with open(utils_js, 'w') as f:
        f.write("""// Utility functions
function formatCurrency(amount) {
    return `$${amount.toFixed(2)}`;
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

module.exports = { formatCurrency, capitalize };
""")

    # README.md
    readme = os.path.join(WORKSPACE_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write("""# Sample Workspace

This workspace contains sample code files for development.

## Files

- `main.py` — Python utility functions
- `utils.js` — JavaScript helper functions

## Usage

Open this workspace in VSCode to get started.
""")

    print(f'Workspace created: {WORKSPACE_DIR}')


def setup_initial():
    print('=== vscode_ext_018 initial_setup.py ===')

    # Step 1: Create workspace
    create_workspace()

    # Step 2: Install 8 extensions (ms-python.python brings debugpy + pylance as deps = 3 total)
    print('\nInstalling extensions...')
    for ext_id in EXTENSIONS:
        install_extension(ext_id)
        time.sleep(1)

    # Step 3: Verify installed extensions
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True,
        text=True,
    )
    installed = [e.strip() for e in result.stdout.strip().splitlines() if e.strip()]
    print(f'\nInstalled extensions ({len(installed)}): {installed}')

    # Step 4: Ensure settings.json has NO disabled extensions (all enabled state)
    settings = load_settings()
    # Remove any disabled list if present (should not be there, but be safe)
    if 'extensions.disabled' in settings:
        del settings['extensions.disabled']
    # Keep existing security settings intact
    save_settings(settings)
    print('Settings updated: no disabled extensions (all enabled)')

    # Step 5: Launch VSCode with workspace (GUI-ready)
    print('\nLaunching VSCode...')
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with workspace on DISPLAY=:0')

    print('\n=== initial_setup.py COMPLETE ===')


setup_initial()
