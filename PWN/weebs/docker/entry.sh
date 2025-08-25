#!/bin/sh
set -eu

# Keep ASLR default; if you want to disable inside container, uncomment:
# echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

exec socat -v TCP-LISTEN:31337,reuseaddr,fork EXEC:/chal,pty,rawer,echo=0


