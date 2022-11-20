from pwn import *
context.arch = 'amd64'

p = remote("chals.2022.squarectf.com", 4096)

gadgets = []
for i in range(1, 101):
    print(f"Round {i} in progress...")
    for g in range(5):
        p.recvuntil(b"Gadget " + str(g).encode() + b":")
        gadget = bytes.fromhex(p.recvline(keepends=False).decode())
        if gadget not in gadgets:
            gadgets.append(gadget)
    p.sendline(b"c")
    p.sendline()

for i in range(1024):
    for j in range(len(gadgets)):
        idx = i*len(gadgets) + j + 1
        with open(str(idx), 'wb') as f:
            f.write(gadgets[j])

p.close()
