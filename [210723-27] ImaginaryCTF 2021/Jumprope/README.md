## Jumprope (Reversing, 200 pts)

### Description

CENSORED and CENSORED Sitting in a tree, H-A-C-K-I-N-G! First comes pwn, Then comes rev, Then comes a flag And a happy dev!

### Attachment

[`jumprope`](jumprope)

### Solution

Checksec:
```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```
```
$ ./jumprope
Ice cream!
Soda Pop!
Cherry on top!
Is your flag exact?
Well, let's find out!

Eighty-eight characters!
A secret well kept!
If you get it right,
I'll shout CORRECT!

>>>
```
Looks like the correct flag input will make it shout CORRECT. In the disassembly, we see `main`, `checkFlag`, `next`, `test`, `c`, `o`, `r`, `e`, `t`. The single-lettered functions simply print out its respective characters, i.e. `c` prints out `'C'`. The `o` and `t` functions, before printing, check if `edi` is `0x1337c0d3` and `0xdeadface`, respectively. Already feels like ROP.

The `main` simply prints the console output in the beginning, and calls `checkflag`. From the disassembly, I constructed a pseudocode ([`jumprope.sol`](jumprope.sol)):
```
val = 2
dead = 0
count = 0
x = <some big bytestring>

def test(a):	// test if prime; return 1 if prime, return 0 if composite
	if (a != 1):
		vc = 2
		while (vc < a-1):
			if (a % vc != 0):
				vc++
			else:
				return 0
		return 1
	return 0

def next(val):
	for(c = 0; c <= 7; c++):
		v18 = 0
		v20 = val
		for(i = 0; i <= 7; i++):
			a = i+1
			if(test(a) != 0):
				a = v20
				a &= 1
				v18 ^= a
			v20 = v20 >> 1
		val = val >> 1
		a = v18 << 7
		val += a
	return val
	
def checkflag():
	&ret = rbp+8;
	scanf("%88s%c", &ret, &dead)
	count = 8
	for (; count <= 95; count++):
		val = next(val)
		ecx= *(char*)(rbp+count)	// our input
		rdx = x[(count-8)*8] // indexed by bytes
		edx = val^edx^ecx
		*(rbp+count) = edx
	return 0
```
`x` is some big data region, that has a non-zero byte every 8 bytes from index 0. Concatenating all the non-zero bytes gives `x = 0xfd3cc40e76ff4b451f40f4e680b8b5e8768e3bf8e4bdc9c73fe6cf15949a8a284e5e1e3f25d42ca936284240938d0fffae2b2bdf7e1a4e0563d088e1a11f5a3d364fae897bd727d029c09ef020df697794e9580fb8ecf924`.

`test` function simply checks if the number is prime by trying division of every positive integer less than the given number. `next` function gets the next value with some bitwise operations. `checkflag` xor's a byte from our input, a non-zero byte from `x`, and the `val` from `next(val)`. `val` is 2 initially. At every loop, it writes the byte to `rbp+count`, where `count` starts from 8 and increases by 1. So this *is* a ROP, we just write return addresses for the functions in the order `c`, `o`, `r`, `r`, `e`, `c`, `t`. For `o` and `t`, we need to put two more values on the stack: `pop rdi; ret` gadget and the values that need to go into `rdi`.
```py
# getting "pop rdi; ret" gadget
In  : from pwn import *
    : ROP(ELF('./jumprope')).rdi
Out : Gadget(0x40148b, ['pop rdi', 'ret'], ['rdi'], 0x8)
```
Then we can get the full ropchain:
```py
from pwn import *
c = 0x401211
o = 0x40122e
r = 0x40125b
e = 0x401278
t = 0x401295
rdi_ret = ROP(ELF('./jumprope')).rdi[0]
o_input = 0x1337c0d3
t_input = 0xdeadface
jumprope = p64(c)+p64(rdi_ret)+p64(o_input)+p64(o)+p64(r)+p64(r)+p64(e)+p64(c)+p64(rdi_ret)+p64(t_input)+p64(t)
```
Finally we need to get the value `val`, simply by translating the pseduocode into python:
```py
# get val
val = 2

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

val_res = b''
for counter in range(88):
    val = next(val)
    va_res += val.to_bytes(1, 'little')
```
The result of the execution of `./jumprope` is our ropchain, which is `x ^ val_res ^ flag`, where `flag` is our input. We want to get the flag, so `flag = jumprope ^ val_res ^ x`.

Full code ([`jumprope.py`](jumprope.py))
```py
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
```
```
$ python3 jumprope.py
b'ictf{n0t_last_night_but_the_night_bef0re_twenty_f0ur_hackers_came_a_kn0cking_at_my_d00r}'
```

### Flag
```
ictf{n0t_last_night_but_the_night_bef0re_twenty_f0ur_hackers_came_a_kn0cking_at_my_d00r}
```
