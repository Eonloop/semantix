from fastapi import FastAPI
import chromadb

client = chromadb.Client()

collection = client.create_collection(name="policies")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}





