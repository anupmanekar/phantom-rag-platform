# Use python:3.11-slim as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the backend directory into the Docker image
COPY backend /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to run the FastAPI application using uvicorn
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
