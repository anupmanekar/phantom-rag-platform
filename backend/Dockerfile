ARG PLATFORM=linux/amd64
# Use python:3.11-slim as the base image
FROM python:3.13-slim


# Set the working directory
WORKDIR /app

# Copy the backend directory into the Docker image
COPY . /app

# Copy the .env file into the Docker image
COPY .env /app/.env

# Copy the requirements.txt file into the Docker image
COPY requirements.txt /app/requirements.txt

# Below are steps for fixing pyarrow installation issue, if occurs

# RUN set -xe \
#     && apk update \
#     && apk add                  --no-cache                  \
#                                 build-base                  \
#                                 cmake                       \
#                                 apache-arrow-dev            \
#     && pip3 install             --upgrade pip               \
#     && pip3 install             --no-cache-dir              \
#                                 --prefer-binary             \
#                                 pyarrow
# Install the required dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8080

# Set the entrypoint to run the FastAPI application using uvicorn
ENTRYPOINT ["uvicorn", "rag_api.entrypoints.app:app", "--host", "0.0.0.0", "--port", "8080"]
