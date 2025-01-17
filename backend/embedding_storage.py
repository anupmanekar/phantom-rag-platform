from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_fireworks import FireworksEmbeddings, ChatFireworks
import numpy as np
import os

class EmbeddingStorage:
    def __init__(self, mongo_uri, db_name, collection_name):
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


    def store_embeddings(self, embeddings):
        self.collection.delete_many({})
        self.collection.insert_many(embeddings)

    def search_embeddings(self, query_embedding, threshold=0.8):
        # all_embeddings = list(self.collection.find({}, {"_id": 0, "embedding": 1, "ticket_id": 1}))
        # embeddings = [item["embedding"] for item in all_embeddings]
        # ticket_ids = [item["ticket_id"] for item in all_embeddings]

        # similarities = cosine_similarity([query_embedding], embeddings)[0]
        # results = []
        # for i, similarity in enumerate(similarities):
        #     if similarity >= threshold:
        #         results.append({"ticket_id": ticket_ids[i], "similarity": similarity})

        # results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]
        return []
    
    def answer_query(self, query: str) -> str:
        print(f"Answering query: {query}")
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        print("Retriever created")
        # Generate context using the retriever, and pass the user question through
        # splits = query.split(":")
        # title = splits[0]
        # query = splits[1]
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
        # Defining the chat prompt
        prompt = ChatPromptTemplate.from_messages(messages=messages)
        print("Prompt created")
        # Parse output as a string
        parse_output = StrOutputParser()
        model1 = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-8b-instruct", max_tokens=None, temperature=0, api_key=os.environ.get("FIREWORKS_API_KEY"))
        # Naive RAG chain
        naive_rag_chain = prompt | model1 | parse_output
        print("Chain created")
        # Run the chain
        result = naive_rag_chain.invoke({"question": query, "output_language": "German", "context":docs})

        return result
    
