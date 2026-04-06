from fastapi import FastAPI, UploadFile, File
import shutil, os
from face_service import get_embedding
from database import add_embedding, search_embedding

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload-event-images/")
async def upload_event_images(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        file_path = f"{UPLOAD_FOLDER}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        embedding = get_embedding(file_path)
        add_embedding(embedding, file_path)

        results.append(file_path)

    return {"files": results}


@app.post("/search/")
async def search(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_FOLDER}/query_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    query_embedding = get_embedding(file_path)
    results = search_embedding(query_embedding)

    return {"matches": results}
