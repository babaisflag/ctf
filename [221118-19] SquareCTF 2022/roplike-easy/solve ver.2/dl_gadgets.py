from pwn import *
from tqdm import tqdm

context.arch = 'amd64'

p = remote("localhost", 49153)

gadgets = set()

for i in tqdm(range(1, 101)):
    for g in range(5):
        p.recvuntil(f"Gadget {g}:".encode())
        gadget = bytes.fromhex(p.recvline(keepends=False).decode())
        gadgets.add(gadget)
    p.sendline(b"c")
    sleep(0.1)
    p.sendline()

for idx, item in enumerate(gadgets):
    with open(f"./gadgets/{str(idx)}", 'wb') as f:
        f.write(item)

p.close()
