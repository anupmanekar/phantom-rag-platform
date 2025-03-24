# Use python:3.11-slim as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the backend directory into the Docker image
COPY . /app

# Copy the .env file into the Docker image
COPY .env /app/.env

# Copy the requirements.txt file into the Docker image
COPY requirements.txt /app/requirements.txt
COPY firestore-genai-experiments.json /app/firestore-genai-experiments.json

# Install the required dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the entrypoint to run the FastAPI application using uvicorn
ENTRYPOINT ["uvicorn", "rag_api.entrypoints.app:app", "--host", "0.0.0.0", "--port", "8080"]
