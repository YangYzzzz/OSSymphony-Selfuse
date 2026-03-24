"""Unit tests for worker/env_pool.py (using mock DesktopEnv)."""

import base64
import time

import pytest

from gateway.models import EnvState, Observation
from worker.env_pool import EnvPool


class TestEnvPoolStartup:
    def test_start_all_creates_n_slots(self, env_factory):
        pool = EnvPool(num_envs=4, env_factory=env_factory)
        pool.start_all()
        assert len(pool._slots) == 4
        for i, slot in enumerate(pool._slots):
            assert slot.local_env_id == i
            slot.env.start.assert_called_once()

    def test_shutdown_all_closes_envs(self, env_factory):
        pool = EnvPool(num_envs=3, env_factory=env_factory)
        pool.start_all()
        envs = [s.env for s in pool._slots]
        pool.shutdown_all()
        for env in envs:
            env.close.assert_called_once()
        assert len(pool._slots) == 0


class TestAcquireRelease:
    def test_acquire_returns_idle_slot(self, env_factory):
        pool = EnvPool(num_envs=2, env_factory=env_factory)
        pool.start_all()
        slot = pool.acquire()
        assert slot is not None
        assert slot.state == EnvState.acquired

    def test_acquire_all_then_none(self, env_factory):
        pool = EnvPool(num_envs=2, env_factory=env_factory)
        pool.start_all()
        s1 = pool.acquire()
        s2 = pool.acquire()
        s3 = pool.acquire()
        assert s1 is not None
        assert s2 is not None
        assert s3 is None

    def test_release_sets_idle(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        pool.start_all()
        slot = pool.acquire()
        assert pool.release(slot.local_env_id) is True
        assert slot.state == EnvState.idle

    def test_release_invalid_id(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        pool.start_all()
        assert pool.release(999) is False


class TestResetEnv:
    def test_reset_calls_env_reset(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        pool.start_all()
        slot = pool.acquire()
        obs = pool.reset_env(slot.local_env_id, task_config={"id": "task1"})
        slot.env.reset.assert_called_once_with(task_config={"id": "task1"})
        assert isinstance(obs, Observation)
        assert obs.instruction == "Open the terminal"

    def test_reset_state_transitions(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        pool.start_all()
        slot = pool.acquire()
        pool.reset_env(slot.local_env_id)
        # After successful reset, state should be ACQUIRED
        assert slot.state == EnvState.acquired

    def test_reset_invalid_id_raises(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        pool.start_all()
        with pytest.raises(ValueError):
            pool.reset_env(999)


class TestStepEnv:
    def test_step_returns_full_response(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        pool.start_all()
        slot = pool.acquire()
        pool.reset_env(slot.local_env_id)
        obs, reward, done, info = pool.step_env(slot.local_env_id, "click(100,200)")
        assert isinstance(obs, Observation)
        assert reward == 0.0
        assert done is False
        assert isinstance(info, dict)
        slot.env.step.assert_called_once_with("click(100,200)", pause=2.0)


class TestEvaluateEnv:
    def test_evaluate_returns_score(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        pool.start_all()
        slot = pool.acquire()
        pool.reset_env(slot.local_env_id)
        score = pool.evaluate_env(slot.local_env_id)
        assert score == 1.0
        slot.env.evaluate.assert_called_once()


class TestObsConversion:
    def test_obs_to_model_base64_encoding(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        raw_bytes = b"\x89PNG fake"
        obs = pool._obs_to_model({"screenshot": raw_bytes, "instruction": "test"})
        assert obs.screenshot_base64 == base64.b64encode(raw_bytes).decode("ascii")

    def test_obs_to_model_screenshot_none(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        obs = pool._obs_to_model({"screenshot": None, "instruction": "test"})
        assert obs.screenshot_base64 is None

    def test_obs_to_model_screenshot_already_string(self, env_factory):
        pool = EnvPool(num_envs=1, env_factory=env_factory)
        obs = pool._obs_to_model({"screenshot": "already_b64", "instruction": "test"})
        assert obs.screenshot_base64 == "already_b64"


class TestStatus:
    def test_get_status(self, env_factory):
        pool = EnvPool(num_envs=3, env_factory=env_factory)
        pool.start_all()
        pool.acquire()
        statuses = pool.get_status()
        assert len(statuses) == 3
        assert statuses[0].state == EnvState.acquired
        assert statuses[1].state == EnvState.idle

    def test_get_free_count(self, env_factory):
        pool = EnvPool(num_envs=3, env_factory=env_factory)
        pool.start_all()
        assert pool.get_free_count() == 3
        pool.acquire()
        assert pool.get_free_count() == 2

    def test_cleanup_expired(self, env_factory):
        pool = EnvPool(num_envs=2, env_factory=env_factory, session_timeout=0.05)
        pool.start_all()
        slot = pool.acquire()
        time.sleep(0.1)
        released = pool.cleanup_expired()
        assert slot.local_env_id in released
        assert slot.state == EnvState.idle
