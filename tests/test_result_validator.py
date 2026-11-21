from app.captcha.result_validator import validate_provider_result
from app.providers.base import VerificationResult


def test_accepts_matching_verified_result():
    result = VerificationResult(verified=True, provider="turnstile", hostname="owned.example")
    assert validate_provider_result(result, expected_provider="turnstile", expected_hostname="owned.example")[0]


def test_rejects_hostname_mismatch():
    result = VerificationResult(verified=True, provider="turnstile", hostname="other.example")
    assert not validate_provider_result(result, expected_provider="turnstile", expected_hostname="owned.example")[0]
