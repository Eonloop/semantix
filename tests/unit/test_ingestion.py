import pytest


def test_can_add_documents(chroma_client, test_data):
    collection = chroma_client.get_or_create_collection(name="ingestion_test")

    collection.add(
        ids=[d["id"] for d in test_data],
        documents=[d["text"] for d in test_data],
        metadatas=[d["metadata"] for d in test_data],
    )

    assert collection.count() == len(test_data)


def test_unsupported_file_type_raises_error(ingestor):
    with pytest.raises(ValueError, match="Unsupported file type"):
        ingestor.ingest("document.csv")


def test_ingest_txt_file(ingestor, sample_txt_file):
    ingestor.ingest(sample_txt_file)
    assert ingestor.collection.count() > 0


def test_ingest_stores_metadata(ingestor, sample_txt_file):
    ingestor.ingest(sample_txt_file)
    results = ingestor.collection.get()
    for meta in results["metadatas"]:
        assert "source" in meta
        assert "chunk_index" in meta
        assert meta["source"] == sample_txt_file


def test_upsert_no_duplicates(ingestor, sample_txt_file):
    ingestor.ingest(sample_txt_file)
    count_after_first = ingestor.collection.count()

    ingestor.ingest(sample_txt_file)
    count_after_second = ingestor.collection.count()

    assert count_after_first == count_after_second


def test_ingest_directory_only_processes_supported_files(ingestor, sample_dir):
    ingestor.ingest_directory(sample_dir)
    results = ingestor.collection.get()
    sources = {meta["source"] for meta in results["metadatas"]}
    for source in sources:
        assert source.endswith((".txt", ".md", ".pdf", ".docx"))
