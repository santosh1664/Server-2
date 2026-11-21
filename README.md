# Server 2 — Browser Challenge Intelligence

Standalone FastAPI + SeleniumBase service for browser diagnostics, challenge classification, and a local synthetic verification demo.

## Scope
This starter does not bypass third-party CAPTCHA/anti-bot systems, automate third-party challenge widgets, generate provider tokens, or submit external applications. It supports read-only browser inspection, evidence classification, and a local arithmetic challenge lifecycle.

## Setup
Python 3.11+ and Chromium are required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080/docs`.

Enable the local demo only in development with `CAPTCHA_DEMO_ENABLED=true`.
The browser inspection endpoint accepts HTTPS URLs and rejects local/private IP destinations. Add network-level egress controls too.

Before production: add durable Redis/PostgreSQL storage, rate limits, audit retention, secret rotation, TLS/private networking, and deployment-specific browser isolation. The in-memory demo is not production storage.
