# -*- coding: utf-8 -*-
"""
Интеграционные тесты API endpoints.
"""
import pytest
from fastapi import status


def test_health_endpoint(client):
    """Тест healthcheck endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_endpoint(client):
    """Тест version endpoint."""
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_create_task_success(client):
    """Тест успешного создания задачи."""
    task_data = {
        "title": "API Test Task",
        "description": "Test description",
        "priority": "high",
        "position": 0
    }
    
    response = client.post("/tasks/", json=task_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "API Test Task"
    assert data["priority"] == "high"
    assert data["status"] == False
    assert "id" in data


def test_get_tasks_empty(client):
    """Тест получения пустого списка задач."""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_data(client):
    """Тест получения списка задач."""
    # Создаём задачи
    client.post("/tasks/", json={"title": "Task 1", "priority": "low"})
    client.post("/tasks/", json={"title": "Task 2", "priority": "high"})
    
    # Получаем список
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_tasks_with_filters(client):
    """Тест фильтрации задач через API."""
    # Создаём задачи
    client.post("/tasks/", json={"title": "High Priority", "priority": "high"})
    client.post("/tasks/", json={"title": "Low Priority", "priority": "low"})
    
    # Фильтр по приоритету
    response = client.get("/tasks/?priority=high")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["priority"] == "high"
    
    # Поиск по тексту
    response = client.get("/tasks/?search=High")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert "High" in tasks[0]["title"]


def test_update_task_success(client):
    """Тест обновления задачи."""
    # Создаём задачу
    create_response = client.post("/tasks/", json={"title": "Original"})
    task_id = create_response.json()["id"]
    
    # Обновляем задачу
    update_data = {"title": "Updated", "status": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated"
    assert updated_task["status"] == True


def test_delete_task_success(client):
    """Тест удаления задачи."""
    # Создаём задачу
    create_response = client.post("/tasks/", json={"title": "To Delete"})
    task_id = create_response.json()["id"]
    
    # Удаляем задачу
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Проверяем, что задача удалена
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_get_nonexistent_task(client):
    """Тест получения несуществующей задачи."""
    response = client.get("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_pagination(client):
    """Тест пагинации."""
    # Создаём 10 задач
    for i in range(10):
        client.post("/tasks/", json={"title": f"Task {i}"})
    
    # Запрашиваем первые 5
    response = client.get("/tasks/?skip=0&limit=5")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 5
    
    # Запрашиваем следующие 5
    response = client.get("/tasks/?skip=5&limit=5")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 5
