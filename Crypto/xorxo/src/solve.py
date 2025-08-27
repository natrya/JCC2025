from Crypto.Util.strxor import strxor
from binascii import unhexlify

cipher_hex = "d34ab5e4bd05ee6c9abad709fc659a89ff1bf565a9a3d719f67da9e7fc03"
cipher = unhexlify(cipher_hex)

known_prefix = b"JCC25{"

key = strxor(cipher[:6], known_prefix)

expanded_key = (key * ((len(cipher) // len(key)) + 1))[:len(cipher)]

plaintext = strxor(cipher, expanded_key)
print("Recovered flag:", plaintext.decode())