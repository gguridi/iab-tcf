import os
import json
import base64
import pytest
from pathlib import Path
from typing import Dict
from iab_tcf.iab_tcf import base64_decode
from iab_tcf.iab_tcf_v2 import decode_v2, ConsentV2
from .conftest import mapbit, mapbit_from_dict, load_seed


@pytest.fixture(
    params=[
        "./seed/v2/consent_a.json",
        "./seed/v2/consent_b.json",
        "./seed/v2/consent_c.json",
    ]
)
def info(request):
    return load_seed(request.param)


@pytest.fixture
def consent(info) -> ConsentV2:
    return decode_v2(info["consent"])


@pytest.fixture
def core(info) -> Dict:
    return info["core"]


def test_version(consent, core):
    assert consent.version == core["version"]


def test_created(consent, core):
    assert consent.created.isoformat() == core["created"]


def test_last_updated(consent, core):
    assert consent.last_updated.isoformat() == core["lastUpdated"]


def test_cmp_id(consent, core):
    assert consent.cmp_id == core["cmpId"]


def test_cmp_version(consent, core):
    assert consent.cmp_version == core["cmpVersion"]


def test_consent_screen(consent, core):
    assert consent.consent_screen == core["consentScreen"]


def test_consent_language(consent, core):
    assert consent.consent_language == core["consentLanguage"].encode()


def test_vendor_list_version(consent, core):
    assert consent.vendor_list_version == core["vendorListVersion"]


def test_tcf_policy_version(consent, core):
    assert consent.tcf_policy_version == core["policyVersion"]


def test_is_service_specific(consent, core):
    assert consent.is_service_specific == core["isServiceSpecified"]


def test_uses_non_standard_stacks(consent, core):
    assert consent.use_non_standard_stacks == core["useNonStandardStacks"]


def test_special_features_optin(consent, core):
    expected = mapbit_from_dict(12, trues=core["specialFeatureOptins"])
    assert consent.special_features_optin == expected


def test_purposes_consented(consent, core):
    expected = mapbit_from_dict(24, trues=core["purposeConsents"])
    for purpose, consented in expected.items():
        assert consent.is_purpose_allowed(purpose) == consented


def test_purposes_legitimate_interests(consent, core):
    expected = mapbit_from_dict(24, trues=core["purposeLegitimateInterests"])
    for purpose, interested in expected.items():
        assert consent.has_purpose_legitimate_interest(purpose) == interested


def test_purpose_one_treatment(consent, core):
    assert consent.purpose_one_treatment == core["purposeOneTreatment"]


def test_publisher_cc(consent, core):
    assert consent.publisher_cc == core["publisherCountryCode"].encode()


def test_max_consent_vendor_id(consent, core):
    assert consent.max_consent_vendor_id == core["maxVendorId"]


def test_is_consent_vendor_allowed(consent, core):
    expected = mapbit_from_dict(core["maxVendorId"], trues=core["vendorConsents"])
    for vendor, allowed in expected.items():
        assert consent.is_vendor_allowed(vendor) == allowed


def test_max_interests_vendor_id(consent, core):
    assert consent.max_interests_vendor_id == core["maxVendorLegitimateInterestsId"]


def test_is_interest_allowed(consent, core):
    expected = mapbit_from_dict(
        core["maxVendorLegitimateInterestsId"], trues=core["vendorLegitimateInterests"]
    )
    for interest, allowed in expected.items():
        assert consent.is_interest_allowed(interest) == allowed


def test_publisher_restrictions(consent, core):
    for publisher, purposes in core["publisherRestrictions"].items():
        for info in purposes:
            restriction = consent.get_restriction(int(publisher), info["purpose"])
            assert restriction.is_not_allowed() == (not info["isAllowed"])
            assert restriction.is_consent_required() == info["isConsentRequired"]
            assert (
                restriction.is_legitimate_interest_required()
                == info["isLegitimateInterestRequired"]
            )


def test_disclosed_vendors(consent, info):
    if "disclosedVendors" in info:
        max_disclosed_vendors = len(consent.oob_disclosed_vendors)
        expected = mapbit_from_dict(max_disclosed_vendors, info["disclosedVendors"])
        assert consent.oob_disclosed_vendors == expected


def test_publisher_tc_purpose_contents(consent, info):
    if "publisherTC" in info:
        expected = mapbit_from_dict(24, info["publisherTC"]["purposeConsents"])
        assert consent.publisher_tc.purposes_consent == expected


def test_publisher_tc_purposes_lit_transparency(consent, info):
    if "publisherTC" in info:
        expected = mapbit_from_dict(
            24, info["publisherTC"]["purposeLegitimateInterests"]
        )
        assert consent.publisher_tc.purposes_lit_transparency == expected
