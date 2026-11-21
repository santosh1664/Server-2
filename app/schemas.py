from pydantic import BaseModel, Field, HttpUrl

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
