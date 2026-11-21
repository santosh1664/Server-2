from contextlib import contextmanager
from typing import Iterator

from seleniumbase import SB


class SeleniumBaseManager:
    """Owns standard SeleniumBase sessions for controlled diagnostics.

    This intentionally does not enable UC/stealth mode or invoke CAPTCHA
    challenge-solving methods. Synthetic verification is handled separately
    by app.demo.service.
    """

    def __init__(self, *, headless: bool = True):
        self.headless = headless

    @contextmanager
    def session(self) -> Iterator[SB]:
        with SB(headless=self.headless) as sb:
            yield sb
