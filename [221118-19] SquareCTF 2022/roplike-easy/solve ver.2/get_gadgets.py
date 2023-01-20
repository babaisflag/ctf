# Get all available gadgets for roplike

from pwn import *
from tqdm import tqdm
import os

context.arch = 'amd64'

with open('glist', 'w') as f1, open('glist-short', 'w') as f2:
    for i in tqdm(range(len(os.listdir('gadgets')))):
        with open(f"gadgets/{i}", "rb") as g:
            data = g.read()
        price = u32(data[:4])
        gadget_bytes = data[4:]
        gadget_disasm = disasm(gadget_bytes)
        gadget_disasm_short = disasm(gadget_bytes, byte=False, offset=False).replace('\n', '; ')
        gadget = f"{data.hex()}({price})"

        f1.write(gadget+'\n')
        f1.write(gadget_disasm+'\n')
        f2.write("{:<34} {:<24} {:>10}".format(gadget_disasm_short, gadget_bytes.hex(), price)+'\n')
