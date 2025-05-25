# syntax=docker/dockerfile:1

############################
# ----- Builder stage ---- #
############################
FROM python:3.13-slim AS builder

# Faster, safer Python defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Python dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

###########################
# ----- Runtime stage --- #
###########################
FROM python:3.13-slim
LABEL maintainer="pazimor"

# Same runtime env‑vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create a dedicated, non‑root user
RUN adduser --disabled-password --gecos '' appuser

# Copy installed packages from builder layer
COPY --from=builder /usr/local /usr/local

# Copy application source
WORKDIR /app
COPY request_service.py .
COPY api.py .
COPY fillroutes/ ./fillroutes
COPY sql/ ./sql

# Switch to the non‑root user for runtime
USER appuser

EXPOSE 4201

# Start the Flask application with Gunicorn (ensure `gunicorn` is in requirements.txt)
CMD ["gunicorn", "--bind", "0.0.0.0:4201", "api:app"]