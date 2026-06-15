"""
Initial Setup: Open VSCode with one integrated terminal
Task ID: vscode_stu_039
Domain: vscode

Creates a realistic project workspace and opens VSCode with a single
integrated terminal visible.
"""

import os
import subprocess
import time

# Set DISPLAY early so pyautogui and subprocess both work with the GUI
os.environ["DISPLAY"] = ":0"

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_039'
PROJECT_DIR = f'{WORKDIR}/web-dashboard'


def create_project():
    """Create a realistic web project workspace."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write('from flask import Flask, jsonify, render_template\n'
                'import os\n\n'
                'app = Flask(__name__)\n\n'
                '@app.route("/")\n'
                'def index():\n'
                '    return render_template("index.html")\n\n'
                '@app.route("/api/status")\n'
                'def status():\n'
                '    return jsonify({\n'
                '        "status": "running",\n'
                '        "version": "1.3.2",\n'
                '        "environment": os.getenv("FLASK_ENV", "production")\n'
                '    })\n\n'
                '@app.route("/api/metrics")\n'
                'def metrics():\n'
                '    return jsonify({\n'
                '        "requests_per_minute": 142,\n'
                '        "avg_response_ms": 23.5,\n'
                '        "active_users": 87\n'
                '    })\n\n'
                'if __name__ == "__main__":\n'
                '    app.run(host="0.0.0.0", port=5050, debug=True)\n')

    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('flask==3.0.2\ngunicorn==21.2.0\nrequests==2.31.0\npytest==8.0.1\n')

    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'tests', 'test_app.py'), 'w') as f:
        f.write('import pytest\nimport sys\nsys.path.insert(0, "..")\nfrom app import app\n\n'
                '@pytest.fixture\ndef client():\n'
                '    app.config["TESTING"] = True\n'
                '    with app.test_client() as client:\n'
                '        yield client\n\n'
                'def test_status(client):\n'
                '    rv = client.get("/api/status")\n'
                '    data = rv.get_json()\n'
                '    assert data["status"] == "running"\n')

    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('# Web Dashboard\n\nA lightweight Flask dashboard for monitoring server metrics.\n')

    print(f'Project created at: {PROJECT_DIR}')


def setup_gui():
    """Open VSCode with project folder and one terminal."""
    import pyautogui

    # Kill any existing VSCode instances for clean state
    subprocess.run(['pkill', '-f', '/usr/share/code/code'], capture_output=True)
    time.sleep(1)

    # Launch VSCode with the project folder
    subprocess.Popen(
        ['code', PROJECT_DIR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for VSCode to fully load
    time.sleep(5)

    # Focus VSCode window
    subprocess.run(['wmctrl', '-a', 'Visual Studio Code'], capture_output=True)
    time.sleep(0.5)

    # Use Command Palette to create a new terminal (more reliable than Ctrl+grave)
    pyautogui.hotkey('ctrl', 'shift', 'p')
    time.sleep(1)
    pyautogui.typewrite('Terminal: Create New', interval=0.02)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)

    print('GUI_READY: VSCode launched with one integrated terminal')


create_project()
setup_gui()
