"""Integration tests for gateway/app.py using FastAPI TestClient + respx mock HTTP."""

import pytest
import httpx
import respx
from fastapi.testclient import TestClient

from gateway.app import create_app
from gateway.dispatcher import WorkerDispatcher
from gateway.session import SessionManager


WORKER_URL = "http://fake-worker:9100"


@pytest.fixture
def gateway_client():
    """Create a TestClient with mocked worker HTTP backend."""
    session_mgr = SessionManager(timeout=600)
    dispatcher = WorkerDispatcher(
        static_workers=[
            {"worker_id": "w1", "url": WORKER_URL, "total_envs": 4, "free_envs": 4},
        ]
    )

    with respx.mock:
        # Pre-configure worker mock responses
        respx.post(f"{WORKER_URL}/worker/acquire").respond(
            200, json={"local_env_id": 0, "vnc_port": 5900}
        )
        respx.post(f"{WORKER_URL}/worker/reset").respond(
            200,
            json={
                "observation": {
                    "screenshot_base64": "abc",
                    "accessibility_tree": "<t/>",
                    "terminal": None,
                    "instruction": "Do something",
                }
            },
        )
        respx.post(f"{WORKER_URL}/worker/step").respond(
            200,
            json={
                "observation": {
                    "screenshot_base64": "def",
                    "accessibility_tree": None,
                    "terminal": None,
                    "instruction": "Do something",
                },
                "reward": 0.0,
                "done": False,
                "info": {},
            },
        )
        respx.post(f"{WORKER_URL}/worker/evaluate").respond(
            200, json={"score": 0.75}
        )
        respx.post(f"{WORKER_URL}/worker/release").respond(
            200, json={"success": True}
        )

        # Use a real httpx.Client that goes through respx mock
        mock_client = httpx.AsyncClient()
        app = create_app(
            config={},
            session_mgr=session_mgr,
            dispatcher=dispatcher,
            http_client=mock_client,
        )
        with TestClient(app) as client:
            yield client, session_mgr, dispatcher


class TestMonitoring:
    def test_health(self, gateway_client):
        client, _, _ = gateway_client
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_workers(self, gateway_client):
        client, _, _ = gateway_client
        resp = client.get("/workers")
        assert resp.status_code == 200
        workers = resp.json()["workers"]
        assert len(workers) == 1
        assert workers[0]["worker_id"] == "w1"


class TestRegister:
    def test_register_new_worker(self, gateway_client):
        client, _, dispatcher = gateway_client
        resp = client.post(
            "/register",
            json={
                "worker_id": "w2",
                "worker_url": "http://w2:9100",
                "total_envs": 2,
                "free_envs": 2,
            },
        )
        assert resp.status_code == 200
        ids = {w["worker_id"] for w in dispatcher.get_workers()}
        assert "w2" in ids


class TestAcquire:
    def test_acquire_success(self, gateway_client):
        client, _, _ = gateway_client
        resp = client.post("/acquire")
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        assert data["vnc_port"] == 5900
        assert data["worker_url"] == WORKER_URL

    def test_acquire_no_workers_503(self):
        """With an empty dispatcher, acquire should fail."""
        session_mgr = SessionManager()
        dispatcher = WorkerDispatcher(static_workers=[])
        mock_client = httpx.AsyncClient()
        app = create_app(
            config={},
            session_mgr=session_mgr,
            dispatcher=dispatcher,
            http_client=mock_client,
        )
        with TestClient(app) as client:
            resp = client.post("/acquire")
            assert resp.status_code == 503


class TestSessionRouting:
    def _acquire_token(self, client):
        resp = client.post("/acquire")
        assert resp.status_code == 200
        return resp.json()["token"]

    def test_reset_with_valid_token(self, gateway_client):
        client, _, _ = gateway_client
        token = self._acquire_token(client)
        resp = client.post(
            "/reset", json={"token": token, "task_config": {"id": "t1"}}
        )
        assert resp.status_code == 200
        assert "observation" in resp.json()

    def test_step_with_valid_token(self, gateway_client):
        client, _, _ = gateway_client
        token = self._acquire_token(client)
        resp = client.post(
            "/step", json={"token": token, "action": "click(0,0)"}
        )
        assert resp.status_code == 200
        assert resp.json()["done"] is False

    def test_evaluate_with_valid_token(self, gateway_client):
        client, _, _ = gateway_client
        token = self._acquire_token(client)
        resp = client.post("/evaluate", json={"token": token})
        assert resp.status_code == 200
        assert resp.json()["score"] == 0.75

    def test_invalid_token_returns_404(self, gateway_client):
        client, _, _ = gateway_client
        resp = client.post("/reset", json={"token": "bad-token"})
        assert resp.status_code == 404

    def test_release_invalidates_token(self, gateway_client):
        client, _, _ = gateway_client
        token = self._acquire_token(client)
        resp = client.post("/release", json={"token": token})
        assert resp.status_code == 200
        # Token should be gone
        resp = client.post("/reset", json={"token": token})
        assert resp.status_code == 404

    def test_release_invalid_token_404(self, gateway_client):
        client, _, _ = gateway_client
        resp = client.post("/release", json={"token": "nope"})
        assert resp.status_code == 404

    def test_step_invalid_token_404(self, gateway_client):
        client, _, _ = gateway_client
        resp = client.post(
            "/step", json={"token": "nope", "action": "click(0,0)"}
        )
        assert resp.status_code == 404

    def test_evaluate_invalid_token_404(self, gateway_client):
        client, _, _ = gateway_client
        resp = client.post("/evaluate", json={"token": "nope"})
        assert resp.status_code == 404
