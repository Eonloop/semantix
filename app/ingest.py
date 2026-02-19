from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import os


class Ingestor:
    def __init__(self, vector_db_path, model_name):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=vector_db_path)
        self.collection = self.client.get_or_create_collection(name="policies")

    def ingest(self, file_path):
        if file_path.endswith(".pdf"):
            loader = PyMuPDFLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file_path.endswith(".txt") or file_path.endswith(".md"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        ids = [f"{file_path}:chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file_path, "chunk_index": i} for i in range(len(chunks))]
        embeddings = self.model.encode(texts).tolist()

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts,
        )

        print(f"Ingested {len(chunks)} chunks from {file_path}")


if __name__ == "__main__":
    input_file = os.path.expanduser(input("Enter the path to the file to ingest: ").strip())
    ingestor = Ingestor(vector_db_path="./data/vector.db", model_name="sentence-transformers/all-MiniLM-L6-v2")
    ingestor.ingest(input_file)