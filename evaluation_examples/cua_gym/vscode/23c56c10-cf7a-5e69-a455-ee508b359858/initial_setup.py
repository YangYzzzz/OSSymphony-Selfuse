"""
Initial Setup: Configure VSCode with a Python project where isort is not configured for code actions on save.
Task ID: vscode_fix_088
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_088'
HOME = os.path.expanduser('~')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'pyproject')


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
    """Create a realistic Python project with unsorted imports."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main application file with deliberately unsorted imports
    main_py = '''\
import sys
import json
from pathlib import Path
import os
from datetime import datetime, timedelta
import re
from collections import OrderedDict, defaultdict
import csv
from typing import List, Dict, Optional
import logging

# Third-party imports (unsorted)
import requests
from flask import Flask, jsonify, request
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String
import pandas as pd


logger = logging.getLogger(__name__)

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///app.db")
engine = create_engine(DATABASE_URL)


class DataProcessor:
    """Processes incoming data records for the analytics pipeline."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or str(Path.home() / ".config" / "processor.json")
        self.records: List[Dict] = []
        self.start_time = datetime.now()
        self._cache: OrderedDict = OrderedDict()

    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Config file not found at %s, using defaults", self.config_path)
            return {"batch_size": 100, "timeout": 30}

    def process_batch(self, raw_data: List[str]) -> List[Dict]:
        results = []
        pattern = re.compile(r"^(\\d{4}-\\d{2}-\\d{2})\\s+(.+)$")
        for line in raw_data:
            match = pattern.match(line)
            if match:
                date_str, content = match.groups()
                record = {
                    "date": datetime.strptime(date_str, "%Y-%m-%d"),
                    "content": content.strip(),
                    "processed_at": datetime.now(),
                }
                results.append(record)
        self.records.extend(results)
        return results

    def export_csv(self, output_path: str):
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "content", "processed_at"])
            writer.writeheader()
            for record in self.records:
                writer.writerow(record)
        logger.info("Exported %d records to %s", len(self.records), output_path)

    def get_stats(self) -> Dict:
        elapsed = datetime.now() - self.start_time
        return {
            "total_records": len(self.records),
            "elapsed_seconds": elapsed.total_seconds(),
            "cache_size": len(self._cache),
        }


@app.route("/api/process", methods=["POST"])
def api_process():
    data = request.get_json()
    processor = DataProcessor()
    results = processor.process_batch(data.get("lines", []))
    return jsonify({"processed": len(results), "stats": processor.get_stats()})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "uptime": str(timedelta(seconds=42))})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    # Utility module with unsorted imports
    utils_py = '''\
import hashlib
from functools import lru_cache
import base64
import hmac
from typing import Any, Union
import secrets
import os
from datetime import datetime


def generate_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_hex(length)


def hash_password(password: str, salt: str = None) -> tuple:
    """Hash a password using SHA-256 with salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    combined = f"{salt}{password}".encode("utf-8")
    hashed = hashlib.sha256(combined).hexdigest()
    return hashed, salt


@lru_cache(maxsize=128)
def encode_data(data: str) -> str:
    """Base64 encode a string."""
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


def verify_signature(payload: str, signature: str, secret: str) -> bool:
    """Verify HMAC-SHA256 signature."""
    expected = hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def get_env_config() -> dict:
    """Load configuration from environment variables."""
    return {
        "debug": os.environ.get("DEBUG", "false").lower() == "true",
        "log_level": os.environ.get("LOG_LEVEL", "INFO"),
        "started_at": datetime.now().isoformat(),
    }
'''
    with open(os.path.join(PROJECT_DIR, 'utils.py'), 'w') as f:
        f.write(utils_py)

    # Test file with unsorted imports
    test_py = '''\
import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import DataProcessor
from utils import generate_token, hash_password, encode_data


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    def test_load_config_default(self):
        config = self.processor.load_config()
        self.assertIn("batch_size", config)
        self.assertIn("timeout", config)

    def test_process_batch_valid(self):
        lines = [
            "2025-03-15 Sales report for Q1",
            "2025-03-16 Updated inventory count",
        ]
        results = self.processor.process_batch(lines)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["content"], "Sales report for Q1")

    def test_process_batch_invalid(self):
        lines = ["invalid line without date"]
        results = self.processor.process_batch(lines)
        self.assertEqual(len(results), 0)

    def test_get_stats(self):
        stats = self.processor.get_stats()
        self.assertEqual(stats["total_records"], 0)
        self.assertGreaterEqual(stats["elapsed_seconds"], 0)


class TestUtils(unittest.TestCase):
    def test_generate_token_length(self):
        token = generate_token(16)
        self.assertEqual(len(token), 32)  # hex doubles

    def test_hash_password(self):
        hashed, salt = hash_password("mypassword")
        self.assertIsNotNone(hashed)
        self.assertIsNotNone(salt)

    def test_encode_data(self):
        result = encode_data("hello")
        self.assertEqual(result, "aGVsbG8=")


if __name__ == "__main__":
    unittest.main()
'''
    with open(os.path.join(PROJECT_DIR, 'test_main.py'), 'w') as f:
        f.write(test_py)

    # requirements.txt
    requirements = '''\
flask>=2.3.0
requests>=2.31.0
numpy>=1.24.0
pandas>=2.0.0
sqlalchemy>=2.0.0
'''
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    print(f'Project created at {PROJECT_DIR}')


def setup_vscode_settings():
    """Configure VSCode settings WITHOUT source.organizeImports in codeActionsOnSave."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Set up some reasonable VSCode settings but do NOT include organizeImports
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Visual Studio Dark",
        "python.analysis.typeCheckingMode": "basic",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    # Ensure editor.codeActionsOnSave exists but does NOT have source.organizeImports
    if "editor.codeActionsOnSave" not in settings:
        settings["editor.codeActionsOnSave"] = {}

    # Remove any existing organizeImports setting if present
    if "source.organizeImports" in settings.get("editor.codeActionsOnSave", {}):
        del settings["editor.codeActionsOnSave"]["source.organizeImports"]

    # Also ensure no Python-specific organizeImports is set
    if "[python]" in settings:
        python_settings = settings["[python]"]
        if "editor.codeActionsOnSave" in python_settings:
            if "source.organizeImports" in python_settings["editor.codeActionsOnSave"]:
                del python_settings["editor.codeActionsOnSave"]["source.organizeImports"]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured at {SETTINGS_PATH}')


def install_isort():
    """Ensure isort is available."""
    try:
        subprocess.run(['pip3', 'install', 'isort'], capture_output=True, check=True)
        print('isort installed successfully')
    except Exception as e:
        print(f'Note: isort install attempt: {e}')


def main():
    create_project()
    setup_vscode_settings()
    install_isort()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with ~/pyproject')


main()
