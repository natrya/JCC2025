### CIPH7 v1 Writeup

This challenge uses a fully invertible 8-step pipeline over bytes with arithmetic in Z_256. The seed is disclosed in the ciphertext header, so the task is to carefully invert each transformation.

- **Ciphertext format**: `CIPH7:1:SEED=0xXXXXXXXX:LEN=N:DATA=BASE64`
- **PRNG**: xorshift32 with the given seed.

### Parameters derived from the seed
- **a**: `1 + 2 * (((seed % 127) + 1) % 127)` (odd multiplier)
- **b0**: `(seed >> 8) & 0xFF`
- **r1**: `(seed >> 24) & 0xFF`
- **r2**: `1 + ((seed >> 16) & 7)`
- **iv**: `(seed ^ 0xA5A5A5A5) & 0xFF`
- **L**: `3 + (seed % 5)`

### Encryption steps (summary)
1. Prefix checksums `c0 = sum(m_i)` and `c1 = sum(i * m_i)`.
2. Affine map per index: `y = (a * x + b0 + i) mod 256`.
3. Global permutation π via Fisher–Yates using PRNG.
4. S-box: `x -> ROTL8(x ^ r1, r2)`.
5. XOR keystream from PRNG.
6. Running sum with IV: `y0 = x0 + iv`, `yi = xi + y(i-1)`.
7. Chunk reversal on blocks of length L.
8. Base64 + header.

### Decryption steps (solver logic)
Apply in reverse order, but consume the PRNG in the same order as encryption:
1. Reverse chunk reversal.
2. Undo running sum: `x0 = y0 - iv`, `xi = yi - y(i-1)`.
3. Build permutation π from PRNG, then build keystream from the same PRNG state.
4. XOR the keystream.
5. Inverse S-box: `x -> ROTR8(x, r2) ^ r1`.
6. Apply π⁻¹ constructed from π.
7. Inverse affine: `x = a_inv * (y - b0 - i) mod 256` where `a_inv` is the modular inverse of `a` modulo 256.
8. Remove the first two bytes and verify `c0` and `c1` against the recovered message.

### Integrity check
After decryption, compute:
- `c0' = sum(m_i) mod 256`
- `c1' = sum(i * m_i) mod 256`
Compare with the first two bytes of the recovered preimage. If they match, the plaintext is consistent.

### Running the tools
```bash
# Encrypt using a random seed
python3 encrypt.py --infile flag.txt --outfile cipher.txt

# Or specify a seed for reproducibility
python3 encrypt.py --seed 0x1234ABCD

# Solve
python3 solver.py --infile cipher.txt
```

### Common pitfalls
- Build π and keystream in the same PRNG order used by encryption.
- Inverse permutation mapping: if encryption uses `out[i] = in[pi[i]]`, the inverse must satisfy `in[j] = out[inv_pi[j]]`.
- Modular inverse exists only for odd `a` (guaranteed by construction).
- Rotation counts are in [1..8); `r2 = 0` never occurs.

### Difficulty
The challenge is designed to require understanding each reversible step (6–10 careful actions) and implementing the correct inverse order and PRNG consumption.
