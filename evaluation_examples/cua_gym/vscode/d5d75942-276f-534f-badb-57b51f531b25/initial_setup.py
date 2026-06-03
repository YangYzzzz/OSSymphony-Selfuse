"""
Initial Setup: View all disabled extensions by filtering the Extensions panel
Task ID: vscode_ext_017
Domain: vs_code

Sets up a VSCode environment with multiple extensions installed,
some of which are disabled, and opens VSCode so the agent can
filter extensions using '@disabled' in the Extensions panel search.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_017'
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
VSCODE_EXTENSIONS_DIR = os.path.join(HOME, '.vscode', 'extensions')
EXTENSIONS_JSON = os.path.join(VSCODE_EXTENSIONS_DIR, 'extensions.json')
WORKSPACE_DIR = os.path.join(HOME, 'workspace')


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


def install_extension_cli(extension_id: str):
    """Install a VSCode extension via CLI."""
    try:
        env = os.environ.copy()
        env['DISPLAY'] = ':0'
        result = subprocess.run(
            ['code', '--install-extension', extension_id, '--force'],
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
        print(f'  Installed {extension_id}: {result.returncode}')
    except Exception as e:
        print(f'  Warning: could not install {extension_id}: {e}')


def disable_extension_in_json(extension_id_prefix: str):
    """
    Mark an installed extension as disabled by editing extensions.json.
    The extensions.json file is a list of objects, each with an 'identifier'
    containing a 'uuid' and an 'id', plus optional 'disabled' flag.
    """
    try:
        if not os.path.exists(EXTENSIONS_JSON):
            print(f'  extensions.json not found at {EXTENSIONS_JSON}, skip disable.')
            return
        with open(EXTENSIONS_JSON, 'r') as f:
            content = f.read().strip()
        if not content:
            return
        exts = json.loads(content)
        changed = False
        for ext in exts:
            ext_id = ext.get('identifier', {}).get('id', '').lower()
            if ext_id.startswith(extension_id_prefix.lower()) or extension_id_prefix.lower() in ext_id:
                ext['disabled'] = True
                changed = True
                print(f'  Disabled extension entry: {ext_id}')
        if changed:
            with open(EXTENSIONS_JSON, 'w') as f:
                json.dump(exts, f, indent=2)
    except Exception as e:
        print(f'  Warning: could not disable extension {extension_id_prefix}: {e}')


def create_workspace():
    """Create a simple workspace with a Python project."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a basic Python project
    main_py = os.path.join(WORKSPACE_DIR, 'main.py')
    if not os.path.exists(main_py):
        with open(main_py, 'w') as f:
            f.write(
                '# Sample Python project\n'
                'def greet(name: str) -> str:\n'
                '    """Return a greeting message."""\n'
                '    return f"Hello, {name}!"\n\n'
                'def calculate_total(prices: list) -> float:\n'
                '    """Calculate the total of a list of prices."""\n'
                '    return sum(prices)\n\n'
                'if __name__ == "__main__":\n'
                '    print(greet("World"))\n'
                '    print(calculate_total([10.99, 24.50, 5.75]))\n'
            )

    readme = os.path.join(WORKSPACE_DIR, 'README.md')
    if not os.path.exists(readme):
        with open(readme, 'w') as f:
            f.write(
                '# Sample Workspace\n\n'
                'This workspace contains a sample Python project.\n\n'
                '## Extensions\n'
                'This workspace has several VSCode extensions configured.\n'
                'Some extensions are currently disabled.\n'
            )

    requirements = os.path.join(WORKSPACE_DIR, 'requirements.txt')
    if not os.path.exists(requirements):
        with open(requirements, 'w') as f:
            f.write('requests>=2.28.0\nnumpy>=1.24.0\npandas>=1.5.0\n')

    print(f'Workspace created: {WORKSPACE_DIR}')


def setup_extensions():
    """
    Install multiple extensions, then disable some of them.
    Extensions to install:
      - ms-python.python (keep enabled)
      - esbenp.prettier-vscode (keep enabled)
      - ms-vscode.cpptools (disable)
      - ritwickdey.liveserver (disable)
      - dbaeumer.vscode-eslint (keep enabled)
      - eamodio.gitlens (disable)
    """
    print('Installing extensions...')

    extensions_to_install = [
        'ms-python.python',
        'esbenp.prettier-vscode',
        'ms-vscode.cpptools',
        'ritwickdey.liveserver',
        'dbaeumer.vscode-eslint',
        'eamodio.gitlens',
    ]

    for ext_id in extensions_to_install:
        install_extension_cli(ext_id)
        time.sleep(1)

    # Give VSCode a moment to update extensions.json
    print('Waiting for extension metadata to be written...')
    time.sleep(3)

    # Disable specific extensions
    extensions_to_disable = [
        'ms-vscode.cpptools',
        'ritwickdey.liveserver',
        'eamodio.gitlens',
    ]
    print('Disabling selected extensions...')
    for ext_id in extensions_to_disable:
        disable_extension_in_json(ext_id)

    # Verify extensions.json state
    if os.path.exists(EXTENSIONS_JSON):
        with open(EXTENSIONS_JSON, 'r') as f:
            exts = json.load(f)
        disabled_count = sum(1 for e in exts if e.get('disabled', False))
        print(f'Extensions.json: {len(exts)} total, {disabled_count} disabled')
    else:
        print('Note: extensions.json not found after install')


def load_settings():
    try:
        with open(os.path.join(VSCODE_USER, 'settings.json'), 'r') as f:
            content = f.read()
        import re
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(os.path.join(VSCODE_USER, 'settings.json'), 'w') as f:
        json.dump(settings, f, indent=4)


def configure_vscode_settings():
    """Configure VSCode settings for the task environment."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    update_settings({
        'editor.fontSize': 14,
        'editor.tabSize': 4,
        'editor.wordWrap': 'on',
        'workbench.colorTheme': 'Default Dark+',
        'extensions.autoUpdate': False,
    })
    print('VSCode settings configured.')


def create_initial():
    print(f'Setting up initial environment for task: {TASK_ID}')

    # 1. Create workspace
    create_workspace()

    # 2. Configure VSCode settings
    configure_vscode_settings()

    # 3. Install and configure extensions
    setup_extensions()

    # 4. Launch VSCode with workspace and Extensions panel open
    # Open VSCode - the agent will need to navigate to Extensions panel and type @disabled
    print('Launching VSCode...')
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)

    print(f'GUI_READY: VSCode launched with workspace at {WORKSPACE_DIR}')
    print(f'Initial setup complete for task: {TASK_ID}')


create_initial()
