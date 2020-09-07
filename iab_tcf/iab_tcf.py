from typing import List
import base64
from .bits import Reader


def segments(consent: str) -> List[str]:
    """Helper to split the core and non core consents."""
    return consent.split(".")


def base64_decode(segment: str) -> bytes:
    """Helper to decode the IAB TCF segments encoded."""
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def version(consent: bytes) -> int:
    """Helper to extract the version from a consent without having
    to wait for the full decoding.
    """
    reader = Reader(consent)
    return reader.read_int(6)
