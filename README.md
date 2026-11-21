# Server 2 — Browser Challenge Intelligence

Standalone FastAPI + SeleniumBase service for browser diagnostics, local synthetic challenge demonstrations, and official server-side verification of CAPTCHA provider tokens.

## Capabilities

- Standard SeleniumBase browser lifecycle and read-only page inspection.
- Passive challenge-signature detection.
- Server-side token verification adapters for Google reCAPTCHA, hCaptcha and Cloudflare Turnstile.
- Exact hostname allowlists and optional action/score checks.
- Local arithmetic challenge demo for exercising workflow states.
- API-key protected endpoints.

**Important:** Provider verification is not automated CAPTCHA solving. A token must first be issued by the provider's supported widget flow on a configured website. Server 2 validates that token with the provider's official Siteverify API. It does not solve visual puzzles or bypass third-party anti-bot protections.

## Setup

Python 3.11+ and a compatible Chrome/Chromium installation are required.

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
~~~

Set a strong API_KEY. Configure provider secrets in .env for local development or in a secret manager for deployment. Never commit .env.

## Endpoints

- GET /health
- GET /api/v1/providers (API key required)
- POST /api/v1/inspect (API key required)
- POST /api/v1/verify/{provider} (API key required; provider token verification)
- POST /api/v1/demo/challenges (API key + demo flag required)
- POST /api/v1/demo/challenges/{challenge_id}/verify (API key + demo flag required)

Pass the API key in the X-API-Key header.

## Provider verification

See docs/provider-verification.md for provider configuration, request/response examples and limitations.

Supported provider names: recaptcha, hcaptcha, turnstile.

## Synthetic demo

Set CAPTCHA_DEMO_ENABLED=true for local development, create a challenge, read the arithmetic prompt, and submit its answer to the verify endpoint. The demo is not a real CAPTCHA or a security control. Demo state is in memory and disappears on restart.

## Remaining integration work

- Connect the Rejekt callback to the exact Rejekt API contract.
- Durable job/session storage and queue.
- Browser process isolation, concurrency limits and network egress controls.
- Rate limiting, audit logging, metrics and secret rotation.
- End-to-end tests against provider-issued test keys configured for your own test hostnames.

Never treat passive challenge detection as proof of verification. Provider outages and invalid tokens fail closed.
