#!/bin/bash
set -e
mkdir -p bin
cd src
gcc -m64 -no-pie -z execstack -fno-stack-protector -O0 -g -o ../bin/ret2shellcode ret2shellcode.c
gcc -m64 -no-pie -fno-stack-protector -O0 -g -o ../bin/ret2win ret2win.c

cd ..
ls -l bin || true

