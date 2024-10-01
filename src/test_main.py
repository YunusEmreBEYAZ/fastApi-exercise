from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello PyBooking!"

def test_upload_file():
    response = client.post("/file/", files={"file": ("test.txt", b"file content")})
    assert response.status_code == 200
    assert response.json() == {"filename": "test.txt", "lines": ["file content"]}

def test_get_user():
    response = client.get("/user/id/1")
    assert response.status_code == 200
    assert response.json() == {
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2000-09-26",
  "gender": "male",
  "hotels": [
    {
      "id": 1,
      "name": "grand hotel",
      "address": "123 Main Street, New York, NY 10001",
      "city": "new york"
    }
  ]
}

def test_get_user_not_found():
    response = client.get("/user/100")
    assert response.status_code == 404
    assert response.json() == {"detail": 'Not Found'}