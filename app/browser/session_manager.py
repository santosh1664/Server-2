from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4


@dataclass
class BrowserSession:
    session_id: str
    status: str
    created_at: str
    metadata: dict = field(default_factory=dict)


class SessionManager:
    """In-memory session metadata registry; use durable storage in production."""
    def __init__(self):
        self._sessions: dict[str, BrowserSession] = {}
        self._lock = RLock()

    def create(self, metadata: dict | None = None) -> BrowserSession:
        session = BrowserSession(str(uuid4()), "created", datetime.now(timezone.utc).isoformat(), metadata or {})
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def set_status(self, session_id: str, status: str) -> BrowserSession:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                raise KeyError("Unknown browser session")
            session.status = status
            return session

    def get(self, session_id: str) -> BrowserSession | None:
        with self._lock:
            return self._sessions.get(session_id)

    def close(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None
