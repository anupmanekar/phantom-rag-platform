# RAG-based Requirements Ingestion & Test Generation

Soluiton for ingesting requirements from Azure DevOps or Jira into firestore and then using RAG based approach to comprehensively generate tests from those requirements.

- **Python**: Primary backend language
- **LLM Provider**: Gemini, FireworksAI
- **Vector DB**: Firestore
- **Operational DB**: Firestore

## Features

- Ingest the requirements from Azure Devops to Firestore
- Read images and store the information related to image in Firestore for each requirement
- Convert the requirement titles to embeddings
- Generate BDD Tests by requirement ID or description based on RAG

Ingestion, Process Images and Conversion to embeddings are available as command line jobs as well as API

## Setup Instructions

### Firestore
1. Setup Firestore (default) collection in GCP Firestore
2. Create a collection named "user_requirements"
3. Create Vector index on Firestore with 768 dimension
    ```
    gcloud firestore indexes composite create \
    --collection-group=user_requirements \
    --query-scope=COLLECTION \
    --field-config=order=ASCENDING,field-path="color" \
    --field-config field-path=vector-field,vector-config='{"dimension":"768", "flat": "{}"}' \
    --database=default
    ```

### Deploy ingestion workloads as Jobs

1. Build docker image
    ```
    docker build -t <image_name> -f ./backend/Dockerfile.jobs ./backend
    ```
2. Push docker to hub
    ```
    docker push <image_name>
    ```
3. Deploy to GCP Cloud Run Jobs

    ![Image](./images/cloud_run_job_config.png)

4. Ensure that service account is attached to your Cloud Run Job

### Deploy ingestion workloads as API

1. Build backend services
    ```
    docker build --platform linux/amd64 -t <image_name> ./backend
    ```
2. Run them locally
    ```
    docker run -p 8080:8080 <image_name>
    ```
3. Deploy on GCP Cloud Run Services

## Running the Application from workstation

1. Start the backend FastAPI application:
    ```sh
    uvicorn backend.app:app --reload
    ```

### Frontend

Need to do lot here.

 QA RAG Based Services API

API documentation for the QA RAG App

**Version:** 1.0.0
**OpenAPI:** 3.1.0

---

## API

- [Endpoints](#endpoints)
    - [GET /generate-bdd-for-ticket](#get-generate-bdd-for-ticket)
    - [GET /generate-bdd-for-features](#get-generate-bdd-for-features)
    - [POST /answer-query](#post-answer-query)
    - [GET /ingest-azure-in-firestore](#get-ingest-azure-in-firestore)
- [Schemas](#schemas)
    - [IngestRequest](#ingestrequest)
    - [Query](#query)
    - [HTTPValidationError](#httpvalidationerror)
    - [ValidationError](#validationerror)

---

## Endpoints

### GET `/generate-bdd-for-ticket`

**Generate Bdd**

- **Query Parameters:**
    - `ticket_id` (integer, required): Ticket Id
- **Responses:**
    - `200 OK`: Successful Response
    - `422 Validation Error`: [HTTPValidationError](#httpvalidationerror)

---

### GET `/generate-bdd-for-features`

**Generate Bdd**

- **Query Parameters:**
    - `description` (string, required): Description
- **Responses:**
    - `200 OK`: Successful Response
    - `422 Validation Error`: [HTTPValidationError](#httpvalidationerror)

---

### POST `/answer-query`

**Search**

- **Request Body:** [Query](#query) (application/json, required)

```
{
  "query": "string"
}
```

- **Responses:**
    - `200 OK`: Successful Response
    - `422 Validation Error`: [HTTPValidationError](#httpvalidationerror)

---



### GET `/ingest-azure-in-firestore`

**Ingest Requirements**

- **Responses:**
    - `200 OK`: Successful Response

---



