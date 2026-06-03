"""
Initial Setup: Open VSCode with ~/project folder containing README.md
Task ID: vscode_wf_004
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_004'
PROJECT_DIR = f'{WORKDIR}/project'
README_PATH = f'{PROJECT_DIR}/README.md'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create README.md with realistic markdown content
    readme_content = """# DataSync Pipeline

A high-performance data synchronization framework for distributed systems.

## Overview

DataSync Pipeline provides a robust solution for real-time data replication
across heterogeneous database environments. It supports both streaming and
batch modes with configurable consistency guarantees.

## Features

- **Real-time streaming** — Sub-second latency for change data capture
- **Schema evolution** — Automatic handling of upstream schema changes
- **Multi-target fanout** — Replicate to multiple downstream systems simultaneously
- **Conflict resolution** — Configurable last-writer-wins or custom merge strategies
- **Monitoring dashboard** — Built-in Prometheus metrics and Grafana templates

## Quick Start

Install the package from PyPI:

```bash
pip install datasync-pipeline
datasync init --config pipeline.yaml
datasync start --source postgres --target elasticsearch
```

## Configuration

The pipeline is configured via a YAML file. Key sections include:

- **source** — Connection details for the upstream database
- **targets** — List of downstream systems to replicate to
- **filters** — Optional row/column filtering rules
- **scheduling** — Cron expressions for batch sync windows

## Architecture

The system is built on three core components:

1. **Extractor** — Reads change events from the source database WAL
2. **Transformer** — Applies schema mappings and data transformations
3. **Loader** — Writes processed events to each configured target

## Contributing

Please read `CONTRIBUTING.md` before submitting pull requests. All changes
must include unit tests and pass the integration test suite.

## License

MIT License. See `LICENSE` for details.
"""
    with open(README_PATH, 'w') as f:
        f.write(readme_content)

    print(f'Initial file created: {README_PATH}')

    # Ensure xdotool is available for future use
    subprocess.run('echo "password" | sudo -S apt-get install -y -qq xdotool 2>/dev/null',
                    shell=True, capture_output=True)

    # Kill any existing VSCode instances for clean state
    subprocess.run(['pkill', '-f', 'code'], capture_output=True)
    time.sleep(1)

    # Open VSCode with the project folder (not the file itself)
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder on DISPLAY=:0')


create_initial()
