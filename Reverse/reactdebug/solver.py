#!/usr/bin/env python3

MASK0 = [5, 7, 9, 11, 13, 15]
TARGET0 = [87, 52, 61, 104, 121, 80]

MASK1 = [17, 23, 5, 31, 7, 11]
TARGET1 = [127, 75, 89, 80, 125, 62]

MASK2 = [9, 4, 12, 1, 3, 7]
TARGET2 = [86, 110, 39, 117, 98, 107]

MASK3 = [13, 26, 39, 52, 65, 78]
TARGET3 = [126, 41, 120, 92, 32, 60]

MASK4_CONST = 0x2A
TARGET4 = [117, 28]

TOTAL_SUM = 2259
TOTAL_XOR = 7
LENGTH = 26


def inv_chunk0():
    # codes ^ mask = target -> codes = target ^ mask
    return [TARGET0[i] ^ MASK0[i] for i in range(6)]


def inv_chunk1():
    # (codes + mask) & 0x7F = target -> codes = (target - mask) & 0x7F
    return [((TARGET1[i] - MASK1[i]) & 0x7F) for i in range(6)]


def inv_chunk2():
    # (codes - mask) & 0x7F = target -> codes = (target + mask) & 0x7F
    return [((TARGET2[i] + MASK2[i]) & 0x7F) for i in range(6)]


def inv_chunk3():
    # codes ^ mask = target -> codes = target ^ mask
    return [TARGET3[i] ^ MASK3[i] for i in range(6)]


def inv_chunk4():
    # ((codes ^ 0x2A) + 7) & 0x7F = target -> codes = (target - 7) ^ 0x2A
    return [((TARGET4[i] - 7) & 0x7F) ^ MASK4_CONST for i in range(2)]


def to_str(codes):
    return ''.join(chr(c) for c in codes)


def main():
    c0 = inv_chunk0()
    c1 = inv_chunk1()
    c2 = inv_chunk2()
    c3 = inv_chunk3()
    c4 = inv_chunk4()

    all_codes = c0 + c1 + c2 + c3 + c4
    s = to_str(all_codes)

    # sanity checks
    if len(s) != LENGTH:
        raise SystemExit('Length mismatch')
    if sum(all_codes) != TOTAL_SUM:
        raise SystemExit('Sum mismatch')
    from functools import reduce
    from operator import ixor
    xor_val = 0
    for v in all_codes:
        xor_val ^= v
    if xor_val != TOTAL_XOR:
        raise SystemExit('XOR mismatch')

    print(s)


if __name__ == '__main__':
    main()