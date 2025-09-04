FROM python:3.9-slim

WORKDIR /app

# Install curl (and clean up cache to keep image small)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY app/ /app/
COPY flag.txt /flag.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 1001 ctfuser
RUN chown -R ctfuser:ctfuser /app
RUN chmod 644 /flag.txt

USER ctfuser

EXPOSE 4001

CMD ["python", "app.py"]
