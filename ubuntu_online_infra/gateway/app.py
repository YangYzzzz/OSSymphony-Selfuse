"""Master Gateway FastAPI application – session management and request routing."""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
import sys
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
    # Debug
    # ------------------------------------------------------------------

    @app.post("/release_all")
    async def release_all(request: Request):
        """For debugging purposes only - releases all tokens from all Workers.
        DO NOT use this in production training!"""
        app_state = request.app.state
        all_sessions = app_state.session_mgr.cleanup_all()
        for sess in all_sessions:
            await app_state.http_client.post(
                f"{sess.worker_url}/worker/release",
                json={"local_env_id": sess.local_env_id},
                timeout=10.0,
            )
            app_state.dispatcher.notify_release(sess.worker_url)
        return {"status": "ok"}
    
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
        logger.info("master /acquire: incoming request from %s", request.client.host if request.client else "unknown")
        result = await state.dispatcher.pick_worker_and_acquire(state.http_client)
        if result is None:
            logger.warning("master /acquire: no available environments")
            raise HTTPException(status_code=503, detail="No available environments")
        worker_url, local_env_id, vnc_port = result
        token = state.session_mgr.create_session(worker_url, local_env_id)
        logger.info(
            "master /acquire: assigned worker=%s local_env_id=%s token=%s vnc_port=%s",
            worker_url,
            local_env_id,
            token,
            vnc_port,
        )
        return MasterAcquireResponse(
            token=token, vnc_port=vnc_port, worker_url=worker_url
        )

    @app.post("/reset")
    async def reset(req: MasterResetRequest, request: Request):
        state = request.app.state
        logger.info("master /reset start: token=%s", req.token)
        sess = state.session_mgr.get_session(req.token)
        if sess is None:
            logger.warning("master /reset: invalid or expired token=%s", req.token)
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        url = f"{sess.worker_url}/worker/reset"
        payload = {"local_env_id": sess.local_env_id, "task_config": req.task_config}
        start = asyncio.get_event_loop().time()
        try:
            logger.info(
                "master /reset -> worker: url=%s local_env_id=%s",
                url,
                sess.local_env_id,
            )
            resp = await state.http_client.post(
                url,
                json=payload,
                timeout=1000.0,
            )
        except httpx.ReadTimeout:
            duration = asyncio.get_event_loop().time() - start
            logger.error(
                "master /reset ReadTimeout: url=%s local_env_id=%s token=%s duration=%.3fs",
                url,
                sess.local_env_id,
                req.token,
                duration,
                exc_info=True,
            )
            raise HTTPException(status_code=504, detail="Worker reset timeout")
        duration = asyncio.get_event_loop().time() - start
        logger.info(
            "master /reset <- worker: status=%s duration=%.3fs",
            resp.status_code,
            duration,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    @app.post("/step")
    async def step(req: MasterStepRequest, request: Request):
        state = request.app.state
        logger.info(
            "master /step start: token=%s action=%s pause=%s",
            req.token,
            req.action,
            req.pause,
        )
        sess = state.session_mgr.get_session(req.token)
        if sess is None:
            logger.warning("master /step: invalid or expired token=%s", req.token)
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        url = f"{sess.worker_url}/worker/step"
        payload = {
            "local_env_id": sess.local_env_id,
            "action": req.action,
            "pause": req.pause,
        }
        start = asyncio.get_event_loop().time()
        try:
            logger.info(
                "master /step -> worker: url=%s local_env_id=%s",
                url,
                sess.local_env_id,
            )
            resp = await state.http_client.post(
                url,
                json=payload,
                timeout=1000.0,
            )
        except httpx.ReadTimeout:
            duration = asyncio.get_event_loop().time() - start
            logger.error(
                "master /step ReadTimeout: url=%s local_env_id=%s token=%s duration=%.3fs",
                url,
                sess.local_env_id,
                req.token,
                duration,
                exc_info=True,
            )
            raise HTTPException(status_code=504, detail="Worker step timeout")
        duration = asyncio.get_event_loop().time() - start
        logger.info(
            "master /step <- worker: status=%s duration=%.3fs",
            resp.status_code,
            duration,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    @app.post("/evaluate")
    async def evaluate(req: MasterEvaluateRequest, request: Request):
        state = request.app.state
        logger.info("master /evaluate start: token=%s", req.token)
        sess = state.session_mgr.get_session(req.token)
        if sess is None:
            logger.warning("master /evaluate: invalid or expired token=%s", req.token)
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        url = f"{sess.worker_url}/worker/evaluate"
        start = asyncio.get_event_loop().time()
        try:
            logger.info(
                "master /evaluate -> worker: url=%s local_env_id=%s",
                url,
                sess.local_env_id,
            )
            resp = await state.http_client.post(
                url,
                json={"local_env_id": sess.local_env_id},
                timeout=300.0,
            )
        except httpx.ReadTimeout:
            duration = asyncio.get_event_loop().time() - start
            logger.error(
                "master /evaluate ReadTimeout: url=%s local_env_id=%s token=%s duration=%.3fs",
                url,
                sess.local_env_id,
                req.token,
                duration,
                exc_info=True,
            )
            raise HTTPException(status_code=504, detail="Worker evaluate timeout")
        duration = asyncio.get_event_loop().time() - start
        logger.info(
            "master /evaluate <- worker: status=%s duration=%.3fs",
            resp.status_code,
            duration,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    @app.post("/release")
    async def release(req: MasterReleaseRequest, request: Request):
        state = request.app.state
        logger.info("master /release start: token=%s", req.token)
        sess = state.session_mgr.remove_session(req.token)
        if sess is None:
            logger.warning("master /release: invalid or expired token=%s", req.token)
            raise HTTPException(status_code=404, detail="Invalid or expired token")
        url = f"{sess.worker_url}/worker/release"
        start = asyncio.get_event_loop().time()
        try:
            logger.info(
                "master /release -> worker: url=%s local_env_id=%s",
                url,
                sess.local_env_id,
            )
            resp = await state.http_client.post(
                url,
                json={"local_env_id": sess.local_env_id},
                timeout=30.0,
            )
        except httpx.ReadTimeout:
            duration = asyncio.get_event_loop().time() - start
            logger.error(
                "master /release ReadTimeout: url=%s local_env_id=%s token=%s duration=%.3fs",
                url,
                sess.local_env_id,
                req.token,
                duration,
                exc_info=True,
            )
            raise HTTPException(status_code=504, detail="Worker release timeout")
        duration = asyncio.get_event_loop().time() - start
        logger.info(
            "master /release <- worker: status=%s duration=%.3fs",
            resp.status_code,
            duration,
        )
        state.dispatcher.notify_release(sess.worker_url)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

    return app
