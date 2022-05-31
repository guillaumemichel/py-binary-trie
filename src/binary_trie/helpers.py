from math import log2

def bytes_to_bitstring(data: bytes, l: int = 0) -> str:
    if l==0:
        l = 8*len(data)
    return "".join(f'{byte:08b}' for byte in data)[-l:]

def int_to_bitstring(i, l: int) -> str:
    return bytes_to_bitstring((i).to_bytes(l//8+1, 'big', signed=False))[-l:]

def bitstring_to_int(bs: str) -> int:
    return int(bs, 2)

def bitstring_to_bytes(bs: str) -> bytes:
    return bitstring_to_int(bs).to_bytes(len(bs)//8 if len(bs)%8==0 else len(bs)//8+1, byteorder='big')

print(bitstring_to_bytes("0011"))