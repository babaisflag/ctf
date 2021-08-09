# Abnormal (Reversing, 250 pts)

Continuation from [Normal](README.md#normal-reversing-150-pts).

## Description

"Nors galore, more and more!", I swore, "Ignore xor, no ors anymore!" In short, neither xor nor or's required, for four more nors restores your xor.

## Attachments

[abnormal.v](abnormal.v) (comments mine)

## Solution

Now we have three functions - `abnormal` consists of `norc` and `nor`, `norc` consists of `norb`, and `norb` consists of `nora`. Let's dig into `nora` first.

```v
module nora(out, in);
    output [1:0] out;
    input [2:0] in;

    nor n1(w1, in[0], in[1]);
    nor n2(w2, in[0], w1);
    nor n3(w3, in[1], w1);
    nor n4(w4, w2, w3);
    nor n5(w5, w4, w4);
    nor n6(w6, w5, in[2]);
    nor n7(w7, w5, w6);
    nor n8(w8, in[2], w6);
    nor n9(w9, w7, w8);
    nor n10(out[0], w9, w9);
    nor n11(w10, in[0], in[0]);
    nor n12(w11, in[1], in[1]);
    nor n13(w12, w10, w11);
    nor n14(w13, in[2], in[2]);
    nor n15(w14, w11, w13);
    nor n16(w15, w12, w14);
    nor n17(w16, w10, w13);
    nor n18(w17, w15, w15);
    nor n19(w18, w17, w16);
    nor n20(out[1], w18, w18);
endmodule
```

So it takes 3 bits as input and outputs 2 bits. Let's try drawing a diagram, first until `n10`.

![image](https://user-images.githubusercontent.com/11196638/128684748-f8d1be5d-6cff-4d6a-a858-2a48b04485b6.png)

This is identical to the diagram from the [Normal](README.md#normal-reversing-150-pts), until `w9`! From the previous challenge, then, `w9 = ~(in[0]^in[1]^in[2])`; `n10` is just `out[0] = w9 nor w9`, which is `~w9`. We now have that `out[0] = in[0]^in[1]^in[2]`.

Now from `n11` to `n20` (simplifying things like `nor n11(w10, in[0], in[0])` to `not n11(w10, in[0])`):

![image](https://user-images.githubusercontent.com/11196638/128686197-505ebbb4-1d2e-4883-b1eb-9bc1aba5c146.png)

Since `~((~a)|(~b))` is `a & b`, `w12 = in0 & in1; w14 = in1 & in2; w16 = in0 & in2`; `w17 = ~w15 = ~(~(w12|w14)) = w12 | w14`; `out1 = ~w18 = ~(~(w17 | w16)) = w17 | w16`. In conclusion, `out1 = (in0 & in1) | (in1 & in2) | (in0 & in2)`. Hmm. Let's look at the truth table:

![image](https://user-images.githubusercontent.com/11196638/128687853-d1183594-3327-4905-8a25-5e51020ea1bf.png)

So output 0 is 1 when an odd number of inputs are 0, output 1 is 1 when 2 or more inputs are 0... hey, it's a [full adder](https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder)! `out[1]` is the carry out bit, and probably `in[2]` is the carry in bit.

Ok, `nora` is a full adder. Let's see what `norb` does. It has 17 bits of output, 33 bits of input. knowing that we have a full adder, topmost bit is likely the carry bit. Looking at each of the additions, it's adding `in[i]` and `in[16+i]`, with the third input being the result of the previous addition. `nora`'s `in[2]` is the carry bit, confirmed; which also means `in[32]` and `out[16]` are also carry bits. Ultimately, `norb` is adding two 16-bit numbers, `in[31~16]` and `in[15~0]`.

`norc` has a similar structure; using `norb`, it adds two 256 bit numbers, `in[511~256]` and `in[255~0]`, with a carry bit.

Loooking at `norc` modules `n1` and `n2`, `n1` just adds `0xa86f06e4e492e2c1ea6f4d5726e6d36bec57cf31472b986a675d3bc8e5d22b81` to input (`w1`), and `n2` adds `0xa5e20394c934fd1198b1517d57e730cd225ccfa064ff42db76c19f3b7c0da91a` and `0x6bf077b696cc4b22c0e56f4d3e6e150e386d6f04479ac502600e01fcdc29f5e4` (`w2`); since `c1` and `c2` is never used within `abnormal`, we may safely ignore it. The rest of the function is `w1 ^ w2`, like those which we've already seen in `nora` and `Normal`. Finally, we want the result of `w1 ^ w2` to be 0, or `w1 == w2`.

```py
In : import binascii
...: a1 = 0xa5e20394c934fd1198b1517d57e730cd225ccfa064ff42db76c19f3b7c0da91a
...: a2 = 0x6bf077b696cc4b22c0e56f4d3e6e150e386d6f04479ac502600e01fcdc29f5e4
...: b1 = 0xa86f06e4e492e2c1ea6f4d5726e6d36bec57cf31472b986a675d3bc8e5d22b81
...: binascii.unhexlify(hex(a1+a2-b1)[2:])
Out: b"ictf{nero'ssonronrosenosoreores}"
```

## Flag
```
ictf{nero'ssonronrosenosoreores}
```

