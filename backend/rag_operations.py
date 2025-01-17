from backend.embedding_storage import EmbeddingStorage
from backend.llm_handler import LLMHandler

class RAGOperations:
    def __init__(self, embedding_storage: EmbeddingStorage, llm_handler: LLMHandler):
        self.embedding_storage = embedding_storage
        self.llm_handler = llm_handler

    def search(self, query: str):
        return self.answer_query(query)

    def answer_query(self, query: str) -> str:
        print(f"Answering query: {query}")
        retriever = self.embedding_storage.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        print("Retriever created")
        docs = retriever.invoke(query)
        print(f"Retrieved documents: {docs}")
        print("Template creation in process")
        messages = [
            (
                "system",
                "You are a software QA tester who uses following pieces of context {context} to answer the question",
            ),
            ("human", "{question}"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages=messages)
        print("Prompt created")
        parse_output = StrOutputParser()
        model1 = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-8b-instruct", max_tokens=None, temperature=0, api_key=os.environ.get("FIREWORKS_API_KEY"))
        naive_rag_chain = prompt | model1 | parse_output
        print("Chain created")
        result = naive_rag_chain.invoke({"question": query, "output_language": "German", "context":docs})

        return result

    def ingest_jira(self, jira_connector, project_key: str, max_tickets: int):
        jql = f"project = {project_key} ORDER BY created DESC"
        tickets = jira_connector.fetch_tickets(jql)[:max_tickets]
        embeddings = jira_connector.convert_to_embeddings(tickets)
        self.embedding_storage.store_embeddings(embeddings)
        return {"message": "Ingestion successful"}

    def ingest_azure(self, azure_connector, project: str):
        query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.WorkItemType] = 'Task' and [System.TeamProject] = '{project}'"
        tickets = azure_connector.fetch_tickets(query)[:100]
        embeddings = azure_connector.convert_to_embeddings(tickets)
        self.embedding_storage.store_embeddings(embeddings)
        return {"message": "Ingestion successful"}
