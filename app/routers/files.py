from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends
from app.dependencies.file import get_file_service
from app.services.file_service import FileService

router = APIRouter()

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    file_service:FileService = Depends(get_file_service)
):
    return await file_service.save_file(file)

@router.post("/multiple")
async def upload_files(
    files: list[UploadFile] = File(...),
    file_service:FileService = Depends(get_file_service)
):
    results = []

    for file in files:
        result = await file_service.save_file(file)
        results.append(result)

    return {
        "files": results
    }