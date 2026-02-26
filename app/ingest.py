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

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}

    def ingest_directory(self, dir_path):
        files = [
            os.path.join(root, f)
            for root, _, filenames in os.walk(dir_path)
            for f in filenames
            if os.path.splitext(f)[1].lower() in self.SUPPORTED_EXTENSIONS
        ]

        if not files:
            print(f"No supported files found in {dir_path}")
            return

        print(f"Found {len(files)} supported file(s) in {dir_path}")
        for file_path in files:
            try:
                self.ingest(file_path)
            except Exception as e:
                print(f"Failed to ingest {file_path}: {e}")


if __name__ == "__main__":
    input_path = os.path.expanduser(input("Enter the path to a file or folder to ingest: ").strip())
    if not os.path.exists(input_path):
        print(f"Path {input_path} does not exist")
        exit(1)
    ingestor = Ingestor(vector_db_path="./data/vector.db", model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.isdir(input_path):
        ingestor.ingest_directory(input_path)
    else:
        ingestor.ingest(input_path)