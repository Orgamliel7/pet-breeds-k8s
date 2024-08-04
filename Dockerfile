# Specifies container image build instructions for producer & consumer apps

# Base image
FROM python:3.9-slim

# working dir
WORKDIR /app


COPY ./producer/requirements.txt ./producer/requirements.txt
COPY ./consumer/requirements.txt ./consumer/requirements.txt

# Dependencies
RUN pip install --no-cache-dir -r producer/requirements.txt
RUN pip install --no-cache-dir -r consumer/requirements.txt

COPY ./producer ./producer
COPY ./consumer ./consumer

# Command to run
CMD ["sh", "-c", "python3 ./producer/main.py & python3 ./consumer/main.py"]
