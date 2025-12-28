import pytest
from fastapi.testclient import TestClient
from test_app import app

# Создаем тестовый клиент
client = TestClient(app)

def test_read_root():
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item():
    """Тест получения item"""
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": None}

def test_read_item_with_query():
    """Тест получения item с query параметром"""
    response = client.get("/items/42?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "test"}

def test_read_item_not_found():
    """Тест несуществующего пути"""
    response = client.get("/nonexistent")
    assert response.status_code == 404