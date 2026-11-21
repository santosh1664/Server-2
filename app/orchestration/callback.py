from app.integrations.rejekt import send_signed_callback


async def report_result(callback_url: str, callback_secret: str, payload: dict) -> None:
    """Send a signed status callback to a configured HTTPS endpoint."""
    await send_signed_callback(callback_url, callback_secret, payload)
