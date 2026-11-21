import hashlib
import hmac

import pytest

from app.integrations.rejekt import send_signed_callback


@pytest.mark.asyncio
async def test_callback_requires_https():
    with pytest.raises(ValueError):
        await send_signed_callback("http://example.test/callback", "secret", {})


@pytest.mark.asyncio
async def test_callback_requires_secret():
    with pytest.raises(ValueError):
        await send_signed_callback("https://example.test/callback", "", {})
