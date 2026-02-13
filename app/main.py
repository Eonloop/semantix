import fastapi
import chromadb


app = FastAPI()


@app.get("/search")
async def search():    
    return

@app.post("/ingest")
async def ingest():
    return