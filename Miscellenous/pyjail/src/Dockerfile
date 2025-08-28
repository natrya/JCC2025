FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y socat && \
    pip install RestrictedPython==7.4

COPY chall.py .
COPY flag.txt .

CMD socat TCP-LISTEN:4013,fork,reuseaddr EXEC:"python3 chall.py",stderr
