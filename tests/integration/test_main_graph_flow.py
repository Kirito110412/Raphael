from fastapi.testclient import TestClient
from interfaces.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "system": "ready"}

def test_task_submission():
    payload = {"input": "test task", "modality": "text", "priority": 1}
    response = client.post("/task", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["input"] == "test task"
