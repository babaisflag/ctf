rm ./gadgets/*
cd asm_src
for file in *.s; do ./compile_gadgets.sh $file; done
cd ../
gcc -O1 ROPlike.c -o roplike
# ./solve.py GDB