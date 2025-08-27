from sympy import mod_inverse
from sympy.ntheory.factor_ import factorint
from Crypto.Util.number import long_to_bytes

e = 65537
N = 171535569705812677946486440394414039183
C = 144920187573935688963094252035058771259

factors = factorint(N)
p, q = list(factors.keys())

phi_N = (p - 1) * (q - 1)

d = mod_inverse(e, phi_N)

M = pow(C, d, N)

flag = long_to_bytes(M).decode()
print(flag)

