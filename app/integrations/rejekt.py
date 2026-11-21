import hashlib
import hmac
import json

import httpx


async def send_signed_callback(
    callback_url: str,
    callback_secret: str,
    payload: dict,
) -> dict:
    """Send a JSON callback signed with HMAC-SHA256.

    The URL and secret must come from trusted server configuration. This helper
    does not discover or accept callback destinations from browser/job input.
    """
    if not callback_url.startswith("https://"):
        raise ValueError("Rejekt callback URL must use HTTPS")
    if not callback_secret:
        raise ValueError("Rejekt callback secret is not configured")

    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    signature = hmac.new(
        callback_secret.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
        response = await client.post(
            callback_url,
            content=body,
            headers={
                "Content-Type": "application/json",
                "X-Server2-Signature": f"sha256={signature}",
            },
        )
        response.raise_for_status()
        return {"status_code": response.status_code}
