# CUDA-enabled base
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install first
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code, model, etc.
COPY src/   /app/src
COPY api/   /app/api
COPY models /app/models

# Add a non-root user for security
RUN useradd -m runner
USER runner

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
