"""
Initial Setup: Configure VSCode editor settings for a pair programming session
Task ID: vscode_we_034
Domain: vscode (editor settings)

Creates an empty VSCode settings.json (default state) and opens VSCode
with a sample workspace folder so the agent can navigate to settings.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
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


def create_initial():
    # Ensure VSCode config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings (default state — no custom settings)
    with open(SETTINGS_PATH, "w") as f:
        json.dump({}, f, indent=4)
    print(f"Settings file created: {SETTINGS_PATH}")

    # Create a sample workspace with some files for context
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a sample Python file so VSCode has something to display
    sample_py = os.path.join(WORKSPACE_DIR, "main.py")
    with open(sample_py, "w") as f:
        f.write('''"""Pair Programming Session - Project Setup"""

import datetime


def calculate_sprint_velocity(completed_points: list[int]) -> float:
    """Calculate average sprint velocity from completed story points."""
    if not completed_points:
        return 0.0
    return sum(completed_points) / len(completed_points)


def format_standup_report(team_members: dict) -> str:
    """Generate a formatted daily standup report."""
    report_lines = [
        f"Daily Standup Report - {datetime.date.today()}",
        "=" * 50,
    ]
    for member, status in team_members.items():
        report_lines.append(f"\\n{member}:")
        report_lines.append(f"  Yesterday: {status.get('yesterday', 'N/A')}")
        report_lines.append(f"  Today: {status.get('today', 'N/A')}")
        report_lines.append(f"  Blockers: {status.get('blockers', 'None')}")
    return "\\n".join(report_lines)


if __name__ == "__main__":
    sprints = [21, 18, 24, 22, 19]
    velocity = calculate_sprint_velocity(sprints)
    print(f"Average velocity: {velocity:.1f} points/sprint")

    team = {
        "Sarah Chen": {
            "yesterday": "Completed auth module refactor",
            "today": "Starting API integration tests",
            "blockers": "None",
        },
        "Marcus Johnson": {
            "yesterday": "Code review for PR #247",
            "today": "Implementing caching layer",
            "blockers": "Waiting for Redis cluster access",
        },
    }
    print(format_standup_report(team))
''')
    print(f"Sample workspace created: {WORKSPACE_DIR}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
