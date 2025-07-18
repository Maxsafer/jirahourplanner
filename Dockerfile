# Use the official Python slim image
FROM python:3.14-rc-slim

# Set working dir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code + templates
COPY . .

# Ensure data directory exists
RUN mkdir -p data

# Tell Flask how to run
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Default command
CMD ["flask", "run"]