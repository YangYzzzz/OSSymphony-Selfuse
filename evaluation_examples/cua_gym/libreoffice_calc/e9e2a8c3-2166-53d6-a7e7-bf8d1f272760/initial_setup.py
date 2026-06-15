"""
Initial Setup: Configure Markdownlint extension in VSCode
Task ID: vscode_we_094
Domain: vscode (settings configuration)

Creates a documentation project with markdown files, installs the
DavidAnson.vscode-markdownlint extension, and opens VSCode with the project.
User settings remain at defaults (no markdownlint.config).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_094'
PROJECT_DIR = f'{WORKDIR}/docs-project'
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


def create_documentation_project():
    """Create a realistic documentation project with markdown files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'guides'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'api'), exist_ok=True)

    # README.md - main project documentation
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# DataFlow Analytics Platform

A comprehensive analytics platform for real-time data processing and visualization.

## Overview

DataFlow Analytics provides enterprise-grade tools for ingesting, transforming, and visualizing streaming data from multiple sources. Built with scalability in mind, it supports horizontal scaling across distributed clusters.

## Features

- **Real-time Processing**: Sub-second latency for streaming data pipelines
- **Custom Dashboards**: Drag-and-drop dashboard builder with 50+ widget types
- **Alert System**: Configurable thresholds with multi-channel notifications
- **API Integration**: RESTful API with OAuth 2.0 authentication
- **Data Connectors**: Pre-built connectors for PostgreSQL, MongoDB, Kafka, and S3

## Quick Start

```bash
pip install dataflow-analytics
dataflow init my-project
dataflow serve --port 8080
```

## Architecture

The platform consists of three core services:

1. **Ingestion Service** - Handles incoming data streams
2. **Processing Engine** - Applies transformations and aggregations
3. **Visualization Layer** - Renders dashboards and reports

<div class="note">
  <p>For production deployments, we recommend using Docker Compose.</p>
</div>

## License

MIT License - see LICENSE file for details.
""")

    # guides/getting-started.md
    with open(os.path.join(PROJECT_DIR, 'guides', 'getting-started.md'), 'w') as f:
        f.write("""# Getting Started with DataFlow

This guide walks you through setting up DataFlow Analytics from scratch. Follow these steps to have a working analytics pipeline within 30 minutes.

## Prerequisites

Before you begin, ensure you have the following installed on your system. Each dependency is critical for different parts of the platform, so do not skip any of them even if they seem optional at first glance.

- Python 3.9 or higher
- Docker Desktop 4.0+
- Node.js 18 LTS (for dashboard components)
- PostgreSQL 14+ (or use the bundled Docker container)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/dataflow/analytics-platform.git
cd analytics-platform
```

### Step 2: Configure Environment

Copy the example configuration and update with your database credentials:

```bash
cp .env.example .env
nano .env
```

### Step 3: Start Services

Launch all services using Docker Compose:

```bash
docker-compose up -d
```

<details>
<summary>Troubleshooting common startup issues</summary>

If the ingestion service fails to start, check that port 9092 is available for Kafka.
</details>

## Next Steps

- Read the [API Reference](../api/reference.md) for endpoint documentation
- Configure [Alert Rules](./alerts.md) for monitoring
- Set up [Data Connectors](./connectors.md) for your data sources
""")

    # api/reference.md
    with open(os.path.join(PROJECT_DIR, 'api', 'reference.md'), 'w') as f:
        f.write("""# API Reference

## Authentication

All API requests require a valid OAuth 2.0 bearer token. Obtain one by calling the token endpoint with your client credentials.

## Endpoints

### GET /api/v1/dashboards

Returns a list of all dashboards accessible to the authenticated user.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number for pagination |
| limit | integer | No | Results per page (default: 20, max: 100) |
| sort_by | string | No | Field to sort by (created_at, updated_at, name) |

**Response:**

```json
{
  "data": [
    {
      "id": "dash_a1b2c3",
      "name": "Sales Overview Q4",
      "created_at": "2025-01-15T10:30:00Z",
      "widget_count": 12
    }
  ],
  "pagination": {
    "total": 45,
    "page": 1,
    "limit": 20
  }
}
```

### POST /api/v1/pipelines

Create a new data processing pipeline.

### DELETE /api/v1/pipelines/{id}

Remove a pipeline and all associated transformations.
""")

    # CONTRIBUTING.md
    with open(os.path.join(PROJECT_DIR, 'CONTRIBUTING.md'), 'w') as f:
        f.write("""# Contributing to DataFlow

We welcome contributions from the community! Please read this guide before submitting pull requests.

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a feature branch from `main`
4. Make your changes with appropriate tests
5. Submit a pull request

## Code Style

- Follow PEP 8 for Python code
- Use ESLint with our configuration for JavaScript
- Write docstrings for all public functions
- Keep line lengths reasonable for readability

## Commit Messages

Use conventional commits format:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions or modifications
""")

    print(f'Documentation project created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Ensure VSCode settings exist but do NOT include markdownlint config."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings (preserve trust settings)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    # Ensure trust settings remain
    settings.setdefault("security.workspace.trust.enabled", False)
    settings.setdefault("security.workspace.trust.startupPrompt", "never")
    settings.setdefault("security.workspace.trust.emptyWindow", False)

    # Explicitly remove any markdownlint config if it somehow exists
    settings.pop("markdownlint.config", None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings ready (no markdownlint config): {SETTINGS_PATH}')


def install_markdownlint():
    """Install the markdownlint extension."""
    result = subprocess.run(
        ['code', '--install-extension', 'DavidAnson.vscode-markdownlint', '--force'],
        capture_output=True, text=True, timeout=120
    )
    print(f'Extension install stdout: {result.stdout.strip()}')
    if result.returncode != 0:
        print(f'Extension install stderr: {result.stderr.strip()}')
    # Verify installation
    result2 = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True, timeout=30
    )
    extensions = result2.stdout.strip().split('\n')
    for ext in extensions:
        if 'markdownlint' in ext.lower():
            print(f'Confirmed extension installed: {ext}')
            break
    else:
        print('WARNING: markdownlint extension not found in list after install')


def main():
    # Step 1: Create the documentation project
    create_documentation_project()

    # Step 2: Setup VSCode settings (without markdownlint config)
    setup_vscode_settings()

    # Step 3: Install markdownlint extension
    install_markdownlint()

    # Step 4: Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with docs-project and DISPLAY=:0')


main()
