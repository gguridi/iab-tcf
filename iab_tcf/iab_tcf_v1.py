from typing import List
from .iab_tcf import base64_decode
from .bits import Reader


class ConsentV1:

    """Represents a v1.1 consent with all the information extracted.

    :param consent: The consent to process in bytes.
    """

    def __init__(self, consent: bytes):
        self._reader: Reader = Reader(consent)
        self.version = self._reader.read_int(6)
        self.created = self._reader.read_time()
        self.last_updated = self._reader.read_time()
        self.cmp_id = self._reader.read_int(12)
        self.cmp_version = self._reader.read_int(12)
        self.consent_screen = self._reader.read_int(6)
        self.consent_language = self._reader.read_string(2)
        self.vendor_list_version = self._reader.read_int(12)
        self.purposes_allowed = self._reader.read_bitfield(24)
        self.max_vendor_id = self._reader.read_int(16)
        self.is_range_encoding = self._reader.read_bool()
        if self.is_range_encoding:
            self.default_consent = self._reader.read_bool()
            self.num_entries = self._reader.read_int(12)
            self.range_entries = self._reader.read_range(self.num_entries)
        else:
            self.consented_vendors = self._reader.read_bitfield(self.max_vendor_id)

    def is_purpose_allowed(self, id: int) -> bool:
        """Checks if a purpose is allowed or not.

        :param id: Purpose id to check if it's allowed or not.
        """
        if id in self.purposes_allowed:
            return self.purposes_allowed[id]
        return False

    def is_vendor_allowed(self, id: int) -> bool:
        """Checks if a vendor is allowed or not.

        :param id: Vendor id to check if it's allowed or not.
        """
        if self.is_range_encoding:
            for (start, end) in self.range_entries:
                if start <= id and id <= end:
                    return not self.default_consent
            return self.default_consent
        return False if id not in self.consented_vendors else self.consented_vendors[id]


def decode_v1(consent: str):
    """Decodes a v1.1 consent string that it's encoded in base64.

    :param consent: base64 encoded consent string.
    """
    return ConsentV1(base64_decode(consent))
