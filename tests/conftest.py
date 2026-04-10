import pytest
import chromadb

from app.ingest import Ingestor
from app.query import Query

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

POLICIES_COLLECTION_NAME = "policies"


@pytest.fixture
def vector_db_path(tmp_path) -> str:
    return str(tmp_path)


@pytest.fixture
def policies_collection(vector_db_path):
    client = chromadb.PersistentClient(path=vector_db_path)
    return client.get_or_create_collection(name=POLICIES_COLLECTION_NAME)


@pytest.fixture(scope="session")
def chroma_client(tmp_path_factory):
    test_db_dir = str(tmp_path_factory.mktemp("data"))
    return chromadb.PersistentClient(path=test_db_dir)


@pytest.fixture
def test_data():
    return [
        {"id": "1", "text": "This is a test document", "metadata": {"source": "test.txt"}},
        {"id": "2", "text": "This is another test document", "metadata": {"source": "test2.txt"}},
        {"id": "3", "text": "This is a third test document", "metadata": {"source": "test3.txt"}},
    ]


@pytest.fixture
def ingestor(vector_db_path):
    return Ingestor(vector_db_path=vector_db_path, model_name=MODEL_NAME)


@pytest.fixture
def sample_txt_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("The refund policy states that users can request a full refund within 14 days. "
                         "After 14 days, partial refunds may be issued at the company's discretion. "
                         "Subscriptions can be cancelled at any time from the account settings page.")
    return str(file_path)


@pytest.fixture
def sample_dir(tmp_path):
    (tmp_path / "doc1.txt").write_text("First document about refund policies and returns.")
    (tmp_path / "doc2.txt").write_text("Second document about privacy and data protection.")
    (tmp_path / "ignore.csv").write_text("col1,col2\nval1,val2")
    (tmp_path / "ignore.json").write_text('{"key": "value"}')
    return str(tmp_path)
