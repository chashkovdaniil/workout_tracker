import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.base import Base
from app.models.exercise import Exercise
from app.models.user import User
from app.models.workout import Workout
from app.models.workout_type import WorkoutType

async def init_db():
    # Создаем движок для подключения к базе данных
    engine = create_async_engine(settings.DATABASE_URL)
    
    # Создаем асинхронную сессию
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with engine.begin() as conn:
        try:
            # Проверяем существование базы данных
            result = await conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :dbname"), 
                                     {"dbname": settings.DATABASE_NAME})
            if not result.scalar():
                # Создаем базу данных, если она не существует
                await conn.execute(text("COMMIT"))  # Закрываем текущую транзакцию
                await conn.execute(text("CREATE DATABASE :dbname"), {"dbname": settings.DATABASE_NAME})
                print(f"Database '{settings.DATABASE_NAME}' created successfully")
        except Exception as e:
            print(f"Error checking/creating database: {e}")
            raise
    
    # Создаем таблицы
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db()) 