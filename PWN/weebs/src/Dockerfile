FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    build-essential gcc socat && \
    rm -rf /var/lib/apt/lists/*

# Proper user + group
RUN useradd -m -u 1000 -s /bin/bash ctf
WORKDIR /home/ctf

# Copy sources and build inside the container for reproducibility
COPY chal.c /home/ctf/chal.c
RUN gcc -O0 -fno-stack-protector -U_FORTIFY_SOURCE -Wall -Wextra -fPIE -pie \
    -o /home/ctf/chal /home/ctf/chal.c -ldl

# Add flag
COPY flag.txt /home/ctf/flag.txt

# Secrets in environment
ENV SECRET1="RASENGAN" \
    SECRET2="CHIDORI" \
    SECRET3="BANKAI" \
    SECRET4="GEAR5"

# Lock down perms; run as unprivileged user
RUN chown -R root:root /home/ctf && \
    chmod 0755 /home/ctf && \
    chmod 0555 /home/ctf/chal && \
    chmod 0444 /home/ctf/flag.txt

EXPOSE 4012

# Run socat as ctf directly
USER ctf
ENTRYPOINT ["socat", "TCP-LISTEN:4012,reuseaddr,fork,nodelay", "EXEC:/home/ctf/chal,pty,rawer,echo=0"]

