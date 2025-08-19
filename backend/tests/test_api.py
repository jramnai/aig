from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_missing_inputs():
    response = client.post("/generate-questions", data={})
    assert response.status_code == 200
    assert "error" in response.json()
