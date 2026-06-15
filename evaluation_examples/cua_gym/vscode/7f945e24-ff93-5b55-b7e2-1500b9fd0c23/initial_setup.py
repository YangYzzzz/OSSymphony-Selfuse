"""
Initial Setup: Create a Celery task-queue project for VSCode debugging task
Task ID: vscode_td_077
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_077'
PROJECT_DIR = f'{WORKDIR}/projects/task-queue'


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

    # Create tasks.py - a realistic Celery tasks file
    tasks_content = '''from celery import Celery
import time
import logging

logger = logging.getLogger(__name__)

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@app.task(bind=True, max_retries=3)
def send_notification(self, user_id, message):
    """Send a notification to a user via the messaging service."""
    try:
        logger.info(f"Sending notification to user {user_id}: {message}")
        # Simulate notification delivery
        time.sleep(0.5)
        return {"status": "delivered", "user_id": user_id}
    except Exception as exc:
        logger.error(f"Failed to send notification: {exc}")
        raise self.retry(exc=exc, countdown=60)


@app.task
def process_order(order_id, items):
    """Process an incoming order from the e-commerce queue."""
    logger.info(f"Processing order {order_id} with {len(items)} items")
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
    time.sleep(1)
    return {
        "order_id": order_id,
        "total": round(total, 2),
        "status": "processed",
        "item_count": len(items),
    }


@app.task(bind=True, rate_limit='10/m')
def generate_report(self, report_type, date_range):
    """Generate analytical reports with rate limiting."""
    logger.info(f"Generating {report_type} report for {date_range}")
    time.sleep(2)
    return {
        "report_type": report_type,
        "date_range": date_range,
        "status": "completed",
        "rows_processed": 15420,
    }


@app.task
def cleanup_expired_sessions():
    """Periodic task to clean up expired user sessions."""
    logger.info("Running session cleanup...")
    time.sleep(0.3)
    cleaned = 47
    logger.info(f"Cleaned up {cleaned} expired sessions")
    return {"cleaned": cleaned}
'''

    with open(os.path.join(PROJECT_DIR, 'tasks.py'), 'w') as f:
        f.write(tasks_content)

    # Create celeryconfig.py
    celeryconfig_content = '''broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

beat_schedule = {
    'cleanup-every-hour': {
        'task': 'tasks.cleanup_expired_sessions',
        'schedule': 3600.0,
    },
}
'''

    with open(os.path.join(PROJECT_DIR, 'celeryconfig.py'), 'w') as f:
        f.write(celeryconfig_content)

    # Create requirements.txt
    requirements_content = '''celery==5.3.6
redis==5.0.1
flower==2.0.1
'''

    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # Create a README
    readme_content = '''# Task Queue Service

A Celery-based task queue for processing asynchronous jobs.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Start Redis: `redis-server`
3. Start worker: `celery -A tasks worker --loglevel=info`
4. Monitor: `celery -A tasks flower`

## Tasks

- `send_notification` - Deliver user notifications
- `process_order` - Process e-commerce orders
- `generate_report` - Generate analytical reports
- `cleanup_expired_sessions` - Clean up stale sessions
'''

    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Ensure NO .vscode/launch.json exists (the task is to create it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json_path = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Files: tasks.py, celeryconfig.py, requirements.txt, README.md')
    print(f'No .vscode/launch.json exists (task requires creating it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
