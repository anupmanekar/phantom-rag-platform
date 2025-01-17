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
