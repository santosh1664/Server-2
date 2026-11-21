from app.config import settings
from app.detection.classifier import classify_evidence
from app.schemas import InspectResponse
from app.security import validate_public_https_url

class SeleniumBaseInspector:
    """Read-only Chromium diagnostics through SeleniumBase CDP mode."""
    def inspect(self, raw_url: str) -> InspectResponse:
        url = validate_public_https_url(raw_url)
        from seleniumbase import SB  # lazy import for API/demo-only environments
        with SB(headless=settings.browser_headless, test=True) as sb:
            sb.activate_cdp_mode(url)
            sb.sleep(2)
            title = sb.get_title()
            final_url = sb.get_current_url()
            html = sb.get_page_source()
            visible_text = sb.get_text("body") if sb.is_element_present("body") else ""
        result = classify_evidence(final_url, html, visible_text)
        return InspectResponse(
            status="needs_review" if result.detected else "page_loaded",
            title=title, final_url=final_url,
            challenge_detected=result.detected,
            providers=result.providers, evidence=result.evidence,
        )
