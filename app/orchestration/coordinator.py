from app.captcha.challenge_state import ChallengeState
from app.detection.detector import ChallengeDetector
from app.providers.base import VerificationResult


class ChallengeCoordinator:
    """Coordinates passive page inspection and provider verification outcomes.

    This coordinator validates tokens issued by configured provider widgets.
    It does not automate challenge solving or bypass provider protections.
    """

    def __init__(self):
        self.detector = ChallengeDetector()

    def classify_page(self, *, url: str, title: str, html: str, visible_text: str) -> dict:
        evidence = self.detector.inspect(
            url=url,
            title=title,
            html=html,
            visible_text=visible_text,
        )
        state = (
            ChallengeState.CHALLENGE_DETECTED
            if evidence.indicators
            else ChallengeState.PAGE_LOADED
        )
        return {
            "state": state.value,
            "challenge_detected": bool(evidence.indicators),
            "providers": evidence.provider_hints,
            "evidence": evidence.indicators,
            "page_url": evidence.page_url,
            "title": evidence.title,
            "collected_at": evidence.collected_at,
        }

    @staticmethod
    def provider_verification_state(result: VerificationResult) -> ChallengeState:
        if result.verified and result.available:
            return ChallengeState.VERIFIED
        if not result.available:
            return ChallengeState.NEEDS_YOU
        return ChallengeState.REJECTED

    @staticmethod
    def synthetic_verification_state(result: dict) -> ChallengeState:
        status = result.get("status")
        if status == "verified" and result.get("accepted") is True:
            return ChallengeState.VERIFIED
        if status == "expired":
            return ChallengeState.FAILED
        if status == "failed":
            return ChallengeState.NEEDS_YOU
        return ChallengeState.VERIFICATION_PENDING
