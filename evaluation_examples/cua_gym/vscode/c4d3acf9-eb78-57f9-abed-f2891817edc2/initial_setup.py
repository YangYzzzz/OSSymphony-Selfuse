"""
Initial Setup: Set up comprehensive file exclusion settings in VSCode
Task ID: vscode_we_039
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_039'
WORKSPACE = f'{WORKDIR}/workspace'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # Create workspace directory structure with Python and JavaScript files
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'src'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'scripts'), exist_ok=True)

    # Python files
    with open(os.path.join(WORKSPACE, 'src', 'app.py'), 'w') as f:
        f.write('''"""Main application module for data processing pipeline."""

import os
import sys
from datetime import datetime

class DataProcessor:
    """Handles ingestion and transformation of raw CSV data."""

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.processed_count = 0

    def run(self):
        """Execute the full processing pipeline."""
        files = [f for f in os.listdir(self.input_dir) if f.endswith(".csv")]
        for filename in files:
            self._process_file(os.path.join(self.input_dir, filename))
            self.processed_count += 1
        print(f"Processed {self.processed_count} files at {datetime.now()}")

    def _process_file(self, filepath: str):
        """Transform a single CSV file."""
        with open(filepath, "r") as fh:
            lines = fh.readlines()
        # placeholder transformation
        transformed = [line.strip().upper() for line in lines]
        out_path = os.path.join(self.output_dir, os.path.basename(filepath))
        with open(out_path, "w") as fh:
            fh.write("\\n".join(transformed))


if __name__ == "__main__":
    processor = DataProcessor("data/raw", "data/processed")
    processor.run()
''')

    with open(os.path.join(WORKSPACE, 'src', 'utils.py'), 'w') as f:
        f.write('''"""Utility functions for the data processing pipeline."""

import hashlib
import logging

logger = logging.getLogger(__name__)


def compute_checksum(filepath: str) -> str:
    """Compute SHA-256 checksum for a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def configure_logging(level: str = "INFO"):
    """Set up structured logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger.info("Logging configured at %s level", level)
''')

    with open(os.path.join(WORKSPACE, 'tests', 'test_app.py'), 'w') as f:
        f.write('''"""Unit tests for the DataProcessor class."""

import os
import tempfile
import unittest
from src.app import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.tmp, "input")
        self.output_dir = os.path.join(self.tmp, "output")
        os.makedirs(self.input_dir)
        os.makedirs(self.output_dir)

    def test_run_processes_csv(self):
        sample = os.path.join(self.input_dir, "sample.csv")
        with open(sample, "w") as f:
            f.write("name,age\\nAlice,30\\nBob,25\\n")
        proc = DataProcessor(self.input_dir, self.output_dir)
        proc.run()
        self.assertEqual(proc.processed_count, 1)


if __name__ == "__main__":
    unittest.main()
''')

    # JavaScript files
    with open(os.path.join(WORKSPACE, 'scripts', 'build.js'), 'w') as f:
        f.write('''/**
 * Build script for bundling frontend assets.
 */

const fs = require("fs");
const path = require("path");

const SRC_DIR = path.join(__dirname, "..", "src");
const DIST_DIR = path.join(__dirname, "..", "dist");

function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

function copyAssets() {
    const assets = fs.readdirSync(SRC_DIR).filter(f => f.endsWith(".css") || f.endsWith(".html"));
    ensureDir(DIST_DIR);
    assets.forEach(file => {
        fs.copyFileSync(path.join(SRC_DIR, file), path.join(DIST_DIR, file));
        console.log(`Copied ${file} to dist/`);
    });
}

copyAssets();
console.log("Build complete.");
''')

    with open(os.path.join(WORKSPACE, 'scripts', 'setup.js'), 'w') as f:
        f.write('''/**
 * Environment setup helper.
 */

const { execSync } = require("child_process");

function checkDependencies() {
    const deps = ["node", "npm", "python3"];
    deps.forEach(dep => {
        try {
            execSync(`which ${dep}`, { stdio: "pipe" });
            console.log(`[OK] ${dep} found`);
        } catch {
            console.error(`[MISSING] ${dep} not found`);
        }
    });
}

checkDependencies();
''')

    with open(os.path.join(WORKSPACE, 'package.json'), 'w') as f:
        f.write('''{
    "name": "data-pipeline-tools",
    "version": "1.0.0",
    "description": "Tooling for the data processing pipeline",
    "main": "scripts/build.js",
    "scripts": {
        "build": "node scripts/build.js",
        "setup": "node scripts/setup.js"
    }
}
''')

    with open(os.path.join(WORKSPACE, 'requirements.txt'), 'w') as f:
        f.write('''pandas>=2.0.0
numpy>=1.24.0
pytest>=7.3.0
black>=23.1.0
flake8>=6.0.0
''')

    # Ensure VSCode user settings directory exists with empty settings
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Initial workspace created: {WORKSPACE}')
    print(f'Empty settings.json created: {SETTINGS_PATH}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
