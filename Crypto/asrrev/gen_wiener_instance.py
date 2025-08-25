import secrets
import math


def egcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def invmod(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("inverse does not exist")
    return x % m


def is_probable_prime(n: int, k: int = 40) -> bool:
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 as 2^r * d with d odd
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # in [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        skip = False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                skip = True
                break
        if skip:
            continue
        return False
    return True


def generate_prime(bits: int) -> int:
    assert bits >= 2
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate


def integer_fourth_root(n: int) -> int:
    # returns floor(n ** 0.25) without floats
    low, high = 0, 1
    while high ** 4 <= n:
        high *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        if mid ** 4 <= n:
            low = mid
        else:
            high = mid
    return low


def main():
    bits = 512
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    root4 = integer_fourth_root(n)
    # Wiener's condition: d < n**0.25 / 3
    bound = max(2, root4 // 4)  # a bit stricter for safety
    while True:
        d = secrets.randbelow(bound - 1) + 1  # in [1, bound-1]
        if d <= 1:
            continue
        if math.gcd(d, phi) != 1:
            continue
        try:
            e = invmod(d, phi)
        except ValueError:
            continue
        if e < n:  # typical RSA public exponent property
            break

    # Load flag from flag.txt if available (binary-safe). Fallback to default.
    try:
        with open("flag.txt", "rb") as f:
            flag = f.read().strip()
        if not flag:
            raise ValueError("flag.txt is empty")
    except Exception:
        flag = b"JCC{wiener_weak_d_rsa_challenge_2025}"

    m = int.from_bytes(flag, "big")
    if m >= n:
        raise ValueError(
            "Flag integer is >= n. Use a shorter flag or increase key size."
        )
    c = pow(m, e, n)

    print("# --- RSA instance (Wiener vulnerable untuk adik adik) ---")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"c = {c}")
    print()
    print("# --- Private (for kita kita aja panitia) ---")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"d = {d}")
    print(f"phi = {phi}")

    # Write participant file
    soal_content = f"""
#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes, bytes_to_long


# Public parameters
n = {n}
e = {e}

# Ciphertext of the flag
c = {c}


def main():
    print("n =", n)
    print("e =", e)
    print("c =", c)


if __name__ == "__main__":
    main()
"""

    with open("soal.py", "w") as f:
        f.write(soal_content)

    # Write organizer secrets
    with open("organizer_private.txt", "w") as f:
        f.write("p = " + str(p) + "\n")
        f.write("q = " + str(q) + "\n")
        f.write("d = " + str(d) + "\n")
        f.write("phi = " + str(phi) + "\n")
        try:
            f.write("flag = " + flag.decode("utf-8") + "\n")
        except Exception:
            # Fallback representation if non-UTF8 bytes
            f.write("flag_hex = " + flag.hex() + "\n")


if __name__ == "__main__":
    main()


