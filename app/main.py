import os
import tempfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.ingest import Ingestor
from app.query import Query


MODEL_NAME = os.getenv("SEMANTIX_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_DB_PATH = os.getenv("SEMANTIX_VECTOR_DB_PATH", "./data/vector.db")

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def ui() -> FileResponse:
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="Missing static/index.html")
    return FileResponse(str(index_path))


@app.get("/search")
async def search(query: str, top_k: int = 5) -> dict[str, Any]:
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is required")

    engine = Query(model_name=MODEL_NAME, vector_db_path=VECTOR_DB_PATH)

    documents, metadatas = engine.query(query)

    results: list[dict[str, Any]] = []
    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        results.append(
            {
                "rank": i + 1,
                "text": doc,
                "metadata": meta,
            }
        )

    return {"query": query, "results": results}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)) -> dict[str, Any]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in Ingestor.SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}. Supported: {sorted(Ingestor.SUPPORTED_EXTENSIONS)}",
        )

    ingestor = Ingestor(vector_db_path=VECTOR_DB_PATH, model_name=MODEL_NAME)

    with tempfile.TemporaryDirectory(prefix="semantix-upload-") as tmpdir:
        tmp_path = Path(tmpdir) / f"upload{suffix}"
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        tmp_path.write_bytes(content)

        ingestor.ingest(str(tmp_path))

    return {"status": "ok", "filename": file.filename}