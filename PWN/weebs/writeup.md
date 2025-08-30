## Weebs Arena Online – PWN (fmt + bof to RCE)

### Overview
- **Theme**: Anime battle arena
- **Bugs**: Format string in `chant()` and stack buffer overflow in `duel()`
- **Goal**: Achieve RCE via libc `system("/bin/sh")`
- **Protections**: PIE disabled, RELRO full, NX enabled, stack canary present
- **Difficulty**: 8/10

### Files
- `src/chal.c`: Vulnerable service
- `Makefile`: Build with chosen mitigations
- `docker/Dockerfile`, `docker/entry.sh`, `docker-compose.yml`: Deployment
- `exploit.py`: Pwntools exploit

### Build & Run (Docker Compose)
```bash
docker compose build
docker compose up -d
# Service on 127.0.0.1:4012
```

### Local Binary (optional)
If you want to run locally outside Docker:
```bash
cd src && make chall && ./chal
```

### Vulnerabilities
1. Format string in `printf(buf)` leaks stack including canary.
2. BOF via `gets(arena)` allows controlled return after canary.
3. Binary prints a stable libc address through `dlsym(RTLD_NEXT, "puts")` to aid remote/libc resolution.

### Exploitation Plan
1. Read banner and parse the puts leak. Compute libc base.
2. Use format string to brute-read many `%p` slots and identify the canary (ends with `00`).
3. Determine padding from buffer start to canary (script tries common values and verifies by safely returning to `menu`).
4. Craft payload: `padding || canary || saved_rbp || ROP(system("/bin/sh"))`.

### Running the Exploit
```bash
# local (auto-detects ./build/chal or ./src/chal)
python3 exploit.py

# remote via docker compose
python3 exploit.py --remote --host 127.0.0.1 --port 4012

# optionally specify libc if needed
python3 exploit.py --remote --host HOST --port PORT --libc /path/to/libc.so.6
```

### Notes on Robustness
- Exploit autodetects canary from format output without hardcoding offsets.
- Padding is auto-discovered by probing common lengths and validating return to `menu`.
- Libc base computed from printed `puts` address, supports mismatched libcs by `--libc`.

### Intended Solve
1. Parse hint leak → compute libc base.
2. Fmt string → leak stack canary.
3. BOF → overwrite return with ROP chain calling `system("/bin/sh")`.

### Potential Pitfalls
- If your environment lacks `gets`, compile on glibc-based systems; container uses Ubuntu 22.04.
- ASLR remains on; exploit works by deriving base addresses.

### Flag Handling
When deployed, run the service under a wrapper that drops a flag to the process environment/current directory. The exploit gains a shell; retrieve the flag via `cat /flag` (add via container if desired).