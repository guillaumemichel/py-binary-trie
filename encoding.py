from helpers import bitstring_to_int, int_to_bitstring
import math, varint


def valid_bitstring(bitstring: str) -> bool:
    """Check if a bitstring is valid."""
    for char in bitstring:
        if char not in "01":
            return False
    return True


def encode_bitstring(bitstring: str) -> int:
    """Encode a binary bitstring into an integer."""
    if not valid_bitstring(bitstring):
        raise ValueError("Invalid bitstring")
    return 2 ** (len(bitstring)) - 1 + bitstring_to_int(bitstring)


def decode_bitstring(code: int) -> str:
    """Decode an integer into a binary bitstring."""
    l = math.floor(math.log2(code + 1))
    return int_to_bitstring(code - 2**l + 1, l)


def bitstring_to_varint(bitstring: str) -> bytes:
    """Encode a binary bitstring into a varint."""
    return varint.encode(encode_bitstring(bitstring))


def varint_to_bitstring(varint_bytes: bytes) -> str:
    """Decode a varint into a binary bitstring."""
    return decode_bitstring(varint.decode_bytes(varint_bytes))
