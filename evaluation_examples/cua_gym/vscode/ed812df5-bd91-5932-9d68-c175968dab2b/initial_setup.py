"""
Initial Setup: Set up a Jupyter notebook environment in VSCode with specific environment variables
Task ID: vscode_py_088
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_088'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
NOTEBOOK_PATH = f'{PROJECT_DIR}/api_client.ipynb'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'

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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic Python helper module used by the notebook
    helper_code = '''\
"""API client utilities for data retrieval."""

import os
import requests


def get_api_client():
    """Create an authenticated API client using environment variables."""
    api_key = os.environ.get("API_KEY")
    base_url = os.environ.get("BASE_URL")
    if not api_key or not base_url:
        raise EnvironmentError(
            "API_KEY and BASE_URL environment variables must be set. "
            "Create a .env file in the project root and configure VSCode to load it."
        )
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    return session, base_url


def fetch_users(session, base_url, limit=50):
    """Fetch user records from the API."""
    response = session.get(f"{base_url}/v1/users", params={"limit": limit})
    response.raise_for_status()
    return response.json()


def fetch_analytics(session, base_url, start_date, end_date):
    """Fetch analytics data for a date range."""
    response = session.get(
        f"{base_url}/v1/analytics",
        params={"start": start_date, "end": end_date},
    )
    response.raise_for_status()
    return response.json()
'''
    with open(f'{PROJECT_DIR}/api_utils.py', 'w') as f:
        f.write(helper_code)

    # Create a requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('requests>=2.28.0\njupyterlab>=4.0.0\nipykernel>=6.25.0\npython-dotenv>=1.0.0\n')

    # Create a README for the project
    readme = """\
# API Analytics Notebook

This project uses a Jupyter notebook to pull data from an external analytics API.

## Setup

1. Create a `.env` file in this directory with your credentials:
   ```
   API_KEY=your_api_key_here
   BASE_URL=https://api.example.com
   ```

2. Configure VSCode to load the `.env` file by adding to your settings:
   ```json
   {
       "python.envFile": "${workspaceFolder}/.env"
   }
   ```

3. Open the notebook and run the cells.
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Create the Jupyter notebook (ipynb is JSON)
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# API Analytics Dashboard\n",
                    "\n",
                    "This notebook connects to our analytics API to fetch and visualize user data.\n",
                    "Make sure your environment variables are properly configured before running."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "import json\n",
                    "from datetime import datetime, timedelta"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Check environment variables are set\n",
                    "api_key = os.environ.get('API_KEY')\n",
                    "base_url = os.environ.get('BASE_URL')\n",
                    "\n",
                    "if not api_key:\n",
                    "    print('WARNING: API_KEY is not set. Please configure your .env file.')\n",
                    "else:\n",
                    "    print(f'API_KEY is configured (length: {len(api_key)})')\n",
                    "\n",
                    "if not base_url:\n",
                    "    print('WARNING: BASE_URL is not set. Please configure your .env file.')\n",
                    "else:\n",
                    "    print(f'BASE_URL: {base_url}')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from api_utils import get_api_client, fetch_users, fetch_analytics\n",
                    "\n",
                    "# Initialize the API client\n",
                    "# This will raise an error if env vars are not configured\n",
                    "session, base_url = get_api_client()\n",
                    "print('API client initialized successfully')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Fetch recent analytics data\n",
                    "end_date = datetime.now().strftime('%Y-%m-%d')\n",
                    "start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')\n",
                    "\n",
                    "analytics = fetch_analytics(session, base_url, start_date, end_date)\n",
                    "print(f'Retrieved {len(analytics.get(\"data\", []))} analytics records')"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(NOTEBOOK_PATH, 'w') as f:
        json.dump(notebook, f, indent=1)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  Notebook: {NOTEBOOK_PATH}')
    print(f'  Helper: {PROJECT_DIR}/api_utils.py')
    print(f'  No .env file exists (task requires creating one)')

    # Verify no .env file exists
    env_path = f'{PROJECT_DIR}/.env'
    if os.path.exists(env_path):
        os.remove(env_path)
        print('  Removed stale .env file')

    # Verify no workspace settings with python.envFile
    settings_path = f'{VSCODE_DIR}/settings.json'
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            try:
                settings = json.load(f)
                if 'python.envFile' in settings:
                    del settings['python.envFile']
                    with open(settings_path, 'w') as fw:
                        json.dump(settings, fw, indent=4)
                    print('  Removed python.envFile from workspace settings')
            except json.JSONDecodeError:
                pass

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
