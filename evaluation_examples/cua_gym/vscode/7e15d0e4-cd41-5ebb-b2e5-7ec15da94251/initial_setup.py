"""
Initial Setup: VSCode with a Git repository, GitLens NOT installed
Task ID: vscode_ext_027
Domain: vs_code

This script:
1. Creates a realistic Git repository at /home/user/workspace with Python files
2. Ensures GitLens extension is NOT installed
3. Configures VSCode settings WITHOUT gitlens.currentLine.enabled set to true
4. Opens VSCode with the workspace
"""

import os
import json
import shlex
import subprocess
import time

HOME = '/home/user'
WORKDIR = HOME
TASK_ID = 'vscode_ext_027'
WORKSPACE = os.path.join(HOME, 'workspace')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            import re
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings: dict):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def uninstall_extension_if_present(extension_id: str):
    """Uninstall extension if it is installed, so the task requires installing it."""
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=30
        )
        if extension_id.lower() in result.stdout.lower():
            print(f"Uninstalling existing {extension_id} extension...")
            subprocess.run(
                ["code", "--uninstall-extension", extension_id],
                capture_output=True, text=True, timeout=60
            )
            print(f"Extension {extension_id} uninstalled.")
        else:
            print(f"Extension {extension_id} is not installed (good).")
    except Exception as e:
        print(f"Warning: could not check/uninstall extension: {e}")


