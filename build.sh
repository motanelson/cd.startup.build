nasm mysys.s -o mysys.bin
python3 linux.py
qemu-system-x86_64 -cdrom cd1.iso