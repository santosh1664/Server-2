# Server 2 — Browser Challenge Intelligence

Standalone FastAPI + SeleniumBase service for browser diagnostics, passive challenge classification, and a local synthetic verification demo.

## Current scope

- Standard SeleniumBase browser lifecycle for controlled QA.
- Read-only page inspection and provider-signature evidence collection.
- Explicit challenge-state transitions.
- Provider adapter contracts and server-side verification architecture.
- Signed HTTPS callback helper.
- Local arithmetic challenge demo for exercising the state lifecycle.

This repository does not include UC/stealth configuration, CAPTCHA-clicking logic, or third-party challenge bypass code. It does not call SeleniumBase's `sb.solve_captcha()`. A page challenge is not considered verified merely because browser automation returned; only a provider-confirmed result can be marked verified.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the module diagram and [docs/patchright-vs-seleniumbase.md](docs/patchright-vs-seleniumbase.md) for the browser framework comparison.

## Setup

Python 3.11+ and Chromium are required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

Open http://127.0.0.1:8080/docs.

Enable the local synthetic demo only in development with `CAPTCHA_DEMO_ENABLED=true`.

The inspection endpoint accepts HTTPS URLs and blocks local/private/reserved destinations. Application-level URL checks are not a replacement for network egress firewall rules.

## Endpoints

- `GET /health`
- `GET /api/v1/providers`
- `POST /api/v1/inspect`
- `POST /api/v1/demo/challenges` (development-only, disabled by default)
- `POST /api/v1/demo/challenges/{challenge_id}/verify` (development-only)

Authenticated endpoints require `X-API-Key`.

## Production gaps

Before production, add:
- Redis/PostgreSQL persistence and a durable job queue.
- Browser process/container isolation and concurrency limits.
- DNS-rebinding-resistant egress controls and redirect revalidation.
- Provider-specific response validation, hostname allowlists and secret rotation.
- Rate limiting, audit retention, metrics and structured logs.
- Rejekt job intake and signed callback endpoint contracts.
- Integration tests against provider-owned test configurations.

The in-memory session and synthetic demo stores are not production storage.
