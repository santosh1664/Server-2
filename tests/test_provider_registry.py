from types import SimpleNamespace

from app.providers.siteverify import build_provider_registry


def test_registry_contains_only_fully_configured_providers():
    settings = SimpleNamespace(
        recaptcha_secret_key="rec-secret",
        recaptcha_allowed_hostnames="owned.example",
        recaptcha_expected_action="",
        recaptcha_minimum_score=0.5,
        hcaptcha_secret_key="",
        hcaptcha_sitekey="",
        hcaptcha_allowed_hostnames="",
        turnstile_secret_key="ts-secret",
        turnstile_allowed_hostnames="owned.example",
        turnstile_expected_action="",
        provider_verify_timeout_seconds=8.0,
    )
    registry = build_provider_registry(settings)
    assert registry.names() == ["recaptcha", "turnstile"]
