FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      gcc make socat ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /srv

# Copy sources and build inside container
COPY src /srv/src
WORKDIR /srv/src
RUN make clean || true && make linux && mv bin/kpop /srv/kpop

# Provide runtime working dir with flag
WORKDIR /srv
COPY src/flag.txt /srv/flag.txt

# Create non-root user
RUN useradd -m ctf && chown root:ctf /srv/flag.txt && chmod 440 /srv/flag.txt
USER ctf

EXPOSE 5000

# Run via socat as a net service
CMD ["socat", "-dd", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:/srv/kpop,stderr,pty,rawer,echo=0"]
