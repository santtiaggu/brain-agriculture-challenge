import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from main import app

client = TestClient(app)

@pytest.fixture
def mock_producer():
    return {
        "id": 1,
        "name": "José da Silva",
        "document": "123.456.789-09",
        "farms": [
            {
                "id": 1,
                "name": "Fazenda Santa Maria",
                "city": "Ribeirão Preto",
                "state": "SP",
                "total_area": 150.0,
                "agricultural_area": 90.0,
                "vegetation_area": 60.0,
                "crops": [
                    {"id": 1, "season": "2023/2024", "name": "Soja"},
                    {"id": 2, "season": "2022/2023", "name": "Milho"},
                ],
            }
        ]
    }


@patch("routers.producer.create_producer")
def test_post_producer(mock_create):
    mock_create.return_value = {"message": "Producer created successfully"}
    payload = {
        "name": "José da Silva",
        "document": "123.456.789-09",
        "farms": []
    }
    response = client.post("/api/producers", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Producer created successfully"}

@patch("routers.producer.list_producers")
def test_post_list_producers(mock_list):
    mock_list.return_value = {
        "total": 1,
        "page": 1,
        "size": 10,
        "producers": []
    }
    response = client.post("/api/producers/list", json={"page": 1, "size": 10})
    assert response.status_code == 200
    assert response.json()["total"] == 1

@patch("routers.producer.get_producer")
def test_get_producer_by_id(mock_get, mock_producer):
    mock_get.return_value = mock_producer
    response = client.get("/api/producers/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("routers.producer.get_producer")
def test_get_producer_by_id_not_found(mock_get):
    mock_get.return_value = None
    response = client.get("/api/producers/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Producer not found"

@patch("routers.producer.update_producer")
def test_put_producer(mock_update):
    mock_update.return_value = {"message": "Producer updated successfully"}
    response = client.put("/api/producers/1", json={
        "name": "Novo Nome",
        "document": "987.654.321-00",
        "farms": []
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Producer updated successfully"

@patch("routers.producer.delete_producer")
def test_delete_producer(mock_delete):
    mock_delete.return_value = {"message": "Producer deleted successfully"}
    response = client.delete("/api/producers/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Producer deleted successfully"
