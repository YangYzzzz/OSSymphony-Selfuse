"""
Initial Setup: Create keybindings for terminal navigation
Task ID: vscode_rrt_077
Domain: vscode

Sets up VSCode with:
- A workspace directory with sample project files
- An empty keybindings.json (no terminal navigation entries)
- Opens VSCode and launches 3 terminal instances (bash, node, python)
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, "keybindings.json")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_workspace_files():
    """Create a realistic workspace directory with sample project files."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main Python file
    with open(os.path.join(WORKSPACE_DIR, "app.py"), "w") as f:
        f.write('''"""
Multi-service monitoring dashboard application.
"""
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceMonitor:
    """Monitors health and performance of microservices."""

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.services = {}
        self.alerts = []
        self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            self.services = {s["name"]: s for s in config.get("services", [])}
            logger.info(f"Loaded {len(self.services)} services from config")
        except FileNotFoundError:
            logger.warning("Config file not found, using defaults")
            self.services = {}

    def check_health(self, service_name):
        """Check health status of a service."""
        if service_name not in self.services:
            return {"status": "unknown", "message": "Service not registered"}
        svc = self.services[service_name]
        return {
            "name": service_name,
            "status": "healthy",
            "endpoint": svc.get("endpoint", ""),
            "checked_at": datetime.now().isoformat(),
        }

    def get_all_statuses(self):
        """Return health status for all registered services."""
        return [self.check_health(name) for name in self.services]


if __name__ == "__main__":
    monitor = ServiceMonitor()
    statuses = monitor.get_all_statuses()
    for status in statuses:
        print(f"  {status['name']}: {status['status']}")
''')

    # Config file
    with open(os.path.join(WORKSPACE_DIR, "config.json"), "w") as f:
        json.dump({
            "services": [
                {"name": "auth-service", "endpoint": "http://localhost:8001/health", "timeout": 5},
                {"name": "data-pipeline", "endpoint": "http://localhost:8002/health", "timeout": 10},
                {"name": "notification-hub", "endpoint": "http://localhost:8003/health", "timeout": 3},
            ],
            "check_interval": 30,
            "alert_threshold": 3
        }, f, indent=2)

    # Node.js helper script
    with open(os.path.join(WORKSPACE_DIR, "server.js"), "w") as f:
        f.write('''const http = require("http");

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  if (req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", uptime: process.uptime() }));
  } else {
    res.writeHead(404);
    res.end("Not Found");
  }
});

server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
''')

    # Requirements file
    with open(os.path.join(WORKSPACE_DIR, "requirements.txt"), "w") as f:
        f.write("flask==3.0.2\nrequests==2.31.0\npandas==2.2.1\npsutil==5.9.8\n")

    print(f"Workspace created at: {WORKSPACE_DIR}")


def setup_keybindings():
    """Create an empty keybindings.json with no terminal navigation entries."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty keybindings array - no terminal navigation entries
    with open(KEYBINDINGS_PATH, "w") as f:
        json.dump([], f, indent=4)

    print(f"Keybindings file created: {KEYBINDINGS_PATH} (empty array)")


def setup_settings():
    """Ensure basic VSCode settings exist."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings if any
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Merge in basic settings without overwriting existing ones
    defaults = {
        "terminal.integrated.defaultProfile.linux": "bash",
        "editor.fontSize": 14,
        "workbench.colorTheme": "Default Dark Modern",
    }
    for key, val in defaults.items():
        if key not in settings:
            settings[key] = val

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Settings file updated: {SETTINGS_PATH}")


def open_vscode_with_terminals():
    """Open VSCode with workspace and create 3 terminal instances via tasks.json."""
    # Create a .vscode/tasks.json that auto-launches 3 terminals on folder open
    vscode_dir = os.path.join(WORKSPACE_DIR, ".vscode")
    os.makedirs(vscode_dir, exist_ok=True)

    # Use VSCode tasks with runOn: folderOpen to auto-start terminals
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "bash terminal",
                "type": "shell",
                "command": "echo 'bash terminal ready'",
                "isBackground": True,
                "presentation": {
                    "reveal": "always",
                    "panel": "dedicated",
                    "group": "terminals"
                },
                "problemMatcher": [],
                "runOptions": {
                    "runOn": "folderOpen"
                }
            },
            {
                "label": "node terminal",
                "type": "shell",
                "command": "echo 'node terminal ready'",
                "isBackground": True,
                "presentation": {
                    "reveal": "always",
                    "panel": "dedicated",
                    "group": "terminals"
                },
                "problemMatcher": [],
                "runOptions": {
                    "runOn": "folderOpen"
                }
            },
            {
                "label": "python terminal",
                "type": "shell",
                "command": "echo 'python terminal ready'",
                "isBackground": True,
                "presentation": {
                    "reveal": "always",
                    "panel": "dedicated",
                    "group": "terminals"
                },
                "problemMatcher": [],
                "runOptions": {
                    "runOn": "folderOpen"
                }
            }
        ]
    }

    with open(os.path.join(vscode_dir, "tasks.json"), "w") as f:
        json.dump(tasks_config, f, indent=4)

    print("Created .vscode/tasks.json for auto-launching terminals")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)

    print("GUI_READY: VSCode launched with workspace and terminal tasks configured")


def main():
    create_workspace_files()
    setup_keybindings()
    setup_settings()
    open_vscode_with_terminals()
    print("Initial setup complete for vscode_rrt_077")


main()
