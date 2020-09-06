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
