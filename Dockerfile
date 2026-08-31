FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, sample documents, and seed script
COPY backend /app/backend
COPY sample_documents /app/sample_documents

ENV PYTHONPATH=/app/backend
ENV PORT=8000

WORKDIR /app/backend

# Seed database and start uvicorn server
CMD python app/database/seed.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
