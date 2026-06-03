"""
Initial Setup: VSCode project with mixed line endings, no workspace settings
Task ID: vscode_code_069
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_069'
PROJECT_DIR = f'{WORKDIR}/project'


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


def write_bytes(path, content_bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(content_bytes)


def create_initial():
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- main.py (LF endings) ---
    main_py = (
        "#!/usr/bin/env python3\n"
        "# Main entry point for the data processing pipeline\n"
        "\n"
        "import os\n"
        "import sys\n"
        "import json\n"
        "from pathlib import Path\n"
        "\n"
        "CONFIG_FILE = 'config.json'\n"
        "OUTPUT_DIR = 'output'\n"
        "\n"
        "\n"
        "def load_config(path):\n"
        "    \"\"\"Load configuration from JSON file.\"\"\"\n"
        "    with open(path, 'r') as f:\n"
        "        return json.load(f)\n"
        "\n"
        "\n"
        "def process_data(records):\n"
        "    \"\"\"Process a list of data records.\"\"\"\n"
        "    results = []\n"
        "    for record in records:\n"
        "        if record.get('active', False):\n"
        "            results.append({\n"
        "                'id': record['id'],\n"
        "                'name': record['name'],\n"
        "                'score': record.get('score', 0) * 1.1\n"
        "            })\n"
        "    return results\n"
        "\n"
        "\n"
        "def main():\n"
        "    config = load_config(CONFIG_FILE)\n"
        "    data = config.get('records', [])\n"
        "    processed = process_data(data)\n"
        "    os.makedirs(OUTPUT_DIR, exist_ok=True)\n"
        "    out_path = os.path.join(OUTPUT_DIR, 'results.json')\n"
        "    with open(out_path, 'w') as f:\n"
        "        json.dump(processed, f, indent=2)\n"
        "    print(f'Processed {len(processed)} records -> {out_path}')\n"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )
    write_bytes(f'{PROJECT_DIR}/main.py', main_py.encode('utf-8'))

    # --- utils.py (CRLF endings) ---
    utils_py = (
        "# Utility functions\r\n"
        "import re\r\n"
        "import datetime\r\n"
        "\r\n"
        "\r\n"
        "def sanitize_name(name):\r\n"
        "    \"\"\"Remove special characters from a name string.\"\"\"\r\n"
        "    return re.sub(r'[^A-Za-z0-9_\\-]', '_', name)\r\n"
        "\r\n"
        "\r\n"
        "def format_date(dt):\r\n"
        "    \"\"\"Return ISO 8601 date string.\"\"\"\r\n"
        "    if isinstance(dt, str):\r\n"
        "        return dt\r\n"
        "    return dt.strftime('%Y-%m-%d')\r\n"
        "\r\n"
        "\r\n"
        "def clamp(value, min_val, max_val):\r\n"
        "    \"\"\"Clamp a numeric value between min and max.\"\"\"\r\n"
        "    return max(min_val, min(max_val, value))\r\n"
        "\r\n"
        "\r\n"
        "def parse_bool(value):\r\n"
        "    \"\"\"Parse a boolean from various representations.\"\"\"\r\n"
        "    if isinstance(value, bool):\r\n"
        "        return value\r\n"
        "    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')\r\n"
        "\r\n"
        "\r\n"
        "TIMESTAMP = datetime.datetime.utcnow().isoformat()\r\n"
    )
    write_bytes(f'{PROJECT_DIR}/utils.py', utils_py.encode('utf-8'))

    # --- index.js (LF endings) ---
    index_js = (
        "// Frontend entry point\n"
        "'use strict';\n"
        "\n"
        "const express = require('express');\n"
        "const path = require('path');\n"
        "const fs = require('fs');\n"
        "\n"
        "const app = express();\n"
        "const PORT = process.env.PORT || 3000;\n"
        "\n"
        "app.use(express.json());\n"
        "app.use(express.static(path.join(__dirname, 'public')));\n"
        "\n"
        "app.get('/api/status', (req, res) => {\n"
        "    res.json({ status: 'ok', version: '1.2.3' });\n"
        "});\n"
        "\n"
        "app.get('/api/data', (req, res) => {\n"
        "    const dataPath = path.join(__dirname, 'data', 'records.json');\n"
        "    if (!fs.existsSync(dataPath)) {\n"
        "        return res.status(404).json({ error: 'Data file not found' });\n"
        "    }\n"
        "    const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));\n"
        "    res.json(data);\n"
        "});\n"
        "\n"
        "app.listen(PORT, () => {\n"
        "    console.log(`Server running on port ${PORT}`);\n"
        "});\n"
        "\n"
        "module.exports = app;\n"
    )
    write_bytes(f'{PROJECT_DIR}/index.js', index_js.encode('utf-8'))

    # --- config.json (CRLF endings) ---
    config_json = (
        "{\r\n"
        "    \"app_name\": \"DataPipeline\",\r\n"
        "    \"version\": \"1.2.3\",\r\n"
        "    \"debug\": false,\r\n"
        "    \"database\": {\r\n"
        "        \"host\": \"localhost\",\r\n"
        "        \"port\": 5432,\r\n"
        "        \"name\": \"pipeline_db\"\r\n"
        "    },\r\n"
        "    \"records\": [\r\n"
        "        {\"id\": 1, \"name\": \"Alice Nguyen\", \"active\": true, \"score\": 88.5},\r\n"
        "        {\"id\": 2, \"name\": \"Brian Okafor\", \"active\": false, \"score\": 72.0},\r\n"
        "        {\"id\": 3, \"name\": \"Clara Mendez\", \"active\": true, \"score\": 95.3},\r\n"
        "        {\"id\": 4, \"name\": \"David Kim\", \"active\": true, \"score\": 61.8},\r\n"
        "        {\"id\": 5, \"name\": \"Elena Petrov\", \"active\": false, \"score\": 78.2}\r\n"
        "    ]\r\n"
        "}\r\n"
    )
    write_bytes(f'{PROJECT_DIR}/config.json', config_json.encode('utf-8'))

    # --- run.sh (LF endings) ---
    run_sh = (
        "#!/bin/bash\n"
        "# Runs the data processing pipeline\n"
        "\n"
        "set -e\n"
        "\n"
        "SCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"\n"
        "cd \"$SCRIPT_DIR\"\n"
        "\n"
        "echo \"Starting pipeline...\"\n"
        "python3 main.py\n"
        "echo \"Pipeline finished.\"\n"
    )
    write_bytes(f'{PROJECT_DIR}/run.sh', run_sh.encode('utf-8'))

    # --- deploy.bat (CRLF endings — .bat files require CRLF) ---
    deploy_bat = (
        "@echo off\r\n"
        "REM Deployment script for Windows\r\n"
        "\r\n"
        "set PROJECT_ROOT=%~dp0\r\n"
        "cd /d %PROJECT_ROOT%\r\n"
        "\r\n"
        "echo Deploying DataPipeline version 1.2.3...\r\n"
        "echo.\r\n"
        "\r\n"
        "REM Install Python dependencies\r\n"
        "pip install -r requirements.txt\r\n"
        "\r\n"
        "REM Run database migrations\r\n"
        "python manage.py migrate\r\n"
        "\r\n"
        "REM Restart service\r\n"
        "net stop DataPipelineService 2>NUL\r\n"
        "net start DataPipelineService\r\n"
        "\r\n"
        "echo Deployment complete.\r\n"
        "pause\r\n"
    )
    write_bytes(f'{PROJECT_DIR}/deploy.bat', deploy_bat.encode('utf-8'))

    # --- README.md (CRLF endings) ---
    readme_md = (
        "# DataPipeline Project\r\n"
        "\r\n"
        "A lightweight data processing pipeline for batch record transformation.\r\n"
        "\r\n"
        "## Requirements\r\n"
        "\r\n"
        "- Python 3.8+\r\n"
        "- Node.js 16+ (for the frontend server)\r\n"
        "\r\n"
        "## Usage\r\n"
        "\r\n"
        "```bash\r\n"
        "bash run.sh\r\n"
        "```\r\n"
        "\r\n"
        "## Configuration\r\n"
        "\r\n"
        "Edit `config.json` to change database settings and records.\r\n"
        "\r\n"
        "## Deployment\r\n"
        "\r\n"
        "On Windows, run `deploy.bat` as Administrator.\r\n"
    )
    write_bytes(f'{PROJECT_DIR}/README.md', readme_md.encode('utf-8'))

    # --- requirements.txt (LF endings) ---
    requirements_txt = (
        "requests>=2.28.0\n"
        "python-dotenv>=1.0.0\n"
        "psycopg2-binary>=2.9.5\n"
        "pydantic>=1.10.0\n"
        "click>=8.1.3\n"
    )
    write_bytes(f'{PROJECT_DIR}/requirements.txt', requirements_txt.encode('utf-8'))

    print(f'Project directory created: {PROJECT_DIR}')
    print(f'Files created with mixed line endings (LF and CRLF):')
    print(f'  LF:   main.py, index.js, run.sh, requirements.txt')
    print(f'  CRLF: utils.py, config.json, deploy.bat, README.md')
    print(f'No .vscode/settings.json exists (task is to create it)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder at DISPLAY=:0')


create_initial()
