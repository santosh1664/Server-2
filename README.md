# Server 2 — Browser Challenge Intelligence

Standalone FastAPI + SeleniumBase service for read-only browser diagnostics and a local synthetic challenge demonstration.

## Scope

- Standard SeleniumBase browser lifecycle.
- Read-only page inspection and passive challenge-signature detection.
- Provider adapter interfaces (not configured by default).
- Local arithmetic challenge demo for exercising workflow states.
- API-key protected endpoints.

This project does **not** implement UC/stealth mode, SeleniumBase `solve_captcha()`, third-party CAPTCHA solving, or anti-bot bypass. The arithmetic demo is not a real CAPTCHA or security control.

## Setup

Python 3.11+ and a compatible Chrome/Chromium installation are required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

Set a strong `API_KEY`. Enable the synthetic demo only in local development:

```dotenv
CAPTCHA_DEMO_ENABLED=true
```

Open http://127.0.0.1:8080/docs.

## Endpoints

- `GET /health`
- `GET /api/v1/providers` (API key required)
- `POST /api/v1/inspect` (API key required)
- `POST /api/v1/demo/challenges` (API key + demo flag required)
- `POST /api/v1/demo/challenges/{challenge_id}/verify` (API key + demo flag required)

Pass the API key in the `X-API-Key` header.

## Synthetic demo

1. Create a challenge.
2. Read the arithmetic prompt.
3. Submit an answer to the verify endpoint.
4. Observe `verified`, `pending`, `failed`, or `expired` and its workflow state.

The service stores demo challenges in memory. They disappear on restart and are not suitable for production.

## Production gaps

- Durable job/session storage and queue.
- Browser process isolation and concurrency limits.
- Network egress controls and redirect/DNS revalidation.
- Provider-specific server-side verification adapters for sites whose owners configure them.
- Rejekt callback implementation and integration tests.
- Rate limiting, audit logging, metrics and secret rotation.

Do not treat challenge detection as proof of a challenge being solved.
