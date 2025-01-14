# RAG-based Jira Ticket Query Application

This application is designed to provide responses to any queries regarding tickets in Jira using Retrieval Augmented Generation (RAG). The application utilizes the following technology stack:

- **Python**: Primary backend language
- **Langchain**: Framework for LLM Orchestration
- **LLM Provider**: FireworksAI
- **Vector DB**: MongoDB
- **Operational DB**: MongoDB
- **Monitoring & Observability**: Langsmith

## Features

- Connects with Jira and converts ticket information into embeddings.
- Stores embeddings in MongoDB as a vector database.
- Searches embeddings with cosine similarity of 80%.
- Summarizes the top 5 search results.
- Exposes search query functionality through an API.
- Provides a Next.js based front end with chat functionality to integrate with the API.

## Setup Instructions

### Backend

1. Set up a Python environment and install necessary dependencies:
    ```sh
    pip install fastapi uvicorn langchain fireworksai pymongo
    ```

2. Create a connection to Jira using Jira's REST API to fetch ticket information.

3. Convert the fetched ticket information into embeddings using FireworksAI embeddings.

4. Store the embeddings in MongoDB as a vector database.

5. Implement a search functionality that uses cosine similarity of 80% to find relevant embeddings.

6. Summarize the top 5 search results using Langchain's LLM orchestration.

7. Expose the search query functionality through a REST API using FastAPI.

8. Run the FastAPI application:
    ```sh
    uvicorn backend.app:app --reload
    ```

### Frontend

1. Set up a Next.js project:
    ```sh
    npx create-next-app@latest
    ```

2. Create a chat interface where users can enter their queries.

3. Integrate the chat interface with the backend API to send user queries and display the summarized results.

4. Run the Next.js application:
    ```sh
    npm run dev
    ```

### Monitoring and Observability

1. Integrate Langsmith for monitoring and observability of the application.

2. Set up logging and error handling to track the performance and issues in the application.

3. Implement metrics and dashboards to monitor the health and usage of the application.

4. Start the Prometheus server for monitoring:
    ```sh
    python monitoring/observability.py
    ```

## Running the Application

1. Start the backend FastAPI application:
    ```sh
    uvicorn backend.app:app --reload
    ```

2. Start the frontend Next.js application:
    ```sh
    npm run dev
    ```

3. Start the Prometheus server for monitoring:
    ```sh
    python monitoring/observability.py
    ```

## Monitoring and Observability

1. Integrate Langsmith for monitoring and observability of the application.

2. Set up logging and error handling to track the performance and issues in the application.

3. Implement metrics and dashboards to monitor the health and usage of the application.

4. Start the Prometheus server for monitoring:
    ```sh
    python monitoring/observability.py
    ```
