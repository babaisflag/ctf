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

## Sanity Check (Misc, 15pts)

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

## Discord (Misc, 15 pts)

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

## Chicken Caesar Salad (Crypto, 50 pts)

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

## Hidden | Forensics | 50

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

## Roos World | Web | 50

## stackoverflow | Pwn | 50

## Fake Canary | Pwn | 100

## Flip Flops | Crypto | 100

**Description**

Yesterday, Roo bought some new flip flops. Let's see how good at flopping you are.

**Attachments**

`flop.py`

**Solution**

`flop.py`:
```
#!/usr/local/bin/python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import os

print('''
                                        ,,~~~~~~,,..
                             ...., ,'~             |
                             \    V                /
                              \  /                 /
                              ;####>     @@@@@     )
                              ##;,      @@@@@@@    )
                           .##/  ~>      @@@@@   .   .
                          ###''#>              '      '
      .:::::::.      ..###/ #>               '         '
     //////))))----~~ ## #}                '            '
   ///////))))))                          '             '
  ///////)))))))\                        '              '
 //////)))))))))))                                      '
 |////)))))))))))))____________________________________).
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||

(yeah they're not flip flops but close enough)

''')

key = os.urandom(16)
iv = os.urandom(16)
flag = open("flag.txt").read().strip()


for _ in range(3):
	print("Send me a string that when decrypted contains 'gimmeflag'.")
	print("1. Encrypt")
	print("2. Check")
	choice = input("> ")
	if choice == "1":
		cipher = AES.new(key, AES.MODE_CBC, iv)
		pt = binascii.unhexlify(input("Enter your plaintext (in hex): "))
		if b"gimmeflag" in pt:
			print("I'm not making it *that* easy for you :kekw:")
		else:
			print(binascii.hexlify(cipher.encrypt(pad(pt, 16))).decode())
	else:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		ct = binascii.unhexlify(input("Enter ciphertext (in hex): "))
		assert len(ct) % 16 == 0
		if b"gimmeflag" in cipher.decrypt(ct):
			print(flag)
		else:
			print("Bad")

print("Out of operations!")
```

So our input is encrypted and decrypted via AES-CBC. I don't know much about encryption, but reading through the [Wikipedia page](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)), the encryption and decryption process involves xor'ing the previous block (16 bytes) of ciphertext with the next block of plaintext/decrypted text. Since the key and IV are initialized before the `for` loop, we have 3 chances to encrypt/decrypt with the same key and IV. Our objective is to recover 'gimmeflag' from the ciphertext, without directly encrypting 'gimmeflag'.

The title and the description a talks about flip flops. Might be something related to bit flipping. Googling "aes cbc bit flipping, the [first result](https://resources.infosecinstitute.com/topic/cbc-byte-flipping-attack-101-approach/) talks about byte flipping attack for aes-cbc. Basically, the decryption process is:
1. Put the current block of ciphertext through decryption with the provided key;
2. then xor the result with the previous block of ciphertext, to recover the plaintext.
![Image of AES-CBC byte flip](/_Images/AESCBCByteFlip.jpg)

So, we need 2 blocks: the "previous block" that will be used to flip a bit (of course, this block will not be recovered as the ciphertext changed), and the "next block" that contains a string that's 1 bit off from the string 'gimmeflag'. We can use the string `AAAAAAAAAAAAAAAAAAAAAAAgimmeflaf`. Since `f` is `0x66` and `g` is `0x67`, we can just flip the bottom-most bit of the first block of the ciphertext to recover `AAAAAAAAAAAAAAAAAAAAAAAgimmeflag`.

```
$ ictf{fl1p_fl0p_b1ts_fl1pped_b6731f96}

                                        ,,~~~~~~,,..
                             ...., ,'~             |
                             \    V                /
                              \  /                 /
                              ;####>     @@@@@     )
                              ##;,      @@@@@@@    )
                           .##/  ~>      @@@@@   .   .
                          ###''#>              '      '
      .:::::::.      ..###/ #>               '         '
     //////))))----~~ ## #}                '            '
   ///////))))))                          '             '
  ///////)))))))\                        '              '
 //////)))))))))))                                      '
 |////)))))))))))))____________________________________).
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||

(yeah they're not flip flops but close enough)


Send me a string that when decrypted contains 'gimmeflag'.
1. Encrypt
2. Check
> 1
Enter your plaintext (in hex): 414141414141414141414141414141414141414141414167696d6d65666c6166
4a02863ece4062105d83eed02314fc6fa55f72a0c5c9cc1f978bccdcd113ae806ba849a330044a25495db6bb8d3b4817
Send me a string that when decrypted contains 'gimmeflag'.
1. Encrypt
2. Check
> 2
Enter ciphertext (in hex): 4a02863ece4062105d83eed02314fc6ea55f72a0c5c9cc1f978bccdcd113ae806ba849a330044a25495db6bb8d3b4817
b"\x01\xcfwg\xe0\xd1B\xa6'\xea\xc7\xf4\xa0\xed\xe3AAAAAAAAgimmeflag\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"
ictf{fl1p_fl0p_b1ts_fl1pped_b6731f96}
Send me a string that when decrypted contains 'gimmeflag'.
1. Encrypt
2. Check
>
```
(the last bit of the 16th byte `0x6f` is flipped to `0x6e`)

