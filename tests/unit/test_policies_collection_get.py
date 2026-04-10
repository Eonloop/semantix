import pytest

def test_policies_collection_starts_empty(policies_collection):
    assert policies_collection.name == "policies"
    out = policies_collection.get(include=["documents", "metadatas"])
    assert out["ids"] == []
    assert policies_collection.count() == 0


@pytest.mark.db
@pytest.mark.slow
def test_policies_collection_get_after_ingest(ingestor, policies_collection, sample_txt_file):
    ingestor.ingest(sample_txt_file)

    out = policies_collection.get(include=["documents", "metadatas"])
    assert len(out["ids"]) == policies_collection.count()
    assert len(out["ids"]) > 0
    assert len(out["documents"]) == len(out["metadatas"]) == len(out["ids"])

    for meta in out["metadatas"]:
        assert meta is not None
        assert "source" in meta
        assert sample_txt_file in meta["source"] or meta["source"] == sample_txt_file