def create_workspace():
    """Create a realistic Git repository with Python project files."""
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create a realistic Python project
    files = {
        'main.py': '''\
#!/usr/bin/env python3
"""
DataPipeline — A lightweight ETL tool for processing sales data.
"""

import os
import sys
import logging
from pipeline.loader import DataLoader
from pipeline.transformer import DataTransformer
from pipeline.exporter import DataExporter


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting DataPipeline v1.3.2")

    config_path = os.environ.get("PIPELINE_CONFIG", "config/pipeline.yaml")
    loader = DataLoader(config_path)
    transformer = DataTransformer()
    exporter = DataExporter(output_dir="output/")

    raw_data = loader.load()
    logger.info(f"Loaded {len(raw_data)} records")

    transformed = transformer.run(raw_data)
    logger.info(f"Transformed {len(transformed)} records")

    exporter.export(transformed)
    logger.info("Export complete")


if __name__ == "__main__":
    main()
''',
        'pipeline/__init__.py': '# DataPipeline package\n__version__ = "1.3.2"\n',
        'pipeline/loader.py': '''\
import yaml
import csv
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load raw data from CSV sources specified in config."""

    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.source = self.config.get("source", "data/sales.csv")

    def load(self) -> list:
        records = []
        with open(self.source, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append(dict(row))
        logger.info(f"Loaded {len(records)} rows from {self.source}")
        return records
''',
        'pipeline/transformer.py': '''\
import logging

logger = logging.getLogger(__name__)


class DataTransformer:
    """Apply business transformation rules to raw sales records."""

    REGION_MAP = {
        "NA": "North America",
        "EU": "Europe",
        "APAC": "Asia Pacific",
        "LATAM": "Latin America",
    }

    def run(self, records: list) -> list:
        transformed = []
        for record in records:
            try:
                item = {
                    "id": record["order_id"],
                    "region": self.REGION_MAP.get(record["region"], record["region"]),
                    "revenue": float(record["amount"]) * 1.08,  # include tax
                    "sales_rep": record["rep_name"].strip().title(),
                    "quarter": self._to_quarter(record["sale_date"]),
                }
                transformed.append(item)
            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping malformed record {record}: {e}")
        return transformed

    @staticmethod
    def _to_quarter(date_str: str) -> str:
        month = int(date_str.split("-")[1])
        q = (month - 1) // 3 + 1
        year = date_str.split("-")[0]
        return f"Q{q}-{year}"
''',
        'pipeline/exporter.py': '''\
import os
import json
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """Export transformed records to JSON files."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export(self, records: list):
        output_path = os.path.join(self.output_dir, "transformed_sales.json")
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)
        logger.info(f"Exported {len(records)} records to {output_path}")
''',
        'config/pipeline.yaml': '''\
source: data/sales.csv
output_dir: output/
log_level: INFO
batch_size: 500
validate_schema: true
''',
        'data/sales.csv': '''\
order_id,region,amount,rep_name,sale_date
ORD-10042,NA,4820.50,sarah chen,2025-01-14
ORD-10043,EU,3125.00,marcus johnson,2025-01-15
ORD-10044,APAC,7890.25,priya nair,2025-01-16
ORD-10045,LATAM,2305.75,carlos reyes,2025-01-17
ORD-10046,NA,6150.00,emily thompson,2025-01-18
ORD-10047,EU,4430.50,david okonkwo,2025-01-21
ORD-10048,APAC,5980.00,aiko tanaka,2025-01-22
ORD-10049,NA,3275.25,james whitfield,2025-01-23
ORD-10050,EU,8920.75,anna kowalski,2025-01-24
ORD-10051,LATAM,1875.00,luis hernandez,2025-01-25
''',
        'README.md': '''\
# DataPipeline

A lightweight ETL pipeline for processing sales data.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Configuration

Edit `config/pipeline.yaml` to set source file, output directory, and other options.
''',
        'requirements.txt': '''\
pyyaml>=6.0
''',
        '.gitignore': '''\
__pycache__/
*.pyc
*.pyo
output/
.env
''',
    }

    # Create directories
    for dir_name in ['pipeline', 'config', 'data', 'output']:
        os.makedirs(os.path.join(WORKSPACE, dir_name), exist_ok=True)

    # Write all files
    for rel_path, content in files.items():
        full_path = os.path.join(WORKSPACE, rel_path)
        with open(full_path, 'w') as fh:
            fh.write(content)
    print(f"Workspace files created in {WORKSPACE}")

    # Initialize git repository
    try:
        # Init git
        subprocess.run(
            ["git", "init", WORKSPACE],
            capture_output=True, text=True
        )
        # Configure git identity for commits
        subprocess.run(
            ["git", "-C", WORKSPACE, "config", "user.email", "dev@example.com"],
            capture_output=True, text=True
        )
        subprocess.run(
            ["git", "-C", WORKSPACE, "config", "user.name", "Dev User"],
            capture_output=True, text=True
        )
        # Add and commit initial files
        subprocess.run(
            ["git", "-C", WORKSPACE, "add", "."],
            capture_output=True, text=True
        )
        result = subprocess.run(
            ["git", "-C", WORKSPACE, "commit", "-m", "Initial commit: DataPipeline v1.3.2"],
            capture_output=True, text=True
        )
        print("Git repo initialized:", result.returncode == 0)
    except Exception as e:
        print(f"Warning: git setup failed: {e}")


def configure_vscode_settings():
    """Set up VSCode settings without GitLens configuration."""
    settings = load_settings()

    # Remove any gitlens settings that might accidentally be enabled
    settings.pop("gitlens.currentLine.enabled", None)
    # Also ensure it's not set to true via explicit disable (no setting = default, but
    # for the task to be meaningful we set it to false explicitly)
    settings["gitlens.currentLine.enabled"] = False

    # Keep other sensible settings
    settings.setdefault("editor.fontSize", 14)
    settings.setdefault("editor.wordWrap", "on")
    settings.setdefault("files.autoSave", "onFocusChange")

    save_settings(settings)
    print(f"VSCode settings configured: {SETTINGS_PATH}")


def create_initial():
    print("=" * 60)
    print(f"Setting up initial environment for task: {TASK_ID}")
    print("=" * 60)

    # 1. Ensure GitLens is NOT installed
    uninstall_extension_if_present("eamodio.gitlens")

    # 2. Create a realistic Git workspace
    create_workspace()

    # 3. Configure VSCode settings (without GitLens settings)
    configure_vscode_settings()

    # 4. Open VSCode with the workspace (GUI-ready startup)
    print("Launching VSCode with workspace...")
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with workspace, DISPLAY=:0")
    print(f"Initial file created: {WORKSPACE}")
    print("Setup complete.")


create_initial()
