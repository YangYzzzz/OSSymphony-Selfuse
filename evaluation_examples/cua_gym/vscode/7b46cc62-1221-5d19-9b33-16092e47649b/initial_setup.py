"""
Initial Setup: Create a Python daemon-service project with no launch.json
Task ID: vscode_td_067
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_067'
PROJECT_DIR = f'{WORKDIR}/projects/daemon-service'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/config', exist_ok=True)

    # Ensure NO .vscode/launch.json exists (remove if present)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json):
        os.remove(launch_json)

    # Create main daemon service file
    with open(f'{PROJECT_DIR}/src/daemon.py', 'w') as f:
        f.write('''\
#!/usr/bin/env python3
"""Daemon service for processing background tasks."""

import time
import logging
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("/tmp/daemon-service.log")]
)
logger = logging.getLogger("daemon-service")

running = True

def signal_handler(signum, frame):
    global running
    logger.info("Received signal %d, shutting down...", signum)
    running = False

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


class TaskProcessor:
    """Processes queued tasks from the message broker."""

    def __init__(self, broker_url="localhost:5672", queue_name="tasks"):
        self.broker_url = broker_url
        self.queue_name = queue_name
        self.processed_count = 0

    def connect(self):
        logger.info("Connecting to broker at %s", self.broker_url)
        # Simulated connection
        return True

    def process_task(self, task_data):
        logger.info("Processing task #%d: %s", self.processed_count + 1, task_data.get("type", "unknown"))
        time.sleep(0.5)  # Simulate processing
        self.processed_count += 1
        return {"status": "completed", "task_id": task_data.get("id")}

    def run(self):
        self.connect()
        logger.info("Daemon started, waiting for tasks on queue '%s'", self.queue_name)
        while running:
            time.sleep(2)
            logger.info("Heartbeat - processed %d tasks so far", self.processed_count)


def main():
    processor = TaskProcessor(
        broker_url="amqp://guest:guest@localhost:5672",
        queue_name="daemon-tasks"
    )
    processor.run()
    logger.info("Daemon shut down cleanly after processing %d tasks", processor.processed_count)


if __name__ == "__main__":
    main()
''')

    # Create config file
    with open(f'{PROJECT_DIR}/config/settings.yaml', 'w') as f:
        f.write('''\
# Daemon Service Configuration
service:
  name: daemon-service
  version: 1.2.3
  environment: development

broker:
  url: amqp://guest:guest@localhost:5672
  queue: daemon-tasks
  prefetch_count: 10
  retry_max: 3
  retry_delay_ms: 1000

logging:
  level: INFO
  file: /var/log/daemon-service/app.log
  max_size_mb: 50
  backup_count: 5

health_check:
  enabled: true
  port: 8081
  interval_sec: 30
''')

    # Create test file
    with open(f'{PROJECT_DIR}/tests/test_daemon.py', 'w') as f:
        f.write('''\
"""Unit tests for the daemon service."""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from daemon import TaskProcessor


class TestTaskProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TaskProcessor(broker_url="localhost:5672", queue_name="test-queue")

    def test_connect(self):
        result = self.processor.connect()
        self.assertTrue(result)

    def test_process_task(self):
        task = {"id": "task-001", "type": "email_notification"}
        result = self.processor.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["task_id"], "task-001")
        self.assertEqual(self.processor.processed_count, 1)

    def test_process_multiple_tasks(self):
        tasks = [
            {"id": "task-001", "type": "email_notification"},
            {"id": "task-002", "type": "data_export"},
            {"id": "task-003", "type": "report_generation"},
        ]
        for task in tasks:
            self.processor.process_task(task)
        self.assertEqual(self.processor.processed_count, 3)


if __name__ == "__main__":
    unittest.main()
''')

    # Create requirements.txt
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('''\
pika==1.3.2
pyyaml==6.0.1
requests==2.31.0
pytest==7.4.3
''')

    # Create a simple README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''\
# Daemon Service

A background task processing daemon that consumes messages from a broker queue.

## Setup

```bash
pip install -r requirements.txt
python src/daemon.py
```

## Testing

```bash
pytest tests/
```
''')

    # Start a background Python process to simulate a running daemon
    env = os.environ.copy()
    subprocess.Popen(
        ['python3', '-c', 'import time\nwhile True:\n    time.sleep(60)'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )

    print(f'Initial project created: {PROJECT_DIR}')
    print('Background Python process started')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
