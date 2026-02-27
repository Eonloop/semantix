import chromadb
import os
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./data/vector.db")
collection = client.get_or_create_collection(name="policies")


class Query:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path="./data/vector.db")
        self.collection = self.client.get_or_create_collection(name="policies")

    def query(self, query_text):
        query_embedding = self.model.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=2,
        )
        return results["documents"][0], results["metadatas"][0]

if __name__ == "__main__":
    query = Query(model_name="sentence-transformers/all-MiniLM-L6-v2")
    query_text = input("Enter your query: ")
    document, metadata = query.query(query_text)
    print(f"Document: {document}")
    print(f"Metadata: {metadata}")