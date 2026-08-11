from uuid import uuid4
from fastapi import UploadFile
from pathlib import Path
from app.core.exceptions import UnsupportedFileTypeExecption, FileTooLargeExecption

class FileService:
    UPLOAD_DIR = Path("uploads")

    ALLOWED_TYPES = {
        "application/pdf",
        "image/pdf",
        "image/jpeg",
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024

    async def save_file(
        self,
        file: UploadFile
    ):
        if file.content_type not in self.ALLOWED_TYPES:
            raise UnsupportedFileTypeExecption()

        extension = Path(
            file.filename
        ).suffix.lower()

        filename = (
            f"{uuid4()}{extension}"
        )

        self.UPLOAD_DIR.mkdir(
            exist_ok=True
        )

        file_path = (
            self.UPLOAD_DIR / filename
        )

        size = 0

        with file_path.open("wb") as buffer:
            while chunk:=await file.read(1024*1024):
                size+=len(chunk)
                if size > self.MAX_FILE_SIZE:
                    file_path.unlink(
                        missing_ok=True
                    )
                    raise FileTooLargeExecption()
                buffer.write(chunk)

        return {
            "filename": filename,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "size": size
        }