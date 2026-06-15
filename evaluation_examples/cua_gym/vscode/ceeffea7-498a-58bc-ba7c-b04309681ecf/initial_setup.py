"""
Initial Setup: VSCode - Install TODO Highlight extension and configure keywords
Task ID: vscode_ext_033
Domain: vs_code

Creates a workspace with code files containing TODO/FIXME comments.
The TODO Highlight extension is NOT installed.
settings.json does NOT contain todohighlight configuration.
"""

import os
import json
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(HOME, 'workspace')
TASK_ID = 'vscode_ext_033'


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


def uninstall_extension_if_present(extension_id: str):
    """Uninstall extension if currently installed, so initial state is clean."""
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if extension_id.lower() in result.stdout.lower():
            subprocess.run(
                ['code', '--uninstall-extension', extension_id],
                capture_output=True, text=True, timeout=60
            )
            print(f'Uninstalled extension: {extension_id}')
        else:
            print(f'Extension not installed (good): {extension_id}')
    except Exception as e:
        print(f'Warning: could not check/uninstall extension: {e}')


def create_initial():
    # --- Ensure workspace directory exists ---
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # --- Create realistic Python project files with TODO/FIXME comments ---
    main_py = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(main_py, 'w') as f:
        f.write('''\
#!/usr/bin/env python3
"""
Project: Task Manager CLI
Author: Alex Rivera
Date: 2025-03-10
"""

import os
import sys
from datetime import datetime


# TODO: Add database persistence layer
class TaskManager:
    """Manages a list of tasks."""

    def __init__(self):
        self.tasks = []
        self._next_id = 1

    def add_task(self, title: str, priority: str = "medium") -> dict:
        """Add a new task to the manager."""
        # TODO: Validate priority value against allowed list
        task = {
            "id": self._next_id,
            "title": title,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "completed": False,
        }
        self.tasks.append(task)
        self._next_id += 1
        return task

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return True
        # FIXME: Should raise TaskNotFoundError instead of returning False
        return False

    def get_pending_tasks(self) -> list:
        """Return all uncompleted tasks."""
        # TODO: Add sorting by priority
        return [t for t in self.tasks if not t["completed"]]

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        # FIXME: This does not handle concurrent access safely
        original_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        return len(self.tasks) < original_len


def display_tasks(tasks: list):
    """Pretty-print a list of tasks."""
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'ID':<5} {'Title':<30} {'Priority':<10} {'Status'}")
    print("-" * 60)
    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        print(f"{task['id']:<5} {task['title']:<30} {task['priority']:<10} {status}")


def main():
    manager = TaskManager()

    # Sample data
    manager.add_task("Review quarterly report", "high")
    manager.add_task("Update project documentation", "medium")
    manager.add_task("Fix login page CSS bug", "high")
    manager.add_task("Write unit tests for API", "medium")
    manager.add_task("Schedule team sync meeting", "low")

    manager.complete_task(1)

    print("=== Task Manager ===")
    print("\\nAll pending tasks:")
    display_tasks(manager.get_pending_tasks())

    # TODO: Implement export to CSV functionality
    # TODO: Add email notification for overdue tasks


if __name__ == "__main__":
    main()
''')

    utils_py = os.path.join(WORKSPACE_DIR, 'utils.py')
    with open(utils_py, 'w') as f:
        f.write('''\
"""
Utility functions for Task Manager
"""

import re
import hashlib
from typing import Optional


def sanitize_title(title: str) -> str:
    """Remove special characters from task title."""
    # FIXME: This strips too aggressively - should allow dashes and underscores
    return re.sub(r"[^a-zA-Z0-9 ]", "", title).strip()


def generate_task_hash(task_id: int, title: str) -> str:
    """Generate a short hash for a task."""
    raw = f"{task_id}:{title}"
    return hashlib.md5(raw.encode()).hexdigest()[:8]


def format_priority(priority: str) -> str:
    """Return a colored label for a priority level."""
    # TODO: Use colorama library for terminal coloring
    labels = {
        "high": "[HIGH]",
        "medium": "[MED] ",
        "low": "[LOW] ",
    }
    return labels.get(priority.lower(), "[???] ")


def parse_date_string(date_str: str) -> Optional[str]:
    """Parse various date formats into ISO 8601."""
    # TODO: Handle timezone-aware dates
    # FIXME: Does not validate leap years correctly
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]
    from datetime import datetime
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).isoformat()
        except ValueError:
            continue
    return None
''')

    config_json = os.path.join(WORKSPACE_DIR, 'config.json')
    with open(config_json, 'w') as f:
        json.dump({
            "app_name": "Task Manager CLI",
            "version": "1.2.0",
            "debug": False,
            "max_tasks": 500,
            "default_priority": "medium",
            "db": {
                "host": "localhost",
                "port": 5432,
                "name": "taskmanager"
            }
        }, f, indent=4)

    # --- Set up VSCode settings WITHOUT todohighlight config ---
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings and remove any todohighlight entries
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        import re
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        settings = json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any todohighlight settings that might exist
    keys_to_remove = [k for k in settings if 'todohighlight' in k.lower()]
    for k in keys_to_remove:
        del settings[k]
        print(f'Removed pre-existing setting: {k}')

    # Ensure baseline settings are present
    settings.setdefault('editor.fontSize', 14)
    settings.setdefault('editor.wordWrap', 'off')
    settings.setdefault('files.autoSave', 'onFocusChange')

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'settings.json updated (no todohighlight config): {SETTINGS_PATH}')

    # --- Ensure TODO Highlight extension is NOT installed ---
    uninstall_extension_if_present('wayou.vscode-todo-highlight')

    print(f'Workspace created at: {WORKSPACE_DIR}')
    print(f'Files: main.py, utils.py, config.json')

    # --- GUI-ready startup: open VSCode with workspace ---
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with workspace (DISPLAY=:0)')


create_initial()
