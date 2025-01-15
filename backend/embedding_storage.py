from pymongo import MongoClient
import numpy as np
import os

class EmbeddingStorage:
    def __init__(self, mongo_uri, db_name, collection_name):
        print(f"Connecting to MongoDB at {mongo_uri}")
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

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
