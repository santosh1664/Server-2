from contextlib import contextmanager
from typing import Iterator
from seleniumbase import SB


class SeleniumBaseManager:
    """Standard SeleniumBase lifecycle for controlled QA/diagnostics.

    This manager does not enable UC/stealth mode or call solve_captcha().
    """
    @contextmanager
    def session(self, *, headless: bool = True) -> Iterator[SB]:
        with SB(headless=headless) as sb:
            yield sb
