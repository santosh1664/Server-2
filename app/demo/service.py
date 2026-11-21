from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from secrets import randbelow
from threading import RLock
from uuid import uuid4


@dataclass
class Record:
    id: str
    prompt: str
    answer: int
    expires_at: datetime
    attempts: int
    max_attempts: int
    status: str = "pending"


class SyntheticChallengeService:
    """Local arithmetic demo only; not a real CAPTCHA or security control."""

    def __init__(self, ttl_seconds: int = 60, max_attempts: int = 3):
        if ttl_seconds < 1 or max_attempts < 1:
            raise ValueError("TTL and max_attempts must be positive")
        self.ttl_seconds = ttl_seconds
        self.max_attempts = max_attempts
        self.records: dict[str, Record] = {}
        self._lock = RLock()

    def create(self) -> dict:
        a, b = randbelow(9) + 1, randbelow(9) + 1
        challenge_id = str(uuid4())
        expiry = datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds)
        prompt = f"What is {a} + {b}?"
        with self._lock:
            self.records[challenge_id] = Record(
                challenge_id, prompt, a + b, expiry, 0, self.max_attempts
            )
        return {
            "id": challenge_id,
            "kind": "arithmetic-demo",
            "prompt": prompt,
            "expires_at": expiry.isoformat(),
            "status": "pending",
            "warning": "Synthetic educational challenge; not a real CAPTCHA.",
        }

    def verify(self, challenge_id: str, answer: str) -> dict:
        with self._lock:
            rec = self.records.get(challenge_id)
            if rec is None:
                return {
                    "accepted": False, "status": "failed",
                    "attempts_remaining": 0, "reason": "Unknown challenge",
                }
            if rec.status != "pending":
                return {
                    "accepted": rec.status == "verified",
                    "status": rec.status,
                    "attempts_remaining": max(0, rec.max_attempts - rec.attempts),
                    "reason": "Challenge is no longer pending",
                }
            if datetime.now(timezone.utc) >= rec.expires_at:
                rec.status = "expired"
                return {
                    "accepted": False, "status": "expired",
                    "attempts_remaining": 0, "reason": "Challenge expired",
                }

            rec.attempts += 1
            ok = answer.strip().isdigit() and int(answer.strip()) == rec.answer
            if ok:
                rec.status = "verified"
            elif rec.attempts >= rec.max_attempts:
                rec.status = "failed"

            return {
                "accepted": ok,
                "status": rec.status,
                "attempts_remaining": max(0, rec.max_attempts - rec.attempts),
                "reason": None if ok else "Incorrect answer",
            }
