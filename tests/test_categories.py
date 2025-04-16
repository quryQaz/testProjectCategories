from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_descendants():
    response = client.get("/categories/2/descendants")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(cat["name"] == "Смартфоны" for cat in data)

def test_get_descendants_not_found():
    response = client.get("/categories/99999/descendants")
    assert response.status_code == 404
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("detail") == "Category not found or has no descendants"

def test_get_descendants_id_not_int():
    response = client.get("/categories/ID_STRING/descendants")
    assert response.status_code == 422