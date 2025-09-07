#!/bin/bash
set -e
mkdir -p bin
cd src
gcc -m64 -no-pie -z execstack -fno-stack-protector -O0 -g -o ../bin/sesuatu sesuatu.c
gcc -m64 -no-pie -fno-stack-protector -O0 -g -o ../bin/hore hore.c

cd ..
ls -l bin || true

