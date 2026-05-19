from shared.constants.base import BASE
from shared.constants.base_62 import BASE62
from shared.constants.length import LENGTH

_BASE62_BYTES = BASE62.encode("ascii")


def encode_int_to_fixed_base62(num: int) -> str:
    n = num
    buf = bytearray(LENGTH)
    for i in range(LENGTH - 1, -1, -1):
        n, r = divmod(n, BASE)
        buf[i] = _BASE62_BYTES[r]
    return buf.decode("ascii")
