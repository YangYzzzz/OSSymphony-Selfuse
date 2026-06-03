"""
Initial Setup: Create a VSCode workspace with an asyncio Python app and basic debug config.
Task ID: vscode_py_072
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_072'
PROJECT_DIR = os.path.join(WORKDIR, 'async_project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
LAUNCH_JSON = os.path.join(VSCODE_DIR, 'launch.json')
APP_FILE = os.path.join(PROJECT_DIR, 'async_server.py')


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
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- Create async_server.py: a realistic asyncio-based Python application ---
    async_server_code = '''\
"""
Async HTTP Server - handles concurrent client connections using asyncio.
Provides REST endpoints for a simple task management system.
"""

import asyncio
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("async_server")

# In-memory task store
tasks: dict[str, dict] = {}
task_counter: int = 0


async def handle_create_task(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Create a new task from the incoming request body."""
    global task_counter
    data = await reader.read(4096)
    body = json.loads(data.decode())

    task_counter += 1
    task_id = f"TASK-{task_counter:04d}"
    tasks[task_id] = {
        "id": task_id,
        "title": body.get("title", "Untitled"),
        "description": body.get("description", ""),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "assigned_to": body.get("assigned_to", None),
        "priority": body.get("priority", "medium"),
    }

    logger.info(f"Created task {task_id}: {tasks[task_id][\'title\']}")
    response = json.dumps(tasks[task_id])
    writer.write(response.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def handle_list_tasks(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Return all tasks as a JSON list."""
    await reader.read(1024)
    result = list(tasks.values())
    response = json.dumps(result, indent=2)
    writer.write(response.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def process_batch(task_ids: list[str]) -> list[dict]:
    """Process a batch of tasks concurrently."""
    async def update_single(tid: str) -> dict:
        await asyncio.sleep(0.1)  # Simulate async I/O
        if tid in tasks:
            tasks[tid]["status"] = "processing"
            logger.info(f"Processing task {tid}")
            await asyncio.sleep(0.5)  # Simulate work
            tasks[tid]["status"] = "completed"
            return tasks[tid]
        return {"error": f"Task {tid} not found"}

    results = await asyncio.gather(*[update_single(tid) for tid in task_ids])
    return results


async def periodic_cleanup(interval: int = 300):
    """Periodically clean up completed tasks older than 1 hour."""
    while True:
        await asyncio.sleep(interval)
        now = datetime.now()
        to_remove = []
        for tid, task in tasks.items():
            if task["status"] == "completed":
                created = datetime.fromisoformat(task["created_at"])
                if (now - created).total_seconds() > 3600:
                    to_remove.append(tid)
        for tid in to_remove:
            del tasks[tid]
            logger.info(f"Cleaned up old task {tid}")


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Main client handler - routes requests to appropriate handlers."""
    addr = writer.get_extra_info("peername")
    logger.info(f"New connection from {addr}")

    try:
        header = await asyncio.wait_for(reader.readline(), timeout=10.0)
        request_line = header.decode().strip()

        if "POST /tasks" in request_line:
            await handle_create_task(reader, writer)
        elif "GET /tasks" in request_line:
            await handle_list_tasks(reader, writer)
        elif "POST /batch" in request_line:
            data = await reader.read(4096)
            body = json.loads(data.decode())
            results = await process_batch(body.get("task_ids", []))
            writer.write(json.dumps(results).encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        else:
            writer.write(b"HTTP/1.1 404 Not Found\\r\\n\\r\\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
    except asyncio.TimeoutError:
        logger.warning(f"Timeout for connection from {addr}")
        writer.close()
        await writer.wait_closed()
    except Exception as exc:
        logger.error(f"Error handling client {addr}: {exc}")
        writer.close()
        await writer.wait_closed()


async def main():
    """Start the async server and background tasks."""
    cleanup_task = asyncio.create_task(periodic_cleanup(interval=300))

    server = await asyncio.start_server(handle_client, "0.0.0.0", 8080)
    addr = server.sockets[0].getsockname()
    logger.info(f"Async Task Server running on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
'''
    with open(APP_FILE, 'w') as f:
        f.write(async_server_code)
    print(f'Created: {APP_FILE}')

    # --- Create a basic launch.json that doesn't handle async well ---
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "debugpy",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal"
            }
        ]
    }
    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)
    print(f'Created: {LAUNCH_JSON}')

    # --- Create a helper module for the project ---
    utils_file = os.path.join(PROJECT_DIR, 'utils.py')
    utils_code = '''\
"""Utility functions for the async task server."""

import asyncio
import json
from typing import Any


async def retry_async(coro_func, max_retries: int = 3, delay: float = 1.0):
    """Retry an async function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await coro_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = delay * (2 ** attempt)
            await asyncio.sleep(wait_time)


def serialize_response(data: Any, status: int = 200) -> bytes:
    """Serialize data to an HTTP-like JSON response."""
    body = json.dumps(data)
    header = f"HTTP/1.1 {status} OK\\r\\nContent-Type: application/json\\r\\nContent-Length: {len(body)}\\r\\n\\r\\n"
    return (header + body).encode()


async def rate_limiter(max_requests: int, period: float):
    """Simple async rate limiter using a semaphore."""
    semaphore = asyncio.Semaphore(max_requests)

    async def acquire():
        await semaphore.acquire()
        asyncio.get_event_loop().call_later(period, semaphore.release)

    return acquire
'''
    with open(utils_file, 'w') as f:
        f.write(utils_code)
    print(f'Created: {utils_file}')

    # --- Create a requirements.txt ---
    req_file = os.path.join(PROJECT_DIR, 'requirements.txt')
    with open(req_file, 'w') as f:
        f.write('debugpy>=1.8.0\naiohttp>=3.9.0\npytest-asyncio>=0.23.0\n')
    print(f'Created: {req_file}')

    # --- Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
