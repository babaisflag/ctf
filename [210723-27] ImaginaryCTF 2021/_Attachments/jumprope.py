from pwn import ROP, ELF, p64
# get val
def test(a):
    if a != 1:
        factor = 2
        while factor < a-1:
            if a % factor != 0:
                factor += 1
            else:
                return 0
        return 1
    return 0

def next(val):
    for c in range(8):
        v18 = 0
        v20 = val
        for i in range(8):
            a = i+1
            if test(a) != 0:
                a = v20
                a &= 1
                v18 ^= a
            v20 = v20 >> 1
        val = val >> 1
        a = v18 << 7
        val += a
    return val

val = 2
val_res = b''
for counter in range(88):
    val = next(val)
    val_res += val.to_bytes(1, 'little')

c = 0x401211
o = 0x40122e
r = 0x40125b
e = 0x401278
t = 0x401295
rdi_ret = ROP(ELF('./jumprope')).rdi[0]
o_input = 0x1337c0d3
t_input = 0xdeadface
jumprope = p64(c)+p64(rdi_ret)+p64(o_input)+p64(o)+p64(r)+p64(r)+p64(e)+p64(c)+p64(rdi_ret)+p64(t_input)+p64(t)

x = 0xfd3cc40e76ff4b451f40f4e680b8b5e8768e3bf8e4bdc9c73fe6cf15949a8a284e5e1e3f25d42ca936284240938d0fffae2b2bdf7e1a4e0563d088e1a11f5a3d364fae897bd727d029c09ef020df697794e9580fb8ecf924.to_bytes(88, 'big')

flag = bytes([j^v^x_ for (j,v,x_) in zip(jumprope, val_res, x)])
print(flag)
