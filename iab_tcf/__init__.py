from .bits import Reader
from .iab_tcf import base64_decode, segments, version
from .iab_tcf_v1 import ConsentV1, decode_v1
from .iab_tcf_v2 import ConsentV2, PubRestrictionEntry, decode_v2


def decode(consent: str):
    """Generic implementation of a IAB TCF decoder.

    It detects if the consent received is v1.1 or v2 and returns
    the appropriate ConsentV1 or ConsentV2 instance.
    """

    if consent:
        consent_segments = segments(consent)
        consent_version = version(base64_decode(consent_segments[0]))
        if consent_version == 1:
            return decode_v1(consent_segments[0])
        elif consent_version == 2:
            return decode_v2(consent)
        raise Exception(f"Unable to process a consent with version {consent_version}")
    raise Exception("Unable to process an empty consent")
