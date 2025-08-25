## KPOP Database PWN (Format String) – Difficulty 7/10

A small net service that contains a format string vulnerability in the search echo. It loads the flag into memory and also cats the flag at startup. The goal is to leak the flag via a format string attack.

### Layout
- `src/kpop.c`: Vulnerable service
- `src/Makefile`: macOS/Linux build, local `serve` via socat
- `Dockerfile`, `docker-compose.yml`: Ubuntu 22.04 container with socat netservice
- `src/flag.txt`: Sample local flag
- `exploit.py`: Pwntools exploit (local process, local net, and remote)
- `requirements.txt`

### Build locally (macOS)
```bash
cd src
make
```
Produces `src/bin/kpop`.

### Run locally (macOS) – interactive
```bash
cd src
make run
```

### Net service locally (socat on 127.0.0.1:9001)
```bash
cd src
make serve
# In another terminal:
nc 127.0.0.1 9001
```

### Docker (Ubuntu 22.04) – net service on 127.0.0.1:9001
```bash
# From repo root
docker compose build
docker compose up -d
# Test
nc 127.0.0.1 9001
```

### Exploit
Install deps:
```bash
python3 -m pip install -r requirements.txt
```

- Local net (expects `make serve` or docker-compose):
```bash
python3 exploit.py local
```

- Remote:
```bash
python3 exploit.py remote --host HOST --port PORT
```

- Spawn process locally (no socat):
```bash
python3 exploit.py proc
```

### Vulnerability
The search handler prints back user input unsafely:
```c
printf("Echo: ");
printf(query, g_flag);
```
Sending `%s` will dereference the extra variadic argument and print the `g_flag` contents.
