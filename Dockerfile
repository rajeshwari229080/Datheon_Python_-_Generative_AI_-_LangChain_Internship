# Production Multi-Stage Dockerfile for ApexAI Operations Suite
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy full application code
COPY . .

# Expose ports:
# 8000: SaaS Operations Portal
# 8001: Task 1 JSON Extractor (FastAPI)
# 8002: Task 2 Grounded RAG (FastAPI)
# 8501: Task 4 Chatbot (Streamlit)
EXPOSE 8000 8001 8002 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command launches unified orchestrator in full-hosting mode
CMD ["python", "launcher.py", "--host-all"]
