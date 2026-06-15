"""
Initial Setup: Configure VSCode Outline view settings
Task ID: vscode_rf_014
Domain: vscode

Creates ~/projects/analytics/data_engine.py with 4 classes, 15 methods,
8 standalone functions, and 20+ module-level variables/constants.
Configures VSCode with Outline sorted alphabetically, all symbol types visible,
Follow Cursor disabled. Opens VSCode with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
WORKDIR = HOME
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
PROJECT_DIR = os.path.join(HOME, "projects", "analytics")
DATA_ENGINE = os.path.join(PROJECT_DIR, "data_engine.py")


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
            import re
            content = f.read()
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


DATA_ENGINE_CONTENT = '''\
"""
Data Engine Module - Analytics Pipeline
========================================
Core data processing engine for the analytics platform.
Handles data ingestion, transformation, aggregation, and export.
"""

import os
import csv
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict

# ============================================================
# Module-level constants and configuration variables
# ============================================================

VERSION = "3.2.1"
BUILD_DATE = "2025-11-15"
ENGINE_NAME = "DataEngine Pro"
MAX_BATCH_SIZE = 10000
DEFAULT_TIMEOUT = 30
CACHE_TTL_SECONDS = 3600
LOG_LEVEL = logging.INFO
DATA_FORMAT_VERSION = 2
SUPPORTED_FORMATS = ["csv", "json", "parquet", "xlsx"]
DEFAULT_ENCODING = "utf-8"
RETRY_ATTEMPTS = 3
COMPRESSION_THRESHOLD = 1048576
NULL_PLACEHOLDER = "<NULL>"
DATE_FORMAT = "%Y-%m-%d"
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
METRIC_PRECISION = 4
PARTITION_KEY = "region"
INDEX_REBUILD_INTERVAL = 86400
QUERY_CACHE_SIZE = 256
ENABLE_PROFILING = False
DEBUG_MODE = False

logger = logging.getLogger(__name__)


# ============================================================
# Standalone functions
# ============================================================

def compute_checksum(data: bytes) -> str:
    """Compute SHA-256 checksum for data integrity verification."""
    return hashlib.sha256(data).hexdigest()


def parse_timestamp(ts_string: str) -> datetime:
    """Parse an ISO-format timestamp string into a datetime object."""
    try:
        return datetime.fromisoformat(ts_string)
    except ValueError:
        return datetime.strptime(ts_string, TIMESTAMP_FORMAT)


def normalize_column_name(name: str) -> str:
    """Normalize column names: lowercase, replace spaces with underscores."""
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def validate_schema(record: dict, schema: dict) -> bool:
    """Validate a data record against the expected schema definition."""
    for field, expected_type in schema.items():
        if field not in record:
            return False
        if not isinstance(record[field], expected_type):
            return False
    return True


def flatten_nested_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flatten a nested dictionary into a single-level dict with dotted keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def merge_records(base: dict, overlay: dict) -> dict:
    """Deep-merge two record dictionaries, overlay takes precedence."""
    result = base.copy()
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_records(result[key], value)
        else:
            result[key] = value
    return result


def calculate_percentile(values: List[float], percentile: float) -> float:
    """Calculate the given percentile from a sorted list of values."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = (len(sorted_vals) - 1) * (percentile / 100.0)
    lower = int(idx)
    upper = lower + 1
    if upper >= len(sorted_vals):
        return sorted_vals[lower]
    weight = idx - lower
    return sorted_vals[lower] * (1 - weight) + sorted_vals[upper] * weight


