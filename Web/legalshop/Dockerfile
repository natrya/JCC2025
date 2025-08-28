FROM python:3.12.2-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 4004

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0 
ENV FLASK_RUN_PORT=4004
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
