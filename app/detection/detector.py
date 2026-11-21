from datetime import datetime, timezone
from app.detection.classifier import classify_evidence
from app.detection.evidence import PageEvidence


class ChallengeDetector:
    """Classifies passive page evidence; does not interact with challenges."""
    def inspect(self, *, url: str, title: str, html: str, visible_text: str) -> PageEvidence:
        result = classify_evidence(url, html, visible_text)
        return PageEvidence(
            page_url=url,
            title=title,
            provider_hints=result.providers,
            indicators=result.evidence,
            collected_at=datetime.now(timezone.utc).isoformat(),
        )
