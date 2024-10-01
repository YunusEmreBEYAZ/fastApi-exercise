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

uvicorn main:app --reload
