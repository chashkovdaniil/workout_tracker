import pytest
from httpx import AsyncClient

from app.core.security import create_access_token
from app.models.user import User

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_register(ac: AsyncClient):
    """Test user registration."""
    # Создаем пользователя
    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data

@pytest.mark.asyncio
async def test_register_duplicate_email(ac: AsyncClient):
    """Test registration with duplicate email."""
    # Создаем первого пользователя
    await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "test2@example.com",
            "username": "testuser2",
            "password": "testpass123"
        }
    )
    
    # Пытаемся создать пользователя с тем же email
    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "test2@example.com",
            "username": "testuser3",
            "password": "testpass123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"].lower() == "email already registered"

@pytest.mark.asyncio
async def test_login(ac: AsyncClient):
    """Test user login."""
    # Регистрируем пользователя
    await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "test3@example.com",
            "username": "testuser3",
            "password": "testpass123"
        }
    )
    
    # Логинимся
    response = await ac.post(
        "/api/v1/auth/login",
        data={
            "username": "test3@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"].lower() == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(ac: AsyncClient):
    """Test login with wrong password."""
    # Регистрируем пользователя
    await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "test4@example.com",
            "username": "testuser4",
            "password": "testpass123"
        }
    )
    
    # Пытаемся залогиниться с неверным паролем
    response = await ac.post(
        "/api/v1/auth/login",
        data={
            "username": "test4@example.com",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"].lower() == "incorrect email or password"

@pytest.mark.asyncio
async def test_login_nonexistent_user(ac: AsyncClient):
    """Test login with nonexistent user."""
    response = await ac.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"].lower() == "incorrect email or password"

@pytest.mark.asyncio
async def test_get_current_user(ac: AsyncClient, auth_headers: dict):
    """Test getting current user info."""
    response = await ac.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data 