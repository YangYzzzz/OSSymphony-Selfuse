"""
Initial Setup: Install Code Spell Checker and add 'microservice' to user dictionary
Task ID: vscode_ext_026
Domain: vs_code

This script sets up the INITIAL state:
- VSCode is open
- A workspace with a Python file that contains the word 'microservice'
- Code Spell Checker is NOT installed
- 'microservice' is NOT in cSpell.userWords
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_026'
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
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


def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        import re
        content_no_comments = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_no_comments)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def uninstall_spell_checker():
    """Ensure Code Spell Checker is NOT installed."""
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True
    )
    if 'streetsidesoftware.code-spell-checker' in result.stdout.lower():
        subprocess.run(
            ['code', '--uninstall-extension', 'streetsidesoftware.code-spell-checker'],
            capture_output=True, text=True
        )
        time.sleep(2)
        print('Uninstalled Code Spell Checker extension.')
    else:
        print('Code Spell Checker is not installed (expected initial state).')


def remove_cspell_user_words():
    """Ensure cSpell.userWords is absent or does not contain 'microservice'."""
    settings = load_settings()
    changed = False

    # Remove cSpell.userWords if it exists
    if 'cSpell.userWords' in settings:
        del settings['cSpell.userWords']
        changed = True
        print("Removed 'cSpell.userWords' from settings.")

    # Also remove if nested under cspell
    if 'cspell.userWords' in settings:
        del settings['cspell.userWords']
        changed = True

    if changed:
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(settings, f, indent=4)


def create_workspace():
    """Create a workspace folder with a Python file mentioning 'microservice'."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # A realistic Python file that uses the word 'microservice' multiple times
    main_py = os.path.join(WORKSPACE_DIR, 'service_registry.py')
    with open(main_py, 'w') as f:
        f.write('''\
"""
Service Registry Module

This module handles registration and discovery of microservice instances
within the distributed architecture.
"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """Registry for managing microservice endpoints."""

    def __init__(self):
        self._services: Dict[str, List[str]] = {}

    def register(self, service_name: str, endpoint: str) -> None:
        """Register a microservice endpoint."""
        if service_name not in self._services:
            self._services[service_name] = []
        self._services[service_name].append(endpoint)
        logger.info(f"Registered microservice '{service_name}' at {endpoint}")

    def discover(self, service_name: str) -> Optional[List[str]]:
        """Discover all endpoints for a given microservice."""
        return self._services.get(service_name)

    def deregister(self, service_name: str, endpoint: str) -> bool:
        """Remove a microservice endpoint from the registry."""
        if service_name in self._services:
            try:
                self._services[service_name].remove(endpoint)
                logger.info(f"Deregistered microservice '{service_name}' at {endpoint}")
                return True
            except ValueError:
                pass
        return False

    def list_services(self) -> List[str]:
        """Return all registered microservice names."""
        return list(self._services.keys())


# Example usage
if __name__ == '__main__':
    registry = ServiceRegistry()
    registry.register('auth-service', 'http://10.0.0.1:8080')
    registry.register('payment-microservice', 'http://10.0.0.2:9000')
    registry.register('auth-service', 'http://10.0.0.3:8080')

    print("Registered services:", registry.list_services())
    print("Auth endpoints:", registry.discover('auth-service'))
''')

    # A README for the workspace
    readme = os.path.join(WORKSPACE_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('''\
# Workspace: Distributed Services

This workspace contains code for managing microservice infrastructure.

## Structure

- `service_registry.py` — Core microservice registry implementation
- `config.json` — Service configuration

## Usage

Each microservice registers itself on startup and deregisters on shutdown.
The registry provides service discovery for all connected components.
''')

    # A config JSON file
    config_json = os.path.join(WORKSPACE_DIR, 'config.json')
    with open(config_json, 'w') as f:
        json.dump({
            'service_name': 'api-gateway',
            'version': '1.2.0',
            'environment': 'development',
            'dependencies': ['auth-service', 'payment-microservice', 'notification-service'],
            'registry_url': 'http://localhost:8500',
            'health_check_interval_seconds': 30
        }, f, indent=4)

    print(f'Workspace created at: {WORKSPACE_DIR}')


def create_initial():
    print('=== Setting up initial state for vscode_ext_026 ===')

    # 1. Create workspace
    create_workspace()

    # 2. Remove Code Spell Checker if present
    uninstall_spell_checker()

    # 3. Remove cSpell.userWords from settings
    remove_cspell_user_words()

    # 4. Open VSCode with the workspace directory
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with workspace at DISPLAY=:0')

    print('=== Initial setup complete ===')
    print(f'Workspace: {WORKSPACE_DIR}')
    print('Extension streetsidesoftware.code-spell-checker: NOT installed')
    print("cSpell.userWords: NOT set in settings.json")


create_initial()
