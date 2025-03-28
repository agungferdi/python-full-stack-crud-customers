FROM python:3.11-slim  

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev pkg-config netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/templates /app/static /app/logs

# Copy the rest of the application
COPY . .

# Make logs directory writeable
RUN chmod -R 777 /app/logs

# Ensure script is executable
RUN chmod +x wait-for-it.sh

EXPOSE 8000

CMD ["./wait-for-it.sh", "db:3306", "--timeout=60", "--", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]