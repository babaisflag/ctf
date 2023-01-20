# Get all available gadgets for roplike

from pwn import *
context.arch = 'amd64'

p = remote("chals.2022.squarectf.com", 4096)
#p = process("roplike-easy")

gadgets = {}
for i in range(1, 101):
    print(f"Round {i} in progress...")
    for g in range(5):
        p.recvuntil(b"Gadget " + str(g).encode() + b":")
        roppis = u32(bytes.fromhex(p.recv(8).decode()))
        gadget = p.recvline(keepends=False).decode()
        gadget_disasm = disasm(bytes.fromhex(gadget))
        gadget += f"({str(roppis)}):"
        gadgets[gadget] = gadget_disasm
    p.sendline(b"c")
    p.sendline()

with open('gadgets-easy', 'w') as f:
    for k,v in gadgets.items():
        print(k)
        print(v)

        f.write(k+'\n')
        f.write(v+'\n')

p.close()
