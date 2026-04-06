from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil, os
from face_service import get_embedding
from database import add_embedding, search_embedding

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 📸 رفع صور المناسبة (نسخة محسّنة)
@app.post(
    "/upload-event-images/",
    summary="Upload multiple images",
    description="ارفع صور المناسبة وسيتم تحليل الوجوه"
)
async def upload_event_images(
    files: List[UploadFile] = File(..., description="اختر صور من جهازك")
):
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        embedding = get_embedding(file_path)
        add_embedding(embedding, file_path)

        results.append(file.filename)

    return {"uploaded_files": results}


# 🔍 البحث عن الشخص
@app.post(
    "/search/",
    summary="Search by face",
    description="ارفع صورة وجهك وسيتم البحث"
)
async def search(
    file: UploadFile = File(..., description="ارفع صورة وجهك")
):
    file_path = os.path.join(UPLOAD_FOLDER, f"query_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    query_embedding = get_embedding(file_path)
    results = search_embedding(query_embedding)

    return {"matches": results}


# 🧪 endpoint اختبار (مهم)
@app.post("/test-upload/")
async def test_upload(files: List[UploadFile] = File(...)):
    return {"filenames": [f.filename for f in files]}
