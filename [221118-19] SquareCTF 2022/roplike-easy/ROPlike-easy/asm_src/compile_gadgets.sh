echo "compiling $1"
as $1 -o $1.out
objcopy -O binary $1.out ../gadgets/${1%.s}
rm $1.out
