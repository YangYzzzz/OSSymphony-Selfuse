"""
Initial Setup: Configure Python import sorting using isort in VSCode
Task ID: vscode_lp_024
Domain: vs_code

Creates a Python project with unorganized imports and basic VSCode settings
(without any isort/organizeImports configuration). Opens VSCode with the project.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
WORKSPACE = os.path.join(HOME, "workspace")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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
    """Create a Python project with unorganized imports."""
    os.makedirs(WORKSPACE, exist_ok=True)

    # Main application file with mixed/unorganized imports
    main_py = """\
import json
import requests
from pathlib import Path
import os
from datetime import datetime, timedelta
import sys
from collections import OrderedDict
import numpy as np
from typing import List, Dict, Optional
import re
from .utils import parse_config, validate_input
import csv
from urllib.parse import urlparse
import hashlib
from dataclasses import dataclass, field
import pandas as pd
from .models import User, Product, Order


@dataclass
class AppConfig:
    name: str
    version: str = "1.0.0"
    debug: bool = False
    max_retries: int = 3
    base_url: str = "https://api.example.com"
    timeout: float = 30.0
    allowed_origins: List[str] = field(default_factory=list)


class DataProcessor:
    def __init__(self, config: AppConfig):
        self.config = config
        self.session = requests.Session()
        self.cache: Dict[str, any] = OrderedDict()
        self.logger = self._setup_logger()

    def _setup_logger(self):
        import logging
        logger = logging.getLogger(self.config.name)
        logger.setLevel(logging.DEBUG if self.config.debug else logging.INFO)
        return logger

    def fetch_data(self, endpoint: str) -> Optional[Dict]:
        url = urlparse(f"{self.config.base_url}/{endpoint}")
        try:
            response = self.session.get(url.geturl(), timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {endpoint}: {e}")
            return None

    def process_csv(self, file_path: Path) -> pd.DataFrame:
        if not file_path.exists():
            raise FileNotFoundError(f"CSV not found: {file_path}")
        df = pd.read_csv(file_path)
        df['processed_at'] = datetime.now().isoformat()
        df['checksum'] = df.apply(
            lambda row: hashlib.md5(str(row.values).encode()).hexdigest(), axis=1
        )
        return df

    def export_results(self, data: List[Dict], output_path: Path):
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        self.logger.info(f"Exported {len(data)} records to {output_path}")


def main():
    config = AppConfig(
        name="data-processor",
        debug=True,
        allowed_origins=["https://app.example.com"]
    )
    processor = DataProcessor(config)
    pattern = re.compile(r'^[A-Z]{2,4}-\\d{4,6}$')
    print(f"Processor initialized: {config.name} v{config.version}")
    print(f"Python {sys.version}")
    print(f"Working directory: {os.getcwd()}")


if __name__ == "__main__":
    main()
"""

    # Utils module with unorganized imports
    utils_py = """\
import re
from typing import Any, Dict
import yaml
import os
from pathlib import Path
import json
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def parse_config(config_path: str) -> Dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, 'r') as f:
        if path.suffix == '.json':
            return json.load(f)
        elif path.suffix in ('.yml', '.yaml'):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")


def validate_input(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
    for key, expected_type in schema.items():
        if key not in data:
            logger.warning(f"Missing required field: {key}")
            return False
        if not isinstance(data[key], expected_type):
            logger.warning(
                f"Field '{key}' expected {expected_type.__name__}, "
                f"got {type(data[key]).__name__}"
            )
            return False
    return True


def sanitize_filename(name: str) -> str:
    sanitized = re.sub(r'[^\\w\\s-]', '', name)
    sanitized = re.sub(r'[\\s]+', '_', sanitized)
    return sanitized.strip('_').lower()


def get_timestamp() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def ensure_directory(path: str) -> Path:
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path
"""

    # Models module with unorganized imports
    models_py = """\
from dataclasses import dataclass, field
import json
from typing import List, Optional
from datetime import datetime
import uuid
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class User:
    username: str
    email: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "is_active": self.is_active,
        }


@dataclass
class Product:
    name: str
    price: float
    sku: str
    category: str
    stock: int = 0
    description: Optional[str] = None

    def is_available(self) -> bool:
        return self.stock > 0


@dataclass
class Order:
    user_id: str
    products: List[Product]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: OrderStatus = OrderStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def total(self) -> float:
        return sum(p.price for p in self.products)

    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status.value,
            "total": self.total,
            "created_at": self.created_at,
        })
"""

    # Create __init__.py
    init_py = """\
from .utils import parse_config, validate_input, sanitize_filename
from .models import User, Product, Order, OrderStatus
"""

    # Write all files
    files = {
        os.path.join(WORKSPACE, "main.py"): main_py,
        os.path.join(WORKSPACE, "utils.py"): utils_py,
        os.path.join(WORKSPACE, "models.py"): models_py,
        os.path.join(WORKSPACE, "__init__.py"): init_py,
    }

    for path, content in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        print(f"Created: {path}")


def setup_vscode_settings():
    """Create basic VSCode settings WITHOUT any isort/organizeImports config."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Add basic Python/editor settings but NO organizeImports
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "editor.renderWhitespace": "selection",
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark+",
        "python.analysis.typeCheckingMode": "basic",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    # Make sure there is NO [python] codeActionsOnSave config
    if "[python]" in settings:
        if "editor.codeActionsOnSave" in settings["[python]"]:
            del settings["[python]"]["editor.codeActionsOnSave"]
            if not settings["[python]"]:
                del settings["[python]"]

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"VSCode settings created: {SETTINGS_PATH}")


def install_isort():
    """Ensure isort is installed in the environment."""
    try:
        subprocess.run(
            ["pip3", "install", "isort"],
            capture_output=True, text=True, timeout=60
        )
        print("isort installed successfully")
    except Exception as e:
        print(f"Warning: could not install isort: {e}")


def main():
    print("=== vscode_lp_024: Initial Setup ===")

    # 1. Create Python project files
    create_project()

    # 2. Set up VSCode settings (without organizeImports)
    setup_vscode_settings()

    # 3. Install isort
    install_isort()

    # 4. Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")

    print("=== Initial setup complete ===")


main()
