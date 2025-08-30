FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gcc \
        libc6 \
        libc6-dev \
        socat \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src /app/src
COPY flag.txt /app/flag.txt

RUN gcc -O2 -no-pie -fno-stack-protector -o /app/store /app/src/store.c

EXPOSE 4011

CMD ["/bin/sh", "-c", "socat TCP-LISTEN:4011,reuseaddr,fork EXEC:/app/store,stderr"]


