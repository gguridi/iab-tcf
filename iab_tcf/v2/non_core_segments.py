from typing import List, Dict, Tuple
from .publisher_tc import PubTCEntry
from ..bits import Reader


class NonCoreSegment:

    """Represents a non core segment that can contain information
    regarding disclosed vendors, allowed vendors or publiser tc.

    :param segment: The segment to process in bytes.
    """

    CORE = 0
    DISCLOSED_VENDORS = 1
    ALLOWED_VENDORS = 2
    PUBLISHER_TC = 3

    def __init__(self, segment: bytes):
        self._reader = Reader(segment)
        self.type = self._reader.read_int(3)

    def is_disclosed_vendors(self):
        """Checks if the non core segment contains information about Disclosed Vendors."""
        return self.type == self.DISCLOSED_VENDORS

    def is_allowed_vendors(self):
        """Checks if the non core segment contains information about Allowed Vendors."""
        return self.type == self.ALLOWED_VENDORS

    def is_publisher_tc(self):
        """Checks if the non core segment contains information about Publisher TC."""
        return self.type == self.PUBLISHER_TC

    def read_vendors(self) -> Dict[int, bool]:
        """If the non core segment is type Disclosed Vendors or Allowed Vendors, this
        method processes its information extracting a map bitfield with
        the vendors enabled.
        """
        max_vendor_id = self._reader.read_int(16)
        is_range_encoding = self._reader.read_bool()
        if is_range_encoding:
            vendors = {}
            num_entries = self._reader.read_int(12)
            for start, end in self._reader.read_range(num_entries):
                vendors = {**vendors, **{i: True for i in range(start, end + 1)}}
            return vendors
        else:
            return self._reader.read_bitfield(max_vendor_id)

    def read_publisher_tc(self) -> PubTCEntry:
        """If the non core segment is type Publisher TC, this
        method processes and extracts the information inside an entry object for
        easy access.
        """
        purposes_consent = self._reader.read_bitfield(24)
        purposes_lit_transparency = self._reader.read_bitfield(24)
        num_custom_purposes = self._reader.read_int(6)
        custom_purposes_consent = self._reader.read_bitfield(num_custom_purposes)
        custom_purposes_lit_transparency = self._reader.read_bitfield(
            num_custom_purposes
        )
        return PubTCEntry(
            purposes_consent=purposes_consent,
            purposes_lit_transparency=purposes_lit_transparency,
            custom_purposes_consent=custom_purposes_consent,
            custom_purposes_lit_transparency=custom_purposes_lit_transparency,
        )
