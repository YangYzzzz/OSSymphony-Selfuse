"""Worker dispatcher – load balancing, health checks, and acquire routing."""

import logging
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import httpx

from gateway.models import AcquireResponse, WorkerRegisterRequest

logger = logging.getLogger(__name__)

MAX_CONSECUTIVE_FAILURES = 3

@dataclass
class WorkerRecord:
    worker_id: str
    url: str
    total_envs: int = 0
    free_envs_ids: List = []
    free_envs: int = 0
    health_envs_ids: List = []
    health_envs: int = 0
    healthy: bool = True
    consecutive_failures: int = 0
    last_heartbeat: float = field(default_factory=time.time)


class WorkerDispatcher:
    """Manages worker registry, health checks, and acquire routing."""

    def __init__(
        self,
        static_workers: Optional[List[Dict[str, Any]]] = None,
        health_check_interval: float = 15.0,
        heartbeat_timeout: float = 120.0,
    ):
        self._workers: Dict[str, WorkerRecord] = {}
        self._lock = threading.Lock()
        self.health_check_interval = health_check_interval
        self.heartbeat_timeout = heartbeat_timeout

        # Load static worker list from config
        for w in (static_workers or []):
            rec = WorkerRecord(
                worker_id=w["worker_id"],
                url=w["url"],
                total_envs=w.get("total_envs", 0),
                free_envs_ids=w.get("free_envs_ids", []),
                health_envs_ids=w.get("health_envs_ids", []),
                free_envs=len(w.get("free_envs_ids", [])),
                health_envs=len(w.get("health_envs_ids", []))
            )
            self._workers[rec.worker_id] = rec

    # ------------------------------------------------------------------
    # Registration (heartbeat)
    # ------------------------------------------------------------------

    def register_worker(self, req: WorkerRegisterRequest) -> None:
        with self._lock:
            existing = self._workers.get(req.worker_id)
            if existing:
                existing.url = req.worker_url
                existing.total_envs = req.total_envs
                existing.free_envs_ids = req.free_envs_ids
                existing.health_envs_ids = req.health_envs_ids
                existing.free_envs = len(req.free_envs_ids)
                existing.health_envs = len(req.health_envs_ids)
                existing.last_heartbeat = time.time()
                existing.healthy = True
                existing.consecutive_failures = 0
            else:
                self._workers[req.worker_id] = WorkerRecord(
                    worker_id=req.worker_id,
                    url=req.worker_url,
                    total_envs=req.total_envs,
                    free_envs_ids=req.free_envs_ids,
                    health_envs_ids=req.health_envs_ids,
                    free_envs=len(req.free_envs_ids),
                    health_envs=len(req.health_envs_ids)
                )

    # ------------------------------------------------------------------
    # Acquire routing
    # ------------------------------------------------------------------

    async def pick_worker_and_acquire(
        self, client: httpx.AsyncClient
    ) -> Optional[Tuple[str, int, int]]:
        """Pick the healthy worker with most free envs and call its /worker/acquire.

        Returns (worker_url, local_env_id, vnc_port) or None.
        """
        candidates = self._sorted_healthy_workers()
        for rec in candidates:
            try:
                resp = await client.post(
                    f"{rec.url}/worker/acquire", timeout=30.0
                )
                if resp.status_code == 200:
                    data = AcquireResponse.model_validate(resp.json())
                    with self._lock:
                        rec.free_envs = max(0, rec.free_envs - 1)
                    return rec.url, data.local_env_id, data.vnc_port
                else:
                    logger.warning(
                        "Worker %s acquire returned %d", rec.worker_id, resp.status_code
                    )
            except Exception:
                logger.warning("Worker %s acquire failed", rec.worker_id, exc_info=True)
        return None

    # ------------------------------------------------------------------
    # Health checks
    # ------------------------------------------------------------------

    async def health_check_all(self, client: httpx.AsyncClient) -> None:
        """Probe all workers and update health status."""
        with self._lock:
            workers = list(self._workers.values())
        for rec in workers:
            try:
                resp = await client.get(
                    f"{rec.url}/worker/health", timeout=10.0
                )
                if resp.status_code == 200:
                    with self._lock:
                        rec.consecutive_failures = 0
                        rec.healthy = True
                    # Also update status if available
                    try:
                        status_resp = await client.get(
                            f"{rec.url}/worker/status", timeout=10.0
                        )
                        if status_resp.status_code == 200:
                            data = status_resp.json()
                            with self._lock:
                                rec.total_envs = data.get("total_envs", rec.total_envs)
                                rec.free_envs = data.get("free_envs", rec.free_envs)
                    except Exception:
                        pass
                else:
                    self._record_failure(rec)
            except Exception:
                self._record_failure(rec)

    def _record_failure(self, rec: WorkerRecord) -> None:
        with self._lock:
            rec.consecutive_failures += 1
            if rec.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                rec.healthy = False
                logger.warning(
                    "Worker %s marked unhealthy after %d failures",
                    rec.worker_id,
                    rec.consecutive_failures,
                )

    # ------------------------------------------------------------------
    # Release notification
    # ------------------------------------------------------------------

    def notify_release(self, worker_url: str) -> None:
        with self._lock:
            for rec in self._workers.values():
                if rec.url == worker_url:
                    rec.free_envs += 1
                    break

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_workers(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {
                    "worker_id": r.worker_id,
                    "url": r.url,
                    "total_envs": r.total_envs,
                    "free_envs_ids": r.free_envs_ids, # List
                    "health_envs_ids": r.health_envs_ids, # List
                    "healthy": r.healthy,
                    "last_heartbeat": r.last_heartbeat
                }
                for r in self._workers.values()
            ]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _sorted_healthy_workers(self) -> List[WorkerRecord]:
        """Return healthy workers sorted by free_envs descending."""
        with self._lock:
            return sorted(
                [r for r in self._workers.values() if r.healthy and r.free_envs > 0],
                key=lambda r: r.free_envs,
                reverse=True,
            )