**Comments**

It seems that the encryption appends the IV at the end of the ciphertext; the ciphertext can be fully recovered without the last block.

**Flag**
```
ictf{fl1p_fl0p_b1ts_fl1pped_b6731f96}
```

## Formatting | Misc | 100

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

## Spelling Test | Misc | 100

**Description**

I made a spelling test for you, but with a twist. There are several words in words.txt that are misspelled by one letter only. Find the misspelled words, fix them, and find the letter that I changed. Put the changed letters together, and you get the flag. Make sure to insert the "{}" into the flag where it meets the format.

NOTE: the words are spelled in American English

**Attachments**

`words.txt`

**Solution**

Using `PyEnchant` for the dictionary, get a list of words with typos and a list of suggested fix; `diff` the two lists with `difflib`.

`words.py`:
``` python
import enchant
import difflib

d = enchant.Dict("en_US")
typo = []
sugg = []
possible = ""

with open("words.txt", "r") as f:
    line = f.readline().strip()
    while line:
        if not d.check(line) and not d.check(line.capitalize()):
            typo.append(line)
            suggestion = d.suggest(line)
            sugg.append(suggestion[0])
            for i,s in enumerate(difflib.ndiff(line,suggestion[0])):
                if s[0] == '-': possible = possible+s[-1]
        line = f.readline().strip()

print(typo)
print(sugg)
print(possible)
```
```
$ python3 words.py
['convirgence', 'translatcr', 'addretsing', 'javascript', 'approachfs', 'namespace', 'subscrybers', 'endangored', 'modufications', 'rehapilitation', 'camputers', 'mastercard', 'classisal', 'munisipality', 'engineereng', 'requiremend', 'generatint', 'recruitmeht', 'yorkshere', 'applicasions', 'instalping', 'changelog', 'broadcesting', 'attractlve', 'enquiries', 'obituarles', 'bibliogriphy', 'avainable', 'wordpress', 'instructiongl', 'strengthenint', 'discherge', 'playstation', 'subscriptisn', 'copyrightet']
['convergence', 'translator', 'addressing', 'java script', 'approaches', 'name space', 'subscribers', 'endangered', 'modifications', 'rehabilitation', 'computers', 'master card', 'classical', 'municipality', 'engineering', 'requirement', 'generating', 'recruitment', 'worksheet', 'applications', 'installing', 'change log', 'broadcasting', 'attractive', 'inquiries', 'obituaries', 'bibliography', 'available', 'word press', 'instructional', 'strengthening', 'discharge', 'play station', 'subscription', 'copyrighted']
ictfyoupassedthyrspelelingtest
```

Something seems off. Looking at the list, it seems that 'yorkshere' became 'worksheet', and 'enquiries' was incorrectly flagged as a typo; 'yorkshere' should become 'yorkshire', so in place of 'yr' should be an 'e'. An extra 'e' between the 'l's should not be there as well. Fixing those issues, we get: `ictfyoupassedthespellingtest`

**Flag**
```
ictf{youpassedthespellingtest}
```

## Stings | Rev | 100
## Vacation | Forensics | 100

**Description**

Roo's cousin was on vacation, but he forgot to tell us where he went! But he posted this image on his social media. Could you track down his location? Submit your answer as ictf{latitude_longitude}, with both rounded to 3 decimal places. Example: ictf{-12.345_42.424} (Note: only the image is needed for this challenge, as this is an OSINT challenge.)

**Attachments**

`image.jpg`

**Solution**

![Vacation Image](/_Attachments/image.jpg)

Zooming in, we see a few things:
1. On the left, in the flag with 'National Treasure', there is a logo that has the year 1965 and 'City of South Lake Tahoe'.
2. On the right, there are a few shops, including a Rock Shop, Tahoe Hemp Company, and Sugar Pine Bakery.

Searching 'city of south lake tahoe sugar pine bakery' in google maps, we do indeed get a location with the rock shop next to it. Right-clicking on the road near it, we get the coordinates: 38.947, -119.96.

![Google Maps Image](/_Images/vacation.PNG)

**Flag**
```
ictf{38.947_-119.961}
```

## Lines | Crypto | 150
## Normal | Reversing | 150
## The First Fit | Pwn | 150
## Jumprope | Reversing | 200
## No Thoughts, Head Empty | Reversing | 200
## linonophobia | Pwn | 200
## Speedrun | Pwn | 200
## Abnormal | Reversing | 250
## It's Not Pwn, I Swear! | Reversing | 250
