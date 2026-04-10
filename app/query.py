import chromadb
from sentence_transformers import SentenceTransformer

__all__ = ["Query"]

class Query:
    def __init__(self, model_name, vector_db_path="./data/vector.db"):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=vector_db_path)
        self.collection = self.client.get_or_create_collection(name="policies")

    def query(self, query_text, k: int | None = 2):
        query_embedding = self.model.encode(query_text).tolist()
        count = self.collection.count()
        if count == 0:
            return [], []
        n_results = 2 if k is None else int(k)
        n_results = max(1, min(n_results, count))
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )
        return results["documents"][0], results["metadatas"][0]

if __name__ == "__main__":
    query = Query(model_name="sentence-transformers/all-MiniLM-L6-v2")
    query_text = input("Enter your query: ")
    document, metadata = query.query(query_text)
    print(f"Document: {document}")
    print(f"Metadata: {metadata}")