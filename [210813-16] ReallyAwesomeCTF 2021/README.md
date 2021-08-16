# ReallyAwesomeCTF 2021

ReallyAwesomeCTF 2021, from August 13 3PM - August 16 3PM (EDT).

## Overview

Writeups to challenges are linked here, arranged by points.

Challenge | Category | Points | Solves | Comments
--------- | -------- | ------ | ------ | --------
[Discord](#Discord-Miscellaneous-50-pts) | Miscellaneous | 50 | Sanity check | 433
[Skyline](#OSINT) | OSINT | 100 | 243
[Triangles](#OSINT) | OSINT | 100 | 451
RSFPWS - Intercepted | Miscellaneous | 150 | 99
[Silver Darlings](#OSINT) | OSINT | 150 | 325
Call&Response | Miscellaneous | 200 | 123
[John Poet](#OSINT) | OSINT | 200 | 285
[OHSHINT](#OSINT) | OSINT | 200 | 172
[50m on the Right](#OSINT) | OSINT | 250 | 300
Missing Tools | Miscellaneous | 250 | 165
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

<image_placeholder>

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

Challenge instance ready at 193.57.159.27:35582. Click here to request a new instance. This challenge also has something on port 35582/udp

This game i'm playing is fun! There's this box that seemingly does nothing though... It sends a "network request" whatever that is. Can you have a look?

(When the game launches, enter the IP and port you get from above. This challenge uses the same files and instance as other RSFPWS challenges)

**Attachments**

[windows_clinet.zip](windows_clinet.zip)

[linux_client.zip](linux_client.zip)

**Solution**

The file given is a unity game. Upon running it and logging in with the given IP address and port, we see:

<image_placeholder>