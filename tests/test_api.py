from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ping():
    response = client.post("/base/chat", json={"message": "Hi"})
    assert response.status_code == 200
    # assert response.json() == {"message": ""}
