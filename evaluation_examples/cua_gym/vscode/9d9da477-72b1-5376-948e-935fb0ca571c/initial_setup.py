"""
Initial Setup: Create Python CLI tool project for VSCode debugging task
Task ID: vscode_gf2_039
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_039'
PROJECT_DIR = f'{WORKDIR}/projects/cli-tool'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)

    # Create cli.py - a realistic Python CLI tool
    cli_py = '''\
#!/usr/bin/env python3
"""
CLI tool for processing JSON data files.

Reads an input JSON file, applies transformations, and writes results
to an output file. Supports verbose logging for debugging.
"""

import argparse
import json
import logging
import sys
from pathlib import Path


def setup_logging(verbose: bool = False):
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def process_data(input_path: str, output_path: str, verbose: bool = False):
    """Read input JSON, transform data, and write output."""
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    logger.info(f"Reading input from: {input_path}")
    input_file = Path(input_path)
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)

    with open(input_file, "r") as f:
        data = json.load(f)

    logger.debug(f"Loaded {len(data)} records from input file")

    # Apply transformations
    results = []
    for idx, record in enumerate(data):
        logger.debug(f"Processing record {idx + 1}: {record.get('id', 'unknown')}")
        transformed = {
            "id": record.get("id"),
            "name": record.get("name", "").strip().title(),
            "status": "processed",
            "original_fields": list(record.keys()),
        }
        results.append(transformed)

    output_data = {
        "total_records": len(results),
        "source": str(input_file.name),
        "results": results,
    }

    output_file = Path(output_path)
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    logger.info(f"Wrote {len(results)} processed records to: {output_path}")
    return output_data


def main():
    parser = argparse.ArgumentParser(
        description="Process JSON data files with optional verbose output"
    )
    parser.add_argument(
        "--input", required=True, help="Path to the input JSON file"
    )
    parser.add_argument(
        "--output", default="output.json", help="Path for the output JSON file"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose debug logging"
    )

    args = parser.parse_args()
    process_data(args.input, args.output, args.verbose)


if __name__ == "__main__":
    main()
'''
    with open(f'{PROJECT_DIR}/cli.py', 'w') as f:
        f.write(cli_py)
    os.chmod(f'{PROJECT_DIR}/cli.py', 0o755)

    # Create a sample input data file
    sample_data = [
        {"id": "EMP001", "name": "sarah chen", "department": "Engineering", "salary": 95000},
        {"id": "EMP002", "name": "marcus johnson", "department": "Marketing", "salary": 78000},
        {"id": "EMP003", "name": "priya patel", "department": "Finance", "salary": 82000},
        {"id": "EMP004", "name": "james wilson", "department": "Engineering", "salary": 91000},
        {"id": "EMP005", "name": "ana rodriguez", "department": "Sales", "salary": 73000},
    ]
    with open(f'{PROJECT_DIR}/data/sample_input.json', 'w') as f:
        json.dump(sample_data, f, indent=2)

    # Create a basic test file
    test_py = '''\
"""Basic tests for cli.py"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cli import process_data


def test_basic_processing():
    """Test that basic data processing works correctly."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([{"id": "T001", "name": "test user"}], f)
        input_path = f.name

    output_path = tempfile.mktemp(suffix=".json")
    try:
        result = process_data(input_path, output_path)
        assert result["total_records"] == 1
        assert result["results"][0]["name"] == "Test User"
        print("test_basic_processing: PASSED")
    finally:
        os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)


if __name__ == "__main__":
    test_basic_processing()
'''
    with open(f'{PROJECT_DIR}/tests/test_cli.py', 'w') as f:
        f.write(test_py)

    # Create a requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('# No external dependencies required\n')

    # Create a README
    readme = '''\
# CLI Data Processor

A command-line tool for processing JSON data files.

## Usage

```bash
python cli.py --input data/sample_input.json --output output.json --verbose
```

## Arguments

- `--input`: Path to the input JSON file (required)
- `--output`: Path for the output file (default: output.json)
- `--verbose`: Enable detailed debug logging
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # DO NOT create .vscode/ directory or launch.json - that is the task!

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: cli.py, data/sample_input.json, tests/test_cli.py, requirements.txt, README.md')

    # GUI-ready: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
