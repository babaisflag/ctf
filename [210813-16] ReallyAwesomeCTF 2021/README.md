# ReallyAwesomeCTF 2021

ReallyAwesomeCTF 2021, from August 13 3PM - August 16 3PM (EDT).

## Overview

Writeups to challenges are linked here, arranged by points.

Challenge | Category | Points | Solves | Comments
--------- | -------- | ------ | ------ | --------
[Discord](#Discord-Miscellaneous-50-pts) | Miscellaneous | 50 | Sanity check | 433
[Skyline](#OSINT) | OSINT | 100 | 243
[Triangles](#OSINT) | OSINT | 100 | 451
[RSFPWS - Intercepted](#RSFPWS---Intercepted-Miscellaneous-150-pts) | Miscellaneous | 150 | 99
[Silver Darlings](#OSINT) | OSINT | 150 | 325
[Call&Response](#Call&Response-Miscellaneous-200-pts) | Miscellaneous | 200 | 123
[John Poet](#OSINT) | OSINT | 200 | 285
[OHSHINT](#OSINT) | OSINT | 200 | 172
[50m on the Right](#OSINT) | OSINT | 250 | 300
[Missing Tools](#Missing-Tools-Miscellaneous-250-pts) | Miscellaneous | 250 | 165
Absolute Dice | Pwn/Reversing | 300 | 74
Dodgy Databases | Pwn/Reversing | 350 | 117
Emojibook | Web | 350 | 133
Lego Car Generator | Pwn/Reversing | 350 | 54
Packed | Pwn/Reversing | 350 | 56

## Writeups

### Discord (Miscellaneous, 50 pts)

**Description**

Come join our [Discord](https://discord.gg/Rrhdvzn)!

**Solution**

I swear I spent way too much time on it because I looked at all the channel descriptions *except for* #general channel. I still don't know how I missed it for so long. But here it is:

![image](https://user-images.githubusercontent.com/11196638/129629365-f4a05b69-ebde-4cbb-884b-a1e624815a18.png)

**Flag**
```
ractf{so_here_we_are_again}
```

### OSINT

Challenge | Location Link | Explanation
--------- | ------------- | -----------
[Triangles](OSINT_images/traingles.jpg) | https://goo.gl/maps/qr7Qbriw2egc8SFBA | Ragusa Foto Festival; in the left down corner, there's a sign with Palazzo Cosentini, etc...
[Skyline](OSINT_images/skyline.jpg) | https://goo.gl/maps/ycHeJL72VyLpFAp97 | Go along London's river, look for two towers and a zipline, with a small river that goes off the side
[Silver Darlings](OSINT_images/silver_darlings.jpg) | https://goo.gl/maps/tgKfk3gWUrgwoEJaA | Cafe de la Mairie, Chambres dhotes
[John Poet](OSINT_images/john_poet.jpg) | https://goo.gl/maps/kofmRvGnRvNGPCQD8 | RHC, glass buildings, parasol; Rail House Cafe
[50m on the Right](OSINT_images/50m_on_the_right.jpg) | https://goo.gl/maps/iwo1hcwe5Sr592RJ8 | on the sign, Bistro 24; also you can *barely* read armacao de pera under the logo
[OHSHINT](OSINT_images/image.jpg) | https://goo.gl/maps/Q9AavYfW8HoxFZHA8 | hint in the metadata of image; look for a big lake northeast of Lancaster; pine lake

### RSFPWS - Intercepted (Miscellaneous, 150 pts)

**Description**

Challenge instance ready at `193.57.159.27:35582`. Click here to request a new instance.  
This challenge also has something on port 35582/udp

This game i'm playing is fun! There's this box that seemingly does nothing though... It sends a "network request" whatever that is. Can you have a look?  
(When the game launches, enter the IP and port you get from above. This challenge uses the same files and instance as other RSFPWS challenges)

**Attachments**

[windows_clinet.zip](windows_clinet.zip)

[linux_client.zip](linux_client.zip)

**Solution**

The file given is a unity game. Upon running it and logging in with the given IP address and port, we see:

![image](https://user-images.githubusercontent.com/11196638/129629507-54ca736b-51bb-4f02-a8ac-024f40229e8e.png)

There are 3 challenges in this game; this one seems to be related to the rightmost one:

![image](https://user-images.githubusercontent.com/11196638/129629604-c45c2625-8f29-4b56-9a67-b18ef65bc763.png)

The challenge also mentions that there's something at the udp port. We'll try wiresharking to capture the packet when I enter the box:

![rsfpws-intercepted](https://user-images.githubusercontent.com/11196638/129629734-e4544dac-0c70-48bb-9bd6-ca3bd15b4312.PNG)

Nice.

**Flag**
```
ractf_N3tw0rking_L`ke_4_B0ss!}
```

### Call&Response (Miscellaneous, 200 pts)

**Description**

Agent,

We're working a major case. We've been called in to covertly investigate a foreign govt agency, the GDGS, by a private organisation. We've finished performing initial reconnaissance of the target building and it's surrounding areas. We know they have a wireless network which they use to carry out live activities. Gaining access here would be substiantial. Problem is, they've somewhat competently secured it using WPA2 EAP-PEAP authentication which means gaining a packet capture of the handshake process is useless as the authentication exchange is carried out over a TLS 1.2 session. Nonetheless, we setup an access point with same ESSID as the target and managed to trick an employee's device into attempting to connect to our AP. In the process, we've obtained an username and certain auth values. We're not entirely sure what we need to do with them.

Can you take a look and help us recover the password?
```
username:    PrinceAli
c:    c3:ae:5e:f9:dc:0e:22:fb
r:    6c:52:1e:52:72:cc:7a:cb:0e:99:5e:4e:1c:3f:ab:d0:bc:39:54:8e:b0:21:e4:d0
```
Flag format is `ractf{recovered_password}`.

**Solution**

I don't know much about WPA2 EAP-PEAP or TLS, but some google search related to WPA2 EAP-PEAP authentication and call and response gives [this](https://solstice.sh/ii-attacking-and-gaining-entry-to-wpa2-eap-wireless-networks/). Based on it, we'll try `asleap`:

![image](https://user-images.githubusercontent.com/11196638/129631307-7acc4ad3-046e-4a3a-8eba-31b440c02259.png)

Noice.

**Flag**
```
ractf{rainbow6}
```

### Missing Tools (Miscellaneous, 250 pts)

**Description**

Challenge instance ready at `193.57.159.27:42380`. Click here to request a new instance.

Man, my friend broke his linux install pretty darn bad. He can only use like, 4 commands. Can you take a look and see if you can recover at least some of his data?

Username: `ractf`  
Password: `8POlNixzDSThy`  
Note: it may take a minute or more for your container to start depending on load

**Solution**

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

**Flag**
```
ractf{std0ut_1s_0v3rr4ted_spl1t_sha}
```
