#!/usr/bin/env python3
"""
Solver for the custom CIPH7 v1 challenge ciphertext produced by encrypt.py.

Given a ciphertext line of the form:
  CIPH7:1:SEED=0xXXXXXXXX:LEN=N:DATA=BASE64

the solver performs the exact inverse of the 8-step pipeline and verifies
checksums. On success, it prints the recovered plaintext and an integrity
status line.
"""

import argparse
import base64
import re
from typing import List, Tuple


def rotr8(value: int, shift: int) -> int:
    s = shift & 7
    v = value & 0xFF
    return ((v >> s) | ((v << (8 - s)) & 0xFF)) & 0xFF


def modular_inverse_odd(a: int, modulus: int = 256) -> int:
    if a % 2 == 0:
        raise ValueError("Multiplier must be odd modulo 256")
    t, new_t = 0, 1
    r, new_r = modulus, a
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r != 1:
        raise ValueError("No inverse exists")
    return t % modulus


class XorShift32:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF
        if self.state == 0:
            self.state = 0x6C8E9CF5

    def next_u32(self) -> int:
        x = self.state & 0xFFFFFFFF
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state

    def next_byte(self) -> int:
        return self.next_u32() & 0xFF

    def randint(self, bound_inclusive: int) -> int:
        if bound_inclusive < 0:
            raise ValueError("bound_inclusive must be >= 0")
        while True:
            r = self.next_u32()
            bound = bound_inclusive + 1
            limit = (0x100000000 // bound) * bound
            if r < limit:
                return r % bound


def fisher_yates_permutation(n: int, rng: XorShift32) -> List[int]:
    pi = list(range(n))
    for i in range(n - 1, 0, -1):
        j = rng.randint(i)
        pi[i], pi[j] = pi[j], pi[i]
    return pi


def invert_permutation(pi: List[int]) -> List[int]:
    inv = [0] * len(pi)
    for i, p in enumerate(pi):
        inv[p] = i
    return inv


def compute_checksums(msg: bytes) -> Tuple[int, int]:
    c0 = 0
    c1 = 0
    for i, b in enumerate(msg):
        c0 = (c0 + b) & 0xFF
        c1 = (c1 + (i * b)) & 0xFF
    return c0, c1


HEADER_RE = re.compile(
    r"^CIPH7:1:SEED=0x([0-9A-Fa-f]{8}):LEN=([0-9]+):DATA=([A-Za-z0-9+/=]+)$"
)


def parse_ciphertext_line(line: str) -> Tuple[int, bytes]:
    m = HEADER_RE.match(line.strip())
    if not m:
        raise ValueError("Invalid ciphertext header format")
    seed_hex, length_str, b64 = m.groups()
    seed = int(seed_hex, 16)
    raw = base64.b64decode(b64)
    declared_len = int(length_str)
    if declared_len != len(raw):
        raise ValueError("Declared LEN does not match data length")
    return seed, raw


def decrypt_bytes(seed: int, data: bytes) -> Tuple[bytes, bool]:
    seed &= 0xFFFFFFFF

    # Step 6 inverse: undo chunk reversal
    L = 3 + (seed % 5)
    work = bytearray(data)
    for i in range(0, len(work), L):
        work[i : i + L] = reversed(work[i : i + L])

    # Step 5 inverse: undo running sum with IV
    iv = (seed ^ 0xA5A5A5A5) & 0xFF
    out = bytearray(len(work))
    prev = 0
    for i, y in enumerate(work):
        if i == 0:
            x = (y - iv) & 0xFF
            prev = y
        else:
            x = (y - prev) & 0xFF
            prev = y
        out[i] = x
    work = out

    # Prepare RNG and consume exactly as in encryption: permutation first, then keystream
    rng = XorShift32(seed)
    pi = fisher_yates_permutation(len(work), rng)
    ks = bytearray(rng.next_byte() for _ in range(len(work)))

    # Step 4 inverse: XOR keystream
    work = bytearray([(x ^ k) & 0xFF for x, k in zip(work, ks)])

    # Step 3 inverse: inverse S-box
    r1 = (seed >> 24) & 0xFF
    r2 = 1 + ((seed >> 16) & 7)
    work = bytearray([rotr8(x, r2) ^ r1 for x in work])

    # Step 2 inverse: apply inverse permutation
    inv_pi = invert_permutation(pi)
    work = bytearray(work[inv_pi[i]] for i in range(len(work)))

    # Step 1 inverse: inverse affine map with index-dependent offset
    a = 1 + 2 * (((seed % 127) + 1) % 127)
    b0 = (seed >> 8) & 0xFF
    a_inv = modular_inverse_odd(a)
    tmp = []
    for i, y in enumerate(work):
        x = (a_inv * ((y - b0 - i) & 0xFF)) & 0xFF
        tmp.append(x)
    work = bytearray(tmp)

    # Step 0: remove checksums and verify
    if len(work) < 2:
        return b"", False
    c0, c1 = work[0], work[1]
    msg = bytes(work[2:])
    cc0, cc1 = compute_checksums(msg)
    ok = (c0 == cc0) and (c1 == cc1)
    return msg, ok


essential_help = """
Input file must contain a single ciphertext line produced by encrypt.py.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve CIPH7 ciphertext and recover plaintext")
    parser.add_argument("--infile", default="cipher.txt", help="Input ciphertext file (default: cipher.txt)")
    args = parser.parse_args()

    with open(args.infile, "r") as f:
        line = f.read().strip()

    seed, raw = parse_ciphertext_line(line)
    pt, ok = decrypt_bytes(seed, raw)
    print(pt.decode('utf-8', errors='replace'))
    print(f"[integrity] checksums {'OK' if ok else 'FAILED'}")


if __name__ == "__main__":
    main()
