import pytest
from conftest import MODEL_NAME
from ingest import Ingestor
from query import Query


@pytest.fixture
def populated_db(tmp_path, sample_txt_file):
    db_path = str(tmp_path)
    ingestor = Ingestor(vector_db_path=db_path, model_name=MODEL_NAME)
    ingestor.ingest(sample_txt_file)
    return db_path


@pytest.fixture
def query_engine(populated_db):
    return Query(model_name=MODEL_NAME, vector_db_path=populated_db)


def test_query_returns_documents_and_metadata(query_engine):
    documents, metadatas = query_engine.query("refund")
    assert isinstance(documents, list)
    assert isinstance(metadatas, list)
    assert len(documents) > 0
    assert len(metadatas) > 0


def test_query_returns_correct_number_of_results(query_engine):
    documents, metadatas = query_engine.query("refund")
    assert len(documents) <= 2
    assert len(documents) == len(metadatas)


def test_metadata_has_expected_fields(query_engine):
    _, metadatas = query_engine.query("refund")
    for meta in metadatas:
        assert "source" in meta
        assert "chunk_index" in meta


def test_query_results_are_relevant(query_engine):
    documents, _ = query_engine.query("refund policy")
    combined = " ".join(documents).lower()
    assert "refund" in combined
