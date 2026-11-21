from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class VerificationResult:
    verified: bool
    provider: str
    reason: str | None = None
    hostname: str | None = None
    action: str | None = None

class VerificationAdapter(ABC):
    """Interface for site-owner-configured server-side verification APIs."""
    provider: str
    @abstractmethod
    async def verify(self, token: str, **context) -> VerificationResult:
        raise NotImplementedError
