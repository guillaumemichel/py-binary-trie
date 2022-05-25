def bytes_to_bit_string(data: bytes) -> str:
    return "".join(f'{byte:08b}' for byte in data)

def int_to_bit_string(i: int, l) -> str:
    return bytes_to_bit_string((i).to_bytes(l//8+1, 'big', signed=False))[-l:]
