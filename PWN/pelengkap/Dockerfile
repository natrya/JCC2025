FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------
# Install tools & Python
# ---------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc-multilib gcc gdb make socat file wget curl && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# Setup challenge workspace
# ---------------------------
RUN mkdir -p /opt/challs
WORKDIR /opt/challs

COPY src/ ./src/

RUN chmod +x ./src/build.sh
RUN cd /opt/challs && ./src/build.sh || true

# ---------------------------
# Create non-root user
# ---------------------------
RUN useradd -m ctfuser || true
USER ctfuser
WORKDIR /home/ctfuser

# Default shell
CMD ["/bin/bash"]

