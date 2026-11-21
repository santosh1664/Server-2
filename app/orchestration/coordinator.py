from app.captcha.challenge_state import ChallengeState
from app.detection.detector import ChallengeDetector


class ChallengeCoordinator:
    """Coordinates passive page inspection and synthetic verification outcomes.

    This coordinator never attempts to bypass third-party challenge systems.
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
    def synthetic_verification_state(result: dict) -> ChallengeState:
        """Map a local synthetic-demo result to a terminal workflow state."""
        status = result.get("status")
        if status == "verified" and result.get("accepted") is True:
            return ChallengeState.VERIFIED
        if status == "expired":
            return ChallengeState.FAILED
        if status == "failed":
            return ChallengeState.NEEDS_YOU
        return ChallengeState.VERIFICATION_PENDING
