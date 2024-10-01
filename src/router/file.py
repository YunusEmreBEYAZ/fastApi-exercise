from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != 'text/plain':
        raise HTTPException(status_code=400, detail="Only plain text files are supported.")
    
    # Read the file contents
    contents = await file.read()
    content_str = contents.decode("utf-8")
    lines = content_str.split("\n")
    
    return {"filename": file.filename, "lines": lines}

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    path = f"images/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "content_type": file.content_type}

@router.get("/download/{name}", response_class=FileResponse)
def download_file(name:str):
    path = f"images/{name}"
    return path