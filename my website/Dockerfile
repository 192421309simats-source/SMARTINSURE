FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy source
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# Ensure DB is seeded at container start if not present
CMD ["/bin/sh", "-c", "py -3 -m scripts.seed_db || true; uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
