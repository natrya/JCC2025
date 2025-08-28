FROM ubuntu:22.04

RUN apt-get update && \
    apt-get -y install curl \
    build-essential libcunit1-dev libudev-dev socat

RUN     useradd ctf
WORKDIR /home/ctf

COPY chall      /home/ctf/
COPY flag.txt   /home/ctf/

RUN chown -R root:root  /home/ctf
RUN chmod -R 555        /home/ctf

EXPOSE 1337
ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork,nodelay,su=ctf", "EXEC:'timeout 60 ./chall'"]