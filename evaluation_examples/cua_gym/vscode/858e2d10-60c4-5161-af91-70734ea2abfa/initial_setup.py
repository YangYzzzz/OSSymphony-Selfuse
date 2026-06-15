"""
Initial Setup: Disable Bracket Pair Colorizer extension in VSCode
Task ID: vscode_ext_006
Domain: vs_code

Initial state: VSCode with the 'Bracket Pair Colorizer' extension installed and ENABLED.
The agent will need to disable it without uninstalling.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_006'
EXTENSIONS_JSON = '/home/user/.vscode/extensions/extensions.json'
WORKSPACE_DIR = f'{WORKDIR}/workspace'


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


def install_extension_cli(extension_id: str):
    """Install a VSCode extension via CLI."""
    result = subprocess.run(
        ["code", "--install-extension", extension_id],
        capture_output=True,
        text=True,
        env={**os.environ, "DISPLAY": ":0"}
    )
    print(f"Install output: {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"Install stderr: {result.stderr.strip()}")


def ensure_extension_enabled():
    """Make sure the extension is installed and NOT disabled (enabled state)."""
    if not os.path.exists(EXTENSIONS_JSON):
        print("extensions.json not found, nothing to modify")
        return

    with open(EXTENSIONS_JSON, 'r') as f:
        extensions = json.load(f)

    modified = False
    for ext in extensions:
        ext_id = ext.get('identifier', {}).get('id', '').lower()
        if 'bracket-pair-colorizer' in ext_id:
            metadata = ext.get('metadata', {})
            if metadata.get('disabled') is True:
                # Remove disabled flag to make it enabled
                del metadata['disabled']
                modified = True
                print(f"Removed 'disabled' flag from {ext_id} (now enabled)")
            else:
                print(f"Extension {ext_id} is already enabled (no disabled flag)")

    if modified:
        with open(EXTENSIONS_JSON, 'w') as f:
            json.dump(extensions, f, indent=2)
        print("extensions.json updated — extension is now enabled")
    else:
        print("No changes needed to extensions.json")


def create_workspace():
    """Create a sample workspace with Python code files for context."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # main.py — realistic Python file with brackets/parentheses/braces
    main_py = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(main_py, 'w') as f:
        f.write("""\
# Project: DataPipeline
# Author: Alex Rivera
# Description: Data processing pipeline with nested structures

import json
from typing import Dict, List, Optional


class DataProcessor:
    \"\"\"Handles transformation of raw input data into structured output.\"\"\"

    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.results: List[Dict] = []
        self.errors: List[str] = []

    def process(self, records: List[Dict]) -> Dict[str, List]:
        \"\"\"Process a batch of records and return summary.\"\"\"
        for record in records:
            try:
                transformed = self._transform(record)
                self.results.append(transformed)
            except ValueError as e:
                self.errors.append(str(e))

        return {
            "processed": self.results,
            "errors": self.errors,
            "stats": {
                "total": len(records),
                "success": len(self.results),
                "failed": len(self.errors),
            }
        }

    def _transform(self, record: Dict) -> Dict:
        \"\"\"Apply transformation rules to a single record.\"\"\"
        if "id" not in record:
            raise ValueError(f"Record missing 'id': {record}")

        return {
            "id": record["id"],
            "name": record.get("name", "Unknown"),
            "tags": [t.strip() for t in record.get("tags", [])],
            "score": float(record.get("score", 0.0)),
            "metadata": {
                "source": self.config.get("source", "default"),
                "version": self.config.get("version", "1.0"),
            }
        }


def load_config(path: str) -> Optional[Dict]:
    \"\"\"Load JSON configuration from file.\"\"\"
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Config load error: {e}")
        return None


if __name__ == "__main__":
    config = {
        "source": "api_v2",
        "version": "2.1.0",
    }
    processor = DataProcessor(config)
    sample_data = [
        {"id": 1, "name": "Alice Chen", "tags": ["finance", "ops"], "score": 95.5},
        {"id": 2, "name": "Bob Martinez", "tags": ["engineering"], "score": 88.0},
        {"id": 3, "name": "Carol Singh", "tags": ["design", "ux"], "score": 91.3},
    ]
    result = processor.process(sample_data)
    print(json.dumps(result, indent=2))
""")

    # utils.py — utility functions
    utils_py = os.path.join(WORKSPACE_DIR, 'utils.py')
    with open(utils_py, 'w') as f:
        f.write("""\
# Utility functions for DataPipeline project

from datetime import datetime
from typing import Any, Dict, List


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    \"\"\"Flatten a nested dictionary with dotted keys.\"\"\"
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def chunk_list(lst: List[Any], size: int) -> List[List[Any]]:
    \"\"\"Split a list into chunks of given size.\"\"\"
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def format_timestamp(dt: datetime = None) -> str:
    \"\"\"Format datetime as ISO 8601 string.\"\"\"
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
""")

    # config.json — sample config file
    config_json = os.path.join(WORKSPACE_DIR, 'config.json')
    with open(config_json, 'w') as f:
        json.dump({
            "source": "api_v2",
            "version": "2.1.0",
            "batch_size": 50,
            "retry_limit": 3,
            "endpoints": {
                "primary": "https://api.example.com/v2/data",
                "fallback": "https://backup.example.com/v2/data"
            }
        }, f, indent=2)

    print(f"Workspace created at {WORKSPACE_DIR}")
    return WORKSPACE_DIR


def setup_initial():
    # Step 1: Install Bracket Pair Colorizer extension if not already installed
    result = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True,
        text=True,
        env={**os.environ, "DISPLAY": ":0"}
    )
    installed = result.stdout.lower()

    if 'bracket-pair-colorizer' not in installed:
        print("Installing Bracket Pair Colorizer extension...")
        install_extension_cli("CoenraadS.bracket-pair-colorizer-2")
        time.sleep(3)
    else:
        print("Bracket Pair Colorizer extension already installed")

    # Step 2: Ensure extension is ENABLED (not disabled)
    ensure_extension_enabled()

    # Step 3: Create workspace with realistic code files
    create_workspace()

    # Step 4: Launch VSCode with the workspace showing the Extensions panel
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print(f"GUI_READY: VSCode launched with workspace at {WORKSPACE_DIR}, DISPLAY=:0")
    print(f"Bracket Pair Colorizer extension is installed and enabled.")


setup_initial()
