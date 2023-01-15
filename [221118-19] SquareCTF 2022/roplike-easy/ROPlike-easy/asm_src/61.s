.intel_syntax noprefix

.ascii "\xFF\xFF\xFF\x00"
mov rax, 0x3c
syscall # easy mode only
ret
