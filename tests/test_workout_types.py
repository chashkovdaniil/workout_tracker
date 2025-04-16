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
    token_data = response.json()
    return {"Authorization": f"Bearer {token_data['access_token']}"}

async def test_create_workout_type(ac: AsyncClient, auth_headers: dict):
    """Тест создания типа тренировки."""
    response = await ac.post(
        "/api/v1/workout-types/",
        json={
            "name": "Test Workout Type",
            "description": "Test Description"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Workout Type"
    assert data["description"] == "Test Description"

async def test_get_workout_types(ac: AsyncClient, auth_headers: dict):
    """Тест получения списка типов тренировок."""
    response = await ac.get("/api/v1/workout-types/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_get_workout_type(ac: AsyncClient, auth_headers: dict):
    """Тест получения типа тренировки по ID."""
    # Создаем тип тренировки
    workout_type_data = {
        "name": "Test Workout Type",
        "description": "Test Description"
    }
    response = await ac.post("/api/v1/workout-types/", json=workout_type_data, headers=auth_headers)
    assert response.status_code == 201
    workout_type_id = response.json()["id"]

    # Получаем тип тренировки
    response = await ac.get(f"/api/v1/workout-types/{workout_type_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workout_type_id
    assert data["name"] == workout_type_data["name"]
    assert data["description"] == workout_type_data["description"]

async def test_update_workout_type(ac: AsyncClient, auth_headers: dict):
    """Тест обновления типа тренировки."""
    # Создаем тип тренировки
    workout_type_data = {
        "name": "Test Workout Type",
        "description": "Test Description"
    }
    response = await ac.post("/api/v1/workout-types/", json=workout_type_data, headers=auth_headers)
    assert response.status_code == 201
    workout_type_id = response.json()["id"]

    # Обновляем тип тренировки
    update_data = {
        "name": "Updated Workout Type",
        "description": "Updated Description"
    }
    response = await ac.put(f"/api/v1/workout-types/{workout_type_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workout_type_id
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]

async def test_update_workout_type_not_found(ac: AsyncClient, auth_headers: dict):
    """Тест обновления несуществующего типа тренировки."""
    update_data = {
        "name": "Updated Workout Type",
        "description": "Updated Description"
    }
    response = await ac.put("/api/v1/workout-types/999", json=update_data, headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Тип тренировки не найден"

async def test_update_workout_type_duplicate_name(ac: AsyncClient, auth_headers: dict):
    """Тест обновления типа тренировки с существующим именем."""
    # Создаем первый тип тренировки
    workout_type1_data = {
        "name": "Test Workout Type 1",
        "description": "Test Description 1"
    }
    response = await ac.post("/api/v1/workout-types/", json=workout_type1_data, headers=auth_headers)
    assert response.status_code == 201
    workout_type1_id = response.json()["id"]

    # Создаем второй тип тренировки
    workout_type2_data = {
        "name": "Test Workout Type 2",
        "description": "Test Description 2"
    }
    response = await ac.post("/api/v1/workout-types/", json=workout_type2_data, headers=auth_headers)
    assert response.status_code == 201
    workout_type2_id = response.json()["id"]

    # Пытаемся переименовать второй тип тренировки в имя первого
    update_data = {"name": workout_type1_data["name"]}
    response = await ac.put(f"/api/v1/workout-types/{workout_type2_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Тип тренировки с таким именем уже существует"

async def test_update_workout_type_partial(ac: AsyncClient, auth_headers: dict):
    """Тест частичного обновления типа тренировки."""
    # Создаем тип тренировки
    workout_type_data = {
        "name": "Test Workout Type",
        "description": "Test Description"
    }
    response = await ac.post("/api/v1/workout-types/", json=workout_type_data, headers=auth_headers)
    assert response.status_code == 201
    workout_type_id = response.json()["id"]

    # Обновляем только имя
    update_data = {"name": "Updated Workout Type"}
    response = await ac.put(f"/api/v1/workout-types/{workout_type_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workout_type_id
    assert data["name"] == update_data["name"]
    assert data["description"] == workout_type_data["description"]

async def test_delete_workout_type(ac: AsyncClient, auth_headers: dict):
    """Тест удаления типа тренировки."""
    # Создаем тип тренировки
    create_response = await ac.post(
        "/api/v1/workout-types/",
        json={
            "name": "Test Workout Type",
            "description": "Test Description"
        },
        headers=auth_headers
    )
    assert create_response.status_code == 201
    workout_type_id = create_response.json()["id"]
    
    # Удаляем тип тренировки
    delete_response = await ac.delete(
        f"/api/v1/workout-types/{workout_type_id}",
        headers=auth_headers
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Тип тренировки успешно удален"
    
    # Проверяем, что тип тренировки действительно удален
    get_response = await ac.get(
        f"/api/v1/workout-types/{workout_type_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404 