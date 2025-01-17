from backend.llm_handler import LLMHandler
from backend.embedding_storage import EmbeddingStorage

class RAGHandler:
    def __init__(self, llm_handler: LLMHandler, embedding_storage: EmbeddingStorage):
        self.llm_handler = llm_handler
        self.embedding_storage = embedding_storage

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
        naive_rag_chain = prompt | self.llm_handler.model | parse_output
        print("Chain created")
        result = naive_rag_chain.invoke({"question": query, "output_language": "German", "context": docs})

        return result
