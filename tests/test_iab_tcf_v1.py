import pytest
from iab_tcf.iab_tcf import base64_decode
from iab_tcf.iab_tcf_v1 import ConsentV1, decode_v1
from .conftest import load_seed, mapbit, mapbit_from_dict


@pytest.fixture(
    params=[
        "./seed/v1/consent_a.json",
        "./seed/v1/consent_b.json",
        "./seed/v1/consent_c.json",
    ]
)
def info(request):
    return load_seed(request.param)


@pytest.fixture
def consent(info) -> ConsentV1:
    return decode_v1(info["consent"])


def test_version(consent, info):
    assert consent.version == info["version"]


def test_created(consent, info):
    assert consent.created.isoformat() == info["created"]


def test_last_updated(consent, info):
    assert consent.last_updated.isoformat() == info["lastUpdated"]


def test_cmp_id(consent, info):
    assert consent.cmp_id == info["cmpId"]


def test_cmp_version(consent, info):
    assert consent.cmp_version == info["cmpVersion"]


def test_consent_screen(consent, info):
    assert consent.consent_screen == info["consentScreen"]


def test_consent_language(consent, info):
    assert consent.consent_language == info["consentLanguage"].encode()


def test_vendor_list_version(consent, info):
    assert consent.vendor_list_version == info["vendorListVersion"]


def test_purposes_allowed(consent, info):
    expected = mapbit(24, trues=info["allowedPurposeIds"])
    for purpose, allowed in expected.items():
        assert consent.is_purpose_allowed(purpose) == allowed


def test_max_vendor_id(consent, info):
    assert consent.max_vendor_id == info["maxVendorId"]


def test_is_vendor_allowed(consent, info):
    expected = mapbit(info["maxVendorId"], trues=info["allowedVendorIds"])
    for vendor, allowed in expected.items():
        assert consent.is_vendor_allowed(vendor) == allowed
