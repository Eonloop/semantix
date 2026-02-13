from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb


class Ingestor:
    def __init__(self, vector_db_path, model_name):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
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

        self.collection.add(
            documents=[chunk.page_content for chunk in chunks],
            ids=[f"chunk_{i}" for i in range(len(chunks))],
        )

        print(f"Ingested {len(chunks)} chunks")


if __name__ == "__main__":
    ingestor = Ingestor(vector_db_path="./data/vector.db", model_name="sentence-transformers/all-MiniLM-L6-v2")
    ingestor.ingest("/home/kingfisher/Dev/semantix/data/sample_policy.pdf")