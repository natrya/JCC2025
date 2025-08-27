from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

e = 65537
p = getPrime(64)
q = getPrime(64)
N = p * q
flag = b"JCC25{0xcaffe}"
M = bytes_to_long(flag)
C = pow(M, e, N)
print(f"Public key (e, N): ({e}, {N})")
print(f"Ciphertext: {C}")