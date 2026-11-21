from app.providers.base import VerificationResult


def validate_provider_result(result: VerificationResult, *, expected_provider: str, expected_hostname: str) -> tuple[bool, str]:
    """Accept only a positive provider result for the configured provider and host."""
    if not result.verified:
        return False, result.reason or "Provider did not verify the response"
    if result.provider != expected_provider:
        return False, "Provider mismatch"
    if result.hostname != expected_hostname:
        return False, "Hostname mismatch"
    return True, "Provider verification accepted"
