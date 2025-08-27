#!/usr/bin/env python3
import argparse
from pathlib import Path
import re
from typing import List


HASH_LENGTH = 32
SEED_DIGITS = 6


def parse_randomize_file(text: str) -> tuple[str, str]:
    # Expect lines: FORMAT=V1, SEED=xxxxxx, ALGO=..., DATA=32hex
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    kv = {}
    for ln in lines:
        if "=" in ln:
            k, v = ln.split("=", 1)
            kv[k.strip().upper()] = v.strip()
    if kv.get("FORMAT") != "V1":
        raise ValueError("Unsupported format")
    seed = kv.get("SEED", "")
    data = kv.get("DATA", "")
    if not re.fullmatch(r"\d{6}", seed):
        raise ValueError("Invalid seed")
    if not re.fullmatch(r"[0-9a-f]{32}", data):
        raise ValueError("Invalid data hex")
    return data, seed


def build_permutation(seed_numeric: int, length: int) -> list[int]:
    import random

    indices = list(range(length))
    rng = random.Random(seed_numeric)
    rng.shuffle(indices)
    return indices


def invert_permutation_apply(output_text: str, permutation: list[int]) -> str:
    # output[k] = input[ permutation[k] ]
    # Recover input by placing output[k] back into index permutation[k]
    recovered = [None] * len(permutation)
    for k, original_index in enumerate(permutation):
        recovered[original_index] = output_text[k]
    return "".join(recovered)  # type: ignore[arg-type]


def hex_alphabet() -> str:
    return "0123456789abcdef"


def build_hex_substitution(seed_numeric: int) -> tuple[dict[str, str], dict[str, str]]:
    import random

    chars = list(hex_alphabet())
    rng = random.Random(seed_numeric ^ 0x9E3779B97F4A7C15)
    rng.shuffle(chars)
    sub = {orig: repl for orig, repl in zip(hex_alphabet(), chars)}
    inv = {v: k for k, v in sub.items()}
    return sub, inv


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


def solve_cipher(randomize_text: str) -> str:
    data, seed_str = parse_randomize_file(randomize_text)
    seed_numeric = int(seed_str)

    # Stage 3 inverse: invert seeded global permutation
    perm3 = build_permutation(seed_numeric ^ 0xA5A5A5, HASH_LENGTH)
    stage2 = invert_permutation_apply(data, perm3)

    # Stage 2 inverse: invert 4x8 spiral permutation
    spiral_perm = spiral_order(4, 8)
    stage1 = invert_permutation_apply(stage2, spiral_perm)

    # Stage 1 inverse: invert hex substitution
    _sub, inv = build_hex_substitution(seed_numeric)
    original_md5 = "".join(inv[c] for c in stage1)

    if not re.fullmatch(r"[0-9a-f]{32}", original_md5):
        raise ValueError("Recovered string is not a valid md5 hex.")
    return original_md5


def find_input_files(directory: Path, filename: str) -> list[Path]:
    target = directory / filename
    return [target] if target.exists() else []


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve randomize.txt to recover the md5 flag.")
    parser.add_argument("--dir", type=Path, default=Path("."), help="directory containing randomize.txt (default: current dir)")
    parser.add_argument("--file", type=str, default="randomize.txt", help="filename to solve (default: randomize.txt)")
    args = parser.parse_args()

    files = find_input_files(args.dir, args.file)
    if not files:
        print("No input file found.")
        return

    f = files[0]
    text = f.read_text(encoding="utf-8")
    md5 = solve_cipher(text)
    print(f"{f.name}: {md5}")
    print(f"Recovered md5: {md5}")


if __name__ == "__main__":
    main()



