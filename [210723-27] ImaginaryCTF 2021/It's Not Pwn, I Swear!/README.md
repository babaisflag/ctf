# It's Not Pwn, I Swear! (Rev, 250 pts)

## Description

I've made a challenge that's not pwn! Just because it looks like a bird and sings like a bird doesn't mean it's pwn. And good thing it's not pwn, because this binary has full protections (including a canary!).

## Attachments

[notpwn](notpwn)

## Solution

Apparently this is totally not a pwn and is a reverse challenge - so let's try putting it through binary ninja.

![image](https://user-images.githubusercontent.com/11196638/128268955-a4539da6-7034-4433-9c3a-888bbf277dcc.png)

Hmm. That looks like a pwn to me. A quick checksec confirms that it has full protections, as described:

![image](https://user-images.githubusercontent.com/11196638/128269049-836b2207-e926-4db6-9e05-d66179f2dd57.png)

Looking at the functions, `main` just calls `vuln`, which is:

![image](https://user-images.githubusercontent.com/11196638/128269192-161acd49-2256-4f53-ab4a-cc5a02dc59f6.png)

The `win` function:

![image](https://user-images.githubusercontent.com/11196638/128269216-0be0d904-bcba-4df7-8217-6806cb6e847b.png)

The `vuln` function has a `gets` function, so we could do a buffer overflow, but there's a canary in the way that we can't do much about.

After thinking about ways to leak the canary or bypass it somehow for 30 minutes, I went and clicked on all the functions. Hey, maybe they hid something in the `__stack_chk_fail` somehow?

![image](https://user-images.githubusercontent.com/11196638/128269495-cc9b7d66-b48c-4dd1-be15-291476670289.png)

Oh.

In hindsight, I should've looked closer at the function list, since there were clearly two `__stack_chk_fail` functions, even in different colors too:

![image](https://user-images.githubusercontent.com/11196638/128269574-82350187-d94e-425c-935e-716236befac1.png)

At least we have it now, so we can reverse this!

![image](https://user-images.githubusercontent.com/11196638/128269849-7e45383f-048e-4c40-a673-f5dfceee00b6.png)

The first large block sets up the stacks with a bunch of bytes; the loop (labeled 2) does some operations 3 times, then the other loop (labeled 3) does some operations 9 times.

The stack after the first large block:

```
        | (continues upward) |rsp+0x98
        | 0x9660243fd1a3e9f4 |rsp+0x90
        | 0x2edf28aed93efc5d |rsp+0x88; let C  = [rsp+0x88] = 0x2edf...
        | 0x65bbfa1e87aa1f8d |rsp+0x80; let B  = [rsp+0x80] = 0x65bb...
        | 0x317ee37c444051c9 |rsp+0x78; let A  = [rsp+0x78] = 0x317e...
        |                    |rsp+0x70; let c2 = [rsp+0x70]
        |       canary       |rsp+0x68; let c1 = [rsp+0x68]
        |  <written by gets> |rsp+0x60
        |  <2 bytes written> |rsp+0x58; the gets function would've written starting from rsp+0x56
        |                    |rsp+0x50
rbp+0x8 |     saved_rip      |rsp+0x48
rbp     |     saved_rbp      |rsp+0x40
rbp-0x8 |                    |rsp+0x38
rbp-0x10|     [rsp+0x70]     |rsp+0x30; has c2
rbp-0x18|     [rsp+0x68]     |rsp+0x28; has c1
rbp-0x20|      rsp+0x70      |rsp+0x20
rbp-0x28|      rsp+0x70      |rsp+0x18; pointer
rbp-0x30| 0x6231726435333364 |rsp+0x10; let X = 0x6231...
rbp-0x38|                    |rsp+0x8
rbp-0x40|         0          |rsp     ; counter for the loop
```

With this, let's look at the loop (label 2):

![Capture](https://user-images.githubusercontent.com/11196638/128280035-4506d7d3-b2b2-4c35-aad5-951ae0301416.PNG)

The first time through the loop, `[rbp-0x18]` (`c1`) is multiplied with `[rbp-0x30]` (`X`), truncated by 2<sup>64</sup>; this result is added to `[rbp-0x10]` which is `[rsp+0x70]` (`c2`). Then `[rbp-0x30]` is updated with the result of the addition, and 8 is added to `[rbp-0x28]`. The `pointer` now is `rsp+0x78`, pointing to `A`. `cmp` compares the value pointed by the `pointer` (currently `A`) with the value calculated previously, saved at `[rbp-0x30]`. If they're not equall, it will call the real `__stk_chk_failed`.

Simplifying, the comparison checks for this:
```
(c1 * X) % (2^64) + c2 == A
```

Going through the loop 3 times, we have 3 equations:
```
(c1 * X) % (2^64) + c2 == A
(c1 * A) % (2^64) + c2 == B
(c1 * B) % (2^64) + c2 == C
```

where `c1` and `c2` are values we can control, and `A`, `B`, `C`, and `X` are fixed values.

Solve for c1 and c2, thereby getting the input we need:
```py
from pwn import p64

A = 0x317ee37c444051c9
B = 0x65bbfa1e87aa1f8d
C = 0x2edf28aed93efc5d
X = 0x6231726435333364
M = pow(2,64)

# first equation - second equation = c1*(X-A) = A-B (modulo M)
# solve c1 by getting modular multiplicative inverse
c1 = pow(X-A, -1, M) * (A-B+M) % M
# then c2 by plugging in c1
c2 = (A - (c1*X)) % M

# The resulting input we need to pass the loop
print(p64(c1)+p64(c2))  # b'th3c@n@ryh@sd!3d'
```

No wonder the description was talking about birds and canaries.

Minding the 10 bytes we need in front due to `gets` in `vuln` reading to `rbp-0x12`:
```py
import pwn
p = pwn.process('./notpwn')
p.recvuntil(b'input: ')
p.sendline(b'A'*10 + b'th3c@n@ryh@sd!3d')
print(p.recvall())
```
gives us the flag.

## Flag
```
ictf{m@ry_h@d_@_pr3++y_b!rd_f3ath3rs_bri6ht_and_ye11ow_}
```

## Afterthoughts

The other loop seems to go through the other data on the stack that was initialized in the first big block, and making it actually become our flag by some operations. I also wasted a lot of time because I mistakenly read one of the `add` as `sub`, and thought I had to overwrite the 8 bytes below the canary instead of above it. It was an interesting challenge overall.
