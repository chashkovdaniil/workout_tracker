import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_scoped_session
from asyncio import current_task
from greenlet import greenlet

# Set test environment variables
os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from app.core.config import settings
from app.database.base import Base
from app.database.session import get_db
from app.main import app

# Test database URL - using existing database
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/workout_tracker_test"

# Создаем engine с поддержкой greenlet
engine_test = create_async_engine(
    TEST_DATABASE_URL,  # Используем тестовую базу данных
    poolclass=NullPool,
    future=True,
    pool_pre_ping=True,
    echo=False,
)

# Создаем фабрику сессий с привязкой к greenlet
async_session_maker = async_sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Создаем scoped session с привязкой к текущему task
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_scoped_session(
        async_session_maker,
        scopefunc=current_task,
    )
    try:
        yield async_session()
    finally:
        await async_session.remove()

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

async def create_database():
    # Создаем engine для подключения к postgres (без указания конкретной базы данных)
    default_engine = create_async_engine(
        os.environ["DATABASE_URL"],
        isolation_level="AUTOCOMMIT"  # Важно для создания базы данных
    )

    async with default_engine.connect() as conn:
        # Проверяем существование базы данных
        result = await conn.execute(text(
            "SELECT 1 FROM pg_database WHERE datname = 'workout_tracker_test'"
        ))
        exists = result.scalar() is not None

        if not exists:
            # Создаем базу данных если её нет
            await conn.execute(text("CREATE DATABASE workout_tracker_test"))

    await default_engine.dispose()

# Обновляем фикстуру setup_db
@pytest_asyncio.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    # Создаем базу данных если её нет
    await create_database()
    
    # Создаем все таблицы перед тестами
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Очищаем данные после тестов
    async with engine_test.begin() as conn:
        await conn.execute(text("DELETE FROM workout_sets"))
        await conn.execute(text("DELETE FROM workout_exercises"))
        await conn.execute(text("DELETE FROM workouts"))
        await conn.execute(text("DELETE FROM exercises"))
        await conn.execute(text("DELETE FROM workout_types"))
        await conn.execute(text("DELETE FROM users"))

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def ac():
    """Async client fixture."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c

@pytest_asyncio.fixture
async def auth_headers(ac: AsyncClient):
    """Фикстура для получения заголовков авторизации."""
    # Регистрируем пользователя
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    await ac.post("/api/v1/auth/register", json=user_data)
    
    # Логинимся и получаем токен
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = await ac.post("/api/v1/auth/login", data=login_data)
    token_data = response.json()
    
    return {"Authorization": f"Bearer {token_data['access_token']}"}