"""Worker FastAPI application – manages local DesktopEnv pool."""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
import yaml
from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool

from gateway.models import (
    AcquireResponse,
    EvaluateRequest,
    EvaluateResponse,
    ReleaseRequest,
    ReleaseResponse,
    ResetRequest,
    ResetResponse,
    StepRequest,
    StepResponse,
    WorkerHealthResponse,
    WorkerRegisterRequest,
    WorkerStatusResponse,
)
from worker.env_pool import EnvPool

logger = logging.getLogger(__name__)


def load_config(path: str) -> Dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)

# Create Desktop Env Instance
def _make_env_factory(cfg: Dict[str, Any]):
    """Return a callable that creates DesktopEnv instances from config."""
    project_root = str(Path(__file__).resolve().parents[1])
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    def _factory():
        from desktop_env.osworld.desktop_env import DesktopEnv

        return DesktopEnv(
            provider_name=cfg.get("provider_name", "docker"),
            path_to_vm=cfg.get("path_to_vm", ""),
            action_space=cfg.get("action_space", "pyautogui"),
            screen_size=tuple(cfg.get("screen_size", [1920, 1080])),
            headless=cfg.get("headless", True),
            require_a11y_tree=cfg.get("require_a11y_tree", True),
            require_terminal=cfg.get("require_terminal", False),
        )

    return _factory


async def _heartbeat_loop(app_state, interval: float = 30.0):
    """Periodically register this worker with the master."""
    async with httpx.AsyncClient() as client:
        while True:
            try:
                req = WorkerRegisterRequest(
                    worker_id=app_state.worker_id,
                    worker_url=app_state.worker_url,
                    total_envs=app_state.pool.num_envs,
                    free_envs=app_state.pool.get_free_count(),
                )
                await client.post(
                    f"{app_state.master_url}/register",
                    json=req.model_dump(),
                    timeout=10.0,
                )
            except Exception:
                logger.warning("Heartbeat to master failed", exc_info=True)
            await asyncio.sleep(interval)


async def _cleanup_loop(app_state, interval: float = 60.0):
    """Periodically release expired env slots."""
    while True:
        await asyncio.sleep(interval)
        try:
            released = await run_in_threadpool(app_state.pool.cleanup_expired)
            if released:
                logger.info("Auto-released expired envs: %s", released)
        except Exception:
            logger.warning("Cleanup error", exc_info=True)


def create_app(config: Optional[Dict[str, Any]] = None, pool: Optional[EnvPool] = None) -> FastAPI:
    """Create the Worker FastAPI app. Accepts optional injected config/pool for testing."""
    cfg = config or {}
    injected = pool is not None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not injected:
            worker_id = cfg.get("worker_id", "worker-0")
            factory = _make_env_factory(cfg)
            app.state.pool = EnvPool(
                num_envs=cfg.get("num_envs", 1),
                env_factory=factory,
                session_timeout=cfg.get("session_timeout", 1800),
            )
            app.state.worker_id = worker_id
            await run_in_threadpool(app.state.pool.start_all)

            tasks = []
            master_url = cfg.get("master_url")
            if master_url:
                app.state.master_url = master_url
                app.state.worker_url = cfg.get(
                    "worker_url", f"http://0.0.0.0:{cfg.get('port', 9100)}"
                )
                tasks.append(asyncio.create_task(_heartbeat_loop(app.state)))

            tasks.append(asyncio.create_task(_cleanup_loop(app.state)))
        else:
            tasks = []

        yield

        for t in tasks:
            t.cancel()
        if not injected:
            await run_in_threadpool(app.state.pool.shutdown_all)

    app = FastAPI(title="OSWorld Worker", lifespan=lifespan)

    # Pre-set state for injected dependencies (works without lifespan)
    if injected:
        app.state.pool = pool
        app.state.worker_id = cfg.get("worker_id", "worker-0")

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @app.get("/worker/health")
    async def health():
        return WorkerHealthResponse()

    @app.get("/worker/status")
    async def status(request: Request):
        p = request.app.state.pool
        return WorkerStatusResponse(
            worker_id=request.app.state.worker_id,
            total_envs=p.num_envs,
            free_envs=p.get_free_count(),
            envs=p.get_status(),
        )

    @app.post("/worker/acquire")
    async def acquire(request: Request):
        slot = await run_in_threadpool(request.app.state.pool.acquire)
        if slot is None:
            raise HTTPException(status_code=503, detail="No idle environments available")
        return AcquireResponse(local_env_id=slot.local_env_id, vnc_port=slot.vnc_port)

    @app.post("/worker/reset")
    async def reset(req: ResetRequest, request: Request):
        try:
            obs = await run_in_threadpool(
                request.app.state.pool.reset_env, req.local_env_id, req.task_config
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return ResetResponse(observation=obs)

    @app.post("/worker/step")
    async def step(req: StepRequest, request: Request):
        try:
            obs, reward, done, info = await run_in_threadpool(
                request.app.state.pool.step_env, req.local_env_id, req.action, req.pause
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return StepResponse(observation=obs, reward=reward, done=done, info=info)

    @app.post("/worker/evaluate")
    async def evaluate(req: EvaluateRequest, request: Request):
        try:
            score = await run_in_threadpool(
                request.app.state.pool.evaluate_env, req.local_env_id
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return EvaluateResponse(score=score)

    @app.post("/worker/release")
    async def release(req: ReleaseRequest, request: Request):
        ok = await run_in_threadpool(request.app.state.pool.release, req.local_env_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Invalid env id")
        return ReleaseResponse(success=True)

    return app
