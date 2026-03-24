"""Unit tests for gateway/models.py."""

import pytest
from pydantic import ValidationError

from gateway.models import (
    AcquireResponse,
    EnvState,
    EvaluateResponse,
    MasterAcquireResponse,
    MasterResetRequest,
    MasterStepRequest,
    Observation,
    ReleaseResponse,
    ResetRequest,
    StepRequest,
    StepResponse,
    WorkerRegisterRequest,
    WorkerStatusResponse,
    EnvSlotStatus,
)


class TestEnvState:
    def test_values(self):
        assert EnvState.idle == "idle"
        assert EnvState.acquired == "acquired"
        assert EnvState.busy == "busy"
        assert EnvState.error == "error"

    def test_all_members(self):
        assert set(EnvState) == {
            EnvState.idle,
            EnvState.acquired,
            EnvState.busy,
            EnvState.error,
        }


class TestObservation:
    def test_full_fields_roundtrip(self):
        obs = Observation(
            screenshot_base64="abc123==",
            accessibility_tree="<tree/>",
            terminal="$ ls",
            instruction="Open Firefox",
        )
        data = obs.model_dump()
        restored = Observation.model_validate(data)
        assert restored == obs

    def test_optional_fields_none(self):
        obs = Observation()
        assert obs.screenshot_base64 is None
        assert obs.accessibility_tree is None
        assert obs.terminal is None
        assert obs.instruction is None

    def test_json_roundtrip(self):
        obs = Observation(screenshot_base64="abc", instruction="do X")
        json_str = obs.model_dump_json()
        restored = Observation.model_validate_json(json_str)
        assert restored == obs


class TestStepRequest:
    def test_default_pause(self):
        req = StepRequest(local_env_id=0, action="click(100,200)")
        assert req.pause == 2.0

    def test_custom_pause(self):
        req = StepRequest(local_env_id=0, action="click(100,200)", pause=5.0)
        assert req.pause == 5.0


class TestWorkerModels:
    def test_acquire_response(self):
        resp = AcquireResponse(local_env_id=2, vnc_port=5902)
        assert resp.local_env_id == 2
        assert resp.vnc_port == 5902

    def test_step_response_roundtrip(self):
        resp = StepResponse(
            observation=Observation(screenshot_base64="img"),
            reward=0.5,
            done=False,
            info={"step": 1},
        )
        data = resp.model_dump()
        restored = StepResponse.model_validate(data)
        assert restored.reward == 0.5
        assert restored.info == {"step": 1}

    def test_evaluate_response(self):
        resp = EvaluateResponse(score=0.85)
        assert resp.score == 0.85

    def test_release_response(self):
        resp = ReleaseResponse(success=True)
        assert resp.success is True

    def test_reset_request_optional_task_config(self):
        req = ResetRequest(local_env_id=0)
        assert req.task_config is None

    def test_worker_status_response(self):
        resp = WorkerStatusResponse(
            worker_id="w1",
            total_envs=4,
            free_envs=2,
            envs=[
                EnvSlotStatus(local_env_id=0, state=EnvState.idle, vnc_port=5900),
                EnvSlotStatus(local_env_id=1, state=EnvState.acquired, vnc_port=5901),
            ],
        )
        assert resp.total_envs == 4
        assert len(resp.envs) == 2


class TestMasterModels:
    def test_master_acquire_response(self):
        resp = MasterAcquireResponse(
            token="tok-123", vnc_port=5900, worker_url="http://w1:9100"
        )
        assert resp.token == "tok-123"

    def test_master_reset_request_inherits_token(self):
        req = MasterResetRequest(token="tok-1", task_config={"id": "task-1"})
        assert req.token == "tok-1"
        assert req.task_config == {"id": "task-1"}

    def test_master_step_request_default_pause(self):
        req = MasterStepRequest(token="tok-1", action="type('hello')")
        assert req.pause == 2.0


class TestWorkerRegisterRequest:
    def test_roundtrip(self):
        req = WorkerRegisterRequest(
            worker_id="w1",
            worker_url="http://10.0.0.1:9100",
            total_envs=4,
            free_envs=3,
        )
        data = req.model_dump()
        restored = WorkerRegisterRequest.model_validate(data)
        assert restored == req


class TestValidationErrors:
    def test_step_request_missing_action(self):
        with pytest.raises(ValidationError):
            StepRequest(local_env_id=0)

    def test_acquire_response_missing_fields(self):
        with pytest.raises(ValidationError):
            AcquireResponse(local_env_id=0)

    def test_master_acquire_missing_token(self):
        with pytest.raises(ValidationError):
            MasterAcquireResponse(vnc_port=5900, worker_url="http://w1:9100")
