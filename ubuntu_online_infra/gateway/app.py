"""Master Gateway FastAPI application – session management and request routing."""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, HTTPException, Request

from gateway.dispatcher import WorkerDispatcher
from gateway.models import (
    MasterAcquireResponse,
    MasterEvaluateRequest,
    MasterReleaseRequest,
    MasterResetRequest,
    MasterStepRequest,
    WorkerRegisterRequest,
)
from gateway.session import SessionManager

logger = logging.getLogger(__name__)


async def _health_check_loop(app_state, interval: float) -> None:
    while True:
        await asyncio.sleep(interval)
        try:
            await app_state.dispatcher.health_check_all(app_state.http_client)
        except Exception:
            logger.warning("Health check loop error", exc_info=True)


async def _session_cleanup_loop(app_state, interval: float) -> None:
    while True:
        await asyncio.sleep(interval)
        try:
            expired = app_state.session_mgr.cleanup_expired()
            for sess in expired:
                try:
                    await app_state.http_client.post(
                        f"{sess.worker_url}/worker/release",
                        json={"local_env_id": sess.local_env_id},
                        timeout=10.0,
                    )
                    app_state.dispatcher.notify_release(sess.worker_url)
                except Exception:
                    logger.warning(
                        "Failed to release expired session %s on worker",
                        sess.token,
                    )
                logger.info("Cleaned up expired session %s", sess.token)
        except Exception:
            logger.warning("Session cleanup error", exc_info=True)


def create_app(
    config: Optional[Dict[str, Any]] = None,
    session_mgr: Optional[SessionManager] = None,
    dispatcher: Optional[WorkerDispatcher] = None,
    http_client: Optional[httpx.AsyncClient] = None,
) -> FastAPI:
    """Create the Master Gateway FastAPI app.

    All dependencies can be injected for testing.
    """
    cfg = config or {}
    injected = session_mgr is not None or dispatcher is not None or http_client is not None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not injected:
            app.state.session_mgr = SessionManager(
                timeout=cfg.get("session_timeout", 1800)
            )
            app.state.dispatcher = WorkerDispatcher(
                static_workers=cfg.get("workers", []),
                health_check_interval=cfg.get("health_check_interval", 15.0),
                heartbeat_timeout=cfg.get("heartbeat_timeout", 120.0),
            )
            app.state.http_client = httpx.AsyncClient(timeout=300.0)

            hc_interval = cfg.get("health_check_interval", 15.0)
            tasks = [
                asyncio.create_task(_health_check_loop(app.state, hc_interval)),
                asyncio.create_task(_session_cleanup_loop(app.state, 60.0)),
            ]
        else:
            tasks = []

        yield

        for t in tasks:
            t.cancel()
        if not injected:
            await app.state.http_client.aclose()

    app = FastAPI(title="OSWorld Master Gateway", lifespan=lifespan)

    # Pre-set state for injected dependencies (works without lifespan)
    if injected:
        app.state.session_mgr = session_mgr or SessionManager(
            timeout=cfg.get("session_timeout", 1800)
        )
        app.state.dispatcher = dispatcher or WorkerDispatcher(
            static_workers=cfg.get("workers", []),
        )
        app.state.http_client = http_client or httpx.AsyncClient(timeout=300.0)

    # ------------------------------------------------------------------
    # Monitoring endpoints
    # ------------------------------------------------------------------

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/workers")
    async def workers(request: Request):
        return {"workers": request.app.state.dispatcher.get_workers()}

    # ------------------------------------------------------------------
    # Worker registration
    # ------------------------------------------------------------------

    @app.post("/register")
    async def register(req: WorkerRegisterRequest, request: Request):
        request.app.state.dispatcher.register_worker(req)
        return {"status": "ok"}

    # ------------------------------------------------------------------
    # Client-facing endpoints
    # ------------------------------------------------------------------

    @app.post("/acquire")
    async def acquire(request: Request):
        state = request.app.state
        result = await state.dispatcher.pick_worker_and_acquire(state.http_client)
        if result is None:
            raise HTTPException(status_code=503, detail="No available environments")
        worker_url, local_env_id, vnc_port = result
        token = state.session_mgr.create_session(worker_url, local_env_id)
        return MasterAcquireResponse(
            token=token, vnc_port=vnc_port, worker_url=worker_url
        )

    @app.post("/reset")
    async def reset(req: MasterResetRequest, request: Request):
        state = request.app.state
        sess = state.session_mgr.get_session(req.token)
        if sess is None:
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        resp = await state.http_client.post(
            f"{sess.worker_url}/worker/reset",
            json={"local_env_id": sess.local_env_id, "task_config": req.task_config},
            timeout=300.0,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    @app.post("/step")
    async def step(req: MasterStepRequest, request: Request):
        state = request.app.state
        sess = state.session_mgr.get_session(req.token)
        if sess is None:
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        resp = await state.http_client.post(
            f"{sess.worker_url}/worker/step",
            json={
                "local_env_id": sess.local_env_id,
                "action": req.action,
                "pause": req.pause,
            },
            timeout=300.0,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    @app.post("/evaluate")
    async def evaluate(req: MasterEvaluateRequest, request: Request):
        state = request.app.state
        sess = state.session_mgr.get_session(req.token)
        if sess is None:
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        resp = await state.http_client.post(
            f"{sess.worker_url}/worker/evaluate",
            json={"local_env_id": sess.local_env_id},
            timeout=300.0,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    @app.post("/release")
    async def release(req: MasterReleaseRequest, request: Request):
        state = request.app.state
        sess = state.session_mgr.remove_session(req.token)
        if sess is None:
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        resp = await state.http_client.post(
            f"{sess.worker_url}/worker/release",
            json={"local_env_id": sess.local_env_id},
            timeout=30.0,
        )
        state.dispatcher.notify_release(sess.worker_url)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    return app
