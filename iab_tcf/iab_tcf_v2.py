import json
from typing import List, Tuple
from .bits import Reader
from .iab_tcf import base64_decode, segments
from .v2.publisher_restriction import PubRestrictionEntry
from .v2.non_core_segments import NonCoreSegment


class ConsentV2:

    """Represents a v2 consent with all the information extracted.

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
        self.tcf_policy_version = self._reader.read_int(6)
        self.is_service_specific = self._reader.read_bool()
        self.use_non_standard_stacks = self._reader.read_bool()
        self.special_features_optin = self._reader.read_bitfield(12)
        self.purposes_consent = self._reader.read_bitfield(24)
        self.purposes_legitimate_interests = self._reader.read_bitfield(24)
        self.purpose_one_treatment = self._reader.read_bool()
        self.publisher_cc = self._reader.read_string(2)
        self.read_consent_vendors()
        self.read_interest_vendors()
        self.read_pub_restriction_entries()

    def read_consent_vendors(self):
        """Reads the consent vendors. It must be called with the
        reader already in the position where the consent vendors start.
        """
        self.max_consent_vendor_id = self._reader.read_int(16)
        self.is_consent_range_encoding = self._reader.read_bool()
        if self.is_consent_range_encoding:
            self.num_consent_entries = self._reader.read_int(12)
            self.consented_vendors_range = self._reader.read_range(
                self.num_consent_entries
            )
        else:
            self.consented_vendors = self._reader.read_bitfield(
                self.max_consent_vendor_id
            )

    def read_interest_vendors(self):
        """Reads the interest vendors. It must be called with the
        reader already in the position where the interest vendors start.
        """
        self.max_interests_vendor_id = self._reader.read_int(16)
        self.is_interests_range_encoding = self._reader.read_bool()
        if self.is_interests_range_encoding:
            self.num_interests_entries = self._reader.read_int(12)
            self.interests_vendors_range = self._reader.read_range(
                self.num_interests_entries
            )
        else:
            self.interests_vendors = self._reader.read_bitfield(
                self.max_interests_vendor_id
            )

    def read_pub_restriction_entries(self):
        """Reads the publisher restriction entries. It must be called with the
        reader already in the position where the publisher restrictions start.
        """
        self.num_pub_restrictions = self._reader.read_int(12)
        self.pub_restriction_entries = []
        for _ in range(self.num_pub_restrictions):
            purpose_id = self._reader.read_int(6)
            restriction_type = self._reader.read_int(2)
            num_entries = self._reader.read_int(12)
            restrictions_range = self._reader.read_range(num_entries)
            self.pub_restriction_entries.append(
                PubRestrictionEntry(
                    purpose_id=purpose_id,
                    restriction_type=restriction_type,
                    restrictions_range=restrictions_range,
                )
            )

    def read_non_core_segments(self, segments: List[str]):
        """Receives list of non core segments and tries to
        parse the information inside them.
        """
        for segment in segments[1:]:
            decoded = base64_decode(segment)
            non_core_segment = NonCoreSegment(decoded)
            if non_core_segment.is_disclosed_vendors():
                self.oob_disclosed_vendors = non_core_segment.read_vendors()
            elif non_core_segment.is_allowed_vendors():
                self.oob_allowed_vendors = non_core_segment.read_vendors()
            elif non_core_segment.is_publisher_tc():
                self.publisher_tc = non_core_segment.read_publisher_tc()

    def is_purpose_allowed(self, id: int) -> bool:
        """Checks if a purpose is allowed or not.

        :param id: Purpose id to check if it's allowed or not.
        """
        if id in self.purposes_consent:
            return self.purposes_consent[id]
        return False

    def has_purpose_legitimate_interest(self, id: int) -> bool:
        if id in self.purposes_legitimate_interests:
            return self.purposes_legitimate_interests[id]
        return False

    def is_vendor_allowed(self, id: int) -> bool:
        """Checks if a vendor is allowed or not.

        :param id: Vendor id to check if it's allowed or not.
        """
        if self.is_consent_range_encoding:
            for (start, end) in self.consented_vendors_range:
                if start <= id and id <= end:
                    return True
            return False
        return False if id not in self.consented_vendors else self.consented_vendors[id]

    def is_interest_allowed(self, id: int) -> bool:
        if self.is_interests_range_encoding:
            for (start, end) in self.interests_vendors_range:
                if start <= id and id <= end:
                    return True
            return False
        return False if id not in self.interests_vendors else self.interests_vendors[id]

    def get_restriction(self, publisher: int, purpose: int) -> PubRestrictionEntry:
        for entry in self.pub_restriction_entries:
            if entry.purpose_id == purpose and entry.is_in_range(publisher):
                return entry
        return None


def decode_v2(consent: str):
    """Decodes a v2 consent string that it's encoded in base64 but split in
    segments.

    :param consent: base64 encoded consent string.
    """
    consent_segments = segments(consent)
    consent = ConsentV2(base64_decode(consent_segments[0]))
    consent.read_non_core_segments(consent_segments)
    return consent
