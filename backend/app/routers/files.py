from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/api/v1/files",
    tags=["files"]
)

@router.get("/{filename}")
def get_file(filename: str):
    file_path = os.path.join("files/", filename)
    return FileResponse(file_path)
