import json
from typing import List, Tuple


class PubRestrictionEntry:

    """Represents a publisher restriction entry that can be used
    to perform several operation on that information.

    :param purpose_id: The purpose this publisher restriction applies to.
    :param restriction_type: The type this restriction applies to.
    :param restrictions_range: The range of publishers this restriction applies to.
    """

    PURPOSE_FLATLY_NOT_ALLOWED = 0
    REQUIRE_CONSENT = 1
    REQUIRE_LEGITIMATE_INTEREST = 2
    UNDEFINED = 3

    def __init__(
        self,
        purpose_id: int,
        restriction_type: str,
        restrictions_range: List[Tuple[int, int]],
    ):
        self.purpose_id = purpose_id
        self.restriction_type = restriction_type
        self.restrictions_range = restrictions_range

    def __repr__(self):
        return json.dumps(
            {
                "purpose": self.purpose_id,
                "restriction_type": self.restriction_type,
                "restrictions_range": self.restrictions_range,
            }
        )

    def is_not_allowed(self):
        """Checks if the restriction type is PURPOSE_FLATLY_NOT_ALLOWED"""
        return self.restriction_type == self.PURPOSE_FLATLY_NOT_ALLOWED

    def is_consent_required(self):
        """Checks if the restriction type is REQUIRE_CONSENT"""
        return self.restriction_type == self.REQUIRE_CONSENT

    def is_legitimate_interest_required(self):
        """Checks if the restriction type is REQUIRE_LEGITIMATE_INTEREST"""
        return self.restriction_type == self.REQUIRE_LEGITIMATE_INTEREST

    def is_in_range(self, publisher: int) -> bool:
        """Checks if the publisher received is affected by this restriction or not"""
        for (start, end) in self.restrictions_range:
            if publisher >= start and publisher <= end:
                return True
        return False

    def is_publisher_restricted(self, publisher: int) -> bool:
        """If the publisher is in the range specified for this restriction
        and the restriction type is PURPOSE_FLATLY_NOT_ALLOWED then the
        publisher is restricted.
        """
        return self.is_not_allowed() and self.is_in_range(publisher)
