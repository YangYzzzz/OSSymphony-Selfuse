"""Integration tests for worker/app.py using FastAPI TestClient + mock DesktopEnv."""

import pytest
from fastapi.testclient import TestClient

from tests.conftest import make_mock_desktop_env
from worker.env_pool import EnvPool
from worker.app import create_app


@pytest.fixture
def worker_client():
    """Create a TestClient with a 2-env mock pool."""
    counter = {"n": 0}

    def factory():
        port = 5900 + counter["n"]
        counter["n"] += 1
        return make_mock_desktop_env(vnc_port=port)

    pool = EnvPool(num_envs=2, env_factory=factory, session_timeout=600)
    pool.start_all()
    app = create_app(config={"worker_id": "test-worker"}, pool=pool)
    with TestClient(app) as client:
        yield client
    pool.shutdown_all()


class TestWorkerHealth:
    def test_health(self, worker_client):
        resp = worker_client.get("/worker/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_status(self, worker_client):
        resp = worker_client.get("/worker/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["worker_id"] == "test-worker"
        assert data["total_envs"] == 2
        assert data["free_envs"] == 2
        assert len(data["envs"]) == 2


class TestWorkerLifecycle:
    def test_acquire_reset_step_evaluate_release(self, worker_client):
        # Acquire
        resp = worker_client.post("/worker/acquire")
        assert resp.status_code == 200
        env_id = resp.json()["local_env_id"]
        assert resp.json()["vnc_port"] >= 5900

        # Reset
        resp = worker_client.post(
            "/worker/reset",
            json={"local_env_id": env_id, "task_config": {"id": "task-1"}},
        )
        assert resp.status_code == 200
        obs = resp.json()["observation"]
        assert obs["instruction"] == "Open the terminal"
        assert obs["screenshot_base64"] is not None

        # Step
        resp = worker_client.post(
            "/worker/step",
            json={"local_env_id": env_id, "action": "click(100,200)", "pause": 1.0},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "observation" in data
        assert "reward" in data
        assert "done" in data

        # Evaluate
        resp = worker_client.post(
            "/worker/evaluate", json={"local_env_id": env_id}
        )
        assert resp.status_code == 200
        assert resp.json()["score"] == 1.0

        # Release
        resp = worker_client.post(
            "/worker/release", json={"local_env_id": env_id}
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    def test_acquire_all_then_503(self, worker_client):
        worker_client.post("/worker/acquire")
        worker_client.post("/worker/acquire")
        resp = worker_client.post("/worker/acquire")
        assert resp.status_code == 503

    def test_reset_invalid_env_id(self, worker_client):
        resp = worker_client.post(
            "/worker/reset", json={"local_env_id": 999}
        )
        assert resp.status_code == 404

    def test_step_invalid_env_id(self, worker_client):
        resp = worker_client.post(
            "/worker/step", json={"local_env_id": 999, "action": "click(0,0)"}
        )
        assert resp.status_code == 404

    def test_evaluate_invalid_env_id(self, worker_client):
        resp = worker_client.post(
            "/worker/evaluate", json={"local_env_id": 999}
        )
        assert resp.status_code == 404

    def test_release_invalid_env_id(self, worker_client):
        resp = worker_client.post(
            "/worker/release", json={"local_env_id": 999}
        )
        assert resp.status_code == 404

    def test_release_then_re_acquire(self, worker_client):
        resp = worker_client.post("/worker/acquire")
        env_id = resp.json()["local_env_id"]
        worker_client.post("/worker/release", json={"local_env_id": env_id})
        # Should be able to acquire again
        resp = worker_client.post("/worker/acquire")
        assert resp.status_code == 200

    def test_status_reflects_acquired(self, worker_client):
        worker_client.post("/worker/acquire")
        resp = worker_client.get("/worker/status")
        data = resp.json()
        assert data["free_envs"] == 1
