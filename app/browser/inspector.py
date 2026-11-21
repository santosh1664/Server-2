from app.browser.seleniumbase_manager import SeleniumBaseManager
from app.config import settings
from app.orchestration.coordinator import ChallengeCoordinator
from app.schemas import InspectResponse
from app.security import validate_public_https_url


class SeleniumBaseInspector:
    """Read-only page diagnostics using standard SeleniumBase browser mode."""

    def __init__(self):
        self.browser_manager = SeleniumBaseManager(
            headless=settings.browser_headless
        )
        self.coordinator = ChallengeCoordinator()

    def inspect(self, raw_url: str) -> InspectResponse:
        url = validate_public_https_url(raw_url)

        with self.browser_manager.session() as sb:
            sb.open(url)
            sb.sleep(2)
            title = sb.get_title()
            final_url = sb.get_current_url()
            html = sb.get_page_source()
            visible_text = (
                sb.get_text("body")
                if sb.is_element_present("body")
                else ""
            )

        result = self.coordinator.classify_page(
            url=final_url,
            title=title,
            html=html,
            visible_text=visible_text,
        )
        return InspectResponse(
            status=result["state"],
            title=result["title"],
            final_url=result["page_url"],
            challenge_detected=result["challenge_detected"],
            providers=result["providers"],
            evidence=result["evidence"],
        )
