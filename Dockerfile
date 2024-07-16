# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements files
COPY ./producer/requirements.txt ./producer/requirements.txt
COPY ./consumer/requirements.txt ./consumer/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r producer/requirements.txt
RUN pip install --no-cache-dir -r consumer/requirements.txt

# Copy the source code
COPY ./producer ./producer
COPY ./consumer ./consumer

# Command to run
CMD ["sh", "-c", "python3 ./producer/main.py & python3 ./consumer/main.py"]
