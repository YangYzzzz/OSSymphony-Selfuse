"""Shared Pydantic request/response models for Master-Worker architecture."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EnvState(str, Enum):
    idle = "idle"
    acquired = "acquired"
    busy = "busy"
    error = "error"


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------

class Observation(BaseModel):
    screenshot_base64: Optional[str] = None
    accessibility_tree: Optional[str] = None
    terminal: Optional[str] = None
    instruction: Optional[str] = None
    code_result: Optional[str] = None


# ---------------------------------------------------------------------------
# Worker-level models
# ---------------------------------------------------------------------------

class AcquireResponse(BaseModel):
    local_env_id: int
    vnc_port: int


class ResetRequest(BaseModel):
    local_env_id: int
    task_config: Optional[Dict[str, Any]] = None


class ResetResponse(BaseModel):
    observation: Observation


class StepRequest(BaseModel):
    local_env_id: int
    action: str
    pause: float = 2.0


class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)


class EvaluateRequest(BaseModel):
    local_env_id: int


class EvaluateResponse(BaseModel):
    score: float


class ReleaseRequest(BaseModel):
    local_env_id: int


class ReleaseResponse(BaseModel):
    success: bool


class WorkerHealthResponse(BaseModel):
    status: str = "ok"


class EnvSlotStatus(BaseModel):
    local_env_id: int
    state: EnvState
    vnc_port: int


class WorkerStatusResponse(BaseModel):
    worker_id: str
    total_envs: int
    free_envs: int
    envs: List[EnvSlotStatus]


# ---------------------------------------------------------------------------
# Master-level models
# ---------------------------------------------------------------------------

class MasterAcquireResponse(BaseModel):
    token: str
    vnc_port: int
    worker_url: str


class TokenRequest(BaseModel):
    """Base class for requests that carry a session token."""
    token: str


class MasterResetRequest(TokenRequest):
    task_config: Optional[Dict[str, Any]] = None


class MasterStepRequest(TokenRequest):
    action: str
    pause: float = 2.0


class MasterEvaluateRequest(TokenRequest):
    pass


class MasterReleaseRequest(TokenRequest):
    pass


# ---------------------------------------------------------------------------
# Worker registration (heartbeat)
# ---------------------------------------------------------------------------

class WorkerRegisterRequest(BaseModel):
    worker_id: str
    worker_url: str
    total_envs: int
    free_envs: int
