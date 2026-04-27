"""Local environment pool managing multiple DesktopEnv instances."""

import base64
import logging
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from gateway.models import EnvSlotStatus, EnvState, Observation

logger = logging.getLogger(__name__)

@dataclass
class EnvSlot:
    local_env_id: int
    env: Any  # DesktopEnv instance
    state: EnvState = EnvState.idle
    vnc_port: int = 0
    last_activity: float = field(default_factory=time.time)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)


class EnvPool:
    """Manages a pool of DesktopEnv instances on a single worker node."""

    def __init__(
        self,
        num_envs: int,
        env_factory: Callable[[int], Any],
        session_timeout: float = 1800.0,
    ):
        self.num_envs = num_envs
        self._env_factory = env_factory
        self.session_timeout = session_timeout
        self._slots: List[EnvSlot] = []
        self._pool_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start_all(self) -> None:
        """Create and start all DesktopEnv instances in parallel."""

        def _create(idx: int) -> EnvSlot:
            env = self._env_factory(idx)
            env.start()
            # Extract VNC port from the provider's ip_address string
            # Format: "127.0.0.1:server_port:chromium_port:vnc_port:vlc_port"
            vnc_port = self._extract_vnc_port(env)
            slot = EnvSlot(local_env_id=idx, env=env, vnc_port=vnc_port)
            logger.info("Started env slot %d (vnc_port=%d)", idx, vnc_port)
            return slot

        with ThreadPoolExecutor(max_workers=self.num_envs) as executor:
            futures = [executor.submit(_create, i) for i in range(self.num_envs)]
            self._slots = [f.result() for f in futures]
        # Sort by local_env_id to ensure consistent ordering
        self._slots.sort(key=lambda s: s.local_env_id)

    def shutdown_all(self) -> None:
        """Close all DesktopEnv instances in parallel."""

        def _close(slot: EnvSlot) -> None:
            try:
                slot.env.close()
            except Exception:
                logger.exception("Error closing env %d", slot.local_env_id)

        with ThreadPoolExecutor(max_workers=self.num_envs) as executor:
            list(executor.map(_close, self._slots))
        self._slots.clear()

    # ------------------------------------------------------------------
    # Acquire / Release
    # ------------------------------------------------------------------

    def acquire(self) -> Optional[EnvSlot]:
        """Find the first IDLE slot and mark it ACQUIRED. Returns None if full."""
        with self._pool_lock:
            for slot in self._slots:
                if slot.state == EnvState.idle:
                    slot.state = EnvState.acquired
                    slot.last_activity = time.time()
                    return slot
        return None

    def release(self, local_env_id: int) -> bool:
        slot = self._get_slot(local_env_id)
        if slot is None:
            return False
        with slot.lock:
            slot.state = EnvState.idle
            slot.last_activity = time.time()
        return True

    # ------------------------------------------------------------------
    # Environment operations
    # ------------------------------------------------------------------

    def reset_env(
        self, local_env_id: int, task_config: Optional[Dict[str, Any]] = None
    ) -> Observation:
        slot = self._get_slot(local_env_id)
        if slot is None:
            raise ValueError(f"Invalid local_env_id: {local_env_id}")
        with slot.lock:
            slot.state = EnvState.busy
            slot.last_activity = time.time()
            try:
                obs_dict = slot.env.reset(task_config=task_config)
                slot.state = EnvState.acquired
                return self._obs_to_model(obs_dict)
            except Exception:
                slot.state = EnvState.error
                raise

    def step_env(
        self, local_env_id: int, action: str, pause: float = 2.0
    ) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        slot = self._get_slot(local_env_id)
        if slot is None:
            raise ValueError(f"Invalid local_env_id: {local_env_id}")
        with slot.lock:
            slot.state = EnvState.busy
            slot.last_activity = time.time()
            try:
                code_result = ""
                if action.startswith("BASH") or action.startswith("PYTHON"):
                    if action.startswith("BASH"):
                        code = action[5:]
                        result = slot.env.controller.run_bash_script(code)
                    else:
                        code = action[7:]
                        result = slot.env.controller.run_python_script(code)
                    if result:
                        code_result += f"Status: {result.get('status', '')}\n"
                        code_result += f"Output: {result.get('output', '')}\n"
                        code_result += f"Error: {result.get('error', '')}\n"
                        if action.startswith("BASH"):
                            code_result += f"Return Code: {result.get('returncode', 0)}\n"
                            
                obs_dict, reward, done, info = slot.env.step(action, pause=pause)
                obs_dict['code_result'] = code_result
                
                slot.state = EnvState.acquired
                return self._obs_to_model(obs_dict), reward, done, info
            except Exception:
                slot.state = EnvState.error
                raise

    def evaluate_env(self, local_env_id: int) -> float:
        slot = self._get_slot(local_env_id)
        if slot is None:
            raise ValueError(f"Invalid local_env_id: {local_env_id}")
        with slot.lock:
            slot.state = EnvState.busy
            slot.last_activity = time.time()
            try:
                score = slot.env.evaluate()
                slot.state = EnvState.acquired
                return score
            except Exception:
                slot.state = EnvState.error
                raise

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def get_status(self) -> List[EnvSlotStatus]:
        return [
            EnvSlotStatus(
                local_env_id=s.local_env_id,
                state=s.state,
                vnc_port=s.vnc_port,
            )
            for s in self._slots
        ]

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def health_check(self) -> str:
        """Check all envs' underlying docker/VM health.

        Returns a short summary string and logs details.
        """
        total = len(self._slots)
        healthy_ids: List[int] = []
        unhealthy_ids: List[int] = []

        for slot in self._slots:
            env = slot.env
            try:
                ok = env.check_health()
            except Exception:
                logger.exception("health_check: error checking env %d", slot.local_env_id)
                ok = False

            if ok:
                if slot.state == EnvState.error:
                    slot.state = EnvState.acquired # Anyway, wait for cleanup expired
                healthy_ids.append(slot.local_env_id)
            else: # Current Logic：Even state is Error, env still work.
                slot.state = EnvState.error
                unhealthy_ids.append(slot.local_env_id)

        if total == 0:
            summary = "no env slots configured"
        elif not unhealthy_ids:
            summary = f"all {total} envs healthy"
        else:
            summary = f"{len(unhealthy_ids)}/{total} envs unhealthy: ids={unhealthy_ids}"

        if len(unhealthy_ids) == 0:
            logger.info(
                "EnvPool health_check summary: %s (healthy=%s, unhealthy=%s)",
                summary,
                healthy_ids,
                unhealthy_ids,
            )
        else:
            logger.error(
                "EnvPool health_check summary: %s (healthy=%s, unhealthy=%s)",
                summary,
                healthy_ids,
                unhealthy_ids,
            )
        return summary
        
    def get_free_count(self) -> int:
        return sum(1 for s in self._slots if s.state == EnvState.idle)

    def get_free_ids(self) -> List:
        return [ids for ids, s in enumerate(self._slots) if s.state == EnvState.idle]

    def get_health_ids(self) -> List:
        return [ids for ids, s in enumerate(self._slots) if s.state != EnvState.error]

    def cleanup_expired(self) -> List[int]:
        """Release slots that have been acquired but inactive beyond timeout.
        Returns list of released local_env_ids."""
        now = time.time()
        released: List[int] = []
        for slot in self._slots:
            if (
                slot.state == EnvState.acquired
                and now - slot.last_activity > self.session_timeout
            ):
                with slot.lock:
                    if (
                        slot.state == EnvState.acquired
                        and now - slot.last_activity > self.session_timeout
                    ):
                        slot.state = EnvState.idle
                        released.append(slot.local_env_id)
                        logger.info(
                            "Auto-released expired env %d", slot.local_env_id
                        )
        return released

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_slot(self, local_env_id: int) -> Optional[EnvSlot]:
        for slot in self._slots:
            if slot.local_env_id == local_env_id:
                return slot
        return None

    @staticmethod
    def _extract_vnc_port(env: Any) -> int:
        """Extract VNC port from DesktopEnv instance."""
        try:
            return env.vnc_port
        except AttributeError:
            return 0

    @staticmethod
    def _obs_to_model(obs_dict: Dict[str, Any]) -> Observation:
        """Convert raw DesktopEnv observation dict to Observation model."""
        screenshot = obs_dict.get("screenshot")
        screenshot_b64 = None
        if screenshot is not None:
            if isinstance(screenshot, bytes):
                screenshot_b64 = base64.b64encode(screenshot).decode("ascii")
            elif isinstance(screenshot, str):
                screenshot_b64 = screenshot
        return Observation(
            screenshot_base64=screenshot_b64,
            accessibility_tree=obs_dict.get("accessibility_tree"),
            terminal=obs_dict.get("terminal"),
            instruction=obs_dict.get("instruction"),
            code_result=obs_dict.get("code_result")
        )
