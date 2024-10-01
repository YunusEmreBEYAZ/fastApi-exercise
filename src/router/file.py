from fastapi import APIRouter, File, UploadFile, HTTPException

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
