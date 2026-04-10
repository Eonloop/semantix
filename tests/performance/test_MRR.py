import pytest

QUERY = "how to prevent sql injection in authentication systems"
EXPECTED_DOC_FRAGMENT = "doc-01-sql-injection.md"


@pytest.mark.db
@pytest.mark.slow
def test_top_result_is_expected_doc_for_sql_injection_query(query_engine_eval_corpus):
    documents, metadatas = query_engine_eval_corpus.query(QUERY)
    assert documents, "no chunks returned from eval index"
    assert metadatas and metadatas[0] is not None
    src = metadatas[0].get("source") or ""
    assert EXPECTED_DOC_FRAGMENT in src, (
        f"expected source containing {EXPECTED_DOC_FRAGMENT!r}, got {src!r}"
    )
