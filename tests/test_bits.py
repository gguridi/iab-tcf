from typing import List
import base64
import pytest
from bitarray import bitarray
from iab_tcf.bits import Reader
from .conftest import mapbit


def test_read_bits_incrementally():
    reader = Reader(b"\xe3\x80")
    assert reader.read_bits(3) == bitarray('111')
    assert reader.read_bits(3) == bitarray('000')
    assert reader.read_bits(3) == bitarray('111')
    assert reader.read_bits(3) == bitarray('000')


@pytest.mark.parametrize("input, output", [
    (b"\x80", True),
    (b"\x00", False),
])
def test_read_bool(input, output):
    reader = Reader(input)
    assert reader.read_bool() == output


@pytest.mark.parametrize("input, bits, output", [
    (b"\xf0", 4, 15),
    (b"\xf8", 5, 31),
    (b"\xfc", 6, 63),
    (b"\xfe", 7, 127),
    (b"\xf7", 8, 247),
    (b"\xf7\x80", 9, 495),
    (b"\xf7\xc0", 10, 991),
    (b"\xf7\xe0", 11, 1983),
    (b"\xf7\xf0", 12, 3967),
])
def test_read_int(input, bits, output):
    reader = Reader(input)
    assert reader.read_int(bits) == output


@pytest.mark.parametrize("input, output", [
    (b"\x38\xdf\x6b\x35\xB0", "2018-05-18T17:48:31"),
    (b";\x94\x85\x17 ", "2020-09-05T21:50:29"),
])
def test_read_time(input, output):
    reader = Reader(input)
    assert reader.read_time().isoformat() == output


@pytest.mark.parametrize("input, length, output", [
    (b"\x04 \xc0", 3 , b"BCD"),
    (b"\x0c @", 3, b"DCB"),
])
def test_read_string(input, length, output):
    reader = Reader(input)
    assert reader.read_string(length) == output


@pytest.mark.parametrize("input, length, output", [
    (b"\xf0", 4, mapbit(4)),
    (b"\xf8", 5, mapbit(5)),
    (b"\xfc", 6, mapbit(6)),
    (b"\xfe", 7, mapbit(7)),
    (b"\xf7", 8, mapbit(8, falses=[5])),
    (b"\xf7\x80", 9, mapbit(9, falses=[5])),
    (b"\xf7\xc0", 10, mapbit(10, falses=[5])),
    (b"\xf7\xe0", 11, mapbit(11, falses=[5])),
    (b"\xf7\xf0", 12, mapbit(12, falses=[5])),
])
def test_read_bitfield(input, length, output):
    reader = Reader(input)
    assert reader.read_bitfield(length) == output


@pytest.mark.parametrize("input, length, output", [
    (b"\x80\x00\x80\x01\x80", 1, [(1, 3)]),
    (b"\x00\x00\x80", 1, [(1, 1)]),
    (b"\x00\x01\x00\x03", 1, [(2, 2)]),
    (b"\x00\x01@\x00\x80\x01\x80", 2, [(2, 2), (2, 6)]),
    
])
def test_read_range(input, length, output):
    reader = Reader(input)
    assert reader.read_range(length) == output
