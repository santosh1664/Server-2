"""Official server-side CAPTCHA token verification adapters.

These adapters validate a token issued by a provider widget on a site the
operator controls. They do not solve visual challenges, automate challenge
interactions, or bypass anti-bot protections.
"""
from __future__ import annotations

from typing import Any

import httpx

from app.providers.base import VerificationAdapter, VerificationResult
from app.providers.registry import ProviderRegistry


def _normalize_host(value: str | None) -> str | None:
    if not value:
        return None
    return value.strip().lower().rstrip(".")


def _host_allowed(hostname: str | None, allowed: set[str]) -> bool:
    normalized = _normalize_host(hostname)
    return bool(normalized and normalized in allowed)


def _safe_error_codes(payload: dict[str, Any]) -> list[str]:
    values = payload.get("error-codes") or payload.get("error_codes") or []
    if not isinstance(values, list):
        return []
    return [str(value)[:80] for value in values[:10]]


class SiteVerifyAdapter(VerificationAdapter):
    endpoint: str

    def __init__(
        self,
        *,
        secret: str,
        allowed_hostnames: set[str],
        timeout_seconds: float = 8.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        if not secret:
            raise ValueError("Provider secret is required")
        normalized = {_normalize_host(host) for host in allowed_hostnames}
        self.allowed_hostnames = {host for host in normalized if host}
        if not self.allowed_hostnames:
            raise ValueError("At least one exact allowed hostname is required")
        self.secret = secret
        self.timeout_seconds = timeout_seconds
        self.transport = transport

    async def _post(self, data: dict[str, str]) -> dict[str, Any] | None:
        # Never log the token, secret, or request body.
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout_seconds,
                follow_redirects=False,
                transport=self.transport,
            ) as client:
                response = await client.post(self.endpoint, data=data)
                response.raise_for_status()
                payload = response.json()
                return payload if isinstance(payload, dict) else None
        except (httpx.HTTPError, ValueError):
            return None

    def _unavailable(self) -> VerificationResult:
        # Fail closed: provider outages must never count as successful checks.
        return VerificationResult(
            verified=False,
            provider=self.provider,
            reason="provider_unavailable",
            available=False,
        )


