# =============================================================================
# Dockerfile for Movie Rating Prediction API
# DDM501 - Lab 1: First ML Product
#
# TODO: Complete this Dockerfile
# =============================================================================

# -----------------------------------------------------------------------------
# Base image
# -----------------------------------------------------------------------------
FROM python:3.10-slim

# -----------------------------------------------------------------------------
# TODO 1: Set working directory
# -----------------------------------------------------------------------------
# Hint: Use WORKDIR /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# -----------------------------------------------------------------------------
# TODO 2: Copy and install dependencies
# -----------------------------------------------------------------------------
# Requirements:
# - Copy requirements.txt first (for Docker cache optimization)
# - Install dependencies with pip (use --no-cache-dir)
#
# Hint:
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# -----------------------------------------------------------------------------
# TODO 3: Copy application code
# -----------------------------------------------------------------------------
# Hint: COPY . .
COPY . .


# -----------------------------------------------------------------------------
# TODO 4: Expose port
# -----------------------------------------------------------------------------
# Hint: EXPOSE 8000
EXPOSE 8000


# -----------------------------------------------------------------------------
# TODO 5: Add health check (BONUS)
# -----------------------------------------------------------------------------
# Requirements:
# - Check every 30 seconds
# - Timeout after 10 seconds
# - Start checking after 5 seconds
# - Retry 3 times before marking unhealthy
# - Use curl to check /health endpoint
#
# Hint:
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8000/health || exit 1
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1


# -----------------------------------------------------------------------------
# TODO 6: Set the startup command
# -----------------------------------------------------------------------------
# Requirements:
# - Run uvicorn with app.main:app
# - Bind to 0.0.0.0:8000
#
# Hint: CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
