FROM ubuntu:20.04

# ---------------------------
# Install tools & Python
# ---------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc-multilib ruby ruby-dev gcc gdb make python3 python3-pip socat file wget curl  binutils elfutils && \
    pip3 install --no-cache-dir pwntools && \
    rm -rf /var/lib/apt/lists/*


# ---------------------------
# Setup challenge workspace
# ---------------------------
RUN mkdir -p /opt/challs/bin
WORKDIR /opt/challs

# Copy source code & flag
COPY src/ret2libc.c ./src/ret2libc.c
COPY src/flag.txt /home/ctfuser/flag.txt

# Compile vulnerable binary
RUN gcc -m64 -g -fno-stack-protector -z relro -no-pie -o ./bin/ret2libc ./src/ret2libc.c
RUN rm -f ./src/ret2lib.c

# ---------------------------
# Create non-root user
# ---------------------------
RUN useradd -m ctfuser || true
USER ctfuser
WORKDIR /home/ctfuser

# Default shell
CMD ["/bin/bash"]

