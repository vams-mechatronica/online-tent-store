# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    build-essential openssl\
    && rm -rf /var/lib/apt/lists/*

# Install pip and setuptools
RUN pip install --upgrade pip setuptools

# Set working directory
WORKDIR /app/src/

# Install dependencies
COPY src/requirements.txt /app/src/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY src/ /app/src/


ENV POSTGRES_PASSWORD=''
ENV POSTGRES_DB='vams-ots'
ENV POSTGRES_USER='root'
ENV POSTGRES_HOST='host.docker.internal'
ENV POSTGRES_PORT='3306'

