from llm_handler import LLMHandler
from embedding_storage import EmbeddingStorage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from monitoring.observability import getLogger

logger = getLogger(__name__)

class RAGHandler:
    def __init__(self, llm_handler: LLMHandler, embedding_storage: EmbeddingStorage):
        self.llm_handler = llm_handler
        self.embedding_storage = embedding_storage

    def answer_query(self, query: str) -> str:
        logger.info(f"Answering query: {query}")
        retriever = self.embedding_storage.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        logger.info("Retriever created")
        docs = retriever.invoke(query)
        logger.info(f"Retrieved documents: {docs}")
        logger.info("Template creation in process")
        messages = [
            (
                "system",
                "You are a software QA tester who uses following pieces of context {context} to answer the question",
            ),
            ("human", "{question}"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages=messages)
        logger.info("Prompt created")
        parse_output = StrOutputParser()
        naive_rag_chain = prompt | self.llm_handler.model | parse_output
        logger.info("Chain created")
        result = naive_rag_chain.invoke({"question": query, "context": docs})

        return result
    
    def generate_bdd(self, task_id: str) -> str:
        logger.info(f"Generating BDD for Task ID: {task_id}")
        retriever = self.embedding_storage.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        logger.info("Retriever created")
        query = f"What is the description for: {task_id}"
        docs = retriever.invoke(query)
        logger.info(f"Retrieved documents: {docs}")
        logger.info("Template creation in process")
        messages = [
            (
                "system",
                "You are a software QA tester who uses following pieces of context {context} to answer the question",
            ),
            ("human", "{question}"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages=messages)
        logger.info("Prompt created")
        parse_output = StrOutputParser()
        naive_rag_chain = prompt | self.llm_handler.model | parse_output
        logger.info("Chain created")
        result = naive_rag_chain.invoke({"question": "Generate the BDD for the requirement", "context": docs})

        return result

