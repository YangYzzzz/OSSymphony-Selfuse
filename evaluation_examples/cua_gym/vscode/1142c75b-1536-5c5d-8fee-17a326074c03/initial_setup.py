"""
Initial Setup: Configure Thunder Client extension in VSCode
Task ID: vscode_we_087
Domain: vscode

Creates an API project workspace with realistic files.
Thunder Client extension is already installed on the VM.
User settings.json is empty (no thunder-client settings).
VSCode opens with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_087'
PROJECT_DIR = os.path.join(WORKDIR, 'api-project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
VSCODE_USER_DIR = os.path.join(WORKDIR, '.config', 'Code', 'User')
USER_SETTINGS = os.path.join(VSCODE_USER_DIR, 'settings.json')


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


def create_project():
    """Create a realistic API project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Main application file
    with open(os.path.join(PROJECT_DIR, 'src', 'app.py'), 'w') as f:
        f.write('''"""
Weather API Service
Provides current weather data and forecasts for cities worldwide.
"""

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# In-memory weather data store
CITIES = {
    "new_york": {"lat": 40.7128, "lon": -74.0060, "timezone": "America/New_York"},
    "london": {"lat": 51.5074, "lon": -0.1278, "timezone": "Europe/London"},
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "timezone": "Asia/Tokyo"},
    "sydney": {"lat": -33.8688, "lon": 151.2093, "timezone": "Australia/Sydney"},
    "paris": {"lat": 48.8566, "lon": 2.3522, "timezone": "Europe/Paris"},
}


@app.route("/api/v1/weather/<city>", methods=["GET"])
def get_weather(city):
    """Get current weather for a city."""
    city_key = city.lower().replace(" ", "_")
    if city_key not in CITIES:
        return jsonify({"error": f"City '{city}' not found"}), 404

    info = CITIES[city_key]
    return jsonify({
        "city": city,
        "coordinates": {"lat": info["lat"], "lon": info["lon"]},
        "temperature": round(random.uniform(5, 35), 1),
        "humidity": random.randint(30, 90),
        "wind_speed": round(random.uniform(0, 30), 1),
        "condition": random.choice(["sunny", "cloudy", "rainy", "partly_cloudy"]),
        "timestamp": datetime.utcnow().isoformat(),
    })


@app.route("/api/v1/forecast/<city>", methods=["GET"])
def get_forecast(city):
    """Get 5-day forecast for a city."""
    city_key = city.lower().replace(" ", "_")
    if city_key not in CITIES:
        return jsonify({"error": f"City '{city}' not found"}), 404

    days = int(request.args.get("days", 5))
    forecast = []
    for i in range(days):
        date = datetime.utcnow() + timedelta(days=i)
        forecast.append({
            "date": date.strftime("%Y-%m-%d"),
            "high": round(random.uniform(15, 35), 1),
            "low": round(random.uniform(0, 20), 1),
            "condition": random.choice(["sunny", "cloudy", "rainy", "partly_cloudy"]),
            "precipitation_chance": random.randint(0, 100),
        })

    return jsonify({"city": city, "forecast": forecast})


@app.route("/api/v1/cities", methods=["GET"])
def list_cities():
    """List all supported cities."""
    return jsonify({"cities": list(CITIES.keys())})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
''')

    # Requirements file
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('''flask==3.0.0
requests==2.31.0
pytest==7.4.3
python-dotenv==1.0.0
''')

    # Test file
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_weather.py'), 'w') as f:
        f.write('''"""Tests for Weather API endpoints."""

import pytest
import json


def test_get_weather_valid_city():
    """Test getting weather for a valid city returns 200."""
    # TODO: implement with test client
    pass


def test_get_weather_invalid_city():
    """Test getting weather for invalid city returns 404."""
    pass


def test_forecast_default_days():
    """Test forecast returns 5 days by default."""
    pass


def test_list_cities():
    """Test listing all supported cities."""
    pass
''')

    # .env.example
    with open(os.path.join(PROJECT_DIR, '.env.example'), 'w') as f:
        f.write('''API_KEY=your_api_key_here
DEBUG=true
PORT=5001
DATABASE_URL=sqlite:///weather.db
''')

    # README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('''# Weather API Service

A REST API providing current weather data and forecasts.

## Endpoints

- `GET /api/v1/weather/<city>` - Current weather
- `GET /api/v1/forecast/<city>` - Multi-day forecast
- `GET /api/v1/cities` - List supported cities

## Setup

```bash
pip install -r requirements.txt
python src/app.py
```

## Testing

Use Thunder Client extension in VSCode to test API endpoints interactively.
''')

    print(f'API project created at: {PROJECT_DIR}')


def setup_empty_user_settings():
    """Ensure VSCode user settings.json is empty (no thunder-client config)."""
    os.makedirs(VSCODE_USER_DIR, exist_ok=True)
    with open(USER_SETTINGS, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'User settings.json set to empty: {USER_SETTINGS}')


def ensure_no_workspace_settings():
    """Make sure workspace .vscode/settings.json does NOT contain thunder-client settings."""
    ws_settings_path = os.path.join(VSCODE_DIR, 'settings.json')
    # Write a minimal workspace settings (no thunder-client config)
    with open(ws_settings_path, 'w') as f:
        json.dump({
            "python.defaultInterpreterPath": "/usr/bin/python3"
        }, f, indent=4)
    print(f'Workspace settings.json created (no thunder-client config): {ws_settings_path}')


def install_thunder_client():
    """Install Thunder Client extension if not already present."""
    result = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True, text=True
    )
    if "rangav.vscode-thunder-client" not in result.stdout.lower():
        print("Installing Thunder Client extension...")
        subprocess.run(
            ["code", "--install-extension", "rangav.vscode-thunder-client", "--force"],
            capture_output=True, text=True
        )
        print("Thunder Client extension installed.")
    else:
        print("Thunder Client extension already installed.")


def main():
    create_project()
    setup_empty_user_settings()
    ensure_no_workspace_settings()
    install_thunder_client()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with api-project folder')


main()
