"""
Initial Setup: Create task_queue.py with 6 TODO comments in # style
Task ID: vscode_rf_020
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_020'
PROJECT_DIR = f'{WORKDIR}/projects/backend'
OUTPUT = f'{PROJECT_DIR}/task_queue.py'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    content = '''\
"""
task_queue.py - Distributed Task Queue Manager

A lightweight task queue implementation for processing background jobs
in the backend service. Supports priority scheduling, retry logic,
and dead-letter queue handling.
"""

import threading
import time
import heapq
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class TaskPriority(Enum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    CRITICAL = 0


@dataclass(order=True)
class Task:
    priority: int
    task_id: str = field(compare=False)
    func: Callable = field(compare=False, repr=False)
    args: tuple = field(default=(), compare=False, repr=False)
    kwargs: dict = field(default_factory=dict, compare=False, repr=False)
    max_retries: int = field(default=3, compare=False)
    retry_count: int = field(default=0, compare=False)
    created_at: datetime = field(default_factory=datetime.now, compare=False)
    status: TaskStatus = field(default=TaskStatus.PENDING, compare=False)


# TODO: Implement a TaskResult dataclass to store execution results with timing metadata


class TaskQueue:
    """Priority-based task queue with concurrent worker support."""

    def __init__(self, max_workers: int = 4, retry_delay: float = 2.0):
        self._queue: List[Task] = []
        self._lock = threading.Lock()
        self._max_workers = max_workers
        self._active_workers = 0
        self._retry_delay = retry_delay
        self._task_registry: Dict[str, Task] = {}
        self._dead_letter_queue: List[Task] = []
        # TODO: Add a metrics collector to track queue throughput and average processing time
        self._shutdown_event = threading.Event()
        self._worker_threads: List[threading.Thread] = []
        logger.info(f"TaskQueue initialized with {max_workers} workers")

    def submit(self, task_id: str, func: Callable, *args,
               priority: TaskPriority = TaskPriority.MEDIUM,
               max_retries: int = 3, **kwargs) -> str:
        """Submit a new task to the queue."""
        task = Task(
            priority=priority.value,
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            max_retries=max_retries,
        )
        with self._lock:
            heapq.heappush(self._queue, task)
            self._task_registry[task_id] = task
        logger.info(f"Task {task_id} submitted with priority {priority.name}")
        return task_id

    def _process_task(self, task: Task) -> bool:
        """Execute a single task with error handling and retry logic."""
        task.status = TaskStatus.RUNNING
        logger.info(f"Processing task {task.task_id} (attempt {task.retry_count + 1})")
        try:
            result = task.func(*task.args, **task.kwargs)
            task.status = TaskStatus.COMPLETED
            # TODO: Persist completed task results to a SQLite database for audit trail
            logger.info(f"Task {task.task_id} completed successfully")
            return True
        except Exception as exc:
            task.retry_count += 1
            if task.retry_count < task.max_retries:
                task.status = TaskStatus.RETRYING
                logger.warning(
                    f"Task {task.task_id} failed (attempt {task.retry_count}/"
                    f"{task.max_retries}): {exc}"
                )
                time.sleep(self._retry_delay)
                with self._lock:
                    heapq.heappush(self._queue, task)
                return False
            else:
                task.status = TaskStatus.FAILED
                self._dead_letter_queue.append(task)
                logger.error(
                    f"Task {task.task_id} permanently failed after "
                    f"{task.max_retries} attempts: {exc}"
                )
                return False

    def _worker_loop(self):
        """Main loop for worker threads."""
        while not self._shutdown_event.is_set():
            task = None
            with self._lock:
                if self._queue:
                    task = heapq.heappop(self._queue)
                    self._active_workers += 1
            if task:
                try:
                    self._process_task(task)
                finally:
                    with self._lock:
                        self._active_workers -= 1
            else:
                time.sleep(0.1)

    def start(self):
        """Start all worker threads."""
        # TODO: Add health check endpoint that reports worker status and queue depth
        for i in range(self._max_workers):
            thread = threading.Thread(
                target=self._worker_loop,
                name=f"TaskWorker-{i}",
                daemon=True,
            )
            thread.start()
            self._worker_threads.append(thread)
        logger.info(f"Started {self._max_workers} worker threads")

    def shutdown(self, wait: bool = True, timeout: float = 30.0):
        """Gracefully shut down the task queue."""
        logger.info("Initiating task queue shutdown...")
        self._shutdown_event.set()
        if wait:
            deadline = time.time() + timeout
            for thread in self._worker_threads:
                remaining = deadline - time.time()
                if remaining > 0:
                    thread.join(timeout=remaining)
        # TODO: Flush any pending metrics and close database connections on shutdown
        logger.info("Task queue shutdown complete")

    def get_status(self, task_id: str) -> Optional[TaskStatus]:
        """Check the current status of a task."""
        task = self._task_registry.get(task_id)
        return task.status if task else None

    @property
    def pending_count(self) -> int:
        """Return the number of tasks waiting in the queue."""
        with self._lock:
            return len(self._queue)

    @property
    def dead_letter_count(self) -> int:
        """Return the number of permanently failed tasks."""
        return len(self._dead_letter_queue)

    def retry_dead_letters(self) -> int:
        """Re-submit all dead-letter tasks back into the main queue."""
        resubmitted = 0
        while self._dead_letter_queue:
            task = self._dead_letter_queue.pop(0)
            task.retry_count = 0
            task.status = TaskStatus.PENDING
            with self._lock:
                heapq.heappush(self._queue, task)
            resubmitted += 1
        logger.info(f"Resubmitted {resubmitted} dead-letter tasks")
        return resubmitted


class ScheduledTaskRunner:
    """Runs tasks on a fixed interval schedule."""

    def __init__(self, queue: TaskQueue):
        self._queue = queue
        self._schedules: Dict[str, dict] = {}
        self._running = False
        # TODO: Support cron-style expressions instead of simple interval-based scheduling

    def add_schedule(self, name: str, func: Callable, interval_seconds: float,
                     priority: TaskPriority = TaskPriority.LOW):
        """Register a recurring task."""
        self._schedules[name] = {
            "func": func,
            "interval": interval_seconds,
            "priority": priority,
            "last_run": None,
        }
        logger.info(f"Scheduled task '{name}' every {interval_seconds}s")

    def _scheduler_loop(self):
        """Check schedules and submit tasks when due."""
        while self._running:
            now = datetime.now()
            for name, schedule in self._schedules.items():
                last_run = schedule["last_run"]
                interval = timedelta(seconds=schedule["interval"])
                if last_run is None or (now - last_run) >= interval:
                    task_id = f"{name}_{now.strftime('%Y%m%d_%H%M%S')}"
                    self._queue.submit(
                        task_id,
                        schedule["func"],
                        priority=schedule["priority"],
                    )
                    schedule["last_run"] = now
            time.sleep(1.0)

    def start(self):
        """Start the scheduler."""
        self._running = True
        thread = threading.Thread(
            target=self._scheduler_loop,
            name="SchedulerThread",
            daemon=True,
        )
        thread.start()
        logger.info("Scheduled task runner started")

    def stop(self):
        """Stop the scheduler."""
        self._running = False
        logger.info("Scheduled task runner stopped")
'''

    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the backend project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Open the specific file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
