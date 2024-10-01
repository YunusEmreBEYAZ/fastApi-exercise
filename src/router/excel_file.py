from fastapi import APIRouter, File, UploadFile, HTTPException, status
import pandas as pd

router = APIRouter(
    prefix= "/excel_file",
    tags=["excel_file"]
)

@router.post("/")
async def upload_excel_file(file: UploadFile = File(...)):
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Only Excel files are supported.")
    
        # Read the file content into a Pandas DataFrame
    try:
        contents = await file.read()  # Read the file's bytes
        df = pd.read_excel(contents, engine='openpyxl')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")
    
    # Convert the DataFrame to a list of dictionaries (or process it as needed)
    data = df.to_dict(orient='records')
    
    return {"filename": file.filename, "data": data}