from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

e = 65537
p = getPrime(64)
q = getPrime(64)
N = p * q
flag = b"JCC25{placeholder}"
M = bytes_to_long(flag)
C = pow(M, e, N)
print(f"Public key (e, N): ({e}, {N})")
print(f"Ciphertext: {C}")
# Public key (e, N): (65537, 171535569705812677946486440394414039183)
# Ciphertext: 144920187573935688963094252035058771259