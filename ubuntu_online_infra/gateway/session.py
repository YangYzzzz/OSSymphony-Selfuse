"""Token-based session manager for Master gateway."""

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Session:
    token: str
    worker_url: str
    local_env_id: int
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)


class SessionManager:
    """Thread-safe token → Session mapping with expiry support."""

    def __init__(self, timeout: float = 1800.0): # 1800s timeout
        self._sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_session(self, worker_url: str, local_env_id: int) -> str:
        token = uuid.uuid4().hex
        session = Session(
            token=token,
            worker_url=worker_url,
            local_env_id=local_env_id,
        )
        with self._lock:
            self._sessions[token] = session
        return token

    def get_session(self, token: str) -> Optional[Session]:
        with self._lock:
            session = self._sessions.get(token)
            if session is not None:
                session.last_activity = time.time()
            return session

    def remove_session(self, token: str) -> Optional[Session]:
        with self._lock:
            return self._sessions.pop(token, None)

    def cleanup_expired(self) -> List[Session]:
        """Remove and return sessions that have exceeded the timeout."""
        now = time.time()
        expired: List[Session] = []
        with self._lock:
            tokens_to_remove = [
                tok
                for tok, sess in self._sessions.items()
                if now - sess.last_activity > self.timeout
            ]
            for tok in tokens_to_remove:
                expired.append(self._sessions.pop(tok))
        return expired
    
    def cleanup_all(self) -> List[Session]:
        """Remove and return all sessions."""
        with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
        return sessions
    
    @property
    def count(self) -> int:
        with self._lock:
            return len(self._sessions)
