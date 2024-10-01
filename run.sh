cd src

# requirements
pip install fastapi
pip install uvicorn
pip install sqlalchemy 
pip install passlib
pip install bcrypt
pip install python-jose
pip install python-multipart
pip install pandas openpyxl
pip install aiofiles
pip install pytest
pip install requests


# run
pip install virtualenv     
.\fastapi-venv\Scripts\Activate.ps1
uvicorn main:app --reload
