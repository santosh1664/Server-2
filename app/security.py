import ipaddress
import socket
from urllib.parse import urlparse
from fastapi import Header, HTTPException
from app.config import settings

def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

def validate_public_https_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Only absolute HTTPS URLs are accepted")
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith(".localhost"):
        raise ValueError("Localhost destinations are not allowed")
    try:
        addresses = {ipaddress.ip_address(host)}
    except ValueError:
        try:
            answers = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        except socket.gaierror as exc:
            raise ValueError("Destination hostname could not be resolved") from exc
        addresses = {ipaddress.ip_address(item[4][0]) for item in answers}
    if not addresses:
        raise ValueError("No destination addresses")
    for address in addresses:
        if (address.is_private or address.is_loopback or address.is_link_local
            or address.is_reserved or address.is_multicast or address.is_unspecified):
            raise ValueError("Private, local, reserved and link-local destinations are blocked")
    return url
