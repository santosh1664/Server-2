# Server 2 architecture

Server 2 is a standalone FastAPI service for read-only browser diagnostics and official server-side verification of provider-issued tokens.

## Provider token verification flow

~~~mermaid
flowchart TD
  A[Owned website renders provider widget] --> B[Provider issues short-lived token]
  B --> C[Owned website backend sends token to Server 2]
  C --> D[API key authentication]
  D --> E[Select configured provider adapter]
  E --> F[Call official Siteverify API]
  F --> G{Provider success and configured claims match?}
  G -->|Yes| H[verified]
  G -->|No| I[rejected]
  F -->|Network or provider unavailable| J[unavailable / human review]
~~~

## Components

- app/browser/: standard SeleniumBase lifecycle and read-only diagnostics.
- app/detection/: passive provider-signature classification.
- app/providers/base.py: provider adapter contract and normalized result.
- app/providers/siteverify.py: Google reCAPTCHA, hCaptcha and Turnstile Siteverify adapters.
- app/captcha/result_validator.py: reusable result validation helper.
- app/orchestration/coordinator.py: maps provider outcomes to workflow states.
- app/main.py: authenticated API endpoints.
- app/integrations/rejekt.py: signed HTTPS callback helper; callback contract is not yet connected to a job endpoint.

## Security boundaries

- Exact provider hostnames are configured server-side; callers cannot supply an expected hostname.
- Provider secrets remain server-side.
- Tokens are not logged, stored, or returned.
- Provider timeouts and malformed responses fail closed.
- Provider verification is not CAPTCHA puzzle solving or anti-bot bypass.
- Rejekt callback delivery must be connected only after its exact API contract is known.
