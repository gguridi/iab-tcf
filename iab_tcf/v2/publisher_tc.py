from typing import Dict


class PubTCEntry:

    """Represents a Publisher TC entry that can be used to retrieve further information.

    :param purposes_consent: The publisher's purposes consent.
    :param purposes_lit_transparency: The publisher's purposes legitimate
        interest consents.
    :param custom_purposes_consent: The publisher's custom purposes consent.
    :param custom_purposes_lit_transparency: The publisher's custom purposes
        legitimate interest consents.
    """

    def __init__(
        self,
        purposes_consent: Dict[int, bool],
        purposes_lit_transparency: Dict[int, bool],
        custom_purposes_consent: Dict[int, bool],
        custom_purposes_lit_transparency: Dict[int, bool],
    ):
        self.purposes_consent = purposes_consent
        self.purposes_lit_transparency = purposes_lit_transparency
        self.custom_purposes_consent = custom_purposes_consent
        self.custom_purposes_lit_transparency = custom_purposes_lit_transparency
