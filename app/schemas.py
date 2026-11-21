from pydantic import BaseModel, Field, HttpUrl, SecretStr


class InspectRequest(BaseModel):
    url: HttpUrl


class InspectResponse(BaseModel):
    status: str
    title: str | None = None
    final_url: str | None = None
    challenge_detected: bool
    providers: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    note: str = "Read-only diagnostics; no CAPTCHA interaction or solving."


class DemoVerifyRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=16)


class ProviderVerifyRequest(BaseModel):
    # Tokens are sensitive, short-lived and single-use. Never log or persist them.
    token: SecretStr


class ProviderVerifyResponse(BaseModel):
    status: str
    workflow_state: str
    verified: bool
    provider: str
    hostname: str | None = None
    action: str | None = None
    score: float | None = None
    error_codes: list[str] = Field(default_factory=list)
    reason: str | None = None
