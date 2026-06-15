"""
Initial Setup: Open VSCode with README.md showing raw markdown text
Task ID: vscode_stu_016
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_016'
OUTPUT = f'{WORKDIR}/README.md'


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
    readme_content = """# DataFlow Pipeline

A high-performance data processing pipeline for real-time analytics.

## Features

- **Stream Processing**: Handle millions of events per second with low latency
- **Fault Tolerance**: Automatic checkpointing and recovery from failures
- **Pluggable Connectors**: Built-in support for Kafka, Redis, PostgreSQL, and S3
- **Monitoring Dashboard**: Real-time metrics and alerting via Grafana integration

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- At least 8GB RAM recommended

### Installation

```bash
git clone https://github.com/acme-corp/dataflow-pipeline.git
cd dataflow-pipeline
pip install -r requirements.txt
```

### Running Locally

```bash
docker-compose up -d          # Start dependencies
python -m dataflow.main       # Launch the pipeline
```

## Configuration

All configuration is managed through `config.yaml`:

| Parameter       | Default   | Description                        |
|-----------------|-----------|-------------------------------------|
| `batch_size`    | 1000      | Number of events per micro-batch   |
| `checkpoint_interval` | 30s | How often state is checkpointed    |
| `max_retries`   | 3         | Retry count for failed tasks       |
| `log_level`     | INFO      | Logging verbosity                  |

## Architecture

The pipeline consists of three main stages:

1. **Ingestion Layer** — Reads from source connectors and buffers events
2. **Transform Engine** — Applies user-defined transformations using a DAG scheduler
3. **Sink Writers** — Writes processed results to destination systems

## API Reference

### `Pipeline.run(source, sink, transforms)`

Starts the pipeline with the given configuration.

**Parameters:**
- `source` (Connector): Input data source
- `sink` (Connector): Output destination
- `transforms` (list[Callable]): Ordered list of transformation functions

**Returns:** `PipelineResult` with execution statistics

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Maintained by the Acme Corp Engineering Team — Last updated March 2026*
"""

    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(readme_content)
    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the README.md file (raw markdown only, no preview)
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with README.md in editor')


create_initial()
