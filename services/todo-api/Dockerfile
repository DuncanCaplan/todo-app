# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .

# Install dependencies to a temporary prefix
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime
FROM python:3.12-slim

# Standard Python env vars for Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create a non-privileged user
RUN adduser --disabled-password --no-create-home appuser

WORKDIR /app

# Pull in the pre-installed packages
COPY --from=builder /install /usr/local

# Copy the app code with the correct ownership
COPY --chown=appuser:appuser app/ ./app

# (Temporary) Create a directory that appuser owns to use as database URL
RUN mkdir -p /app/data && chown appuser:appuser /app/data

# Switch to the non-root user
USER appuser

EXPOSE 8000

# Using the list format for CMD is preferred (exec form)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]