class RecaptchaSiteVerify(SiteVerifyAdapter):
    provider = "recaptcha"
    endpoint = "https://www.google.com/recaptcha/api/siteverify"

    def __init__(
        self,
        *,
        secret: str,
        allowed_hostnames: set[str],
        expected_action: str | None = None,
        minimum_score: float = 0.5,
        timeout_seconds: float = 8.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        super().__init__(
            secret=secret,
            allowed_hostnames=allowed_hostnames,
            timeout_seconds=timeout_seconds,
            transport=transport,
        )
        self.expected_action = expected_action
        self.minimum_score = minimum_score

    async def verify(self, token: str, **context) -> VerificationResult:
        if not token or len(token) > 4096:
            return VerificationResult(False, self.provider, "invalid_token")
        payload = await self._post({"secret": self.secret, "response": token})
        if payload is None:
            return self._unavailable()

        hostname = _normalize_host(payload.get("hostname"))
        action = payload.get("action")
        score = payload.get("score")
        errors = _safe_error_codes(payload)

        if payload.get("success") is not True:
            return VerificationResult(False, self.provider, "provider_rejected", hostname, action, score, errors)
        if not _host_allowed(hostname, self.allowed_hostnames):
            return VerificationResult(False, self.provider, "hostname_mismatch", hostname, action, score, errors)
        if self.expected_action and action != self.expected_action:
            return VerificationResult(False, self.provider, "action_mismatch", hostname, action, score, errors)
        if score is not None:
            try:
                if float(score) < self.minimum_score:
                    return VerificationResult(False, self.provider, "score_below_threshold", hostname, action, float(score), errors)
            except (TypeError, ValueError):
                return VerificationResult(False, self.provider, "invalid_score", hostname, action, None, errors)

        return VerificationResult(True, self.provider, hostname=hostname, action=action, score=score, error_codes=errors)


class HCaptchaSiteVerify(SiteVerifyAdapter):
    provider = "hcaptcha"
    endpoint = "https://api.hcaptcha.com/siteverify"

    def __init__(
        self,
        *,
        secret: str,
        sitekey: str,
        allowed_hostnames: set[str],
        timeout_seconds: float = 8.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        super().__init__(
            secret=secret,
            allowed_hostnames=allowed_hostnames,
            timeout_seconds=timeout_seconds,
            transport=transport,
        )
        if not sitekey:
            raise ValueError("hCaptcha sitekey is required")
        self.sitekey = sitekey

    async def verify(self, token: str, **context) -> VerificationResult:
        if not token or len(token) > 4096:
            return VerificationResult(False, self.provider, "invalid_token")
        payload = await self._post({
            "secret": self.secret,
            "response": token,
            "sitekey": self.sitekey,
        })
        if payload is None:
            return self._unavailable()

        hostname = _normalize_host(payload.get("hostname"))
        errors = _safe_error_codes(payload)
        if payload.get("success") is not True:
            return VerificationResult(False, self.provider, "provider_rejected", hostname, error_codes=errors)

        # hCaptcha recommends binding verification to the expected sitekey.
        # Its hostname field can be absent or "not-provided", so it is not
        # treated as the sole authentication control.
        if hostname and hostname != "not-provided" and not _host_allowed(hostname, self.allowed_hostnames):
            return VerificationResult(False, self.provider, "hostname_mismatch", hostname, error_codes=errors)

        return VerificationResult(True, self.provider, hostname=hostname, error_codes=errors)


class TurnstileSiteVerify(SiteVerifyAdapter):
    provider = "turnstile"
    endpoint = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    def __init__(
        self,
        *,
        secret: str,
        allowed_hostnames: set[str],
        expected_action: str | None = None,
        timeout_seconds: float = 8.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        super().__init__(
            secret=secret,
            allowed_hostnames=allowed_hostnames,
            timeout_seconds=timeout_seconds,
            transport=transport,
        )
        self.expected_action = expected_action

    async def verify(self, token: str, **context) -> VerificationResult:
        if not token or len(token) > 2048:
            return VerificationResult(False, self.provider, "invalid_token")
        payload = await self._post({
            "secret": self.secret,
            "response": token,
        })
        if payload is None:
            return self._unavailable()

        hostname = _normalize_host(payload.get("hostname"))
        action = payload.get("action")
        errors = _safe_error_codes(payload)
        if payload.get("success") is not True:
            return VerificationResult(False, self.provider, "provider_rejected", hostname, action, error_codes=errors)
        if not _host_allowed(hostname, self.allowed_hostnames):
            return VerificationResult(False, self.provider, "hostname_mismatch", hostname, action, error_codes=errors)
        if self.expected_action and action != self.expected_action:
            return VerificationResult(False, self.provider, "action_mismatch", hostname, action, error_codes=errors)

        return VerificationResult(True, self.provider, hostname=hostname, action=action, error_codes=errors)


def _parse_hostnames(value: str) -> set[str]:
    return {
        normalized
        for part in value.split(",")
        if (normalized := _normalize_host(part))
    }


def build_provider_registry(settings) -> ProviderRegistry:
    """Build only adapters with complete server-side configuration."""
    registry = ProviderRegistry()

    if settings.recaptcha_secret_key and settings.recaptcha_allowed_hostnames:
        registry.register(RecaptchaSiteVerify(
            secret=settings.recaptcha_secret_key,
            allowed_hostnames=_parse_hostnames(settings.recaptcha_allowed_hostnames),
            expected_action=settings.recaptcha_expected_action or None,
            minimum_score=settings.recaptcha_minimum_score,
        ))

    if (
        settings.hcaptcha_secret_key
        and settings.hcaptcha_sitekey
        and settings.hcaptcha_allowed_hostnames
    ):
        registry.register(HCaptchaSiteVerify(
            secret=settings.hcaptcha_secret_key,
            sitekey=settings.hcaptcha_sitekey,
            allowed_hostnames=_parse_hostnames(settings.hcaptcha_allowed_hostnames),
        ))

    if settings.turnstile_secret_key and settings.turnstile_allowed_hostnames:
        registry.register(TurnstileSiteVerify(
            secret=settings.turnstile_secret_key,
            allowed_hostnames=_parse_hostnames(settings.turnstile_allowed_hostnames),
            expected_action=settings.turnstile_expected_action or None,
        ))

    return registry
