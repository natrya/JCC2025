#!/usr/bin/env python3
import argparse
import hashlib
import random
import re
from pathlib import Path

# https://nikko.id/read.php?id=so-random

NUM_PROBLEMS_DEFAULT = 10
SEED_DIGITS = 6
HASH_LENGTH = 32


def read_md5_from_flag(flag_path: Path) -> str:
    text = flag_path.read_text(encoding="utf-8").strip().lower()
    if re.fullmatch(r"[0-9a-f]{32}", text):
        return text
    sample = hashlib.md5(b"NIKKO_ENGGALIANO_PRATAMA").hexdigest()
    return sample


def derive_seed_from_md5(flag_md5: str) -> str:
    numeric_seed = int(flag_md5, 16) % 1_000_000
    return f"{numeric_seed:06d}"


def build_permutation(seed_numeric: int, length: int) -> list[int]:
    indices = list(range(length))
    rng = random.Random(seed_numeric)
    rng.shuffle(indices)
    return indices


def apply_permutation(text: str, permutation: list[int]) -> str:
    return "".join(text[j] for j in permutation)


def hex_alphabet() -> str:
    return "0123456789abcdef"


def build_hex_substitution(seed_numeric: int) -> tuple[dict[str, str], dict[str, str]]:
    # Build a seeded random bijection on hex alphabet
    chars = list(hex_alphabet())
    rng = random.Random(seed_numeric ^ 0x9E3779B97F4A7C15)
    rng.shuffle(chars)
    sub = {orig: repl for orig, repl in zip(hex_alphabet(), chars)}
    inv = {v: k for k, v in sub.items()}
    return sub, inv


def apply_substitution(text: str, sub: dict[str, str]) -> str:
    return "".join(sub[c] for c in text)


def spiral_order(rows: int, cols: int) -> list[int]:
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    order: list[int] = []
    while left <= right and top <= bottom:
        for c in range(left, right + 1):
            order.append(top * cols + c)
        top += 1
        if top > bottom:
            break
        for r in range(top, bottom + 1):
            order.append(r * cols + right)
        right -= 1
        if left > right:
            break
        for c in range(right, left - 1, -1):
            order.append(bottom * cols + c)
        bottom -= 1
        if top > bottom:
            break
        for r in range(bottom, top - 1, -1):
            order.append(r * cols + left)
        left += 1
    return order


def generate_single(flag_md5: str, out_file: Path) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    seed_str = derive_seed_from_md5(flag_md5)
    seed_numeric = int(seed_str)
    sub, _inv = build_hex_substitution(seed_numeric)
    stage1 = apply_substitution(flag_md5, sub)
    spiral_perm = spiral_order(4, 8)
    stage2 = apply_permutation(stage1, spiral_perm)
    perm3 = build_permutation(seed_numeric ^ 0xA5A5A5, HASH_LENGTH)
    final_cipher = apply_permutation(stage2, perm3)

    content = (
        "FORMAT=NIKKO\n"
        f"SEED={seed_str}\n"
        f"DATA={final_cipher}\n"
    )
    out_file.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate randomize.txt from md5 in flag.txt using a reversible algorithm.")
    parser.add_argument("--out", type=Path, default=Path("randomize.txt"), help="output file (default: randomize.txt)")
    parser.add_argument("--flag", type=Path, default=Path("flag.txt"), help="path to flag.txt containing md5 hex")
    args = parser.parse_args()

    flag_md5 = read_md5_from_flag(args.flag)
    generate_single(flag_md5, args.out)
    print(f"Generated {args.out.resolve()}.")


if __name__ == "__main__":
    main()