from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

class EmbeddingStorage:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("DB_NAME")]
        self.collection = self.db[os.getenv("COLLECTION_NAME")]

    def store_embeddings(self, embeddings):
        self.collection.insert_many(embeddings)

    def search_embeddings(self, query_embedding, threshold=0.8):
        all_embeddings = list(self.collection.find({}, {"_id": 0, "embedding": 1, "ticket_id": 1}))
        embeddings = [item["embedding"] for item in all_embeddings]
        ticket_ids = [item["ticket_id"] for item in all_embeddings]

        similarities = cosine_similarity([query_embedding], embeddings)[0]
        results = []
        for i, similarity in enumerate(similarities):
            if similarity >= threshold:
                results.append({"ticket_id": ticket_ids[i], "similarity": similarity})

        results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]
        return results
