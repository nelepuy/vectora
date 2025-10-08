# -*- coding: utf-8 -*-
"""
Тесты для CRUD операций с задачами.
"""
import pytest
from app import crud, schemas, models
from datetime import datetime


def test_create_task(db, test_user_id):
    """Тест создания задачи."""
    task_data = schemas.TaskCreate(
        title="Тестовая задача",
        description="Описание тестовой задачи",
        priority="high",
        position=0
    )
    
    created_task = crud.create_task(db, task_data, test_user_id)
    
    assert created_task.id is not None
    assert created_task.title == "Тестовая задача"
    assert created_task.user_id == test_user_id
    assert created_task.status == False
    assert created_task.priority == "high"


def test_get_tasks(db, test_user_id):
    """Тест получения списка задач."""
    # Создаём несколько задач
    for i in range(3):
        task_data = schemas.TaskCreate(
            title=f"Задача {i}",
            priority="normal",
            position=i
        )
        crud.create_task(db, task_data, test_user_id)
    
    tasks = crud.get_tasks(db, test_user_id)
    
    assert len(tasks) == 3
    assert all(t.user_id == test_user_id for t in tasks)


def test_get_tasks_with_filters(db, test_user_id):
    """Тест фильтрации задач."""
    # Создаём задачи с разными параметрами
    crud.create_task(db, schemas.TaskCreate(title="Высокий", priority="high"), test_user_id)
    crud.create_task(db, schemas.TaskCreate(title="Низкий", priority="low"), test_user_id)
    crud.create_task(db, schemas.TaskCreate(title="Средний", priority="normal"), test_user_id)
    
    # Фильтр по приоритету
    high_priority_tasks = crud.get_tasks(db, test_user_id, priority="high")
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0].priority == "high"
    
    # Поиск по тексту
    search_results = crud.get_tasks(db, test_user_id, search="Высокий")
    assert len(search_results) == 1
    assert "Высокий" in search_results[0].title


def test_update_task(db, test_user_id):
    """Тест обновления задачи."""
    # Создаём задачу
    task = crud.create_task(
        db,
        schemas.TaskCreate(title="Старое название", priority="low"),
        test_user_id
    )
    
    # Обновляем задачу
    update_data = schemas.TaskUpdate(title="Новое название", priority="high", status=True)
    updated_task = crud.update_task(db, task.id, update_data, test_user_id)
    
    assert updated_task.title == "Новое название"
    assert updated_task.priority == "high"
    assert updated_task.status == True


def test_delete_task(db, test_user_id):
    """Тест удаления задачи."""
    # Создаём задачу
    task = crud.create_task(
        db,
        schemas.TaskCreate(title="Удалить меня"),
        test_user_id
    )
    
    # Удаляем задачу
    crud.delete_task(db, task.id, test_user_id)
    
    # Проверяем, что задача удалена
    tasks = crud.get_tasks(db, test_user_id)
    assert len(tasks) == 0


def test_get_task_by_id_not_found(db, test_user_id):
    """Тест получения несуществующей задачи."""
    from app.exceptions import TaskNotFoundError
    
    with pytest.raises(TaskNotFoundError):
        crud.get_task_by_id(db, 999, test_user_id)


def test_user_isolation(db):
    """Тест изоляции задач между пользователями."""
    user1_id = "user1"
    user2_id = "user2"
    
    # Создаём задачи для user1
    crud.create_task(db, schemas.TaskCreate(title="Задача user1"), user1_id)
    
    # Создаём задачи для user2
    crud.create_task(db, schemas.TaskCreate(title="Задача user2"), user2_id)
    
    # Проверяем изоляцию
    user1_tasks = crud.get_tasks(db, user1_id)
    user2_tasks = crud.get_tasks(db, user2_id)
    
    assert len(user1_tasks) == 1
    assert len(user2_tasks) == 1
    assert user1_tasks[0].title == "Задача user1"
    assert user2_tasks[0].title == "Задача user2"
