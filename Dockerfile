FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Train model and seed database if not already present
RUN python -m ml.train && python seed.py

EXPOSE 5000

ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

CMD ["python", "run.py"]
