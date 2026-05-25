# Use a lightweight official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Upgrade system packages to patch high/medium security vulnerabilities
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
#update the Python Core tools to fix base image vulnerabilities
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Copy only the requirements first (optimizes Docker layer caching)
COPY requirements.txt .

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and frontend templates
COPY src/ ./src/

# Expose the port Gunicorn will run on
EXPOSE 5000

# Start the app using Gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
