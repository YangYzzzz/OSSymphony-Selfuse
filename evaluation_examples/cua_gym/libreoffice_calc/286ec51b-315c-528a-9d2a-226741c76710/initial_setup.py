"""
Initial Setup: Create data_pipeline.py with input validation logic inline in run_pipeline()
Task ID: vscode_py_018
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_018'
FILE_PATH = os.path.join(WORKDIR, 'data_pipeline.py')


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


# The Python file content. Lines 25-35 contain input validation logic inside run_pipeline().
# Line numbering (1-indexed):
#  1: import logging
#  2: import sys
#  3: from typing import Any, Dict, List, Optional
#  4: (blank)
#  5: (blank)
#  6: logger = logging.getLogger(__name__)
#  7: (blank)
#  8: (blank)
#  9: class PipelineError(Exception):
# 10:     """Custom exception for pipeline failures."""
# 11:     pass
# 12: (blank)
# 13: (blank)
# 14: def load_config(path: str) -> Dict[str, Any]:
# 15:     ...
# 16:     ...
# 17:     ...
# 18:     ...
# 19:     ...
# 20: (blank)
# 21: (blank)
# 22: def run_pipeline(data: List[Dict], config: Dict[str, Any]) -> List[Dict]:
# 23:     ...
# 24:     ...
# 25-35: input validation logic (11 lines)
# 36+: rest of pipeline

FILE_CONTENT = '''\
import logging
import sys
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class PipelineError(Exception):
    """Custom exception for pipeline failures."""
    pass


def load_config(path: str) -> Dict[str, Any]:
    """Load pipeline configuration from a JSON file."""
    import json
    with open(path, "r") as f:
        config = json.load(f)
    return config


def run_pipeline(data: List[Dict], config: Dict[str, Any]) -> List[Dict]:
    """Execute the data processing pipeline on the input records."""
    results = []
    for record in data:
        if not isinstance(record, dict):
            logger.error("Record is not a dictionary: %s", type(record))
            raise PipelineError(f"Expected dict, got {type(record).__name__}")
        if "id" not in record:
            logger.error("Record missing required field 'id': %s", record)
            raise PipelineError("Missing required field: id")
        if not isinstance(record.get("value"), (int, float)):
            logger.error("Field 'value' has invalid type in record %s", record.get("id"))
            raise PipelineError(f"Invalid type for 'value' in record {record.get('id')}")
        if record["value"] < config.get("min_value", 0):
            logger.warning("Record %s below minimum threshold, skipping", record["id"])
            continue
        if record["value"] > config.get("max_value", 1000000):
            logger.warning("Record %s above maximum threshold, skipping", record["id"])
            continue
        if record.get("status") is None:
            logger.warning("Record %s has null status, defaulting to 'pending'", record["id"])
            record["status"] = "pending"

        # Transform phase
        transformed = _transform_record(record, config)
        results.append(transformed)

    logger.info("Pipeline complete: %d/%d records processed", len(results), len(data))
    return results


def _transform_record(record: Dict, config: Dict[str, Any]) -> Dict:
    """Apply transformations to a single record."""
    output = dict(record)
    scale_factor = config.get("scale_factor", 1.0)
    output["value"] = round(record["value"] * scale_factor, 4)
    output["processed"] = True
    if config.get("add_timestamp", False):
        from datetime import datetime
        output["timestamp"] = datetime.utcnow().isoformat()
    return output


def save_results(results: List[Dict], output_path: str) -> None:
    """Write processed results to a JSON file."""
    import json
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    logger.info("Results saved to %s", output_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = load_config("pipeline_config.json")

    import json
    with open("input_data.json", "r") as f:
        data = json.load(f)

    results = run_pipeline(data, config)
    save_results(results, "output_data.json")
'''


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)
    with open(FILE_PATH, 'w') as f:
        f.write(FILE_CONTENT)

    print(f'Created {FILE_PATH}')

    # Verify line count and that lines 25-35 contain validation logic
    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()
    print(f'Total lines: {len(lines)}')
    print(f'Line 25: {lines[24].rstrip()}')
    print(f'Line 35: {lines[34].rstrip()}')

    # Launch VSCode with the file open
    launch_gui(f'code "{FILE_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
