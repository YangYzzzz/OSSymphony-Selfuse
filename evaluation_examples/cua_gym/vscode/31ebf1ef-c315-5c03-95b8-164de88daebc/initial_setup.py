"""
Initial Setup: Python debugger not stopping at breakpoints in library code
Task ID: vscode_fix_070
Domain: vscode

Creates a Python project with a launch.json that has justMyCode: true,
preventing debugging into third-party library code.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_070'
PROJECT_DIR = os.path.join(WORKDIR, 'pyproject')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    # Create project directory structure
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- main.py: realistic Python file that imports third-party code ---
    main_py = os.path.join(PROJECT_DIR, 'main.py')
    with open(main_py, 'w') as f:
        f.write('''\
import os
import json
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None

API_BASE_URL = "https://api.weatherstation.example.com/v2"
API_KEY = os.environ.get("WEATHER_API_KEY", "demo-key-12345")


class WeatherClient:
    """Client for fetching weather data from external API."""

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or API_KEY
        self.base_url = base_url or API_BASE_URL
        self.session = requests.Session() if requests else None
        self._cache = {}

    def get_forecast(self, city: str, days: int = 5) -> dict:
        """Fetch weather forecast for a given city.

        The requests library internally handles connection pooling,
        retries, and SSL verification. To debug connection issues,
        we need to step into the library code.
        """
        cache_key = f"{city}:{days}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        if not self.session:
            raise RuntimeError("requests library is not installed")

        url = f"{self.base_url}/forecast"
        params = {
            "city": city,
            "days": days,
            "key": self.api_key,
            "units": "metric",
        }

        # BUG: When debugging, breakpoints inside requests.get() are
        # ignored because justMyCode is set to true in launch.json.
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        self._cache[cache_key] = data
        return data

    def get_current_temperature(self, city: str) -> float:
        """Get current temperature for a city."""
        forecast = self.get_forecast(city, days=1)
        return forecast.get("current", {}).get("temp_c", 0.0)


def format_report(forecast_data: dict) -> str:
    """Format forecast data into a readable report."""
    lines = []
    lines.append(f"Weather Report - Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    city = forecast_data.get("location", {}).get("name", "Unknown")
    lines.append(f"Location: {city}")

    for day in forecast_data.get("forecast", {}).get("days", []):
        date = day.get("date", "N/A")
        high = day.get("high_c", "N/A")
        low = day.get("low_c", "N/A")
        condition = day.get("condition", "N/A")
        lines.append(f"  {date}: {condition}, High: {high}C, Low: {low}C")

    return "\\n".join(lines)


def main():
    client = WeatherClient()

    cities = ["San Francisco", "Tokyo", "London", "Sydney"]

    for city in cities:
        try:
            forecast = client.get_forecast(city)
            report = format_report(forecast)
            print(report)
            print()
        except Exception as e:
            print(f"Error fetching forecast for {city}: {e}")


if __name__ == "__main__":
    main()
''')

    # --- utils.py: helper module ---
    utils_py = os.path.join(PROJECT_DIR, 'utils.py')
    with open(utils_py, 'w') as f:
        f.write('''\
"""Utility functions for the weather project."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def celsius_to_fahrenheit(temp_c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (temp_c * 9 / 5) + 32


def format_temperature(temp: float, unit: str = "C") -> str:
    """Format temperature with unit symbol."""
    symbol = "\\u00b0"
    return f"{temp:.1f}{symbol}{unit}"


def validate_city_name(city: str) -> Optional[str]:
    """Validate and normalize city name."""
    if not city or not city.strip():
        logger.warning("Empty city name provided")
        return None
    normalized = city.strip().title()
    return normalized
''')

    # --- requirements.txt ---
    reqs = os.path.join(PROJECT_DIR, 'requirements.txt')
    with open(reqs, 'w') as f:
        f.write('''\
requests>=2.28.0
python-dotenv>=1.0.0
pytest>=7.0.0
''')

    # --- .vscode/launch.json with justMyCode: true (THE PROBLEM) ---
    launch_json = os.path.join(VSCODE_DIR, 'launch.json')
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Debug Current File",
                "type": "debugpy",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": True
            },
            {
                "name": "Python: Debug Main",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "console": "integratedTerminal",
                "justMyCode": True,
                "args": []
            }
        ]
    }
    with open(launch_json, 'w') as f:
        json.dump(launch_config, f, indent=4)

    # --- .vscode/settings.json ---
    settings_json = os.path.join(VSCODE_DIR, 'settings.json')
    settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "files.trimTrailingWhitespace": True,
        "python.analysis.typeCheckingMode": "basic"
    }
    with open(settings_json, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'launch.json has justMyCode: true (the problem to fix)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
