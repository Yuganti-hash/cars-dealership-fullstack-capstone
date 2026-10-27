# Multi-stage Dockerfile for Cars Dealership Full-Stack Application
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/server/requirements.txt

# Copy application code
COPY . /app/

WORKDIR /app/server

# Run migrations and database population
RUN python manage.py migrate --noinput && \
    python setup_data.py

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose server port
EXPOSE 8000

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT}/ || exit 1

# Start the application using Gunicorn (production) or Django runserver fallback
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${PORT}"]
