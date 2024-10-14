cd src

# requirements
pip install fastapi
pip install uvicorn
pip install sqlalchemy 
pip install passlib
pip install bcrypt
pip install python-jose
pip install python-multipart
pip install aiofiles
pip install requests
pip install pytest

uvicorn main:app --reload
