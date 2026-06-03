"""
Initial Setup: Install Bracket Pair Colorizer extension and disable native colorization
Task ID: vscode_we_060
Domain: vscode

Sets up the pre-task state:
- Extension CoenraadS.bracket-pair-colorizer-2 is installed
- Native bracket pair colorization is explicitly disabled in settings.json
- VSCode is open with a sample project
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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_sample_project():
    """Create a sample project with nested brackets for the extension to colorize."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # A Python file with nested brackets to demonstrate bracket colorization
    main_py = os.path.join(WORKSPACE_DIR, "main.py")
    with open(main_py, "w") as f:
        f.write('''\
def calculate_quarterly_revenue(sales_data):
    """Calculate quarterly revenue from nested sales data structure."""
    quarterly_totals = {}
    for region in sales_data:
        for quarter in sales_data[region]:
            if quarter not in quarterly_totals:
                quarterly_totals[quarter] = 0
            for product in sales_data[region][quarter]:
                amount = sales_data[region][quarter][product]
                if isinstance(amount, (int, float)):
                    quarterly_totals[quarter] += amount
    return quarterly_totals


def process_employee_records(records):
    """Process employee records with complex nested structures."""
    departments = {}
    for record in records:
        dept = record.get("department", "Unknown")
        if dept not in departments:
            departments[dept] = {
                "employees": [],
                "total_salary": 0,
                "avg_performance": 0,
            }
        departments[dept]["employees"].append({
            "name": record["name"],
            "role": record.get("role", "Staff"),
            "salary": record.get("salary", 0),
            "performance_scores": [
                score for score in record.get("reviews", [])
                if isinstance(score, (int, float))
            ],
        })
        departments[dept]["total_salary"] += record.get("salary", 0)

    for dept_info in departments.values():
        all_scores = [
            s for emp in dept_info["employees"]
            for s in emp["performance_scores"]
        ]
        if all_scores:
            dept_info["avg_performance"] = sum(all_scores) / len(all_scores)

    return departments


if __name__ == "__main__":
    sample_sales = {
        "North America": {
            "Q1": {"Widget A": 45230, "Widget B": 32100, "Widget C": 18750},
            "Q2": {"Widget A": 51200, "Widget B": 28900, "Widget C": 22400},
        },
        "Europe": {
            "Q1": {"Widget A": 38100, "Widget B": 41200, "Widget C": 15600},
            "Q2": {"Widget A": 42300, "Widget B": 39800, "Widget C": 19200},
        },
    }
    result = calculate_quarterly_revenue(sample_sales)
    for q, total in sorted(result.items()):
        print(f"{q}: ${total:,.2f}")
''')

    # A JavaScript file with deeply nested callbacks/brackets
    app_js = os.path.join(WORKSPACE_DIR, "app.js")
    with open(app_js, "w") as f:
        f.write('''\
const express = require('express');
const app = express();

function initializeRoutes(config) {
    const routes = config.routes.map((route) => {
        return {
            path: route.path,
            handler: (req, res) => {
                const data = processRequest(req, {
                    validate: (input) => {
                        return Object.keys(input).every((key) => {
                            return typeof input[key] !== 'undefined';
                        });
                    },
                    transform: (input) => {
                        return Object.entries(input).reduce((acc, [key, value]) => {
                            acc[key] = Array.isArray(value) ? value.filter((v) => v !== null) : value;
                            return acc;
                        }, {});
                    },
                });
                res.json({ success: true, data });
            },
        };
    });
    return routes;
}

module.exports = { initializeRoutes };
''')

    print(f"Sample project created at {WORKSPACE_DIR}")


def install_bracket_colorizer():
    """Install the Bracket Pair Colorizer 2 extension."""
    print("Installing CoenraadS.bracket-pair-colorizer-2...")
    result = subprocess.run(
        ["code", "--install-extension", "CoenraadS.bracket-pair-colorizer-2", "--force"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    print(f"stdout: {result.stdout}")
    if result.returncode != 0:
        print(f"stderr: {result.stderr}")
    # Verify installation
    check = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True)
    if "CoenraadS.bracket-pair-colorizer-2" in check.stdout:
        print("Extension installed successfully.")
    else:
        print("WARNING: Extension may not have installed correctly.")
        print(f"Installed extensions: {check.stdout}")


def setup_settings():
    """Explicitly disable native bracket pair colorization."""
    update_settings({
        "editor.bracketPairColorization.enabled": False,
        "editor.guides.bracketPairs": False,
    })
    print(f"Settings updated: native bracket colorization disabled")


def main():
    create_sample_project()
    install_bracket_colorizer()
    setup_settings()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print("GUI_READY: VSCode launched with workspace on DISPLAY=:0")


main()
