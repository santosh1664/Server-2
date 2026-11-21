from fastapi import Depends, FastAPI, HTTPException
from app.config import settings
from app.demo.service import SyntheticChallengeService
from app.orchestration.coordinator import ChallengeCoordinator
from app.schemas import InspectRequest, InspectResponse, DemoVerifyRequest
from app.security import require_api_key

app = FastAPI(
    title="Server 2 — Browser Challenge Intelligence",
    version="0.2.0",
    description=(
        "Read-only browser diagnostics and a local synthetic verification demo. "
        "No third-party CAPTCHA solving or bypass is implemented."
    ),
)
demo = SyntheticChallengeService(
    settings.demo_challenge_ttl_seconds,
    settings.demo_max_attempts,
)
coordinator = ChallengeCoordinator()


@app.get("/health")
def health():
    return {"status": "ok", "service": "server-2"}


@app.get("/api/v1/providers", dependencies=[Depends(require_api_key)])
def providers():
    return {
        "configured": [],
        "available_interfaces": ["recaptcha", "hcaptcha", "turnstile"],
        "note": "Provider adapter contracts only; no provider adapters are configured.",
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
