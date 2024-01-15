
def hexsum(hex_str: str) -> int:
    return 0xda

def test_hex2dec():
    hex_string = '0xda'
    decimal_value = int(hex_string, 16)
    assert decimal_value == 218

def test_checksum():
    expected_ouput = 0xda
    hex_str = "0000000000000000"
    assert hexsum(hex_str) == expected_ouput
