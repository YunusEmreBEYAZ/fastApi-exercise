cd src

# requirements
pip install fastapi
pip install uvicorn
pip install sqlalchemy 
pip install passlib
pip install bcrypt
pip install python-jose

uvicorn main:app --reload
