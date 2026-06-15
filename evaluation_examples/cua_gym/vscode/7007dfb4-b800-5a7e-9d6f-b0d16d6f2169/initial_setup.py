"""
Initial Setup: Convert single-quoted strings to double-quoted strings in config.py
Task ID: vscode_edit_055
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_055'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/config.py'

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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Create a 35-line Python configuration file using single-quoted strings
    # Exactly 12 single-quoted string values, no embedded quotes
    config_content = (
        "# Application Configuration\n"
        "# Project: MyWebApp v2.3\n"
        "\n"
        "# Database settings\n"
        "DATABASE_HOST = 'localhost'\n"
        "DATABASE_PORT = 5432\n"
        "DATABASE_NAME = 'mydb'\n"
        "DATABASE_USER = 'admin'\n"
        "DATABASE_PASSWORD = 'securepass123'\n"
        "\n"
        "# Application settings\n"
        "APP_NAME = 'MyWebApp'\n"
        "DEBUG = False\n"
        "SECRET_KEY = 'django-insecure-k9x2p'\n"
        "\n"
        "# Logging configuration\n"
        "LOG_LEVEL = 'INFO'\n"
        "LOG_FILE = '/var/log/mywebapp/app.log'\n"
        "\n"
        "# Cache settings\n"
        "CACHE_BACKEND = 'memcached'\n"
        "CACHE_TIMEOUT = 300\n"
        "\n"
        "# Email settings\n"
        "EMAIL_HOST = 'smtp.example.com'\n"
        "EMAIL_PORT = 587\n"
        "EMAIL_USE_TLS = True\n"
        "\n"
        "# Static files and timezone\n"
        "STATIC_URL = '/static/'\n"
        "TIME_ZONE = 'UTC'\n"
        "\n"
        "# Limits\n"
        "SESSION_COOKIE_AGE = 1209600\n"
        "MAX_UPLOAD_SIZE = 5242880\n"
    )

    with open(OUTPUT, 'w') as f:
        f.write(config_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the config.py file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
