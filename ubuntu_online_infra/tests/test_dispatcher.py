"""Unit tests for gateway/dispatcher.py (mock HTTP)."""

import pytest
import httpx
import respx

from gateway.dispatcher import WorkerDispatcher, MAX_CONSECUTIVE_FAILURES
from gateway.models import WorkerRegisterRequest


@pytest.fixture
def static_workers():
    return [
        {"worker_id": "w1", "url": "http://w1:9100", "total_envs": 4, "free_envs": 3},
        {"worker_id": "w2", "url": "http://w2:9100", "total_envs": 4, "free_envs": 1},
    ]


@pytest.fixture
def dispatcher(static_workers):
    return WorkerDispatcher(static_workers=static_workers)


class TestStaticWorkers:
    def test_loads_static_workers(self, dispatcher):
        workers = dispatcher.get_workers()
        ids = {w["worker_id"] for w in workers}
        assert ids == {"w1", "w2"}

    def test_sorted_by_free_envs(self, dispatcher):
        candidates = dispatcher._sorted_healthy_workers()
        assert candidates[0].worker_id == "w1"  # 3 free > 1 free


class TestRegistration:
    def test_register_new_worker(self, dispatcher):
        req = WorkerRegisterRequest(
            worker_id="w3", worker_url="http://w3:9100", total_envs=2, free_envs=2
        )
        dispatcher.register_worker(req)
        workers = dispatcher.get_workers()
        ids = {w["worker_id"] for w in workers}
        assert "w3" in ids

    def test_register_updates_existing(self, dispatcher):
        req = WorkerRegisterRequest(
            worker_id="w1", worker_url="http://w1:9100", total_envs=4, free_envs=0
        )
        dispatcher.register_worker(req)
        for w in dispatcher.get_workers():
            if w["worker_id"] == "w1":
                assert w["free_envs"] == 0


class TestHealthCheck:
    @pytest.mark.asyncio
    async def test_health_check_success(self, dispatcher):
        with respx.mock:
            respx.get("http://w1:9100/worker/health").respond(200, json={"status": "ok"})
            respx.get("http://w1:9100/worker/status").respond(
                200, json={"worker_id": "w1", "total_envs": 4, "free_envs": 4, "envs": []}
            )
            respx.get("http://w2:9100/worker/health").respond(200, json={"status": "ok"})
            respx.get("http://w2:9100/worker/status").respond(
                200, json={"worker_id": "w2", "total_envs": 4, "free_envs": 1, "envs": []}
            )
            async with httpx.AsyncClient() as client:
                await dispatcher.health_check_all(client)

        for w in dispatcher.get_workers():
            assert w["healthy"] is True

    @pytest.mark.asyncio
    async def test_consecutive_failures_mark_unhealthy(self, dispatcher):
        with respx.mock:
            # Make w1 fail repeatedly
            respx.get("http://w1:9100/worker/health").respond(500)
            respx.get("http://w2:9100/worker/health").respond(200, json={"status": "ok"})
            respx.get("http://w2:9100/worker/status").respond(
                200, json={"worker_id": "w2", "total_envs": 4, "free_envs": 1, "envs": []}
            )
            async with httpx.AsyncClient() as client:
                for _ in range(MAX_CONSECUTIVE_FAILURES):
                    await dispatcher.health_check_all(client)

        for w in dispatcher.get_workers():
            if w["worker_id"] == "w1":
                assert w["healthy"] is False
            else:
                assert w["healthy"] is True

    @pytest.mark.asyncio
    async def test_unhealthy_worker_excluded_from_dispatch(self, dispatcher):
        # Manually mark w1 unhealthy
        dispatcher._workers["w1"].healthy = False
        candidates = dispatcher._sorted_healthy_workers()
        assert all(c.worker_id != "w1" for c in candidates)


class TestNotifyRelease:
    def test_notify_release_increments_free(self, dispatcher):
        old = None
        for w in dispatcher.get_workers():
            if w["worker_id"] == "w1":
                old = w["free_envs"]
        dispatcher.notify_release("http://w1:9100")
        for w in dispatcher.get_workers():
            if w["worker_id"] == "w1":
                assert w["free_envs"] == old + 1


class TestPickWorkerAndAcquire:
    @pytest.mark.asyncio
    async def test_success(self, dispatcher):
        with respx.mock:
            respx.post("http://w1:9100/worker/acquire").respond(
                200, json={"local_env_id": 0, "vnc_port": 5900}
            )
            async with httpx.AsyncClient() as client:
                result = await dispatcher.pick_worker_and_acquire(client)
        assert result is not None
        worker_url, env_id, vnc_port = result
        assert worker_url == "http://w1:9100"
        assert env_id == 0
        assert vnc_port == 5900

    @pytest.mark.asyncio
    async def test_first_503_falls_to_second(self, dispatcher):
        with respx.mock:
            respx.post("http://w1:9100/worker/acquire").respond(503)
            respx.post("http://w2:9100/worker/acquire").respond(
                200, json={"local_env_id": 1, "vnc_port": 5901}
            )
            async with httpx.AsyncClient() as client:
                result = await dispatcher.pick_worker_and_acquire(client)
        assert result is not None
        assert result[0] == "http://w2:9100"

    @pytest.mark.asyncio
    async def test_all_fail_returns_none(self, dispatcher):
        with respx.mock:
            respx.post("http://w1:9100/worker/acquire").respond(503)
            respx.post("http://w2:9100/worker/acquire").respond(503)
            async with httpx.AsyncClient() as client:
                result = await dispatcher.pick_worker_and_acquire(client)
        assert result is None

    @pytest.mark.asyncio
    async def test_pick_decrements_free_envs(self, dispatcher):
        with respx.mock:
            respx.post("http://w1:9100/worker/acquire").respond(
                200, json={"local_env_id": 0, "vnc_port": 5900}
            )
            async with httpx.AsyncClient() as client:
                await dispatcher.pick_worker_and_acquire(client)
        for w in dispatcher.get_workers():
            if w["worker_id"] == "w1":
                assert w["free_envs"] == 2  # was 3, now 2
