import httpx
import pytest

from app.providers.siteverify import HCaptchaSiteVerify, RecaptchaSiteVerify, TurnstileSiteVerify


def transport_for(payload):
    def handler(request):
        return httpx.Response(200, json=payload)
    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_turnstile_accepts_success_for_allowed_host_and_action():
    adapter = TurnstileSiteVerify(
        secret="test-secret",
        allowed_hostnames={"owned.example"},
        expected_action="contact",
        transport=transport_for({"success": True, "hostname": "owned.example", "action": "contact"}),
    )
    result = await adapter.verify("provider-token")
    assert result.verified is True
    assert result.provider == "turnstile"


@pytest.mark.asyncio
async def test_turnstile_rejects_wrong_hostname():
    adapter = TurnstileSiteVerify(
        secret="test-secret",
        allowed_hostnames={"owned.example"},
        transport=transport_for({"success": True, "hostname": "other.example"}),
    )
    result = await adapter.verify("provider-token")
    assert result.verified is False
    assert result.reason == "hostname_mismatch"


@pytest.mark.asyncio
async def test_recaptcha_checks_hostname_action_and_score():
    adapter = RecaptchaSiteVerify(
        secret="test-secret",
        allowed_hostnames={"owned.example"},
        expected_action="submit",
        minimum_score=0.7,
        transport=transport_for({
            "success": True, "hostname": "owned.example",
            "action": "submit", "score": 0.9,
        }),
    )
    result = await adapter.verify("provider-token")
    assert result.verified is True
    assert result.score == 0.9


@pytest.mark.asyncio
async def test_recaptcha_rejects_low_score():
    adapter = RecaptchaSiteVerify(
        secret="test-secret",
        allowed_hostnames={"owned.example"},
        minimum_score=0.7,
        transport=transport_for({"success": True, "hostname": "owned.example", "score": 0.2}),
    )
    result = await adapter.verify("provider-token")
    assert result.verified is False
    assert result.reason == "score_below_threshold"


@pytest.mark.asyncio
async def test_hcaptcha_binds_verification_to_configured_sitekey():
    seen = {}

    def handler(request):
        seen["body"] = request.content.decode()
        return httpx.Response(200, json={"success": True, "hostname": "owned.example"})

    adapter = HCaptchaSiteVerify(
        secret="test-secret",
        sitekey="public-sitekey",
        allowed_hostnames={"owned.example"},
        transport=httpx.MockTransport(handler),
    )
    result = await adapter.verify("provider-token")
    assert result.verified is True
    assert "sitekey=public-sitekey" in seen["body"]


@pytest.mark.asyncio
async def test_provider_network_failure_fails_closed():
    def handler(request):
        raise httpx.ConnectError("offline")

    adapter = TurnstileSiteVerify(
        secret="test-secret",
        allowed_hostnames={"owned.example"},
        transport=httpx.MockTransport(handler),
    )
    result = await adapter.verify("provider-token")
    assert result.verified is False
    assert result.available is False
    assert result.reason == "provider_unavailable"


@pytest.mark.asyncio
async def test_empty_or_oversized_token_is_rejected_without_network():
    adapter = TurnstileSiteVerify(
        secret="test-secret",
        allowed_hostnames={"owned.example"},
        transport=transport_for({"success": True, "hostname": "owned.example"}),
    )
    assert (await adapter.verify("")).reason == "invalid_token"
    assert (await adapter.verify("x" * 2049)).reason == "invalid_token"
