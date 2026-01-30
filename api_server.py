from fastapi import FastAPI, UploadFile, File
import shutil
import os

from orgagent import (
    initialize_pinecone,
    ingest_documents,
    get_llm,
    get_answer
)

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------------------
# Initialize ONCE at startup
# ---------------------------------
vectorstore = initialize_pinecone()
llm = get_llm()


# ---------------------------------
# Upload + ingest
# ---------------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_documents(vectorstore)  # your pipeline uses folder internally
    return {"status": "indexed"}


# ---------------------------------
# Chat
# ---------------------------------
@app.post("/chat")
async def chat(query: str):
    answer, sources = get_answer(query, vectorstore, llm)

    return {
        "response": answer,
        "sources": sources
    }


# ---------------------------------
# Stats
# ---------------------------------
@app.get("/stats")
def stats():
    return {"documents": len(os.listdir(UPLOAD_DIR))}
