import pytest

QUERY = "how to prevent sql injection in authentication systems"
EXPECTED_DOC_FRAGMENT = "doc-01-sql-injection.md"


def _source_contains(metadatas: list, fragment: str) -> bool:
    for m in metadatas:
        if m and fragment in (m.get("source") or ""):
            return True
    return False


@pytest.mark.db
@pytest.mark.slow
def test_recall_at_k_top_ranked_doc(query_engine_eval_corpus):
    documents, metadatas = query_engine_eval_corpus.query(QUERY)
    assert documents
    assert _source_contains(metadatas, EXPECTED_DOC_FRAGMENT)


@pytest.mark.db
@pytest.mark.slow
def test_recall_at_k_with_k(query_engine_eval_corpus):
    documents, metadatas = query_engine_eval_corpus.query(QUERY, k=1)
    assert len(documents) == 1
    assert len(metadatas) == 1
    assert _source_contains(metadatas, EXPECTED_DOC_FRAGMENT)


@pytest.mark.db
@pytest.mark.slow
def test_recall_at_k_with_none_k_returns_default_top_two(query_engine_eval_corpus):
    documents, metadatas = query_engine_eval_corpus.query(QUERY, k=None)
    assert len(documents) == 2
    assert len(metadatas) == 2
