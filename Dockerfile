# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg pkg-config libmariadb-dev-compat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory in the container
WORKDIR /main

# Install Python dependencies
COPY requirements.txt /main/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . /main/
