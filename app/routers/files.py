from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from app.dependencies.file import get_file_service
from app.services.file_service import FileService

router = APIRouter()

UploadedFiles = Annotated[
    list[UploadFile],
    File(...,description="One or more files to upload"),
]

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    file_service:FileService = Depends(get_file_service)
):
    return await file_service.save_file(file)

@router.post("/multiple")
async def upload_files(
    files: UploadedFiles,
    file_service:FileService = Depends(get_file_service)
):
    results = []

    for file in files:
        result = await file_service.save_file(file)
        results.append(result)

    return {
        "files": results
    }

@router.post("/document")
async def document_upload(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    file_service: FileService = Depends(get_file_service)
):
    result = await file_service.save_file(file)
    return {
        "file": result,
        "document_type": document_type
    }

@router.get("/stream")
async def stream():
    def generate():
        for i in range(10):
            yield f"Stream {i+1}\n"

    return StreamingResponse(generate(), media_type="text/plain")

@router.get("/{filename}")
async def download(filename: str):
    file_path = Path("uploads") / filename