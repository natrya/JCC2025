FROM ubuntu:22.04

RUN apt-get update && \
    apt-get -y install curl \
    build-essential libcunit1-dev libudev-dev socat

# Proper user + group
RUN useradd -m -u 1000 -s /bin/bash ctf
WORKDIR /home/ctf

COPY chall /home/ctf/
COPY flag.txt /home/ctf/

RUN chown -R root:root /home/ctf && \
    chmod -R 555 /home/ctf && \
    chmod +x /home/ctf/chall

EXPOSE 4009

# Run socat as ctf directly
USER ctf
ENTRYPOINT ["socat", "TCP-LISTEN:4009,reuseaddr,fork,nodelay", "EXEC:timeout 60 /home/ctf/chall"]
