### Reverse Engineering Writeup

- **Challenge**: React-based CTF (reverse, difficulty ~8/10). Input must satisfy multiple validators. No `flag{}` header; input is the raw flag.
- **Goal**: Find the string that passes all checks.

### High-level structure
- UI shows checklist of validators.
- The code splits the input into 5 chunks (sizes 6,6,6,6,2) and applies per-chunk reversible transforms plus several global constraints.
- All logic lives in `src/validators.js` (compiled by Vite), which is ideal for reverse engineering from the built bundle.

### Validators overview
- **Length must match**: Exactly 26 characters.
- **Underscores in place**: Underscores at positions 5, 12, and 20 (0-based).
- **Ending and uppercase**: Last char is `?`; total uppercase letters are 3.
- **Totals: sum & xor**: Sum of char codes is 2259, XOR of all codes is 7.
- **Chunk#0 transform**: First 6 chars `XOR`-ed with mask `[5,7,9,11,13,15]` equals target `[87,52,61,104,121,80]`.
- **Chunk#1 transform**: Next 6 chars `(code + mask) & 0x7F` with mask `[17,23,5,31,7,11]` equals `[127,75,89,80,125,62]`.
- **Chunk#2 transform**: Next 6 chars `(code - mask) & 0x7F` with mask `[9,4,12,1,3,7]` equals `[86,110,39,117,98,107]`.
- **Chunk#3 transform**: Next 6 chars `XOR` with `[13,26,39,52,65,78]` equals `[126,41,120,92,32,60]`.
- **Chunk#4 transform**: Tail 2 chars `((code ^ 0x2A) + 7) & 0x7F` equals `[117,28]`.
- **Weighted mod checks**: For each chunk, sum of `(i+1)*code` mod 97 equals `[43,6,3,50,0]`.
- **Digit frequencies**: Counts are `3:4`, `4:2`, `1:1`.
- **Reverse prefix**: First 5 characters reversed equal `tc43R`.

All transforms are reversible, which makes the final flag uniquely determined.

### Reversing approach
1. Locate `validators.js` in the built output or dev source. Identify masks and targets.
2. Invert per-chunk transforms:
   - XOR -> XOR with same mask.
   - Add-mask -> subtract mask under `& 0x7F`.
   - Subtract-mask -> add mask under `& 0x7F`.
   - Tail op -> reverse the arithmetic and XOR.
3. Concatenate recovered chunks to get the candidate.
4. Confirm with the global constraints (sum/xor/positions/weighted mods/digit counts).

### Provided solver
`solver.py` implements the inverses and reconstructs the exact flag, then asserts the global constraints. Run:

```bash
python3 solver.py
```

It prints the flag.

### Result
The recovered flag is the string that the web UI accepts as fully valid. Follow the solver or redo the steps manually by reversing each validator.
