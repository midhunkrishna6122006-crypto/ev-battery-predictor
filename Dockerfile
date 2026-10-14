# Production-ready Dockerfile for EV Battery Digital Twin & Range Predictor
# Fulfills CIT 19MAM56 AML Lab - Rubric Component 4 (Docker & Cloud Deployment)

FROM python:3.11-slim

# Set environment variables to optimize Python within Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PORT=7860

# Set working directory inside container
WORKDIR /app

# Install essential system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install optimized Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application codebase
COPY . .

# Expose ports:
# 7860: Standard Hugging Face Spaces Web UI
# 8000: Production FastAPI REST Inference Endpoint
# 8501: Local Streamlit default
EXPOSE 7860 8000 8501

# Default command: Launch interactive UI on port 7860 for Hugging Face Spaces
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
