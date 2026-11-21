from fastapi import Depends, FastAPI, HTTPException

from app.config import settings
from app.demo.service import SyntheticChallengeService
from app.orchestration.coordinator import ChallengeCoordinator
from app.providers.siteverify import build_provider_registry
from app.schemas import (
    DemoVerifyRequest,
    InspectRequest,
    InspectResponse,
    ProviderVerifyRequest,
    ProviderVerifyResponse,
)
from app.security import require_api_key

app = FastAPI(
    title="Server 2 — Browser Challenge Intelligence",
    version="0.3.0",
    description=(
        "Browser diagnostics, synthetic challenge demonstrations, and "
        "official server-side verification of provider-issued tokens."
    ),
)
demo = SyntheticChallengeService(
    settings.demo_challenge_ttl_seconds,
    settings.demo_max_attempts,
)
coordinator = ChallengeCoordinator()
provider_registry = build_provider_registry(settings)


@app.get("/health")
def health():
    return {"status": "ok", "service": "server-2"}


@app.get("/api/v1/providers", dependencies=[Depends(require_api_key)])
def providers():
    return {
        "configured": provider_registry.names(),
        "supported": ["recaptcha", "hcaptcha", "turnstile"],
        "verification": "Official provider Siteverify APIs; no challenge bypass.",
    }


@app.post(
    "/api/v1/inspect",
    response_model=InspectResponse,
    dependencies=[Depends(require_api_key)],
)
def inspect(request: InspectRequest):
    from app.browser.inspector import SeleniumBaseInspector

    try:
        return SeleniumBaseInspector().inspect(str(request.url))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Browser inspection failed: {type(exc).__name__}",
        ) from exc


@app.post(
    "/api/v1/verify/{provider}",
    response_model=ProviderVerifyResponse,
    dependencies=[Depends(require_api_key)],
)
async def verify_provider(provider: str, request: ProviderVerifyRequest):
    adapter = provider_registry.get(provider.lower())
    if adapter is None:
        raise HTTPException(
            status_code=503,
            detail=f"Provider '{provider}' is not configured on Server 2",
        )

    # The token is forwarded only to the matching provider's official
    # Siteverify endpoint. It is not logged, stored, or returned to callers.
    result = await adapter.verify(request.token.get_secret_value())

    if not result.available:
        status = "unavailable"
    elif result.verified:
        status = "verified"
    else:
        status = "rejected"

    return ProviderVerifyResponse(
        status=status,
        verified=result.verified,
        provider=result.provider,
        hostname=result.hostname,
        action=result.action,
        score=result.score,
        error_codes=result.error_codes,
        reason=result.reason,
    )


@app.post("/api/v1/demo/challenges", dependencies=[Depends(require_api_key)])
def create_demo():
    if not settings.captcha_demo_enabled:
        raise HTTPException(status_code=404, detail="Synthetic demo is disabled")
    return demo.create()


@app.post(
    "/api/v1/demo/challenges/{challenge_id}/verify",
    dependencies=[Depends(require_api_key)],
)
def verify_demo(challenge_id: str, request: DemoVerifyRequest):
    if not settings.captcha_demo_enabled:
        raise HTTPException(status_code=404, detail="Synthetic demo is disabled")

    result = demo.verify(challenge_id, request.answer)
    state = coordinator.synthetic_verification_state(result)
    return {**result, "workflow_state": state.value}
