#!/usr/bin/env python3
"""
Encrypt a message (by default from flag.txt) using a custom 8-step
invertible transformation pipeline. Output a single-line armored
ciphertext containing the seed and data, suitable for challenge
distribution.

Format:
  CIPH7:1:SEED=0xXXXXXXXX:LEN=N:DATA=BASE64

Steps (over Z_256):
  0) Prefix two checksums c0=Σ m_i, c1=Σ i m_i (mod 256)
  1) Affine byte map: x -> a*x + b0 + i (mod 256), with odd a
  2) Global permutation π via Fisher–Yates driven by xorshift32(seed)
  3) Nonlinear S-box: x -> ROTL8(x XOR r1, r2)
  4) Keystream XOR: x -> x XOR ks[i]
  5) Running sum with IV: y[i] = x[i] + y[i-1] (y[-1]=iv)
  6) Chunk reversal of length L = 3 + (seed mod 5)
  7) Base64 encode; attach header with seed and length

All steps are precisely inverted by solver.py.
"""

import argparse
import base64
import os
from typing import List, Tuple


def rotl8(value: int, shift: int) -> int:
    """Rotate an 8-bit integer left by shift (0..7)."""
    s = shift & 7
    v = value & 0xFF
    return ((v << s) | (v >> (8 - s))) & 0xFF


def modular_inverse_odd(a: int, modulus: int = 256) -> int:
    """Return modular inverse of odd a modulo 2^k (here 256)."""
    if a % 2 == 0:
        raise ValueError("Multiplier must be odd modulo 256")
    # Extended Euclidean Algorithm specialized to modulus 256
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
    """xorshift32 PRNG with 32-bit state."""

    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF
        if self.state == 0:
            self.state = 0x6C8E9CF5  # non-zero default

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
        # Use rejection sampling for unbiased result
        while True:
            r = self.next_u32()
            # 2^32 % (bound+1) can bias; trim using highest multiple
            bound = bound_inclusive + 1
            limit = (0x100000000 // bound) * bound
            if r < limit:
                return r % bound


def fisher_yates_permutation(n: int, rng: XorShift32) -> List[int]:
    """Generate a permutation of [0..n-1] using Fisher–Yates with rng."""
    pi = list(range(n))
    for i in range(n - 1, 0, -1):
        j = rng.randint(i)
        pi[i], pi[j] = pi[j], pi[i]
    return pi


def apply_permutation(data: List[int], pi: List[int]) -> List[int]:
    """Return data' where data'[i] = data[pi[i]]."""
    return [data[pi_i] for pi_i in pi]


def compute_checksums(msg: bytes) -> Tuple[int, int]:
    """Compute c0 = sum m_i, c1 = sum i*m_i modulo 256 over i starting at 0."""
    c0 = 0
    c1 = 0
    for i, b in enumerate(msg):
        c0 = (c0 + b) & 0xFF
        c1 = (c1 + (i * b)) & 0xFF
    return c0, c1


def encrypt_bytes(message: bytes, seed: int) -> str:
    """Encrypt message bytes using the fixed pipeline and return armored string."""
    seed &= 0xFFFFFFFF
    rng = XorShift32(seed)

    c0, c1 = compute_checksums(message)
    work = bytearray([c0, c1]) + bytearray(message)

    a = 1 + 2 * (((seed % 127) + 1) % 127)
    b0 = (seed >> 8) & 0xFF

    tmp = []
    for i, x in enumerate(work):
        y = (a * x + b0 + i) & 0xFF
        tmp.append(y)
    work = bytearray(tmp)

    pi = fisher_yates_permutation(len(work), rng)
    work = bytearray(apply_permutation(list(work), pi))

    r1 = (seed >> 24) & 0xFF
    r2 = 1 + ((seed >> 16) & 7)
    work = bytearray([rotl8(x ^ r1, r2) for x in work])

    ks = bytearray(rng.next_byte() for _ in range(len(work)))
    work = bytearray([(x ^ k) & 0xFF for x, k in zip(work, ks)])

    iv = (seed ^ 0xA5A5A5A5) & 0xFF
    acc = 0
    out = bytearray()
    for i, x in enumerate(work):
        if i == 0:
            acc = (x + iv) & 0xFF
        else:
            acc = (x + acc) & 0xFF
        out.append(acc)
    work = out

    L = 3 + (seed % 5)
    rev = bytearray(work)
    for i in range(0, len(rev), L):
        rev[i : i + L] = reversed(rev[i : i + L])
    work = rev

    armored = base64.b64encode(bytes(work)).decode('ascii')
    header = f"CIPH7:1:SEED=0x{seed:08X}:LEN={len(work)}:DATA={armored}"
    return header


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt flag.txt into challenge ciphertext")
    parser.add_argument("--infile", default="flag.txt", help="Input file containing the plaintext (default: flag.txt)")
    parser.add_argument("--outfile", default="cipher.txt", help="Output file for the ciphertext (default: cipher.txt)")
    parser.add_argument("--seed", type=lambda x: int(x, 0), default=None, help="32-bit seed in int or 0xHEX. If omitted, random is used")
    args = parser.parse_args()

    with open(args.infile, "rb") as f:
        pt = f.read().rstrip(b"\n")

    seed = args.seed if args.seed is not None else int.from_bytes(os.urandom(4), "big")
    ct_line = encrypt_bytes(pt, seed)

    with open(args.outfile, "w") as f:
        f.write(ct_line + "\n")

    print(ct_line)


if __name__ == "__main__":
    main()
