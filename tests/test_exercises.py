import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def get_auth_headers(ac: AsyncClient) -> dict:
    """Получение заголовков авторизации."""
    # Регистрация пользователя
    await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )

    # Вход в систему
    response = await ac.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

async def test_create_exercise(ac: AsyncClient, auth_headers: dict):
    """Тест создания упражнения."""
    response = await ac.post(
        "/api/v1/exercises/",
        json={
            "name": "Test Exercise",
            "description": "Test Description",
            "muscle_groups": ["chest"]
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Exercise"
    assert data["description"] == "Test Description"
    assert data["muscle_groups"] == ["chest"]

async def test_get_exercises(ac: AsyncClient, auth_headers: dict):
    """Тест получения списка упражнений."""
    response = await ac.get("/api/v1/exercises/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_get_exercise(ac: AsyncClient, auth_headers: dict):
    """Тест получения конкретного упражнения."""
    # Создаем упражнение
    create_response = await ac.post(
        "/api/v1/exercises/",
        json={
            "name": "Test Exercise",
            "description": "Test Description",
            "muscle_groups": ["chest"]
        },
        headers=auth_headers
    )
    exercise_id = create_response.json()["id"]
    
    # Получаем упражнение
    response = await ac.get(f"/api/v1/exercises/{exercise_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Exercise"
    assert data["description"] == "Test Description"
    assert data["muscle_groups"] == ["chest"]

async def test_update_exercise(ac: AsyncClient, auth_headers: dict):
    """Тест обновления упражнения."""
    # Создаем упражнение
    create_response = await ac.post(
        "/api/v1/exercises/",
        json={
            "name": "Test Exercise",
            "description": "Test Description",
            "muscle_groups": ["chest"]
        },
        headers=auth_headers
    )
    exercise_id = create_response.json()["id"]
    
    # Обновляем упражнение
    response = await ac.put(
        f"/api/v1/exercises/{exercise_id}",
        json={
            "name": "Updated Exercise",
            "description": "Updated Description",
            "muscle_groups": ["back"]
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Exercise"
    assert data["description"] == "Updated Description"
    assert data["muscle_groups"] == ["back"]

async def test_delete_exercise(ac: AsyncClient, auth_headers: dict):
    """Тест удаления упражнения."""
    # Создаем упражнение
    create_response = await ac.post(
        "/api/v1/exercises/",
        json={
            "name": "Test Exercise",
            "description": "Test Description",
            "muscle_groups": ["chest"]
        },
        headers=auth_headers
    )
    exercise_id = create_response.json()["id"]
    
    # Удаляем упражнение
    response = await ac.delete(f"/api/v1/exercises/{exercise_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Проверяем, что упражнение удалено
    get_response = await ac.get(f"/api/v1/exercises/{exercise_id}", headers=auth_headers)
    assert get_response.status_code == 404 