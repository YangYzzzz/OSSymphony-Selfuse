"""
Initial Setup: Configure VSCode with a Python project, no custom snippets.
Task ID: vscode_prod_037
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_037'
PROJECTS_DIR = os.path.join(WORKDIR, 'projects', 'scripts')
ERROR_HANDLER = os.path.join(PROJECTS_DIR, 'error_handler.py')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
PYTHON_SNIPPETS = os.path.join(SNIPPETS_DIR, 'python.json')


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
    # Create project directory structure
    os.makedirs(PROJECTS_DIR, exist_ok=True)

    # Create a realistic error_handler.py file
    error_handler_content = '''"""
Error handling utilities for the data processing pipeline.

This module provides centralized error handling, logging, and retry
mechanisms for various pipeline stages including data ingestion,
transformation, and export.
"""

import logging
import traceback
from datetime import datetime
from typing import Optional, Callable, Any

logger = logging.getLogger(__name__)


class PipelineError(Exception):
    """Base exception for pipeline-related errors."""
    def __init__(self, message: str, stage: str = "unknown", severity: str = "error"):
        super().__init__(message)
        self.stage = stage
        self.severity = severity
        self.timestamp = datetime.now()


class DataIngestionError(PipelineError):
    """Raised when data ingestion from source fails."""
    def __init__(self, message: str, source: str = ""):
        super().__init__(message, stage="ingestion")
        self.source = source


class TransformationError(PipelineError):
    """Raised when data transformation step fails."""
    def __init__(self, message: str, transform_name: str = ""):
        super().__init__(message, stage="transformation")
        self.transform_name = transform_name


class ExportError(PipelineError):
    """Raised when exporting results fails."""
    def __init__(self, message: str, destination: str = ""):
        super().__init__(message, stage="export")
        self.destination = destination


def log_error(error: Exception, context: Optional[dict] = None) -> None:
    """Log an error with optional context information."""
    error_info = {
        "type": type(error).__name__,
        "message": str(error),
        "traceback": traceback.format_exc(),
        "timestamp": datetime.now().isoformat(),
    }
    if context:
        error_info["context"] = context
    if isinstance(error, PipelineError):
        error_info["stage"] = error.stage
        error_info["severity"] = error.severity
    logger.error(f"Pipeline error: {error_info}")


def retry_operation(
    func: Callable,
    max_retries: int = 3,
    delay_seconds: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Any:
    """Retry a function call with exponential backoff.

    Args:
        func: The callable to retry.
        max_retries: Maximum number of retry attempts.
        delay_seconds: Initial delay between retries in seconds.
        backoff_factor: Multiplier for delay after each retry.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        The return value of the successful function call.

    Raises:
        The last exception if all retries are exhausted.
    """
    last_exception = None
    current_delay = delay_seconds

    for attempt in range(max_retries + 1):
        try:
            result = func()
            if attempt > 0:
                logger.info(f"Operation succeeded on attempt {attempt + 1}")
            return result
        except exceptions as e:
            last_exception = e
            log_error(e, context={"attempt": attempt + 1, "max_retries": max_retries})
            if attempt < max_retries:
                import time
                logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {current_delay:.1f}s..."
                )
                time.sleep(current_delay)
                current_delay *= backoff_factor

    raise last_exception


def handle_pipeline_stage(stage_name: str):
    """Decorator for pipeline stage functions with automatic error handling."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"Starting pipeline stage: {stage_name}")
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.info(f"Stage '{stage_name}' completed in {elapsed:.2f}s")
                return result
            except PipelineError:
                raise
            except Exception as e:
                raise PipelineError(
                    f"Unexpected error in stage '{stage_name}': {e}",
                    stage=stage_name,
                )
        return wrapper
    return decorator


# --- Pipeline stages using the decorator ---

@handle_pipeline_stage("data_ingestion")
def ingest_data(source_path: str) -> dict:
    """Read and validate raw data from source."""
    import csv
    records = []
    with open(source_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))
    if not records:
        raise DataIngestionError("No records found", source=source_path)
    return {"records": records, "count": len(records)}


@handle_pipeline_stage("validation")
def validate_data(data: dict) -> dict:
    """Validate ingested data for completeness and correctness."""
    records = data.get("records", [])
    valid_records = []
    invalid_count = 0
    for record in records:
        if all(v is not None and v != '' for v in record.values()):
            valid_records.append(record)
        else:
            invalid_count += 1
            logger.warning(f"Skipping invalid record: {record}")
    return {
        "records": valid_records,
        "valid_count": len(valid_records),
        "invalid_count": invalid_count,
    }


@handle_pipeline_stage("export")
def export_results(data: dict, output_path: str) -> str:
    """Export processed data to output file."""
    import csv
    records = data.get("records", [])
    if not records:
        raise ExportError("No records to export", destination=output_path)
    fieldnames = list(records[0].keys())
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    return output_path
'''

    with open(ERROR_HANDLER, 'w') as f:
        f.write(error_handler_content)
    print(f'Created: {ERROR_HANDLER}')

    # Create a few supporting files to make the project look realistic
    utils_file = os.path.join(PROJECTS_DIR, 'config.py')
    with open(utils_file, 'w') as f:
        f.write('''"""Configuration settings for the data pipeline."""

# Source and destination paths
DATA_SOURCE = "/data/incoming/daily_feed.csv"
EXPORT_PATH = "/data/processed/output.csv"
LOG_DIR = "/var/log/pipeline"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2.0
BACKOFF_FACTOR = 2.0

# Validation rules
REQUIRED_FIELDS = ["id", "name", "value", "timestamp"]
MAX_RECORD_AGE_DAYS = 30
''')
    print(f'Created: {utils_file}')

    main_file = os.path.join(PROJECTS_DIR, 'run_pipeline.py')
    with open(main_file, 'w') as f:
        f.write('''"""Main entry point for the data processing pipeline."""

import sys
import logging
from error_handler import (
    ingest_data, validate_data, export_results,
    PipelineError, retry_operation
)
from config import DATA_SOURCE, EXPORT_PATH, MAX_RETRIES, RETRY_DELAY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Pipeline started")
    try:
        raw_data = retry_operation(
            lambda: ingest_data(DATA_SOURCE),
            max_retries=MAX_RETRIES,
            delay_seconds=RETRY_DELAY,
        )
        validated = validate_data(raw_data)
        logger.info(
            f"Validation: {validated[\'valid_count\']} valid, "
            f"{validated[\'invalid_count\']} invalid"
        )
        output = export_results(validated, EXPORT_PATH)
        logger.info(f"Pipeline complete. Output: {output}")
    except PipelineError as e:
        logger.critical(f"Pipeline failed at stage \'{e.stage}\': {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected pipeline failure: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
''')
    print(f'Created: {main_file}')

    # Ensure NO custom Python snippets exist
    if os.path.exists(PYTHON_SNIPPETS):
        os.remove(PYTHON_SNIPPETS)
        print(f'Removed existing python snippets: {PYTHON_SNIPPETS}')

    # GUI-ready startup: open VSCode with the project folder and error_handler.py
    launch_gui(f'code "{PROJECTS_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{ERROR_HANDLER}"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
