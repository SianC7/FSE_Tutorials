FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5001

# Default command runs Flask app on 0.0.0.0 (accessible from outside container)
CMD ["python", "-u", "app.py"]
