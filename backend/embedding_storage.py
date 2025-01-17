from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_fireworks import FireworksEmbeddings, ChatFireworks
import numpy as np
import os

class EmbeddingStorage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmbeddingStorage, cls).__new__(cls)
        return cls._instance

    def __init__(self, mongo_uri, db_name, collection_name):
        if not hasattr(self, 'initialized'):
            print(f"Connecting to MongoDB at {mongo_uri}")
            self.client = MongoClient(mongo_uri)
            self.db = self.client.get_database(db_name)
            self.collection = self.db.get_collection(collection_name)
            self.embeddings = FireworksEmbeddings(model='nomic-ai/nomic-embed-text-v1.5')
            self.vector_store = MongoDBAtlasVectorSearch.from_connection_string(
                connection_string=mongo_uri,
                namespace=db_name + "." + collection_name,
                embedding=self.embeddings,
                index_name="vector_index",
                text_key="ticket_title",
            )
            self.model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-8b-instruct", max_tokens=None, temperature=0, api_key=os.environ.get("FIREWORKS_API_KEY"))
            self.initialized = True

    @classmethod
    def get_instance(cls, mongo_uri=None, db_name=None, collection_name=None):
        if not cls._instance:
            cls._instance = cls(mongo_uri, db_name, collection_name)
        return cls._instance

    def store_embeddings(self, embeddings):
        self.collection.delete_many({})
        self.collection.insert_many(embeddings)

    def search_embeddings(self, query_embedding, threshold=0.8):
        return []
    
    def answer_query(self, query: str) -> str:
        print(f"Answering query: {query}")
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
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
