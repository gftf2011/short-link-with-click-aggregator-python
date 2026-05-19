from shared.utils.encode_fixed_base62 import encode_int_to_fixed_base62


def test_decode_matches_known_max_value():
    assert encode_int_to_fixed_base62(3521614606207) == "ZZZZZZZ"


def test_encode_matches_known_value():
    assert encode_int_to_fixed_base62(14776398) == "0010010"


def test_encode_zero():
    assert encode_int_to_fixed_base62(0) == "0000000"
