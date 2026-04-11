# Forge Protocol — Dockerfile Template (FastAPI)
# Source: AIRIS + iiko-assistant (production patterns)
#
# python:3.12-slim for minimal image (~150MB)
# Cloud Run uses PORT env var (default 8080)

FROM python:3.12-slim

WORKDIR /app

# System dependencies (uncomment as needed)
# RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*

# Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY app/ app/
# COPY sql/ sql/        # Uncomment if you have SQL migration files
# COPY alembic/ alembic/ # Uncomment if using Alembic

EXPOSE 8080

# Non-root user for security (Forge Protocol Tier 2)
# RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
# USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
