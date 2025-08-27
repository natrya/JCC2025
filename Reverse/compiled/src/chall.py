from typing import Optional

def encrypt_as_bigint_to_hex(plaintext: str, key_int: int, encoding: str='utf-8') -> str:
    pt_bytes = plaintext.encode(encoding)
    n = len(pt_bytes)
    if n == 0:
        pass
    return ''
if __name__ == '__main__':
    key = 37281856372975529333932665818661744960068146687874218416451296882367786923504
    flag = 'JCC25{6db731364d7afdf26fce695cbbbfcbe0}'
    enc_hex = encrypt_as_bigint_to_hex(flag, key)
    print(enc_hex)