# Official CAPTCHA provider token verification

Server 2 can verify short-lived tokens issued by CAPTCHA widgets configured on websites operated by the service owner. This is **server-side token verification**, not automated CAPTCHA solving.

A website renders its provider widget. After the challenge is completed through the provider's supported flow, the browser receives a short-lived token. The website sends that token to its backend, and the backend (or a trusted service such as Server 2) verifies it with the provider's official Siteverify API.

Server 2 does not solve image puzzles, automate challenge interactions, or manufacture provider tokens.

## Supported adapters

| Provider | Official verification endpoint |
|---|---|
| Google reCAPTCHA | https://www.google.com/recaptcha/api/siteverify |
| hCaptcha | https://api.hcaptcha.com/siteverify |
| Cloudflare Turnstile | https://challenges.cloudflare.com/turnstile/v0/siteverify |

## Configuration

Copy .env.example to .env. Set secrets only in the deployment environment or secret manager. Never commit .env.

- RECAPTCHA_SECRET_KEY, RECAPTCHA_ALLOWED_HOSTNAMES
- HCAPTCHA_SECRET_KEY, HCAPTCHA_SITEKEY, HCAPTCHA_ALLOWED_HOSTNAMES
- TURNSTILE_SECRET_KEY, TURNSTILE_ALLOWED_HOSTNAMES

Hostnames are exact comma-separated hostnames, not URLs or wildcard patterns. Use separate provider keys for development/test and production.

For reCAPTCHA v3, optionally configure RECAPTCHA_EXPECTED_ACTION and RECAPTCHA_MINIMUM_SCORE. For Turnstile, optionally configure TURNSTILE_EXPECTED_ACTION.

## API

All endpoints require X-API-Key.

GET /api/v1/providers lists configured adapters without exposing credentials.

POST /api/v1/verify/turnstile

Request:

~~~json
{
  "token": "provider-issued-short-lived-token"
}
~~~

The same route pattern is available for recaptcha and hcaptcha.

Response example:

~~~json
{
  "status": "verified",
  "workflow_state": "verified",
  "verified": true,
  "provider": "turnstile",
  "hostname": "example.com",
  "action": "contact",
  "score": null,
  "error_codes": [],
  "reason": null
}
~~~

Possible statuses:

- verified: provider accepted the token and configured hostname/action checks passed.
- rejected: provider rejected the token or a configured claim did not match.
- unavailable: provider could not be reached or returned an unusable response. Fail closed and route to review/retry; never treat this as verified.

Tokens are not persisted or logged. Provider tokens are short-lived and single-use; request a fresh token after a failed or expired attempt.

## Provider-specific behavior

- Google reCAPTCHA tokens are verified using Google's Siteverify endpoint. The response hostname is checked against the configured exact hostname allowlist. If an expected v3 action is configured, it must match. A score threshold is applied when a score is returned.
- hCaptcha verification includes the configured sitekey in the Siteverify request. hCaptcha documents that its hostname field may be absent or not-provided; when present, Server 2 rejects a hostname outside the configured allowlist. The sitekey binding is also checked by hCaptcha.
- Turnstile verification checks success, exact hostname, and the configured action when one is set.

## What this does not do

This endpoint does not retrieve a token from an arbitrary third-party page, interact with challenge puzzles, bypass browser integrity checks, or guarantee a challenge can be completed automatically. The token must come from the provider's supported widget flow on a configured site.

## Official references

- Google: https://developers.google.com/recaptcha/docs/verify
- hCaptcha: https://docs.hcaptcha.com/
- Cloudflare: https://developers.cloudflare.com/turnstile/get-started/server-side-validation/
