"""End-to-end tests: Master + Worker both as in-process ASGI apps."""

import asyncio

import httpx
import pytest

from tests.conftest import make_mock_desktop_env
from gateway.app import create_app as create_master
from gateway.dispatcher import WorkerDispatcher
from gateway.session import SessionManager
from worker.app import create_app as create_worker
from worker.env_pool import EnvPool


def _make_pool(num_envs: int = 2) -> EnvPool:
    counter = {"n": 0}

    def factory():
        port = 5900 + counter["n"]
        counter["n"] += 1
        return make_mock_desktop_env(vnc_port=port)

    pool = EnvPool(num_envs=num_envs, env_factory=factory, session_timeout=600)
    pool.start_all()
    return pool


@pytest.fixture
def e2e_clients():
    """Create master + worker as in-process ASGI apps connected via httpx."""
    pool = _make_pool(num_envs=2)
    worker_app = create_worker(config={"worker_id": "e2e-worker"}, pool=pool)

    # We'll route master's HTTP calls to the worker ASGI app
    worker_transport = httpx.ASGITransport(app=worker_app)
    worker_base = "http://test-worker"
    worker_client = httpx.AsyncClient(transport=worker_transport, base_url=worker_base)

    session_mgr = SessionManager(timeout=600)
    dispatcher = WorkerDispatcher(
        static_workers=[
            {
                "worker_id": "e2e-worker",
                "url": worker_base,
                "total_envs": 2,
                "free_envs": 2,
            }
        ]
    )

    master_app = create_master(
        config={},
        session_mgr=session_mgr,
        dispatcher=dispatcher,
        http_client=worker_client,
    )
    master_transport = httpx.ASGITransport(app=master_app)
    master_client = httpx.AsyncClient(
        transport=master_transport, base_url="http://test-master"
    )

    yield master_client, worker_client, pool

    pool.shutdown_all()


@pytest.mark.asyncio
class TestE2ELifecycle:
    async def test_full_single_task(self, e2e_clients):
        master, _, _ = e2e_clients

        # Acquire
        resp = await master.post("/acquire")
        assert resp.status_code == 200
        token = resp.json()["token"]
        assert resp.json()["vnc_port"] >= 5900

        # Reset
        resp = await master.post(
            "/reset", json={"token": token, "task_config": {"id": "task-1"}}
        )
        assert resp.status_code == 200
        obs = resp.json()["observation"]
        assert obs["instruction"] == "Open the terminal"

        # Step x2
        for _ in range(2):
            resp = await master.post(
                "/step", json={"token": token, "action": "click(100,200)"}
            )
            assert resp.status_code == 200
            assert "observation" in resp.json()

        # Evaluate
        resp = await master.post("/evaluate", json={"token": token})
        assert resp.status_code == 200
        assert resp.json()["score"] == 1.0

        # Release
        resp = await master.post("/release", json={"token": token})
        assert resp.status_code == 200

    async def test_multiple_concurrent_sessions(self, e2e_clients):
        master, _, _ = e2e_clients

        tokens = []
        for _ in range(2):
            resp = await master.post("/acquire")
            assert resp.status_code == 200
            tokens.append(resp.json()["token"])

        # Both can reset in parallel
        results = await asyncio.gather(
            master.post("/reset", json={"token": tokens[0]}),
            master.post("/reset", json={"token": tokens[1]}),
        )
        for r in results:
            assert r.status_code == 200

        # Release both
        for t in tokens:
            resp = await master.post("/release", json={"token": t})
            assert resp.status_code == 200

    async def test_release_then_reacquire(self, e2e_clients):
        master, _, _ = e2e_clients

        # Acquire both slots
        t1 = (await master.post("/acquire")).json()["token"]
        t2 = (await master.post("/acquire")).json()["token"]

        # All full
        resp = await master.post("/acquire")
        assert resp.status_code == 503

        # Release one
        await master.post("/release", json={"token": t1})

        # Can acquire again
        resp = await master.post("/acquire")
        assert resp.status_code == 200

        # Cleanup
        await master.post("/release", json={"token": t2})
        await master.post("/release", json={"token": resp.json()["token"]})

    async def test_invalid_token_after_release(self, e2e_clients):
        master, _, _ = e2e_clients

        token = (await master.post("/acquire")).json()["token"]
        await master.post("/release", json={"token": token})

        resp = await master.post("/step", json={"token": token, "action": "x"})
        assert resp.status_code == 404

    async def test_worker_health_through_master(self, e2e_clients):
        master, _, _ = e2e_clients
        resp = await master.get("/health")
        assert resp.status_code == 200

        resp = await master.get("/workers")
        assert resp.status_code == 200
        assert len(resp.json()["workers"]) == 1
