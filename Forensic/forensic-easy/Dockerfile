FROM python:3.10-slim

# Buat user non-root
RUN useradd -ms /bin/bash ctf
USER ctf
WORKDIR /home/ctf

# Copy challenge
COPY src/ .

# Expose port
EXPOSE 4017

# Jalankan server
CMD ["python3", "main.py"]

