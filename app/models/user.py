from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class User(Base):
    """
    Модель пользователя.
    
    Атрибуты:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя (уникальный)
        username (str): Имя пользователя (уникальное)
        hashed_password (str): Хешированный пароль
        is_active (bool): Статус активности пользователя
        created_at (datetime): Дата и время создания пользователя
        workout_types (relationship): Связь с типами тренировок пользователя
        exercises (relationship): Связь с упражнениями пользователя
        workouts (relationship): Связь с тренировками пользователя
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workout_types = relationship("WorkoutType", back_populates="user", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="user", cascade="all, delete-orphan")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan") 