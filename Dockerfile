# Use slim Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install OS packages that help build wheels / SSL / CA certs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*

# Create app dir and non-root user
WORKDIR /app
RUN useradd -m appuser

# Copy dependency list first (better layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . /app

# Switch to non-root
USER appuser

# Expose the FastAPI port
EXPOSE 8000

# Start the API
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
