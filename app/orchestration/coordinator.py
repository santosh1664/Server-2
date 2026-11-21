from app.captcha.challenge_state import ChallengeState
from app.detection.detector import ChallengeDetector


class ChallengeCoordinator:
    """Coordinates passive detection and state classification only."""
    def __init__(self):
        self.detector = ChallengeDetector()

    def classify_page(self, *, url: str, title: str, html: str, visible_text: str) -> dict:
        evidence = self.detector.inspect(url=url, title=title, html=html, visible_text=visible_text)
        state = ChallengeState.CHALLENGE_DETECTED if evidence.indicators else ChallengeState.PAGE_LOADED
        return {
            "state": state.value,
            "challenge_detected": bool(evidence.indicators),
            "providers": evidence.provider_hints,
            "evidence": evidence.indicators,
            "page_url": evidence.page_url,
            "title": evidence.title,
            "collected_at": evidence.collected_at,
        }
