from typing import List, Dict, Tuple
from bitarray import bitarray
from bitarray.util import ba2int
from datetime import datetime


class Reader:

    """Represents a bit reader that can extract bits sequentially from
    a bytes consent and return a representation in different formats.

    :param consent: The consent to process in bytes.
    """

    def __init__(self, consent: bytes):
        self._pointer = 0
        self._consent = bitarray(endian="big")
        self._consent.frombytes(consent)

    def read_bits(self, n: int) -> bitarray:
        """Reads the number of bits requested from the pointer position
        and automatically advances the pointer of the reader
        for the subsequent read_bits calls.

        :param n: Number of bits to retrieve.
        """
        self._pointer += n
        return self._consent[self._pointer - n : self._pointer]

    def read_bool(self) -> bool:
        """Reads a bit and returns the value as boolean."""
        return self.read_bits(1).all()

    def read_int(self, n: int) -> int:
        """Reads certain number of bits from the pointer position
        and returns the value as integer.

        :param n: Number of bits to retrieve and transform into int.
        """
        return ba2int(self.read_bits(n))

    def read_time(self) -> datetime:
        """Reads 36 bits (the length TCF uses for timestamps) and transforms
        the value into a utc datetime object with seconds granularity.
        """
        seconds = int(self.read_int(36) / 10)
        return datetime.utcfromtimestamp(seconds)

    def read_character(self) -> bytes:
        """Reads 6 bits and returns the value as a character starting with A"""
        return bytes([b"A"[0] + self.read_int(6)])

    def read_string(self, n: int) -> bytes:
        """Reads certain number of bits from the pointer position
        and returns the value as string character by character.

        :param n: Number of bits to retrieve and transform into string.
        """
        return b"".join([self.read_character() for _ in range(n)])

    def read_bitfield(self, n: int) -> Dict[int, bool]:
        """Reads certain number of bits from the pointer position
        and returns the value as a dictionary. The key is the bit
        position (starting by 1) and the value is True if the bit is
        1 and False if the bit is 0.

        :param n: Number of bits to retrieve and transform into the
            dictionary. The dictionary will have as many keys as n.
        """
        return {i + 1: self.read_bool() for i in range(n)}

    def read_range(self, n: int) -> List[Tuple[int, int]]:
        """Reads a complex "ranged" type from the reader given
        the number of ranges we are expecting to find.

        For each range:
        - The first bit indicates if it's a range or just a value.
        - If it's a range, the next 16 bits are the start int and the 
            next 16 bits are the end int.
        - If it's not a range, the next 16 bits are the start and the 
            end is the same as start.

        :param n: Number of ranges we are going to process.
        """
        ranges = []
        for i in range(n):
            is_range = self.read_bool()
            start = self.read_int(16)
            end = start if not is_range else self.read_int(16)
            ranges.append((start, end))
        return ranges
