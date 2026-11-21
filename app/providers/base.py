from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class VerificationResult:
    """Sanitized outcome from an official provider Siteverify endpoint."""

    verified: bool
    provider: str
    reason: str | None = None
    hostname: str | None = None
    action: str | None = None
    score: float | None = None
    error_codes: list[str] = field(default_factory=list)
    available: bool = True


class VerificationAdapter(ABC):
    """Interface for site-owner-configured server-side token verification."""

    provider: str

    @abstractmethod
    async def verify(self, token: str, **context) -> VerificationResult:
        raise NotImplementedError
