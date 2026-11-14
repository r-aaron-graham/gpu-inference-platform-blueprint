from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_echoes_fixture():
    response = client.post("/predict", json={"inputs": [1, 2]})
    assert response.status_code == 200
    assert response.json() == {"outputs": [1, 2]}


def test_empty_prediction_is_rejected():
    assert client.post("/predict", json={"inputs": []}).status_code == 400
