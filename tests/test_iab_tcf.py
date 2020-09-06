import pytest
from iab_tcf import decode
from .conftest import load_seed


@pytest.mark.parametrize(
    "file",
    [
        "./seed/v1/consent_a.json",
        "./seed/v1/consent_b.json",
        "./seed/v1/consent_c.json",
    ],
)
def test_decode_v1(file):
    data = load_seed(file)
    assert decode(data["consent"]).version == 1


@pytest.mark.parametrize(
    "file",
    [
        "./seed/v2/consent_a.json",
        "./seed/v2/consent_b.json",
        "./seed/v2/consent_c.json",
    ],
)
def test_decode_v2(file):
    data = load_seed(file)
    assert decode(data["consent"]).version == 2


def test_decode_raises_exception_if_consent_is_empty():
    with pytest.raises(Exception, match="Unable to process an empty consent"):
        decode("")


def test_decode_raises_exception_if_consent_is_not_base64():
    with pytest.raises(ValueError):
        decode("@£$%^")


def test_decode_raises_exception_if_consent_version_is_not_one_or_two():
    with pytest.raises(Exception, match="Unable to process a consent with version 47"):
        decode("validbase64")
