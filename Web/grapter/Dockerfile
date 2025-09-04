FROM python:3.11-slim

WORKDIR /app

# Install curl (and clean up cache to keep image small)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

ENV DB_PATH=/app/data/app.db
RUN mkdir -p /app/data

EXPOSE 4003

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "4003"]