def format_file_size(size_bytes: int) -> str:
    """Convert byte count to human-readable file size string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


# ============================================================
# Class definitions
# ============================================================

class DataSource:
    """Represents a configurable data source connection."""

    def __init__(self, name: str, source_type: str, connection_string: str):
        self.name = name
        self.source_type = source_type
        self.connection_string = connection_string
        self.is_connected = False
        self.last_accessed = None
        self.record_count = 0

    def connect(self) -> bool:
        """Establish connection to the data source."""
        logger.info(f"Connecting to {self.name} ({self.source_type})")
        self.is_connected = True
        self.last_accessed = datetime.now()
        return True

    def disconnect(self):
        """Close the data source connection gracefully."""
        logger.info(f"Disconnecting from {self.name}")
        self.is_connected = False

    def fetch_records(self, limit: int = MAX_BATCH_SIZE) -> List[dict]:
        """Fetch records from the data source up to the specified limit."""
        if not self.is_connected:
            raise ConnectionError(f"Not connected to {self.name}")
        self.last_accessed = datetime.now()
        return []

    def get_metadata(self) -> dict:
        """Return metadata about the data source configuration."""
        return {
            "name": self.name,
            "type": self.source_type,
            "connected": self.is_connected,
            "record_count": self.record_count,
        }


class TransformPipeline:
    """Manages a sequence of data transformation steps."""

    def __init__(self, pipeline_id: str):
        self.pipeline_id = pipeline_id
        self.steps = []
        self.execution_log = []
        self.is_running = False
        self.total_processed = 0

    def add_step(self, step_name: str, transform_func, config: dict = None):
        """Add a named transformation step to the pipeline."""
        self.steps.append({
            "name": step_name,
            "func": transform_func,
            "config": config or {},
        })

    def remove_step(self, step_name: str) -> bool:
        """Remove a transformation step by name."""
        original_count = len(self.steps)
        self.steps = [s for s in self.steps if s["name"] != step_name]
        return len(self.steps) < original_count

    def execute(self, data: List[dict]) -> List[dict]:
        """Run all pipeline steps sequentially on the input data."""
        self.is_running = True
        result = data
        for step in self.steps:
            start_time = datetime.now()
            result = step["func"](result, **step["config"])
            elapsed = (datetime.now() - start_time).total_seconds()
            self.execution_log.append({
                "step": step["name"],
                "records": len(result),
                "elapsed_seconds": elapsed,
            })
        self.total_processed += len(data)
        self.is_running = False
        return result

    def get_execution_summary(self) -> dict:
        """Return a summary of the last pipeline execution."""
        return {
            "pipeline_id": self.pipeline_id,
            "steps_count": len(self.steps),
            "total_processed": self.total_processed,
            "log": self.execution_log[-len(self.steps):] if self.execution_log else [],
        }


class AggregationEngine:
    """Performs statistical aggregation and grouping operations on datasets."""

    def __init__(self):
        self.cache = {}
        self.aggregation_functions = {
            "sum": sum,
            "count": len,
            "mean": lambda vals: sum(vals) / len(vals) if vals else 0,
            "min": min,
            "max": max,
        }

    def group_by(self, records: List[dict], key: str) -> Dict[str, List[dict]]:
        """Group records by the specified key field."""
        groups = defaultdict(list)
        for record in records:
            group_key = record.get(key, NULL_PLACEHOLDER)
            groups[str(group_key)].append(record)
        return dict(groups)

    def aggregate(self, records: List[dict], field: str, func_name: str) -> float:
        """Apply an aggregation function to a specific field across records."""
        if func_name not in self.aggregation_functions:
            raise ValueError(f"Unknown aggregation: {func_name}")
        values = [r[field] for r in records if field in r and isinstance(r[field], (int, float))]
        return round(self.aggregation_functions[func_name](values), METRIC_PRECISION)

    def pivot_table(self, records: List[dict], row_key: str, col_key: str, value_key: str) -> dict:
        """Create a pivot table from the dataset."""
        pivot = {}
        for record in records:
            row = str(record.get(row_key, ""))
            col = str(record.get(col_key, ""))
            val = record.get(value_key, 0)
            if row not in pivot:
                pivot[row] = {}
            pivot[row][col] = pivot[row].get(col, 0) + val
        return pivot

    def running_average(self, records: List[dict], field: str, window: int = 5) -> List[float]:
        """Calculate a running average over the specified field with given window size."""
        values = [r.get(field, 0) for r in records]
        result = []
        for i in range(len(values)):
            window_vals = values[max(0, i - window + 1):i + 1]
            result.append(round(sum(window_vals) / len(window_vals), METRIC_PRECISION))
        return result


class ExportManager:
    """Handles exporting processed data to various output formats."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.export_history = []
        os.makedirs(output_dir, exist_ok=True)

    def export_csv(self, records: List[dict], filename: str) -> str:
        """Export records to a CSV file and return the output path."""
        output_path = os.path.join(self.output_dir, filename)
        if not records:
            return output_path
        fieldnames = list(records[0].keys())
        with open(output_path, "w", newline="", encoding=DEFAULT_ENCODING) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        self._log_export(output_path, "csv", len(records))
        return output_path

    def export_json(self, records: List[dict], filename: str, indent: int = 2) -> str:
        """Export records to a JSON file with optional indentation."""
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, "w", encoding=DEFAULT_ENCODING) as f:
            json.dump(records, f, indent=indent, default=str)
        self._log_export(output_path, "json", len(records))
        return output_path

    def get_export_history(self) -> List[dict]:
        """Return the history of all export operations."""
        return self.export_history.copy()

    def _log_export(self, path: str, fmt: str, count: int):
        """Record an export operation in the history log."""
        self.export_history.append({
            "path": path,
            "format": fmt,
            "record_count": count,
            "timestamp": datetime.now().isoformat(),
        })
'''


def create_initial():
    # 1. Create project directory and data_engine.py
    os.makedirs(PROJECT_DIR, exist_ok=True)
    with open(DATA_ENGINE, "w") as f:
        f.write(DATA_ENGINE_CONTENT)
    print(f"Created: {DATA_ENGINE}")

    # 2. Configure VSCode settings for initial state:
    #    - Outline sorted alphabetically
    #    - All symbol types visible (variables, constants shown)
    #    - Follow Cursor disabled
    update_settings({
        "outline.sortOrder": "type",
        "outline.showVariables": True,
        "outline.showConstants": True,
        "outline.showClasses": True,
        "outline.showFunctions": True,
        "outline.showMethods": True,
        "breadcrumbs.followCursor": False,
        "outline.followCursor": False,
    })
    print(f"Updated VSCode settings: {SETTINGS_PATH}")

    # 3. Launch VSCode with the project folder and open data_engine.py
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code --reuse-window "{DATA_ENGINE}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
