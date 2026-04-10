from pathlib import Path

import pytest

from app.ingest import Ingestor
from app.query import Query

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@pytest.fixture(scope="session")
def query_engine_eval_corpus(tmp_path_factory):
    db_path = str(tmp_path_factory.mktemp("perf_eval_db"))
    repo_root = Path(__file__).resolve().parents[2]
    eval_dir = repo_root / "eval_corpus"
    if not eval_dir.is_dir():
        pytest.skip(f"eval_corpus not found at {eval_dir}")

    ingestor = Ingestor(vector_db_path=db_path, model_name=MODEL_NAME)
    ingestor.ingest_directory(str(eval_dir))

    return Query(model_name=MODEL_NAME, vector_db_path=db_path)
