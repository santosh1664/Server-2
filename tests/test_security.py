import pytest
from app.security import validate_public_https_url

@pytest.mark.parametrize("url", [
    "http://example.com", "https://localhost", "https://127.0.0.1",
    "https://192.168.1.10",
])
def test_reject_local_or_non_https(url):
    with pytest.raises(ValueError):
        validate_public_https_url(url)
