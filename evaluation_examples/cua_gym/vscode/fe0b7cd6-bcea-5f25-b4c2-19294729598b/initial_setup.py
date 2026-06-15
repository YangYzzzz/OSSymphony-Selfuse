"""
Initial Setup: Configure Markdown linting in VSCode
Task ID: vscode_gf5_043
Domain: vscode

Creates ~/projects/documentation/README.md with 4 markdownlint violations:
- MD013: line length > 80 chars
- MD041: first line is not an H1 heading
- MD022: missing blank line before heading
- MD032: missing blank line before list
Opens VSCode with the documentation folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_043'
PROJECT_DIR = f'{WORKDIR}/projects/documentation'
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

    # Build README.md with exactly 4 markdownlint violations:
    # MD041: First line is NOT an H1 (it's a paragraph)
    # MD013: Line exceeding 80 characters
    # MD022: No blank line before heading (## section directly after paragraph)
    # MD032: No blank line before list (list directly after paragraph)
    #
    # The file must be realistic technical documentation content.

    # MD041: First line is not H1 (it's a plain paragraph) — triggers MD041
    # MD013: First line is >80 chars — triggers MD013
    # MD022: "## Architecture Overview" has no blank line before it — triggers MD022
    # MD032: List items after "The required dependencies are:" have no blank line — triggers MD032
    #
    # All other headings and lists have proper blank lines so no extra violations.
    readme_content = """\
Welcome to the Documentation Portal for the Cloud Infrastructure Management Platform - this is the central resource hub for all team members.
## Architecture Overview

The platform is built on a microservices architecture deployed across
multiple availability zones for high availability and fault tolerance.
Each service communicates through an asynchronous message queue backed
by RabbitMQ, with Redis caching layers for frequently accessed data.

The core services include:

- **API Gateway** - Routes external requests to internal services
- **Auth Service** - Handles OAuth2 and SAML authentication flows
- **Config Manager** - Manages environment-specific configurations
- **Deployment Engine** - Orchestrates blue-green deployments

## Getting Started

To set up your local development environment, you will need Docker,
kubectl, and our internal CLI tool installed. Follow the steps below.

The required dependencies are:
- Docker Desktop 4.25 or later
- kubectl v1.28+
- Node.js 20 LTS
- Python 3.11+

### Prerequisites

Make sure you have access to our internal package registry. Contact
DevOps if you need credentials.

## Troubleshooting

If you encounter connection timeouts during local development, check
that your VPN is active and the proxy settings are configured correctly.
"""

    with open(README_PATH, 'w') as f:
        f.write(readme_content)

    print(f'Initial file created: {README_PATH}')

    # Ensure markdownlint extension is NOT installed
    try:
        subprocess.run(
            ['code', '--uninstall-extension', 'DavidAnson.vscode-markdownlint'],
            capture_output=True, timeout=30
        )
    except Exception:
        pass

    # Open VSCode with the documentation folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
