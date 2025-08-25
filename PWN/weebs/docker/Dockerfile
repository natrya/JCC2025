FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       socat build-essential gcc gdb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source and build inside container for reproducibility
COPY Makefile /app/Makefile
COPY src/ /app/src/

RUN make rebuild \
    && useradd -m -u 10001 pwn \
    && mkdir -p /service \
    && cp build/chal /chal \
    && echo "JCC2025{example_flag_replace_me}" > /flag \
    && chown -R pwn:pwn /chal /service

COPY docker/entry.sh /service/entry.sh
RUN chmod +x /service/entry.sh

EXPOSE 31337
USER pwn
ENTRYPOINT ["/service/entry.sh"]


